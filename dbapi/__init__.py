from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object("config.Dbapi")

db_engine = create_engine(app.config["CONNECT_STRING"])
Session = sessionmaker(bind=db_engine)
db_session = Session()

from dbapi.controllers.task import *
from dbapi.controllers.user import *
