from sqlalchemy import Column, Integer, String
from .base import Base

class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    last_id = Column(Integer, server_default=None, nullable=True)
