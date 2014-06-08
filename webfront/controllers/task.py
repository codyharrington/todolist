__author__ = 'cody'

from webfront import app, login_manager, task_manager
from flask import render_template, redirect, flash
from flask_login import current_user, login_required
from webfront.models.task import *
from webfront.models.user import *
from utils.request_utils import *

@app.route("/task/add", methods=["GET"])
@login_required
def add_task():
    return render_template("task/task.html", task=LocalTask())

@app.route("/task/add", methods=["POST"])
@login_required
def process_new_task():
    name = form_data("name")
    if name is None:
        return redirect("/task/add")

    new_task = LocalTask()
    new_task["name"] = name
    new_task["desc"] = form_data("desc")
    new_task["points"] = int(form_data("points")) if form_data("points") is not None and form_data("points").isdigit() else 0
    new_task["userid"] = current_user["id"]
    new_task["start"] = datetime.now()

    response = task_manager.save_new_task(new_task)
    if "err" in response:
        flash(response["err"], category="error")
        return redirect("/task/add")
    flash(TASK_CREATED, category="success")
    return redirect("/")

@app.route("/task/edit/<id>", methods=["GET"])
@login_required
def edit_task(id):
    task = task_manager.get_task(id)
    if task is None:
        flash(TASK_NOT_FOUND, category="error")
        return redirect("/")
    else:
        return render_template("task/task.html", task=task)

@app.route("/task/edit/<id>", methods=["POST"])
@login_required
def submit_task_edit(id):
    name = form_data("name")
    if name is None:
        return redirect("/task/add")

    updated_task = task_manager.get_task(id)
    updated_task["name"] = name
    updated_task["desc"] = form_data("desc")
    updated_task["points"] = form_data("points")

    response = task_manager.update_existing_task(updated_task)
    if "err" in response:
        flash(response["err"], category="error")
    else:
        flash(UPDATE_SUCCESSFUL, category="success")
    return redirect("/")

@app.route("/task/delete/<id>")
@login_required
def delete_task(id):
    response = task_manager.delete_task(id)
    if "err" in response:
        flash(response["err"], category="error")
    return redirect("/")

@app.route("/task/finish/<id>")
@login_required
def complete_task(id):
    response = task_manager.finish_task(id)
    if "err" in response:
        flash(response["err"], category="error")
    else:
        flash(UPDATE_SUCCESSFUL, category="success")
    return redirect("/")