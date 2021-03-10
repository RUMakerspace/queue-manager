from flask import current_app, Blueprint, render_template
from model.db import PrintJob

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
def show_dash():
    return "This is the dashboard."

@dashboard.route("/prints")
def show_dash_prints():
    return PrintJob.query.all()

@dashboard.route('/prints/add', methods=["GET", "POST"])
def add_print():
    pass