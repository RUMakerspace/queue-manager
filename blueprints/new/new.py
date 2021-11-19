from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from helpers.alexandria import produceUsers

new = Blueprint("new", __name__, template_folder="templates")

import time


@new.route("/")
def show():
    try:
        usersName = request.args.to_dict()
        users = None
        if "usersName" not in usersName:
            users = produceUsers()
        return render_template(
            "gcode.html",
            usersName=usersName,
            users=users,
            currDate=time.strftime("%Y.%m.%d"),
        )
    except TemplateNotFound:
        abort(404)


@new.route("api/upload", methods=["POST"])
def acceptNewPrints(userName=None):
    print(request.form.to_dict())
    print(request.files.to_dict())

    return "OK", 200
