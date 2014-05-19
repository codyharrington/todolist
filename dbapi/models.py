__author__ = 'cody'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    username = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    desc = Column(String)
    owner = Column(String, ForeignKey("user.username"), nullable=False)
