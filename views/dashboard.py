from flask import current_app, Blueprint, render_template

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
def show_dash():
    return "This is the dashboard."