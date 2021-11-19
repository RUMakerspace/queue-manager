import sys, os
import json
import datetime
import re
from pprint import pprint

# Flask
from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
import flask

# Flask Login
from users import Users
import flask_login
from flask_login import LoginManager, login_required, login_user, logout_user

# APScheduler for scheduled tasks.
from flask_apscheduler import APScheduler

application = Flask(__name__)
# Flask Login needs a key.
application.secret_key = open("supersecret.key").read()

# Enable APScheduler.
scheduler = APScheduler()
scheduler.init_app(application)
scheduler.api_enabled = True  # may need to be disabled
application.app_context().push()
scheduler.start()

from helpers.alexandria import (
    produceUsers,
    produceUserSubmissions,
    produceJobsMetadata,
    produceToFileParentInfo,
)
import json


@scheduler.task("interval", id="poke_at_alexandria", seconds=12)
def lexandria_poke():
    produceToFileParentInfo()
    produceJobsMetadata()


users = Users("./db/users.json", application)

from blueprints.recent.recent import recent
from blueprints.new.new import new as newPrint

application.register_blueprint(recent, url_prefix="/recent")
application.register_blueprint(newPrint, url_prefix="/new")

### LOGIN MANAGER
login_manager = flask_login.LoginManager()
login_manager.init_app(application)

# This function is just to set a session timer.
@application.before_request
def before_request():
    flask.session.permanent = True
    application.permanent_session_lifetime = datetime.timedelta(minutes=20)
    flask.session.modified = True


@login_manager.user_loader
def user_loader(username):
    return users.find_user(username)


# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get("username")
#     password = request.form.get("password")
#
#     user = users.try_login_user(username, password)
#
#     if user:
#         user.is_authenticated = True
#
#     return user


@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return flask.render_template("pw.html")
    if request.method == "POST":
        # Login and validate the user.
        # user should be an instance of your `User` class
        if "username" not in flask.request.form:
            flask.redirect(flask.url_for("indexPage"))

        username = flask.request.form["username"]
        pw = flask.request.form["password"]

        print(f"{username}: {pw}")
        auth_user = users.try_login_user(username, pw)

        if auth_user:
            login_user(auth_user)

        return flask.redirect(url_for("indexPage"))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(url_for("login"))


@application.route("/protected")
@flask_login.login_required
def protected():
    return "Logged in as: " + flask_login.current_user.id


@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("indexPage"))


from helpers.alexandria import readDataFromFile


@application.route("/")
def mainThing():
    dataq = readDataFromFile()
    print(len(dataq))
    dataq = sorted(dataq, key=lambda x: (len(x["dates"]), x["user"]))
    # dataq = sorted(dataq, key = lambda x : len(x['user']))
    return render_template("main.html", dat=dataq, enumerate=enumerate)
