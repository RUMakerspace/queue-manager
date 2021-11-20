from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from helpers.alexandria import (
    produceUsers,
    userExists,
    userFolderExists,
    makeUserFolder,
    makeUserProjectFolder,
)

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


@new.route("makeNewUserPrint", methods=["POST"])
def acceptNewPrints(userName=None):
    userData = request.form.to_dict()

    if userExists(userData["usersName"]):
        if userFolderExists(userData["usersName"], userData["folderNameIG"]):
            flash("That user already has a folder that exists there.", "alert-danger")

    else:
        makeUserFolder(userData["usersName"])
        makeUserProjectFolder(userData["usersName"], userData["folderNameIG"])
        flash(
            "User {} created with a project file of {}.".format(
                userData["usersName"], userData["folderNameIG"]
            ),
            "alert-success",
        )

    return redirect(
        url_for(
            "new.show",
            usersName=userData["usersName"],
            userProjectFolder=userData["folderNameIG"],
        )
    )


@new.route("api/upload", methods=["POST"])
def uploadUserPrints():
    formdata = request.files.to_dict()
    print(request.form.to_dict())
    print(formdata)
    return "OK", 200
