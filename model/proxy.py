from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True)
    server = Column(String(512), nullable=False)
    port = Column(Integer, nullable=False)
    secret = Column(String(512), nullable=False)
    # foreign key 1 to many
    reports = relationship('Report', back_populates='proxy')

    # constrian
    __table_args__ = (UniqueConstraint('server', 'port', 'secret'),)

