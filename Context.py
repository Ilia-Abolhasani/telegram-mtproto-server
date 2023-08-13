import os
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# models
from model.base import Base
from model.agent import Agent
from model.channel import Channel
from model.isp import ISP
from model.proxy import Proxy
from model.report import Report


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
        
    def add_proxy(self, server, port, secret):
        proxy = self.get_proxy(server, port, secret)
        if(not proxy):
            new_proxy = Proxy(server=server, port=port, secret=secret)
            self.session.add(new_proxy)
            self.session.commit()
    # endregion 

    # region agent
    # endregion 

    # region isp
    # endregion 

    # region report
    # endregion 

    