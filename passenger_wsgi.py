import sys, os
import json
import datetime
import re
from pprint import pprint

# Print Databases
from queue import Queue
from tinydb import TinyDB, where

# Flask
from flask import Flask, render_template, redirect, url_for, jsonify, request
import flask

# Flask Login
from users import Users
import flask_login
from flask_login import LoginManager, login_required, login_user, logout_user

application = Flask(__name__)
application.secret_key = open("supersecret.key").read()

# Our database layer.
queue = Queue("./db/print.json")
users = Users("./db/users.json", application)

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


@login_required
@application.route("/")
def indexPage():
    # TODO: Query
    prints = queue.get_prints(20)
    return render_template("main.html", prints=prints)


@application.route("/finished")
def finishedPage():
    # TODO: Query
    prints = queue.get_prints(20)
    return render_template(
        "main.html",
        prints=prints,
        finished=True,
        statusBar="Sorry, this page is still a work in progress.<br><br>It's not very useful yet, but we're working on it.  Hang tight!",
    )


@application.route("/add", methods=["GET", "POST"])
@login_required
def addPage():
    # TODO: Fix?
    if request.method == "POST":
        queue.add_print(request.form.to_dict())
        return redirect(url_for("indexPage"))
    return render_template("add.html")


@application.route("/manage/<id>/<action>", methods=["GET", "POST"])
@login_required
def changePrintStatus(id, action):
    if request.method == "GET":
        queue.log(id, action, "")
    elif request.method == "POST":
        data = request.form.to_dict()["note"]
        queue.log(id, action, data)
    return redirect(url_for("indexPage"))


@application.route("/manage/<id>")
def managePrint(id):
    return queue.get_print(id)


@login_required
@application.route("/edit/<id>", methods=["GET", "POST"])
def editPrint(id):
    id = int(id)
    if request.method == "POST":
        item = request.form.to_dict()
        queue.edit_print(id, item)
        return redirect(url_for("indexPage"))
    if request.method == "GET":
        job = queue.get_print(id)
        log = queue.get_log(id)

        return render_template("edit.html", actions=log, printjob=job)
