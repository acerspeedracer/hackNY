import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = "/<username>/songs"
ALLOWED_EXTENSIONS = set(['ogg', 'wav', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS	

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename = filename))

@app.route('/<username>/songs/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#http://flask.pocoo.org/docs/patterns/fileuploads/#uploading-files
