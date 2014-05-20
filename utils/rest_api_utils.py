__author__ = 'cody'
import requests
from ujson import dumps, loads
from flask import Response
from utils.messages import *
from utils.exceptions import *

class HTTPStatusCodes():
    OK = 200
    CREATED = 201
    # Used after a DELETE request
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORISED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

    IM_A_TEAPOT = 418
    # This one means that the request is syntactically valid but semantically invalid
    UNPROCESSABLE_ENTITY = 422

    INTERNAL_SERVER_ERROR = 500

class RestClient(object):

    def __init__(self, api_url):
        self.api_url = api_url.rstrip("/")

    def get_resource(self, uri):
        response = requests.get("{}/{}".format(self.api_url, uri.rstrip("/")))
        if response.status_code == HTTPStatusCodes.NOT_FOUND:
            raise NotFoundException
        elif response.status_code == HTTPStatusCodes.INTERNAL_SERVER_ERROR:
            raise InternalServerErrorException
        else:
            return loads(response.text), response.status_code

    def post_resource(self, uri, data={}):
        response = requests.post("{}/{}".format(self.api_url, uri.lstrip("/")), data)
        if response.status_code == HTTPStatusCodes.NOT_FOUND:
            raise NotFoundException
        elif response.status_code == HTTPStatusCodes.INTERNAL_SERVER_ERROR:
            raise InternalServerErrorException
        else:
            return loads(response.text), response.status_code

    def put_resource(self, uri, data={}):
        response = requests.put("{}/{}".format(self.api_url, uri.lstrip("/")), data)
        if response.status_code == HTTPStatusCodes.NOT_FOUND:
            raise NotFoundException
        elif response.status_code == HTTPStatusCodes.INTERNAL_SERVER_ERROR:
            raise InternalServerErrorException
        else:
            return loads(response.text), response.status_code

    def delete_resource(self, uri):
        response = requests.get("{}/{}".format(self.api_url, uri.lstrip("/")))
        if response.status_code == HTTPStatusCodes.NOT_FOUND:
            raise NotFoundException
        elif response.status_code == HTTPStatusCodes.INTERNAL_SERVER_ERROR:
            raise InternalServerErrorException
        else:
            return loads(response.text), response.status_code


def rest_jsonify(data={}, status=HTTPStatusCodes.OK, **kwargs):
    """This method can take optional keyword arguments which will be added to the
    dictionary to convert to json. Good for adding err or message parameters"""
    if len(kwargs) > 0:
        data.update(kwargs)
    return Response(response=dumps(data), mimetype="application/json", status=status)

def validate_convert_request(request_data, required_headers=[]):
    try:
        data = loads(request_data)
    except ValueError:
        raise MalformedJSONException
    if len(data) == 0:
        raise NoDataException
    elif not isinstance(data, dict):
        raise ExpectedJSONObjectException
    elif not all([header in data for header in required_headers]):
        raise InsufficientFieldsException(INSUFFICIENT_FIELDS.format(", ".join(required_headers)))
    else:
        return data


