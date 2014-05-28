__author__ = 'cody'

from flask import Flask
from flask_login import LoginManager
from webfront.models.user import *
from webfront.models.task import *

app = Flask(__name__)
app.config.from_object('config.Webfront')
app.secret_key = app.config["SECRET_KEY"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = app.config["LOGIN_URI"]
login_manager.login_message_category = "warning"

user_manager = UserManager(app.config["DATABASE_URL"])
task_manager = TaskManager(app.config["DATABASE_URL"])

from webfront.controllers.main import *
from webfront.controllers.login import *
from webfront.controllers.error import *

