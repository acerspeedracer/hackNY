from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask import render_template
from flask import request
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

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
  app.run(debug=True)
