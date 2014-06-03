__author__ = 'cody'

from webfront import app, user_manager, task_manager
from flask_login import login_required, current_user
from flask import render_template, redirect, flash
from datetime import datetime
from utils.request_utils import *
from utils.messages import *
from webfront.models.task import LocalTask

@app.route("/")
@login_required
def root():
    tasks = {"active": [], "inactive": [], "completed": []}
    for task in current_user["tasks"]:
        if task["start"] is None or not task["enabled"]:
            tasks["inactive"].append(task)
        elif task["start"] < datetime.now():
            tasks["active"].append(task)
        elif task["end"] is not None and task["end"] < datetime.now():
            tasks["completed"].append(task)
    return render_template("main.html", current_user=current_user, tasks=tasks)

@app.route("/task/add", methods=["GET"])
@login_required
def add_task():
    return render_template("task/task.html")

@app.route("/task/add", methods=["POST"])
@login_required
def process_new_task():
    name = form_data("name")
    if name is None:
        return redirect("/task/add")

    new_task = LocalTask()
    new_task["name"] = name
    new_task["desc"] = form_data("desc")
    new_task["points"] = form_data("points")
    new_task["enabled"] = checkbox_value("enabled")
    new_task["userid"] = current_user["id"]
    if new_task["enabled"]:
        new_task["start"] = datetime.now()
    else:
        new_task["start"] = None

    response = task_manager.save_new_task(new_task)
    if "err" in response:
        flash(response["err"], category="error")
        return redirect("/task/add")
    flash(TASK_CREATED, category="success")
    return redirect("/")







