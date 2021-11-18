from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

new = Blueprint("new", __name__, template_folder="templates")


@new.route("/")
def show():
    try:
        usersName = request.args.to_dict()["usersName"]
        return render_template("gcode.html", usersName=usersName)
    except TemplateNotFound:
        abort(404)


@new.route("api/upload", methods=["POST"])
def acceptNewPrints(userName=None):
    print(request.form.to_dict())
    print(request.files.to_dict())

    return "OK", 200
