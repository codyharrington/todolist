__author__ = 'cody'

from todolist import app

@app.route("/")
def root():
    return "Hello world"

