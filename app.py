from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route("/")
def email():
  return "apples"

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
  app.run(debug=True)
