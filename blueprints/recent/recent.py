from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

recent = Blueprint("recent", __name__, template_folder="templates")


@recent.route("/")
def show():
    try:
        return "bla"
    except TemplateNotFound:
        abort(404)
