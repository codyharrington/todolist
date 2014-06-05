__author__ = 'cody'

class Config():
    """Base configuration class. Any variable set here is loaded in all apps"""
    DEBUG = True
    SECRET_KEY = "1234"

class Webfront(Config):
    DATABASE_URL = "http://localhost:5000"
    LOGIN_URI = "/login"
    RECAPTCHA_VERIFY_URL = "http://www.google.com/recaptcha/api/verify"
    RECAPTCHA_PUBLIC_KEY = ""
    RECAPTCHA_PRIVATE_KEY = ""
    DISABLE_ALL_RECAPTCHA = True # Overrides the enabled fields below.
    REACTIVE_RECAPTCHA_ENABLED = False # Triggers on suspicious activity
    FORCED_RECAPTCHA_ENABLED = False # User always has to fill this one in
    FAILED_ATTEMPTS_CAPTCHA_THRESHOLD = 3

class Dbapi(Config):
    USER = "todolist"
    PASSWORD = "todolist"
    HOST = "localhost"
    PORT = "5432"
    DBNAME = "todolist"

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
        USER, PASSWORD, HOST, PORT, DBNAME
    )






