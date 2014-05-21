__author__ = 'cody'

import flask
from dbapi import app
from flask import request
from dbapi.models import *
from utils.rest_api_utils import *
from utils.exceptions import *

@app.route("/user", methods=["GET"])
def get_all_users():
    all_users = [user.todict() for user in flask.g.db_session.query(User).all()]
    return rest_jsonify(all_users)

@app.route("/user", methods=["POST", "PUT"])
def create_new_user():
    data = validate_convert_request(request.data, required_headers=User.required_fields)
    user = flask.g.db_session.query(User).filter(User.username == data["username"]).first()
    if user is not None:
        raise AlreadyExistsException
    else:
        user = User()
        user.fromdict(data)
        flask.g.db_session.add(user)
        flask.g.db_session.commit()
        return rest_jsonify(message=NEW_USER_CREATED.format(user.username), status=HTTPStatusCodes.CREATED)

@app.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    user = flask.g.db_session.query(User).filter(User.username == username).scalar()
    if user is None:
        raise NotFoundException
    else:
        flask.g.db_session.delete(user)
        flask.g.db_session.commit()
        return rest_jsonify(message=RESOURCE_DELETED, status=HTTPStatusCodes.NO_CONTENT)

@app.route("/user/<username>", methods=["GET"])
def get_specific_user(username):
    user = flask.g.db_session.query(User).filter(User.username == username).scalar()
    if user is None:
        raise NotFoundException
    else:
        return rest_jsonify(user.todict())

@app.route("/user/authenticate", methods=["POST"])
def authenticate_user():
    data = validate_convert_request(request.data, required_headers=["username", "password"])
    user = flask.g.db_session.query(User).filter(User.username == data["username"]).scalar()
    if user is None:
        raise NotFoundException
    elif not user.check_password(data["password"]):
        raise AuthenticationFailureException
    else:
        return rest_jsonify(user.todict())

@app.route("/user/<username>/tasks", methods=["GET"])
def get_user_tasks(username):
    matching_tasks = [task.todict() for task in flask.g.db_session.query(Task).filter(Task.owner == username).all()]
    return rest_jsonify(matching_tasks)

