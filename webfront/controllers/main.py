__author__ = 'cody'

from webfront import app

@app.route("/")
def root():
    return "Hello world"

