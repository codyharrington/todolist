__author__ = 'cody'
from webfront import app
from utils.rest_api_utils import *
import requests
from ujson import loads, dumps

class LocalUser():
    data = {}

    def __init__(self, data):
        self.data = data

    def is_authenticated(self):
        pass

    def is_active(self):
        pass

    def is_anonymous(self):
        return False

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
            return None
        else:
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
            return LocalUser(response_obj)





