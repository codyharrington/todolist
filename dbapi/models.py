__author__ = 'cody'

from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


# The below code was taken from
# https://blogs.gnome.org/danni/2013/03/07/generating-json-from-sqlalchemy-objects/
# with an added fromdict() method

# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def todict(self):
        return self.columnitems

    def fromdict(self, dict_obj):
        map(self.__setattr__, dict_obj.keys(), dict_obj.values())

# Define our schema

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
