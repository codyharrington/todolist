__author__ = 'cody'

import flask
from flask import request
from dbapi import app
from dbapi.models import *
from utils.rest_api_utils import *

@app.route("/task/<id>", methods=["GET"])
def get_task(id):
    task = flask.g.db_session.query(Task).filter(Task.id == id).scalar()
    if task is None:
        raise NotFoundException(TASK_NOT_FOUND)
    return rest_jsonify(task.todict())

@app.route("/task", methods=["GET"])
def get_all_tasks():
    all_tasks = [task.todict() for task in flask.g.db_session.query(Task).all()]
    return rest_jsonify(all_tasks)

@app.route("/task", methods=["POST", "PUT"])
def create_new_task():
    data = validate_convert_request(request.data)
    task = flask.g.db_session.query(Task).filter(Task.name == data["name"]).first()
    if task is not None:
        raise AlreadyExistsException(TASK_ALREADY_EXISTS)
    else:
        task = Task(data)
        flask.g.db_session.add(task)
        flask.g.db_session.commit()
        return rest_jsonify(message=TASK_CREATED, status=HTTPStatusCodes.CREATED)

@app.route("/task/<id>", methods=["POST", "PUT"])
def update_task(id):
    data = validate_convert_request(request.data)
    task = flask.g.db_session.query(Task).filter(Task.id == id).scalar()
    if task is None:
        raise NotFoundException(TASK_NOT_FOUND)
    else:
        task.fromdict(data)
        flask.g.db_session.merge(task)
        flask.g.db_session.commit()
        return rest_jsonify(message=RESOURCE_UPDATED)

@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    task = flask.g.db_session.query(Task).filter(Task.id == id).scalar()
    if task is None:
        raise NotFoundException(TASK_NOT_FOUND)
    else:
        flask.g.db_session.delete(task)
        flask.g.db_session.commit()
        return rest_jsonify(message=RESOURCE_DELETED, status=HTTPStatusCodes.NO_CONTENT)

@app.route("/task/<id>/finish", methods=["POST", "PUT"])
def complete_task(id):
    task = flask.g.db_session.query(Task).filter(Task.id == id).scalar()
    if task is None:
        raise NotFoundException(TASK_NOT_FOUND)
    else:
        task.end = datetime.now()
        flask.g.db_session.commit()
        return rest_jsonify(message=RESOURCE_UPDATED)


