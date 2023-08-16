from sqlalchemy import Column, Integer, String, BigInteger
from .base import Base


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    last_id = Column(BigInteger, server_default=None, nullable=True)
