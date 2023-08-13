from sqlalchemy import Column, Integer, String
from .base import Base

class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True)
    server = Column(String(100))
    port = Column(Integer)
    secret = Column(String(200))
