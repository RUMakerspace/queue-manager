import sys, os
import requests
import json
import datetime

if sys.version < "2.4":
    os.execl("/usr/bin/python3.6", "python3.6", *sys.argv)

# Change before deploy.
try:
	with open('debug_run.py') as w:
		debug = True
except:
	debug=False

if not debug:
    INTERP = os.path.join(os.environ["HOME"], "frcregs.com", "bin", "python")
    if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)
    sys.path.append(os.getcwd())

from flask import Flask, render_template, redirect, url_for, jsonify, request
import flask

application = Flask(__name__)
application.secret_key = open('supersecret.key').read()

### LOGIN SHIT
import flask_login
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
login_manager = flask_login.LoginManager()
login_manager.init_app(application)

users = json.loads(open('userdb.json').read())

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
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user
    
@application.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == 'GET':
        return flask.render_template('pw.html')
    if request.method == 'POST':
        # Login and validate the user.
        # user should be an instance of your `User` class
        if 'email' not in flask.request.form:
            flask.redirect(flask.url_for('index'))
        email = flask.request.form['email']
        try:
            if flask.request.form['password'] == users[email]['password']:
                user = User()
                user.id = email
                login_user(user)

        except:
            flask.redirect(url_for('logout'))
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.

        return flask.redirect(flask.url_for('index'))
    
@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user
    
@application.route('/login',methods=['POST','GET'])
def loginHelper():
    if request.method == 'POST':
        passphrase = request.form['passphrase']     
        if passphrase in passwords2:
            id = passphrase
            user = User()
            login_user(user)
    if request.method == 'GET':
        return render_template('pw.html')
    #print(request.values)     
    return redirect(url_for('index'))

@application.route('/')    
def indexPage():
	return render_template('main.html')
	
@application.route('/add', methods=['GET','POST'])    
def addPage():
	if request.method == "POST":
		from pprint import pprint
		pprint(request.form)
	return render_template('add.html')
