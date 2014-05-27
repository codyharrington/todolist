__author__ = 'cody'
from webfront import app
from utils.rest_api_utils import *
import requests
from ujson import loads, dumps

class LocalUser():
    """A user here is really only a container for JSON, and an object for Flask-Login.
    The real user is in the DB API"""
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
        return self.data["id"]

class UserManager(RestClient):

    def __init__(self, api_url):
        super().__init__(api_url)

    def get_user(self, username):
        response_obj, status = self.get_resource("user/{}".format(username))
        if status != HTTPStatusCodes.OK:
            print(response_obj)
            return None
        return LocalUser(response_obj)

    def save_new_user(self, username, password, email=""):
        data = {"username": username, "password": password, "email": email}
        response_obj, status = self.put_resource("user", data=data)
        if status != HTTPStatusCodes.CREATED:
            print(response_obj)
        return response_obj

    def update_existing_user(self, local_user):
        data = local_user.data
        response_obj, status = self.post_resource("user/{}".format(data["username"]))
        if status != HTTPStatusCodes.OK:
            print(response_obj)
        return response_obj

    def delete_user(self, username):
        response_obj, status = self.delete_resource("user/{}".format(username))
        if status != HTTPStatusCodes.NO_CONTENT:
            print(response_obj)
        return response_obj

    def authenticate_user(self, username, password):
        data = {"username": username, "password": password}
        response_obj, status = self.post_resource("user/authenticate", data=data)
        if status != HTTPStatusCodes.OK:
            print(response_obj)
            return None
        return LocalUser(response_obj)





