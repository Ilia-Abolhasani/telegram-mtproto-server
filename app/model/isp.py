from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class ISP(Base):
    __tablename__ = 'isp'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String(128), nullable=False)

    
    # foreign key 1 to many
    agents = relationship('Agent', back_populates='isp')
