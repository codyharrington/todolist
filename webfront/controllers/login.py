__author__ = 'cody'
import flask
from webfront import app, user_manager, login_manager
from webfront.controllers import *
from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, login_required
from utils.recaptcha_utils import *
from utils.messages import *
from webfront.models.user import LocalUser

@login_manager.user_loader
def load_user(username):
    # Cache the current user so we aren't always re-fetching it from the DB API
    if not hasattr(flask.g, "current_user"):
        flask.g.current_user = user_manager.get_user(username)
    return flask.g.current_user

# These doubled up routes could each just use one method, but for
# clarity I've separate them out

@app.route("/login", methods=["GET"])
def load_login_page():
    recaptcha_enabled = should_display_captcha(request.remote_addr)
    return render_template("login.html", recaptcha_enabled=recaptcha_enabled,
                           recaptcha_pub_key=app.config["RECAPTCHA_PUBLIC_KEY"])

@app.route("/login", methods=["POST"])
def process_login():
    username = form_data("username")
    password = form_data("password")

    if honeypot_fields_used(["nick", "key"]):
        app.logger.warning("{} entered data into the honeypot fields on login".format(request.remote_addr))
        set_ip_to_threshold(request.remote_addr)
        flash(DUMMY_FIELD_DATA, category="error")
        return redirect("/login")

    if should_display_captcha(request.remote_addr):
        if check_fields_empty(form_data("c_challenge"), form_data("c_response")):
            flash(EMPTY_CAPTCHA, category="warning")
            return redirect("/login")
        passed, message = check_recaptcha(app.config["RECAPTCHA_PRIVATE_KEY"], app.config["RECAPTCHA_VERIFY_URL"])
        if passed == "false":
            app.logger.warning("{} failed the captcha on login".format(request.remote_addr))
            flash(message, category="error")
            return redirect("/login")

    if check_fields_empty(username, password):
        flash(EMPTY_USERNAME_OR_PASSWORD, category="warning")
    else:
        user = user_manager.authenticate_user(username, password)
        if user is None:
            flash(INCORRECT_USERNAME_OR_PASSWORD, category="error")
            app.logger.warning("{} failed authentication".format(request.remote_addr))
        else:
            clear_failed_logins(request.remote_addr)
            flash(LOGIN_SUCCESSFUL, category="success")
            login_user(user)
            return redirect("/")
    increment_failed_logins(request.remote_addr)
    return redirect("/login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/signup", methods=["GET"])
def load_signup_page():
    recaptcha_enabled = should_display_captcha(request.remote_addr, forced_captcha=True)
    return render_template("signup.html", recaptcha_enabled=recaptcha_enabled,
                           recaptcha_pub_key=app.config["RECAPTCHA_PUBLIC_KEY"])

@app.route("/signup", methods=["POST"])
def process_signup():
    username = form_data("username")
    password = form_data("password")
    repassword = form_data("repassword")
    email = form_data("email")

    if honeypot_fields_used(["nick", "key", "rekey", "addy"]):
        app.logger.warning("{} entered data into the honeypot fields on signup".format(request.remote_addr))
        set_ip_to_threshold(request.remote_addr)
        flash(DUMMY_FIELD_DATA, category="error")
        return redirect("/signup")

    passed, message = check_recaptcha(app.config["RECAPTCHA_PRIVATE_KEY"], app.config["RECAPTCHA_VERIFY_URL"])
    if passed == "false":
        app.logger.warning("{} failed the captcha on signup".format(request.remote_addr))
        flash(message, category="error")
        return redirect("/signup")

    if check_fields_empty(username, password, repassword):
        flash(NOT_ALL_REQUIRED_FIELDS_RECEIVED, category="error")
    elif password != repassword:
        flash(PASSWORDS_NOT_MATCH, category="warning")
    else:
        response = user_manager.save_new_user(LocalUser({"username": username, "password": password, "email": email}))
        if "err" not in response:
            clear_failed_logins(request.remote_addr)
            flash(USER_CREATED, category="success")
            return redirect("/login")
        else:
            flash(response["err"], category="error")
    increment_failed_logins(request.remote_addr)
    return redirect("/signup")
