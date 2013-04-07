from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import os
from werkzeug.contrib.fixers import ProxyFix
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost',9003)

@app.route("/")
def index():
	return render_template("register.html")

@app.route("/home/<username>")
def user_page(username):
	db = client.launchpad
	allUsers = db.users
	user = allUsers.find_one({"user":username})
	allSongs = user['songs']
	return render_template("keyboard.html",username=username,songs=allSongs)

@app.route("/register",methods=['GET'])
def create_register_page ():
	try:
		username = request.args.get("username",None)
	except Exception as e:
		return str(e)
	db = client.launchpad
	allUsers = db.users
	user = allUsers.find_one({"user":username})
	if user == None:
		newUser = {"user":username,"songs":[]}
		allUsers.insert(newUser)
		user = allUsers.find_one({"user":username})
	return redirect(url_for("user_page",username=username))

@app.route("/keyboard")
def create_keyboard_page ():
	return render_template("keyboard.html")

ALLOWED_EXTENSIONS = set(['ogg', 'wav', 'mp3'])


def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/<username>', methods = ['GET', 'POST'])
def upload_file(username):
	try :
		if request.method == 'POST':
			filelist = request.files.getlist('files')
			for f in filelist :
				if f and allowed_file(f.filename):
					filename = secure_filename(f.filename)
					clean_filename = filename.replace('.', '_')
					if not os.path.exists('public/%s/'%username):
						os.makedirs('public/%s/'%username)
					f.save(os.path.join('public/%s/'%username, filename))
					db = client.launchpad
					allUsers = db.users
					user = allUsers.find_one({"user":username})
					if user == None:
						return "Not a user"
					fnd = allUsers.find_one({"user":username,"songs":{"$elemMatch":{"file":clean_filename}}})
					if fnd != None:
						continue
					song = {"file":clean_filename, "loc":'%s/%s'%(username,filename)}
					allUsers.update({"user":username},{"$push": {"songs":song}})
		return render_template('test.html',username=username)
	except Exception as e:
		return "%s"%str(e)

#I dont think this does anything
@app.route('/<username>/songs/<filename>')
def uploaded_file(username, filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/<username>/uploadthings')
def uploadthings(username):
	return render_template('test.html',username=username)


if __name__ == "__main__":
	app.run(debug=True)
