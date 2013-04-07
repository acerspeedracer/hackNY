from flask import Flask, request, redirect, url_for, render_template
from werkzeug.contrib.fixers import ProxyFix
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost',9003)

@app.route("/")
def email():
  return "apple pie"

@app.route("/<username>")
def create_user_page (username):
  db = client.launchpad
  allUsers = db.users
  user = allUsers.find_one({"user":username})
  if user == None:
    newUser = {"user":username,"test":"New person woot"}
    allUsers.insert(newUser)
    user = allUsers.find_one({"user":username})
  test = user["test"]
  return test

UPLOAD_FOLDER = "/<username>/songs"
ALLOWED_EXTENSIONS = set(['ogg', 'wav', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/<username>/upload/<filename>', methods = ['GET', 'POST'])
def upload_file(username, filename):
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', username = username, filename = filename))

@app.route('/<username>/songs/<filename>')
def uploaded_file(username, filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/<username>/uploadthings')
def uploadthings(username):
  return render_template(test.html)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
  app.run(debug=True)
