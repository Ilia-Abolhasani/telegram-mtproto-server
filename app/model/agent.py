from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Agent(Base):
    __tablename__ = 'agent'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    isp_id = Column(Integer, ForeignKey('isp.id'), nullable=False)
    name = Column(String(128))
    cron_expression_speed_test = Column(String(64), nullable=False)
    cron_expression_ping = Column(String(64), nullable=False)
    batch_size_ping = Column(Integer, nullable=False)
    batch_size_speed_test = Column(Integer, nullable=False)
    encrypted_key = Column(String(128), nullable=False)

    # Define the relationship with the Report model
    reports = relationship('Report', back_populates='agent')
    isp = relationship('ISP', back_populates='agents')