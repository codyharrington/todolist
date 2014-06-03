__author__ = 'cody'
from flask import request

def form_data(key):
    if key in request.form and len(request.form[key]) > 0:
        return request.form[key]
    else:
        return None

def checkbox_value(key):
    if key in request.form:
        return True
    return False

def request_arg(key):
    if key in request.args:
        return request.args[key]
    else:
        return None