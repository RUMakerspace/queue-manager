import sys, os
import json
import datetime
import re

# Print Databases
from queue import Queue
from tinydb import TinyDB, where

# Flask
from flask import Flask, render_template, redirect, url_for, jsonify, request
import flask

# Flask Login
import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

# TODO: Phase out DataProvider, functions are provided by TinyDB
from DataProvider import DataProvider
from pprint import pprint

application = Flask(__name__)
application.secret_key = open("supersecret.key").read()

# Our database layer.
queue = Queue('./db/print.json') 
userdb = TinyDB('./db/user.json') 

userdb.upsert({'name': 'Rutgers', 'password': 'Makerspace', 'logged-in': True}, where('name') == 'Rutgers')

db = DataProvider()

### LOGIN SHIT
login_manager = flask_login.LoginManager()
login_manager.init_app(application)

class User(flask_login.UserMixin):
    pass

# This function is just to set a session timer.
@application.before_request
def before_request():
    flask.session.permanent = True
    application.permanent_session_lifetime = datetime.timedelta(minutes=20)
    flask.session.modified = True


@login_manager.user_loader
def user_loader(username):
    if not userdb.search(where('name').matches(username, flags=re.IGNORECASE)):
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if not userdb.search(where('email').matches(email, flags=re.IGNORECASE)):
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    pw = request.form['password']
    user.is_authenticated = userdb.search((where('email') == email) & (where('password') == pw))
    # user.is_authenticated = request.form["password"] == users[email]["password"]
    return user


@application.route("/login", methods=["GET", "POST"])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == "GET":
        return flask.render_template("pw.html")
    if request.method == "POST":
        # Login and validate the user.
        # user should be an instance of your `User` class
        if "email" not in flask.request.form:
            flask.redirect(flask.url_for("indexPage"))

        email = flask.request.form["email"]

        try:
            pw = flask.request.form["password"]
            if userdb.search((where('name') == email) & (where('password') == pw)):
                user = User()
                user.id = email
                login_user(user)
                flask.redirect(url_for("indexPage"))

        except:
            flask.redirect(url_for("logout"))
        return flask.redirect(flask.url_for("indexPage"))


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


# XXX REFACTOR HAS / HASN'T FINISHED LIST
def hasNotFinished(item):
    for k in item["printHistory"]:
        if k["action"] == "finished":
            return False
    return True


def hasFinished(item):
    for k in item["printHistory"]:
        if k["action"] == "finished":
            return True
    return False


@login_required
@application.route("/")
def indexPage():
    # TODO: Query
    prints = queue.get_n(20)
    # prints = list(filter(hasNotFinished, prints))
    return render_template("main.html", prints=prints)


@application.route("/finished")
def finishedPage():
    # TODO: Query
    prints = queue.get_n(20)
    # prints = [x for x in prints if hasFinished(x)]
    return render_template("main.html", prints=prints, finished=True)


@application.route("/add", methods=["GET", "POST"])
@login_required
def addPage():
    # TODO: Fix?
    if request.method == "POST":
        queue.add(request.form.to_dict())
        return redirect(url_for("indexPage"))
    return render_template("add.html")


@application.route("/manage/<id>/<action>", methods=["GET", "POST"])
@login_required
def changePrintStatus(id, action):
    if request.method == "GET":
        db.addPrintLog(id, action, "")
    elif request.method == "POST":
        data = request.form.to_dict()["note"]
        db.addPrintLog(id, action, data)
    return redirect(url_for("indexPage"))

@application.route("/manage/<id>")
def managePrint(id):
    return queue.get(id)

@login_required
@application.route("/edit/<id>", methods=["GET", "POST"])
def editPrint(id):
    id = int(id)
    if request.method == "POST":
        job = queue.get(id)
        item = request.form.to_dict()
        item["hash"] = id
        item["printHistory"] = job["printHistory"]
        queue.edit(id, item)
        return redirect(url_for("indexPage"))
    if request.method == "GET":
        job = queue.get(id)
        return render_template(
            "edit.html", actions=job["printHistory"], printjob=job
        )
