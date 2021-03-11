from flask import current_app, Blueprint, render_template

default = Blueprint('default', __name__, url_prefix='/')

@default.route('/')
def show_overview():
    return render_template("index.html")