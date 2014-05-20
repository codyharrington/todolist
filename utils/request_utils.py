__author__ = 'cody'
from flask import request

def form_data(key):
    if key in request.form:
        return request.form[key]
    else:
        return None

def request_arg(key):
    if key in request.args:
        return request.args[key]
    else:
        return None