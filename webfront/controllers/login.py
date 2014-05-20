__author__ = 'cody'
from webfront import app, user_manager, login_manager
from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, login_required
from utils.request_utils import *
from utils.messages import *

@login_manager.user_loader
def load_user(username):
    return user_manager.get_user(username)

# These doubled up routes could each just use one method, but for
# clarity I've separate them out

@app.route("/login", methods=["GET"])
def load_login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    username = form_data("username")
    password = form_data("password")

    if username is None or password is None:
        flash(EMPTY_USERNAME_OR_PASSWORD)
    else:
        user = user_manager.authenticate_user(username, password)
        if user is None:
            flash(INCORRECT_USERNAME_OR_PASSWORD)
        else:
            login_user(user)
            return redirect("/")
    return redirect("/login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/signup", methods=["GET"])
def load_signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def process_signup():
    username = form_data("username")
    password = form_data("password")
    repassword = form_data("repassword")
    email = form_data("email")

    if username is None or password is None or repassword is None:
        flash(NOT_ALL_REQUIRED_FIELDS_RECEIVED)
    elif password != repassword:
        flash(PASSWORDS_NOT_MATCH)
    else:
        email = "" if email is None else email
        user_manager.create_user(username, password, email)
        flash(NEW_USER_CREATED.format(username))
        return redirect("/login")
    return redirect("/signup")
