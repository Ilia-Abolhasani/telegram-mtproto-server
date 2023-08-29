import os
import mysql.connector
from sqlalchemy import create_engine, text, func, or_
from sqlalchemy.orm import sessionmaker
from app.util.DotDict import DotDict

# models
from app.model.base import Base
from app.model.agent import Agent
from app.model.channel import Channel
from app.model.isp import ISP
from app.model.proxy import Proxy
from app.model.speed_report import SpeedReport
from app.model.ping_report import PingReport
from app.model.setting import Setting
from collections.abc import Iterable


class Context:
    def __init__(self):
        # config
        self.max_report_ping = 10
        self.max_report_speed = 10
        self.max_timeouts = 5
        self.successful_pings = 5
        self.max_ping_value = 10000
        self.exponential_decay = 0.9
        self.ping_score_weight = 0.4
        self.speed_score_weight = 0.6
        #
        db_name = os.getenv("database_name")
        db_user = os.getenv("database_user")
        db_pass = os.getenv("database_pass")
        db_host = os.getenv("database_host")
        db_port = os.getenv("database_port")
        db_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        # Create a session factory
        Session = sessionmaker(bind=engine,)
        self.session = Session()

    def _detach(self, obj):
        if (obj is None):
            return obj
        if isinstance(obj, Iterable):
            for item in obj:
                self.session.expunge(item)
        else:
            self.session.expunge(obj)
        return obj

    def attach(self, obj):
        self.session.add(obj)

    def get_all_channel(self):
        channels = self.session.query(Channel).all()
        return self._detach(channels)

    # proxy
    def get_top_proxies(self, limit):
        max_avg_speed = self.session.execute(
            text(
                f"""
                SELECT max(average_spped) FROM (
                    SELECT proxy_id, AVG(speed) as average_spped FROM speed_report
                GROUP by proxy_id) t
            """)
        ).scalar()
        max_ping = self.max_ping_value
        decay = self.exponential_decay
        ping_weight = self.ping_score_weight
        speed_weight = self.speed_score_weight

        query = f"""
            SELECT
                p.id AS proxy_id,
                p.connect AS connect,
                p.server as server,
                p.port as port ,
                p.secret as secret,
                COALESCE({ping_weight} * ping_score + {speed_weight} * speed_score, 0) AS final_weighted_score
            FROM proxy p
            LEFT JOIN (
	            SELECT
	                proxy_id,
	                ( {max_ping} - (SUM(weighted_ping) / SUM(weight))) / {max_ping} AS ping_score
	            FROM (
                    SELECT
                        proxy_id,
                        CASE WHEN ping = -1 THEN {max_ping} ELSE ping END AS adjusted_ping,
                        ({decay} * POWER({decay}, ROW_NUMBER() OVER (PARTITION BY proxy_id ORDER BY updated_at DESC) - 1)) AS weight,
                        CASE WHEN ping = -1 THEN {max_ping} ELSE ping END * ({decay} * POWER({decay}, ROW_NUMBER() OVER (PARTITION BY proxy_id ORDER BY updated_at DESC) - 1)) AS weighted_ping
                    FROM ping_report
                ) AS weighted_data
                GROUP BY proxy_id
            ) r ON p.id = r.proxy_id
            LEFT JOIN (
                SELECT
                    proxy_id,
                    (SUM(weighted_speed) / SUM(weight)) / {max_avg_speed} AS speed_score
                FROM (
                    SELECT
                        proxy_id,
                        speed,
                        ({decay} * POWER({decay}, ROW_NUMBER() OVER (PARTITION BY proxy_id ORDER BY updated_at DESC) - 1)) AS weight,
                        speed * ({decay} * POWER({decay}, ROW_NUMBER() OVER (PARTITION BY proxy_id ORDER BY updated_at DESC) - 1)) AS weighted_speed
                    FROM speed_report
                ) AS weighted_data
                GROUP BY proxy_id
            ) q ON p.id = q.proxy_id
            WHERE connect = 1
            ORDER BY final_weighted_score DESC
            LIMIT {limit};
        """
        proxies = self.session.execute(text(query)).all()
        return proxies

    def get_proxy(self, server, port, secret):
        proxy = self.session.query(Proxy).filter(
            Proxy.server == server,
            Proxy.port == port,
            Proxy.secret == secret).first()
        return self._detach(proxy)

    def add_proxy(self, server, port, secret, commit):
        proxy = self.get_proxy(server, port, secret)
        if (not proxy):
            new_proxy = Proxy(server=server, port=port, secret=secret)
            self.session.add(new_proxy)
            if (commit):
                self.session.commit()

    def get_proxy_ping(self, agent_id, disconnect):
        result = None
        if (disconnect):
            result = self.session.query(Proxy).filter(
                Proxy.connect == 0
            ).all()
        else:
            result = self.session.query(Proxy).filter(
                or_(Proxy.connect.is_(None), Proxy.connect == 1)
            ).all()
        return self._detach(result)

    def get_proxy_speed(self, agent_id):
        result = self.session.query(Proxy).filter(
            Proxy.connect == 1
        ).all()
        return self._detach(result)

    def proxies_connection_update(self):
        query = f"""
                UPDATE proxy
	            JOIN (
	            	SELECT proxy_id, sum(timeouts) as timeouts, sum(successful_pings) as successful_pings
	            		from (
                            SELECT
                            	report.proxy_id as proxy_id,
	            				CASE WHEN report.ping = -1 THEN 1 ELSE 0 END AS timeouts,
                                CASE WHEN report.ping != -1 THEN 1 ELSE 0 END AS successful_pings
                            FROM ping_report as report
	            			) p GROUP BY p.proxy_id
                 ) AS subquery ON proxy.id = subquery.proxy_id
	            SET proxy.connect = CASE
	            	WHEN subquery.timeouts >= {self.max_timeouts} THEN 0
	            	WHEN subquery.successful_pings >= {self.successful_pings} THEN 1
	            	ELSE NULL
	            END;
            """
        self.session.execute(text(query))
        self.session.commit()

    # agent
    def get_agent(self, agent_id):
        agent = self.session.query(Agent).filter(
            Agent.id == agent_id).first()
        return self._detach(agent)

    # ping report
    def get_ping_report_count(self, proxy_id):
        result = self.session.query(func.count(PingReport.id)).filter_by(
            proxy_id=proxy_id
        ).scalar()
        return result

    def add_ping_report(self, agent_id, proxy_id, ping):
        new_report = PingReport(
            agent_id=agent_id,
            proxy_id=proxy_id,
            ping=ping,
        )
        self.session.add(new_report)
        count = self.get_ping_report_count(proxy_id)
        if (count >= self.max_report_ping):
            for _ in range(self.max_report_ping, count):
                oldest_report = self.session.query(PingReport).filter_by(
                    agent_id=agent_id,
                    proxy_id=proxy_id
                ).order_by(PingReport.updated_at).first()
                self.session.delete(oldest_report)
        self.session.commit()

    def add_bach_ping_report(self, agent_id, reports):
        for report in reports:
            report = DotDict(report)
            self.add_ping_report(
                agent_id,
                report.proxy_id,
                report.ping,
            )

    # speed report
    def get_speed_report_count(self, proxy_id):
        result = self.session.query(func.count(SpeedReport.id)).filter_by(
            proxy_id=proxy_id
        ).scalar()
        return result

    def add_speed_report(self, agent_id, proxy_id, speed):
        new_report = SpeedReport(
            agent_id=agent_id,
            proxy_id=proxy_id,
            speed=speed
        )
        self.session.add(new_report)
        count = self.get_speed_report_count(proxy_id)
        if (count >= self.max_report_speed):
            for _ in range(self.max_report_speed, count):
                oldest_report = self.session.query(SpeedReport).filter_by(
                    agent_id=agent_id,
                    proxy_id=proxy_id
                ).order_by(SpeedReport.updated_at).first()
                self.session.delete(oldest_report)
        self.session.commit()

    def add_bach_speed_report(self, agent_id, reports):
        for report in reports:
            report = DotDict(report)
            self.add_speed_report(
                agent_id,
                report.proxy_id,
                report.speed,
            )

    # setting
    def get_setting(self, key):
        setting = self.session.query(Setting).filter_by(key=key).first()
        return self._detach(setting)

    def add_or_update_setting(self, key, value):
        setting = self.session.query(Setting).filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            new_setting = Setting(key=key, value=value)
            self.session.add(new_setting)
        self.session.commit()
