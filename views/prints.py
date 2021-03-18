from flask import current_app, Blueprint, render_template, redirect, request, url_for
from datetime import timedelta
from model.db import PrintJob, db

prints = Blueprint('prints', __name__, url_prefix='/prints')

@prints.route('/')
def show_prints():
    return render_template("prints/index.html", prints=PrintJob.query.all())

@prints.route('/add', methods=["GET", "POST"])
def add_print():
    if request.method == "GET":
        return render_template("prints/add.html")
    elif request.method == "POST":
        # TODO: Add author to printjob
        job_name = request.form.get("job_name")
        netid = request.form.get("netid")
        length = timedelta(
            days=int(request.form.get("l_days")),
            hours=int(request.form.get("l_hours")),
            minutes=int(request.form.get("l_mins")))

        db.session.add(PrintJob(
            job_name=job_name, 
            netid=netid, 
            length=length))

        db.session.commit()

        return redirect(url_for("prints.show_prints"))
    else:
        return "Invalid method!"

@prints.route('/remove/<id>')
def remove_print(id):
    db.session.delete(PrintJob.query.get(id))
    db.session.commit()

    return redirect(url_for("prints.show_prints"))

@prints.route('/edit/<id>', methods=["GET", "POST"])
def edit_print(id):
    print_job = PrintJob.query.get(id)

    if request.method == "GET":
        return render_template("prints/edit.html", job=print_job)
    elif request.method == "POST":
        print_job.job_name = request.form.get("job_name")
        print_job.netid = request.form.get("netid")
        print_job.length = timedelta(
            days=int(request.form.get("l_days")),
            hours=int(request.form.get("l_hours")),
            minutes=int(request.form.get("l_mins")))

        return redirect(url_for("prints.show_prints"))
    else:
        return "Invalid method!"
