from flask import Flask
from flask import request
from flask import jsonify
from model import db_words
import json

app = Flask(__name__)
router = "/api/word/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db = db_words.database(connect['host'],connect['user'],connect['password'],connect['database'])

@app.route(f"{router}get/<int:id>",methods=['GET'])
def getWord(id):
    if request.method == "GET":
        return jsonify(db.getWord(id))

@app.route(f"{router}add/?fr=<french>&?normand=<normand>", methods=['GET'])
def addWord(french,normand):
    if db.word_exists(french) == None:
        db.addWord(french,normand)
        id = db.word_exists(french)
        word = db.getWord(id)
        return (f"""
            <h1> Les mots {french} et {normand} ont été rajoutés à la base de donnée </h1>
            <p> ID: {id} - français: {word['fr']}
        """)
    else:
        return (f"""
            <h1> Le mot existe déjà dans la base de donnée</h1>
        """)

@app.route(f"{router}edit/?id=<id>&?french=<french>&?normand=<normand>",methods=["GET"])
def updateWord(id,french,normand):
    db.updateWord(id,french,normand)

@app.route(f"{router}delete/?id=<id>",methods=["GET"])
def deleteWord(id):
    if db.word_exists(id) != None:
        db.removeWord(id)
    else:
        return (f"""
            <h1>Le mot n'existe pas dans la base de donnée.</h1>
        """)
    
