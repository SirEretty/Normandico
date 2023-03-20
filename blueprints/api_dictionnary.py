from flask import Blueprint, request, jsonify, render_template,Flask,redirect,url_for,abort, flash
from model.db_words import Dict
from model.db_users import Users
import requests as req
import json
from markupsafe import escape
import json

api_dictionnary = Blueprint('api_dictionnary', __name__)
router = "/api/words/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db_dict = Dict(connect['host'],connect['user'],connect['password'],connect['database'])
db_user = Users(connect['host'],connect['user'],connect['password'],connect['database'])

@api_dictionnary.route(f"{router}get",methods=['GET'])
def getWord(word=None,id=None):    
    
    if id == None:
        id  = request.args.get('id', None)
    if word == None:
        word  = request.args.get('word', None)

    if id is not None or id == "":
        return jsonify(db_dict.getWord(id))
    elif word is None:
        return jsonify(db_dict.getAllWord())
    
    if db_dict.word_exists(word) != False:
        return jsonify(db_dict.getWord(db_dict.word_exists(word)))
    return jsonify(False)

@api_dictionnary.route(f"{router}add", methods=['POST'])
def addWord(word_french=None,word_normand=None,token=None):
    if 'user_token' in request.cookies:
        token = request.cookies.get('user_token')
    if request.method != "POST":
        return abort(404)
    if db_user.check_token(token) is False:
        return abort(401)
    
    if word_french == None:
        word_french = request.form["fr"]
    if word_normand == None:
        word_normand = request.form['normand']

    if db_dict.word_exists(word_french) == True:
        return jsonify(False)

    if db_dict.addWord(word_french,word_normand) == True:
        return jsonify(True)
    
    return jsonify(False)

@api_dictionnary.route(f"{router}edit",methods=["POST"])
def updateWord(id=None,french=None,normand=None,token=None):
    if 'user_token' in request.cookies:
        token = request.cookies.get('user_token')
    if request.method != "POST":
        return abort(404)
    if db_user.check_token(token) is False:
        return abort(401)
    
    if id == None:
        id = request.form["id"]
    if french == None:
        french = request.form["fr"]
    if normand == None:
        normand = request.form['normand']

    if db_dict.updateWord(id,french,normand):
        return jsonify(True)
    return jsonify(False)
    
@api_dictionnary.route(f"{router}delete",methods=["POST"])
def deleteWord(id=None,token=None):
    if 'user_token' in request.cookies:
        token = request.cookies.get('user_token')
    if request.method != "POST":
        return abort(404)
    if db_user.check_token(token) is False:
        return abort(401)

    if id == None:
        id = request.form["id"]

    if db_dict.getWord(id):
        if db_dict.removeWord(id):
            return jsonify(True)
    return jsonify(False)
    
