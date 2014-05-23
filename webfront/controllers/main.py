__author__ = 'cody'

from webfront import app
from flask_login import login_required
from flask import render_template

@app.route("/")
@login_required
def root():
    return render_template("main.html")

