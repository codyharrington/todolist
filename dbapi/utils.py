__author__ = 'cody'
from dbapi import app
from ujson import dumps

def rest_jsonify(data):
    return app.response_class(dumps(data), mimetype="application/json")
