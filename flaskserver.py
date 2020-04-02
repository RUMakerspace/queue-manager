import sqlite3
from flask import Flask, escape, request, g, render_template, send_from_directory
from pprint import pprint
app = Flask(__name__, static_url_path='')

@app.route('/')
def mHomePage():
	return render_template("new_job.html")

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
	#for k, v in result.items():
	#	print(k,v)

	return ""

if __name__=='__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
	
conn.close()



