__author__ = 'cody'

from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Webfront')

login_manager = LoginManager()
login_manager.init_app(app)

from webfront.models.user import *
user_manager = UserManager(app.config["DATABASE_URL"])

from webfront.controllers.main import *
from webfront.controllers.login import *
from webfront.controllers.error import *

