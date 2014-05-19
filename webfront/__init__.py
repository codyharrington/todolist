__author__ = 'cody'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Webfront')

from webfront.controllers import main

