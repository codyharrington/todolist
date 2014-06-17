__author__ = 'cody'

from utils.exceptions import *
from utils.rest_api_utils import *
from utils.error_utils import *
from dbapi import app
from sqlalchemy.exc import SQLAlchemyError
import traceback

@app.errorhandler(ExpectedJSONObjectException)
def not_json_object(e):
    app.logger.error("{}\n{}", format(EXPECTED_JSON_OBJECT, traceback.print_exc()))
    traceback.format_exc()
    return rest_jsonify(err=EXPECTED_JSON_OBJECT, status=HTTPStatusCodes.UNPROCESSABLE_ENTITY)

@app.errorhandler(MalformedJSONException)
def malformed_json(e):
    app.logger.error("{}\n{}", format(MALFORMED_JSON, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=MALFORMED_JSON, status=HTTPStatusCodes.BAD_REQUEST)

@app.errorhandler(InsufficientFieldsException)
def insufficient_fields(e):
    app.logger.error("{}\n{}", format(INSUFFICIENT_FIELDS, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=INSUFFICIENT_FIELDS.format(e), status=HTTPStatusCodes.UNPROCESSABLE_ENTITY)

@app.errorhandler(NotFoundException)
def not_found(e):
    app.logger.error("{}\n{}", format(RESOURCE_NOT_FOUND, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=handle_default_err_msg(e, RESOURCE_NOT_FOUND),
                        status=HTTPStatusCodes.NOT_FOUND)

@app.errorhandler(AlreadyExistsException)
def already_exists(e):
    app.logger.error("{}\n{}", format(RESOURCE_ALREADY_EXISTS, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=handle_default_err_msg(e, RESOURCE_ALREADY_EXISTS),
                        status=HTTPStatusCodes.FORBIDDEN)

@app.errorhandler(NoDataException)
def no_data(e):
    app.logger.error("{}\n{}", format(REQUEST_EMPTY, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=REQUEST_EMPTY, status=HTTPStatusCodes.UNPROCESSABLE_ENTITY)

@app.errorhandler(AuthenticationFailureException)
def authentication_failed(e):
    app.logger.error("{}\n{}", format(AUTHENTICATION_FAILURE, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=AUTHENTICATION_FAILURE, status=HTTPStatusCodes.UNAUTHORISED)

@app.errorhandler(SQLAlchemyError)
def database_error(e):
    app.logger.error("{}\n{}", format(INTERNAL_EXCEPTION, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=INTERNAL_EXCEPTION, status=HTTPStatusCodes.INTERNAL_SERVER_ERROR)

@app.errorhandler(InternalServerErrorException)
def internal_server_error(e):
    app.logger.error("{}\n{}", format(INTERNAL_EXCEPTION, traceback.print_exc()))
    traceback.print_exc()
    return rest_jsonify(err=INTERNAL_EXCEPTION, status=HTTPStatusCodes.INTERNAL_SERVER_ERROR)
