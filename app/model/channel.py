from sqlalchemy import Column, Integer, Boolean, String, BigInteger
from .base import Base


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    name = Column(String(128), nullable=True)
    last_id = Column(BigInteger, server_default=None, nullable=True)
    is_public = Column(Boolean, server_default='1', nullable=False)
    chat_id = Column(BigInteger, nullable=True)
