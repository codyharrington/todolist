__author__ = 'cody'

from utils.rest_api_utils import *
from datetime import datetime, timedelta

class LocalTask():
    data = {}

    def __init__(self, data={}):
        self.data = data

    def set_data(self, data_obj):
        self.data = data_obj

class TaskManager(RestClient):

    def __init__(self, api_url):
        super().__init__(api_url)

    def get_task(self, task_id):
        response_obj, status = self.get_resource("task/{}".format(task_id))
        if status != HTTPStatusCodes.OK:
            print(response_obj)
            return None
        return LocalTask(response_obj)

    def create_task(self, name, desc="", start=None, end=None, user=None):
        if start is None:
            start = datetime.now()
        if end is None:
            end = datetime.now() + timedelta(hours=1)
        data = {"name": name, "desc": desc, "start": start, "end": end, "userid": user}
        response_obj, status = self.put_resource("task", data=data)
        if status != HTTPStatusCodes.CREATED:
            print(response_obj)
            return None
        return LocalTask(response_obj)

    def save_task(self, local_task):
        data = local_task.data
        response_obj, status = self.post_resource("/task/{}".format(data["id"]), data=data)
        if status != HTTPStatusCodes.OK:
            print(response_obj)
        return response_obj

    def delete_task(self, task_id):
        response_obj, status = self.delete_resource("/task/{}".format(task_id))
        if status != HTTPStatusCodes.NO_CONTENT:
            print(response_obj)
        return response_obj



