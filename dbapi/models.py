__author__ = 'cody'

from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from dbapi import app_bcrypt
from bcrypt import gensalt


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
        forbidden_fields = ["id", "required_fields"]
        [dict_obj.__delitem__(field) for field in forbidden_fields if field in dict_obj]
        [self.__setattr__(key, dict_obj[key]) for key in dict_obj.keys() if key in self.columns]

# Define our schema

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(10), nullable=False, unique=True)
    email = Column(String(20), unique=True)
    password = Column(String(100))
    salt = Column(String(50))
    tasks = relationship("Task")
    required_fields = ["username", "password"]

    def __init__(self, dict_obj=None):
        if dict_obj is None:
            dict_obj = {}
        self.fromdict(dict_obj)

    def set_password(self, password):
        self.salt = gensalt()
        self.password = app_bcrypt.generate_password_hash(self.salt + str(password))

    def check_password(self, password):
        return app_bcrypt.check_password_hash(self.password, self.salt + str(password))

    def todict(self):
        data = super().todict()
        # We don't want to reveal the salt or password
        if "password" in data:
            del data["password"]
        if "salt" in data:
            del data["salt"]
        if "tasks" in data:
            data["tasks"] = [task.todict() for task in data["tasks"]]
        else:
            data["tasks"] = []
        return data

    def fromdict(self, dict_obj):
        super().fromdict(dict_obj)
        # We want to make sure that the password is stored in the database as a hash
        if "password" in dict_obj:
            self.set_password(dict_obj["password"])
        if "tasks" in dict_obj:
            self.tasks = [Task(task) for task in dict_obj["tasks"]]
        else:
            self.tasks = []


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    points = Column(Integer)
    start = Column(DateTime)
    end = Column(DateTime)
    desc = Column(String(1000))
    userid = Column(Integer, ForeignKey("user.id"))
    required_fields = ["name"]

    def __init__(self, dict_obj=None):
        if dict_obj is None:
            dict_obj = {}
        self.fromdict(dict_obj)


