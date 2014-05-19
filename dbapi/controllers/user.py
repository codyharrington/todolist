__author__ = 'cody'

from dbapi import app, db_session
from dbapi.models import *
from dbapi.utils import rest_jsonify

@app.route("/user", methods=["GET"])
def get_all_users():
    all_users = map(User.todict, db_session.query(User).all())
    return rest_jsonify(all_users)

@app.route("/user/<username>", methods=["GET"])
def get_specific_user(username):
    user = db_session.query(User.username == username).scalar()
    return rest_jsonify(user)

@app.route("/user/<username>/tasks", methods=["GET"])
def get_user_tasks(username):
    matching_tasks = map(Task.todict, db_session.query(Task.owner == username).all())
    return rest_jsonify(matching_tasks)

