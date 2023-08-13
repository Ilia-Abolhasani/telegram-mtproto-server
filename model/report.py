from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Report(Base):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agent.id'), nullable=False)
    proxy_id = Column(Integer, ForeignKey('proxy.id'), nullable=False)
    connected = Column(Boolean, nullable=False)
    ping = Column(Integer, server_default=None, nullable=True)
    download_speed = Column(Integer, server_default=None, nullable=True)
    upload_speed = Column(Integer, server_default=None, nullable=True)

    
    agent = relationship('Agent', back_populates='reports')
    proxy = relationship('Proxy', back_populates='reports')


