from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Agent(Base):
    __tablename__ = 'agent'

    id = Column(Integer, primary_key=True)                    
    isp_id = Column(Integer, ForeignKey('isp.id'), nullable=False)
    name = Column(String(128))
    # Define the relationship with the Report model
    reports = relationship('Report', back_populates='agent')
    isp = relationship('ISP', back_populates='agents')