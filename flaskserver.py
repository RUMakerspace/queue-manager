import sqlite3
from flask import Flask, escape, request, g, render_template, send_from_directory
from pprint import pprint
app = Flask(__name__, static_url_path='')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("example.db")
        #db.cursor().execute('''CREATE TABLE IF NOT EXISTS printjobs (name text, data blob)''')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def addPrint(test, test2):
	x = get_db().cursor()
	x.execute('''INSERT INTO printjobs VALUES (?,?)''',(test,test2))
	get_db().commit()

@app.route('/')
def mHomePage():
	return render_template("new_job.html")

#These two paths are responsible for showing off our static paths without needing a total reorg.
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/dist/<path:path>')
def sendDist(path):
    return send_from_directory('dist', path)



#Main method essentially.  Doesn't have to be PUT/POST, just POST would work but we lose nothing by accepting both.
@app.route('/job/add', methods = ['PUT', "POST"])
def addToDB():
	result = request.form
	pprint(result)
	
	addPrint("we got","data!")
	return mHomePage()

if __name__=='__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)



