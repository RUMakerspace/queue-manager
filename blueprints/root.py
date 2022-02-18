from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('root', __name__, url_prefix='/')

@bp.route("/")
def route_main():
    return "Hello, World!"
