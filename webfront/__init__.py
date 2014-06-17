__author__ = 'cody'

import os
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_login import LoginManager
from utils.config_utils import load_config_object
from webfront.models.user import UserManager
from webfront.models.task import TaskManager
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
load_config_object(app, "Webfront")
app.secret_key = app.config["SECRET_KEY"]

app.wsgi_app = ProxyFix(app.wsgi_app)

log_handler = RotatingFileHandler(os.path.join(app.config["LOG_DIRECTORY"], __name__),
                                  maxBytes=app.config["MAX_LOG_BYTES"], backupCount=1)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(Formatter(app.config["LOG_FORMAT_STRING"]))
app.logger.addHandler(log_handler)
app_logger = app.logger

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = app.config["LOGIN_URI"]
login_manager.login_message_category = "warning"

user_manager = UserManager(app.config["DATABASE_URL"])
task_manager = TaskManager(app.config["DATABASE_URL"])

failed_ip_login_attempt_counts = {}

from webfront.controllers.main import *
from webfront.controllers.login import *
from webfront.controllers.error import *
from webfront.controllers.task import *
from webfront.controllers.user import *

