__author__ = 'cody'

from webfront import app, user_manager
from flask_login import login_required, current_user,logout_user
from flask import render_template, redirect, flash
from utils.request_utils import form_data
from utils.messages import *

@app.route("/user/delete", methods=["GET"])
@login_required
def display_delete_user_page():
    return render_template("user/user_delete.html")

@app.route("/user/delete", methods=["POST"])
@login_required
def delete_current_user():
    password = form_data("password")
    response = user_manager.authenticate_user(current_user["username"], password)
    if response is None:
        flash(INCORRECT_USERNAME_OR_PASSWORD, category="error")
        return redirect("/user/delete")
    else:
        response = user_manager.delete_user(current_user["username"])
        if "err" in response:
            flash(response["err"], category="error")
            return redirect("/")
        flash(USER_DELETED, category="success")
        return redirect("/logout")

@app.route("/user/repassword", methods=["GET"])
@login_required
def display_change_password_page():
    return render_template("user/user_repassword.html")

@app.route("/user/repassword", methods=["POST"])
@login_required
def change_current_user_password():
    password = form_data("password")
    repassword = form_data("repassword")
    if password != repassword:
        flash(PASSWORDS_NOT_MATCH, category="warning")
        return redirect("/user/repassword")
    else:
        current_user["password"] = password
        response = user_manager.update_existing_user(current_user)
        if "err" in response:
            flash(response["err"], category="error")
            return redirect("/user/password")
        else:
            flash(PASSWORDS_CHANGED_SUCCESSFULLY, category="success")
            return redirect("/")




