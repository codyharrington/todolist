__author__ = 'cody'
from webfront import app
from utils.rest_api_utils import *
import requests
from ujson import loads, dumps

class LocalUser():
    data = {}
    enabled = True

    def __init__(self, data={}):
        self.data = data

    def is_authenticated(self):
        # If a user isn't authenticated, we get None instead
        # so there is no point in implementing this
        return True

    def is_active(self):
        # To be updated once email confirmations are implemented
        return self.enabled

    def is_anonymous(self):
        # We currently have no concept of anonymous users
        return False

    def set_data(self, data_obj):
        self.data = data_obj

    def get_id(self):
        return self.data["username"]

class UserManager(RestClient):

    def __init__(self, api_url):
        super().__init__(api_url)

    def get_user(self, username):
        data, status = self.get_resource("user/{}".format(username))
        if status == HTTPStatusCodes.NOT_FOUND:
            return None
        return LocalUser(data)

    def create_user(self, username, password, email=""):
        data = {"username": username, "password": password, "email": email}
        response_obj = self.put_resource("user", data=data)
        return response_obj

    def delete_user(self, username):
        data, status = self.delete_resource("user/{}".format(username))
        return data

    def authenticate_user(self, username, password):
        data = {"username": username, "password": password}
        response_obj, status = self.post_resource("user/authenticate", data=data)
        if status == HTTPStatusCodes.UNAUTHORISED:
            return None
        else:
            return LocalUser(response_obj)





