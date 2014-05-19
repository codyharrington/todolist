__author__ = 'cody'
from webfront import app
from flask import render_template, request

@app.route("/login", methods=["GET"])
def load_login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    print(request.args)
    return "Ye"
