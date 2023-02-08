from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from dictionnary import appdict
from markupsafe import escape
import json


app = Flask(__name__)
app.register_blueprint(appdict)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/words/")
def renderWords():
    return render_template("dictionnary.html")