__author__ = 'cody'

import traceback
from webfront import app
from utils.rest_api_utils import HTTPStatusCodes
from utils.exceptions import *
from flask import request

@app.errorhandler(InternalServerErrorException)
def internal_server_error(e):
    traceback.print_exc()

@app.errorhandler(NotFoundException)
def not_found(e):
    traceback.print_exc()
