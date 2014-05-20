__author__ = 'cody'

import flask
from dbapi import app
from dbapi.models import *
from utils.rest_api_utils import rest_jsonify

@app.route("/task/<id>", methods=["GET"])
def get_task(id):
    task = flask.g.db_session.query(Task).filter(Task.id == id).scalar()
    return rest_jsonify(task)
