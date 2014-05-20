__author__ = 'cody'

from webfront import app
from flask_login import login_required

@app.route("/")
@login_required
def root():
    return "Logged in."

