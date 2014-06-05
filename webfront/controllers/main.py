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
    tasks = {"active": [], "completed": []}
    for task in current_user["tasks"]:
        if task["end"] is None and datetime.utcfromtimestamp(task["start"]) < datetime.now():
            tasks["active"].append(task)
        elif task["end"] is not None and datetime.utcfromtimestamp(task["end"]) < datetime.now():
            task["duration"] = (datetime.utcfromtimestamp(task["start"]) - datetime.utcfromtimestamp(task["end"])).total_seconds()
            tasks["completed"].append(task)
    return render_template("main.html", current_user=current_user, tasks=tasks)










