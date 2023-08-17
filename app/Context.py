import os
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.util.DotDict import DotDict

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

    def get_proxy_ping(self, agent_id, batch):
        return self.session.query(Proxy).limit(batch).all()

    def get_proxy_speed_tests(self, agent_id, batch):
        return self.session.query(Proxy).limit(batch).all()

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
    def add_reports(self, agent_id, reports):
        for report in reports:
            report = DotDict(report)
            new_report = Report(
                agent_id=agent_id,
                proxy_id=report.proxy_id,
                ping=report.ping,
                download_speed=report.download_speed,
                upload_speed=report.upload_speed,
            )
            self.session.add(new_report)
        self.session.commit()

    # endregion
