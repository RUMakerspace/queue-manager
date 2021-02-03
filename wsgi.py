import sys, os
import json
import datetime
import re

import flask
from flask import Flask, render_template, redirect, url_for, jsonify, request

from DataProvider import DataProvider
from pprint import pprint

import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from tinydb import TinyDB, where

# Start with constructing the flask app
application = Flask(__name__)
application.secret_key = open("supersecret.key").read()

# Generate databases for logins and prints
print_db = TinyDB('prints.json')

class User(flask_login.UserMixin):
    pass

# This function is just to set a session timer.
@application.before_request
def before_request():
    flask.session.permanent = True
    application.permanent_session_lifetime = datetime.timedelta(minutes=20)
    flask.session.modified = True

@application.route("/")
def indexPage():
    # TODO: Render prints.json
    return render_template("main.html")
