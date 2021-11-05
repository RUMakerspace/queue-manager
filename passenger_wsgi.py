import sys, os
import json
import datetime
import re
from pprint import pprint

# Print Databases
from queue import Queue

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
    id = int(id)
    if request.method == "GET":
        queue.set_status(id, action)
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


@login_required
@application.route("/edit/delete/<idx>", methods=["POST"])
def delete_print(idx):
    id_num = int(idx)
    queue.remove_print(id_num)
    return redirect(url_for("indexPage"))


from parsers.gcode import extractPrusaGCodeInfo, extractPrusaThumbnails
from parsers.ufp import getGCode, extractThumbnails, getMaterials


@application.route("/api/postfile", methods=["POST"])
def postfileTest():
    print(request.form.to_dict())
    files = request.files.to_dict()
    for f in files:
        # print(files[f].read())
        # print(dir(files[f]))

        if files[f].filename.endswith(".ufp"):

            fileData = files[f]

            getGCode(fileData)
            print("Ultimaker Cura UFP")

            thumbs = extractThumbnails(files[f])
            getMaterials(files[f])
            return render_template("imgs.html", thumbs=thumbs)

        if files[f].mimetype in [
            "text/x.gcode",
            "text/x-gcode",
        ]:  # mimetypes for prusa gcode I think. https://mimetype.io/gcode
            # We extract the file here to avoid issues wrt stream decoding.  May be an issue for very big files.  _okay_ for now.
            fileData = files[f].read().decode("utf-8")
            extractPrusaGCodeInfo(filename=files[f].filename, fileData=fileData)
            # thumbs = extractPrusaThumbnails(fileData)
            # return render_template("imgs.html", thumbs=thumbs)

    return "OK", 200


@application.route("/gcode")
def gcode():
    return render_template("gcode.html", netid="dhayden7")
