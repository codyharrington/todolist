__author__ = 'cody'
from webfront import app
from utils.rest_api_utils import *
import requests
from ujson import loads, dumps

class LocalUser():
    data = {}
    authenticated = False
    enabled = False

    def __init__(self, data={}):
        self.data = data

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True # To be updated once email confirmations are implemented

    def is_anonymous(self):
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
        return LocalUser(data)

    def create_user(self, username, password, email=""):
        data = {"username": username, "password": password, "email": email}
        response_obj, status = self.put_resource("user", data=data)
        if status == HTTPStatusCodes.FORBIDDEN:
            print(ALREADY_EXISTS)
        return response_obj

    def delete_user(self, username):
        data, status = self.delete_resource("user/{}".format(username))
        return data

    def authenticate_user(self, username, password):
        data = {"username": username, "password": password}
        response_obj, status = self.post_resource("user/authenticate", data=data)
        if status == HTTPStatusCodes.UNAUTHORISED:
            print(AUTHENTICATION_FAILURE)
            return None
        else:
            user = LocalUser(response_obj)
            user.authenticated = True
            return user





