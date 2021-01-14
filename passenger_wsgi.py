import sys, os
import requests
import json
import datetime

### TODO LIST
# Clean up logic for bulk prints.
# have a key renamer group that doesn't suck?
# Edit page for prints.
# Print status change log?
# Dashboard for TV?
# IPO dropdown
if sys.version < "2.4":
    os.execl("/usr/bin/python3.6", "python3.6", *sys.argv)

# Change before deploy.
try:
    with open("debug_run.py") as w:
        debug = True
except:
    debug = False

from flask import Flask, render_template, redirect, url_for, jsonify, request
import flask

application = Flask(__name__)
application.secret_key = open("supersecret.key").read()

# Our database layer.
from DataProvider import DataProvider
from pprint import pprint

db = DataProvider()

### LOGIN SHIT
import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

login_manager = flask_login.LoginManager()
login_manager.init_app(application)

users = json.loads(open("userdb.json").read())


class User(flask_login.UserMixin):
    pass


@application.before_request
def before_request():
    flask.session.permanent = True
    application.permanent_session_lifetime = datetime.timedelta(minutes=20)
    flask.session.modified = True


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form["password"] == users[email]["password"]

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
            if flask.request.form["password"] == users[email]["password"]:
                user = User()
                user.id = email
                login_user(user)

        except:
            flask.redirect(url_for("logout"))
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.

        return flask.redirect(flask.url_for("indexPage"))


@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@application.route("/login", methods=["POST", "GET"])
def loginHelper():
    if request.method == "POST":
        passphrase = request.form["passphrase"]
        if passphrase in passwords2:
            id = passphrase
            user = User()
            login_user(user)
    if request.method == "GET":
        return render_template("pw.html")
    # print(request.values)
    return redirect(url_for("index"))

    # We return whether there is a finished
    # tag inside the history, and return False
    # , to mean it *has* finished, if it has.


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


@application.route("/")
@login_required
def indexPage():
    prints = db.getPrints(-1)
    prints = list(filter(hasNotFinished, prints))
    return render_template("main.html", prints=prints)


@application.route("/finished")
def finishedPage():
    prints = db.getPrints(-1)
    prints = [x for x in prints if hasFinished(x)]
    return render_template("main.html", prints=prints, finished=True)


@application.route("/add", methods=["GET", "POST"])
def addPage():
    if request.method == "POST":
        db.addPrint(request.form.to_dict())
        return redirect(url_for("indexPage"))
    return render_template("add.html")


# XXX TODO
# Implement this page's logic.
@application.route("/manage/<hash>", methods=["GET", "POST"])
def managePrint(hash):
    if request.method == "POST":
        print("Post bois")
    return jsonify(db.getPrintByHash(hash))


@application.route("/manage/<hash>/<action>", methods=["GET", "POST"])
def changePrintStatus(hash, action):
    if request.method == "GET":
        db.addPrintLog(hash, action, "")
    elif request.method == "POST":
        data = request.form.to_dict()["note"]
        db.addPrintLog(hash, action, data)
    return redirect(url_for("indexPage"))


@application.route("/edit/<hash>", methods=["GET", "POST"])
def editPrint(hash):
    if request.method == "POST":
        dbItem = db.getPrintByHash(hash)
        item = request.form.to_dict()
        item["hash"] = hash
        item["printHistory"] = dbItem["printHistory"]
        item["unixTime"] = dbItem["unixTime"]
        db.editPrint(hash, item)
        db.addPrintLog(hash, "edited", "")
        return redirect(url_for("indexPage"))
    if request.method == "GET":
        printjob = db.getPrintByHash(hash)
        return render_template(
            "edit.html", actions=printjob["printHistory"], printjob=printjob
        )
