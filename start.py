from flask import Flask
from flask import request
from flask import jsonify
from model import database
import json

app = Flask(__name__)

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db = database.database(connect['host'],connect['user'],connect['password'],connect['database'])

@app.route("/")
def start():
    return("<h1>Hello World<h1>")

@app.route("/api/word/get/<int:id>",methods=['GET'])
def get(id):
    if request.method == "GET":
        return jsonify(db.getWord(id))

@app.route("/api/word/add/?fr=<french>&?normand=<normand>", methods=['POST'])
def add(french,normand):
    db.addWord(french,normand)
    id = db.word_exists(french)
    word = db.getWord(id)
    
    return (f"""
    <h1> Les mots {french} et {normand} ont été rajoutés à la base de donnée </h1>
    <p> ID: {id} - français: {word['fr']}
    """)
