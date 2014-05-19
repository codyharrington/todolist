__author__ = 'cody'

class Config():
    """Base configuration class. Any variable set here is loaded in all apps"""
    DEBUG = True

class Webfront(Config):
    pass

class Dbapi(Config):
    USER = "todolist"
    PASSWORD = "todolist"
    HOST = ""
    PORT = ""
    DBNAME = "todolist"
    CONNECT_STRING = "postgresql+psycopg2://{0}:{1}@/{2}".format(
        USER, PASSWORD, DBNAME
    )






