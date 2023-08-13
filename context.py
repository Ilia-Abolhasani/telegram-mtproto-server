import os
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model.base import Base

db_name = os.getenv("database_name")
db_user = os.getenv("database_user")
db_pass = os.getenv("database_pass")
db_host = os.getenv("database_host")
db_port = os.getenv("database_port")
db_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

