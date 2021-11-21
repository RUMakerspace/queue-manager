from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from helpers.alexandria import (
    produceUsers,
    userExists,
    userFolderExists,
    makeUserFolder,
    makeUserProjectFolder,
)

edit = Blueprint("edit", __name__, template_folder="templates")


@edit.route("/")
def show():
    try:
        return render_template("edit.html")
    except TemplateNotFound:
        abort(404)


@edit.route("save", methods=["POST"])
def savePrintStatus():
    return "OK", 200
