__author__ = 'cody'
from os.path import exists

def load_config_object(app, class_name):
    app.config.from_object("config.{}".format(class_name))
    if exists("local_config.py"):
        app.config.from_object("local_config.{}".format(class_name))
