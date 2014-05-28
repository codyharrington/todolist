__author__ = 'cody'

from webfront import app, user_manager, task_manager
from flask_login import login_required, current_user
from flask import render_template, redirect
from datetime import datetime

@app.route("/")
@login_required
def root():
    tasks = {"active": [], "upcoming": [], "inactive": [], "completed": []}
    for task in current_user["tasks"]:
        if task["start"] is None:
            tasks["inactive"].append(task)
        elif task["start"] > datetime.now():
            tasks["upcoming"].append(task)
        elif task["start"] < datetime.now():
            tasks["active"].append(task)
        elif task["end"] is not None and task["end"] < datetime.now():
            tasks["completed"].append(task)
    return render_template("main.html", current_user=current_user, tasks=tasks)

@app.route("/task/add")
@login_required
def add_task():
    return render_template("task/new_task.html")

