__author__ = 'cody'

from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
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
        [self.__setattr__(key, dict_obj[key]) for key in dict_obj.keys() if key in self.columns]

# Define our schema

class User(Base):
    __tablename__ = "user"
    username = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    salt = Column(String)
    required_fields = ["username", "password"]

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
        return data

    def fromdict(self, dict_obj):
        super().fromdict(dict_obj)
        # We want to make sure that the password is stored in the database as a hash
        if "password" in dict_obj:
            self.set_password(dict_obj["password"])


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)
    desc = Column(String)
    owner = Column(String, ForeignKey("user.username"), nullable=False)
    required_fields = ["name"]


