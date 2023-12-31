from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Agent(Base):
    __tablename__ = 'agent'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isp_id = Column(Integer, ForeignKey('isp.id'), nullable=False)
    name = Column(String(128))
    encrypted_key = Column(String(128), nullable=False)

    # Define the relationship with the Report model
    ping_reports = relationship('PingReport', back_populates='agent')
    speed_reports = relationship('SpeedReport', back_populates='agent')
    isp = relationship('ISP', back_populates='agents')
