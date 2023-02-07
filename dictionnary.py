from flask import Flask
from flask import request
from flask import jsonify
from model import db_words
from markupsafe import escape
import json

app = Flask(__name__)
router = "/api/words/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db = db_words.words(connect['host'],connect['user'],connect['password'],connect['database'])

@app.route("/")
def main():
    return ("<h1>Hello Run</h1>")

@app.route(f"{router}get/<int:id>",methods=['GET'])
def getWord(id):
    if request.method == "GET":
        return jsonify(db.getWord(id))

@app.route(f"{router}add/fr=<french>&normand=<normand>", methods=['GET'])
def addWord(french,normand):
    if db.addWord(french,normand) == True:
        return (f"""
            <h1> Les mots {french} et {normand} ont été rajoutés à la base de donnée</h1>
        """)
    else:
        return (f"""
            <h1> Les mots existent déjà dans la base de donnée</h1>
        """)

@app.route(f"{router}edit/?id=<id>&?french=<french>&?normand=<normand>",methods=["GET"])
def updateWord(id,french,normand):
    if db.updateWord(id,french,normand):
        return (f""" 
            <h1> Changement effectué ! </h1>
        """)

@app.route(f"{router}delete/<int:id>",methods=["GET"])
def deleteWord(id): 
    if db.getWord(id):
        if db.removeWord(id):
            return (f"""
                <h1>Le mot a été supprimé</h1>
            """)
        else:
            return(f"""
                <h1>Le mot n'a pas pu être supprimé de la base de donnée ou bien n'existe pas dans celle-ci ! </h1>
            """)
    else:
        return(f"""
                <h1>Le mot n'existe pas dans la base de donnée ! </h1>
            """)

@app.route(f"{router}search/<word>&lang=<language>",methods=["GET"])
def searchWord(word,language):
    if db.word_exists(word) != False:
        match language:
            case "fr":
                return jsonify(db.getWord(db.word_exists(word))['fr'])
            case "normand":
                return jsonify(db.getWord(db.word_exists(word))['normand'])
            case _:
                return (jsonify(False))
    else:
        return (f""" 
            <h1> {word} n'a pas été trouvé ! </h1>
        """)