from flask import Blueprint, request, jsonify, render_template,Flask,redirect,url_for,abort
from model.db_words import Dict
from model.db_users import Users
import requests as req
import json
from markupsafe import escape
import json

dict = Blueprint('dictionnary', __name__)
router = "/api/words/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db_dict = Dict(connect['host'],connect['user'],connect['password'],connect['database'])
db_user = Users(connect['host'],connect['user'],connect['password'],connect['database'])

@dict.route("/admin/")
def render_words():
    if db_user.check_token(request.cookies.get('user_token')) is False or "user_token" not in request.cookies:
        return redirect(url_for('users.connexion'))
    
    html = ""
    try:
        for word in db_dict.getAllWord():
            html += f"""
                <tr>
                    <td>{word['id']}</td>
                    <td>{word['fr']}</td>
                    <td>{word['normand']}</td>
                </tr>
            """
    except:
        html = f"""
                <tr>
                </tr>
            """
    return render_template("administration.html", tableWords = html)

@dict.route(f"{router}get/<int:id>",methods=['GET'])
def getWord(id):
    if request.method == "GET":
        return jsonify(db_dict.getWord(id))

@dict.route(f"{router}add", methods=['POST'])
def addWord():
    if request.method != "POST":
        return abort('405')
    french = request.form["fr"]
    normand = request.form['normand']

    if db_dict.addWord(french,normand) == True:
        return jsonify(True)

@dict.route(f"{router}edit",methods=["POST"])
def updateWord():
    if db_user.check_token(request.cookies.get('user_token')) is False or "user_token" not in request.cookies:
        return redirect(url_for('users.connexion'))
    
    if request.method == "POST":
        id = request.form["id"]
        french = request.form["fr"]
        normand = request.form['normand']

        if db_dict.updateWord(id,french,normand):
            return (f""" 
                <h1> Changement effectué ! </h1>
            """)
    

@dict.route(f"{router}delete",methods=["POST"])
def deleteWord():
    if db_user.check_token(request.cookies.get('user_token')) is False or "user_token" not in request.cookies:
        return redirect(url_for('users.connexion'))
    
    if request.method == "POST":
        id = request.form["id"]

    if db_dict.getWord(id):
        if db_dict.removeWord(id):
            return (f"""
                <h1>Le mot a été supprimé</h1>
            """)
        else:
            return(f"""
                <h1>Le mot n'a pas pu être supprimé de la base de donnée ou bien n'existe pas dans celle-ci ! </h1>
            """)

@dict.route(f"{router}search",methods=["POST"])
def searchWord():
    if request.method == "POST":
        word = request.form["word"]
        language = request.form["lang"]

    if db_dict.word_exists(word) != False:
        match language:
            case "fr":
                return jsonify(db_dict.getWord(db_dict.word_exists(word))['fr'])
            case "normand":
                return jsonify(db_dict.getWord(db_dict.word_exists(word))['normand'])
            case _:
                return (jsonify(False))
    else:
        return (f""" 
            <h1> {word} n'a pas été trouvé ! </h1>
        """)

@dict.route(f"{router}",methods=["GET"])
def getAllWords():
    return db_dict.getAllWord()