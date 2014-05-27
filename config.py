__author__ = 'cody'

class Config():
    """Base configuration class. Any variable set here is loaded in all apps"""
    DEBUG = True
    SECRET_KEY = "1234" # Change this in production

class Webfront(Config):
    DATABASE_URL = "http://localhost:5000"
    LOGIN_URI = "/login"

class Dbapi(Config):
    USER = "todolist"
    PASSWORD = "todolist"
    HOST = "localhost"
    PORT = "5432"
    DBNAME = "todolist"

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
        USER, PASSWORD, HOST, PORT, DBNAME
    )






