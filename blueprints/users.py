from flask import Flask
from flask import request
from flask import jsonify
from model import db_users
from markupsafe import escape
import json

app = Flask(__name__)
router = "/api/users/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db = db_users.users(connect['host'],connect['user'],connect['password'],connect['database'])

@app.route("/")
def main():
    return ("<h1>Hello Run</h1>")

@app.route(f"{router}add/username=<user>&email=<email>&pswd=<pwsd>")
def addAccount(user,email,pwsd):
    return jsonify(db.add_user(user,email,pwsd))

@app.route(f"{router}connect/email=<email>&pswd=<pwsd>")
def checkMail(email,pwsd):
    if db.check_user(email,pwsd):
        pass
