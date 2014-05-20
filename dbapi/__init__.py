from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object("config.Dbapi")

db_engine = create_engine(app.config["CONNECT_STRING"])
Session = sessionmaker(bind=db_engine)
db_session = Session()

app_bcrypt = Bcrypt(app)

from dbapi.controllers.task import *
from dbapi.controllers.user import *
from dbapi.controllers.error import *
