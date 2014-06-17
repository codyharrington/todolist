__author__ = 'cody'
from webfront.models import LocalBase
from utils.rest_api_utils import *

class LocalUser(LocalBase):
    enabled = True

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

    def get_id(self):
        return self["username"]

class UserManager(RestClient):

    def __init__(self, api_url):
        super().__init__(api_url)

    def get_user(self, username):
        response_obj, status = self.get_resource("user/{}".format(username))
        if status != HTTPStatusCodes.OK:
            print(response_obj)
            return None
        return LocalUser(response_obj["data"])

    def save_new_user(self, local_user):
        response_obj, status = self.post_resource("user", data=local_user.copy())
        if status != HTTPStatusCodes.CREATED:
            print(response_obj)
        return response_obj

    def update_existing_user(self, local_user):
        response_obj, status = self.put_resource("user/{}".format(local_user["username"]), data=local_user.copy())
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
        return LocalUser(response_obj["data"])





