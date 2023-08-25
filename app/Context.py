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


class Context:
    def __init__(self):
        # config
        self.max_report_ping = 10
        self.max_report_speed = 10
        self.max_timeouts = 5
        self.successful_pings = 5
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
        Session = sessionmaker(bind=engine)
        self.session = Session()
        print("hi")

    def get_all_channel(self):
        return self.session.query(Channel).all()

    # proxy
    def get_top_proxies(self, limit):
        return self.session.query(Proxy).filter(
            Proxy.connect == 1
        ).limit(limit).all()

    def get_proxy(self, server, port, secret):
        proxy = self.session.query(Proxy).filter(
            Proxy.server == server,
            Proxy.port == port,
            Proxy.secret == secret).first()
        return proxy

    def add_proxy(self, server, port, secret, commit):
        proxy = self.get_proxy(server, port, secret)
        if (not proxy):
            new_proxy = Proxy(server=server, port=port, secret=secret)
            self.session.add(new_proxy)
            if (commit):
                self.session.commit()

    def get_proxy_ping(self, agent_id, disconnect):
        if (disconnect):
            return self.session.query(Proxy).filter(
                Proxy.connect == 0
            ).all()
        else:
            return self.session.query(Proxy).filter(
                or_(Proxy.connect.is_(None), Proxy.connect == 1)
            ).all()

    def get_proxy_speed(self, agent_id):
        return self.session.query(Proxy).filter(
            Proxy.connect == 1
        ).all()

    def proxies_connection_update(self):
        self.session.execute(
            f"""
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
        )
        self.session.commit()

    # agent
    def get_agent(self, agent_id):
        agent = self.session.query(Agent).filter(
            Agent.id == agent_id).first()
        return agent

    # ping report
    def get_ping_report_count(self, proxy_id):
        return self.session.query(func.count(PingReport.id)).filter_by(
            proxy_id=proxy_id
        ).scalar()

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
        return self.session.query(func.count(SpeedReport.id)).filter_by(
            proxy_id=proxy_id
        ).scalar()

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
        return setting

    def add_or_update_setting(self, key, value):
        setting = self.session.query(Setting).filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            new_setting = Setting(key=key, value=value)
            self.session.add(new_setting)
        self.session.commit()
