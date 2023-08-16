from sqlalchemy import Column, Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    server = Column(String(1024), nullable=False)
    port = Column(Integer, nullable=False)
    secret = Column(String(1024), nullable=False)
    ip = Column(Integer, nullable=True)
    connect = Column(Boolean, nullable=True)

    # foreign key 1 to many
    reports = relationship('Report', back_populates='proxy')

    # constrian
    __table_args__ = (UniqueConstraint('server', 'port', 'secret'),)
    