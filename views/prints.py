from flask import current_app, Blueprint, render_template, redirect, request, url_for
from model.db import PrintJob

prints = Blueprint('prints', __name__, url_prefix='/prints')

@prints.route('/')
def show_prints():
    return f"{PrintJob.query.all()}"

@prints.route('/add', methods=["GET", "POST"])
def add_print():
    if request.method == "GET":
        return render_template("prints/add.html")
    elif request.method == "POST":
        job_name = request.form.get("job_name")
        print(f"{job_name}")
        return redirect(url_for("prints.show_prints"))
    else:
        return "Invalid method!"

@prints.route('/remove/<id>')
def remove_print(id):
    return redirect(url_for("prints.show_prints"))