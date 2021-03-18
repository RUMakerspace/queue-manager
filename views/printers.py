from flask import current_app, Blueprint, render_template, redirect, request, url_for
from datetime import timedelta
from model.db import Printer, db

printers = Blueprint('printers', __name__, url_prefix='/printers')

@printers.route('/')
def show_printers():
    return f"{Printer.query.all()}"

@printers.route('/add', methods=["GET", "POST"])
def add_printer():
    if request.method == "GET":
        return render_template("printers/add.html")
    elif request.method == "POST":
        name = request.form.get("name")
        func = request.form.get("func")

        db.session.add(Printer(
            name=name, 
            func=func))

        db.session.commit()

        return redirect(url_for("printers.show_printers"))
    else:
        return "Invalid method!"

@printers.route('/remove/<id>')
def remove_printer(id):
    db.session.delete(Printer.query.get(id))
    db.session.commit()

    return redirect(url_for("printers.show_printers"))

@printers.route('/edit/<id>', methods=["GET", "POST"])
def edit_printer(id):
    printer = Printer.query.get(id)

    if request.method == "GET":
        return render_template("printers/edit.html", printer=printer)
    elif request.method == "POST":
        printer.name = request.form.get("name")
        printer.func = request.form.get("func")

        return redirect(url_for("printers.show_printers"))
    else:
        return "Invalid method!"
