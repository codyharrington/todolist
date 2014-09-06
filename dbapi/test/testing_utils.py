__author__ = 'cody'
import dbapi
import unittest
import os
from dbapi import app
from dbapi.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils.messages import *
from utils.rest_api_utils import *

class DbapiTestCase(unittest.TestCase):
    def init_db(self):
        connection = self.engine.connect()
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))
        Base.query = db_session.query_property()
        Base.metadata.create_all(bind=connection)
        return db_session

    def close_db(self, blah):
        blah.flush()
        blah.commit()

    def setUp(self):
        app.config["TESTING"] = True
        dbapi.init_db = self.init_db
        self.app = app.test_client()
        self.engine = create_engine("sqlite:////tmp/temp.db", convert_unicode=True)
        self.session = self.init_db()

        self.test_user = self.create_user({"username": "johnsmith",
                                           "password": "password",
                                           "email": "testemail"})
        self.test_task = self.create_task({"name": "testtask",
                                           "userid": self.test_user.id})

        from flask.globals import current_app

        with app.app_context():
            current_app.init_db = self.init_db
            current_app.close_db = self.close_db

    def tearDown(self):
        if os.path.isfile("/tmp/temp.db"):
            os.remove("/tmp/temp.db")

    def create_user(self, user_dict):
        test_user = User(user_dict)
        self.session.add(test_user)
        self.session.commit()
        return test_user

    def create_task(self, task_dict):
        test_task = Task(task_dict)
        self.session.add(test_task)
        self.session.commit()
        return test_task
