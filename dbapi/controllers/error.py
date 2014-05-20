__author__ = 'cody'

from utils.exceptions import *
from utils.rest_api_utils import *
from dbapi import app
from sqlalchemy.exc import SQLAlchemyError
import traceback

@app.errorhandler(ExpectedJSONObjectException)
def not_json_object(e):
    traceback.print_exc()
    return rest_jsonify(err=EXPECTED_JSON_OBJECT, status=HTTPStatusCodes.UNPROCESSABLE_ENTITY)

@app.errorhandler(MalformedJSONException)
def malformed_json(e):
    traceback.print_exc()
    return rest_jsonify(err=MALFORMED_JSON, status=HTTPStatusCodes.BAD_REQUEST)

@app.errorhandler(InsufficientFieldsException)
def insufficient_fields(e):
    traceback.print_exc()
    return rest_jsonify(err=INSUFFICIENT_FIELDS, status=HTTPStatusCodes.UNPROCESSABLE_ENTITY)

@app.errorhandler(NotFoundException)
def not_found(e):
    traceback.print_exc()
    return rest_jsonify(err=NOT_FOUND, status=HTTPStatusCodes.NOT_FOUND)

@app.errorhandler(AlreadyExistsException)
def already_exists(e):
    traceback.print_exc()
    return rest_jsonify(err=ALREADY_EXISTS, status=HTTPStatusCodes.FORBIDDEN)

@app.errorhandler(NoDataException)
def no_data(e):
    traceback.print_exc()
    return rest_jsonify(err=REQUEST_EMPTY, status=HTTPStatusCodes.UNPROCESSABLE_ENTITY)

@app.errorhandler(AuthenticationFailureException)
def authentication_failed(e):
    traceback.print_exc()
    return rest_jsonify(err=AUTHENTICATION_FAILURE, status=HTTPStatusCodes.UNAUTHORISED)

@app.errorhandler(SQLAlchemyError)
def database_error(e):
    traceback.print_exc()
    return rest_jsonify(err=INTERNAL_EXCEPTION, status=HTTPStatusCodes.INTERNAL_SERVER_ERROR)

@app.errorhandler(InternalServerErrorException)
def internal_server_error(e):
    traceback.print_exc()
    return rest_jsonify(err=INTERNAL_EXCEPTION, status=HTTPStatusCodes.INTERNAL_SERVER_ERROR)
