from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class SpeedReport(Base):
    __tablename__ = 'speed_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(Integer, ForeignKey('agent.id'), nullable=False)
    proxy_id = Column(Integer, ForeignKey('proxy.id'), nullable=False)
    speed = Column(Integer, server_default=None, nullable=True)

    agent = relationship('Agent', back_populates='speed_reports')
    proxy = relationship('Proxy', back_populates='speed_reports')
