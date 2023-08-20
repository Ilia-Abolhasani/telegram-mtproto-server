import os
import mysql.connector
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
from app.util.DotDict import DotDict
from sqlalchemy import update
from sqlalchemy.sql import case
from sqlalchemy.orm import aliased


# models
from app.model.base import Base
from app.model.agent import Agent
from app.model.channel import Channel
from app.model.isp import ISP
from app.model.proxy import Proxy
from app.model.report import Report
from app.model.setting import Setting


class Context:
    def __init__(self):
        # config
        self.max_report = 10
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

    def _execute_custom_query(self, query):
        self.session.execute(text(query))
        self.session.commit()

    # region channel
    def get_all_channel(self):
        return self.session.query(Channel).all()

    # endregion

    # region proxy
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

    def get_proxy_ping(self, agent_id):
        return self.session.query(Proxy).all()

    def get_proxy_speed_tests(self, agent_id):
        return self.session.query(Proxy).all()

    def proxies_connection_update(self):
        self._execute_custom_query(
            f"""
                UPDATE proxy
                JOIN (
                    SELECT
                        report.proxy_id as proxy_id,
                        CASE WHEN report.ping = -1 THEN 1 ELSE 0 END AS timeouts,
                        CASE WHEN report.ping != -1 THEN 1 ELSE 0 END AS successful_pings
                    FROM report
                    GROUP BY report.proxy_id
                ) AS subquery ON proxy.id = subquery.proxy_id
                SET proxy.connect = CASE
                    WHEN subquery.timeouts >= {self.max_timeouts} THEN 0
                    WHEN subquery.successful_pings >= {self.successful_pings} THEN 1
                    ELSE NULL
                END;
            """
        )

    # endregion

    # region agent

    def get_agent(self, agent_id):
        agent = self.session.query(Agent).filter(
            Agent.id == agent_id).first()
        return agent
    # endregion

    # region isp
    # endregion

    # region report
    def get_report_count(self, proxy_id):
        return self.session.query(func.count(Report.id)).filter_by(
            proxy_id=proxy_id
        ).scalar()

    def add_report(self, agent_id, proxy_id, ping, download_speed, upload_speed, commit=True):
        new_report = Report(
            agent_id=agent_id,
            proxy_id=proxy_id,
            ping=ping,
            download_speed=download_speed,
            upload_speed=upload_speed,
        )
        self.session.add(new_report)
        count = self.get_report_count(proxy_id)
        if (count >= self.max_report):
            for _ in range(self.max_report, count):
                oldest_report = self.session.query(Report).filter_by(
                    agent_id=agent_id,
                    proxy_id=proxy_id
                ).order_by(Report.updated_at).first()
                self.session.delete(oldest_report)
        if (commit):
            self.session.commit()

    def add_reports(self, agent_id, reports):
        for report in reports:
            report = DotDict(report)
            self.add_report(
                agent_id,
                report.proxy_id,
                report.ping,
                report.download_speed,
                report.upload_speed,
                False
            )
        self.session.commit()

    # endregion
