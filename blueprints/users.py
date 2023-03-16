from flask import Flask,Blueprint, request, jsonify, render_template, make_response,abort,redirect,flash,url_for
from model.db_users import Users
from blueprints.dictionnary import dict
from markupsafe import escape
import json

users = Blueprint('users', __name__)
router = "/api/users/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db_users = Users(connect['host'],connect['user'],connect['password'],connect['database'])

@users.route("/connexion/")
def connexion():
    if db_users.check_token(request.cookies.get('user_token')) and 'user_token' in request.cookies:
        return redirect(url_for('dictionnary.render_words'))
    return render_template("connexion.html")

@users.route(f"{router}add",methods=['POST'])
def add_user():
    if request.method != "POST":
        abort(404,description = "La page n'a pas été trouvée !")
    if request.form['email'] == "" or request.form['mdp'] == "" or request.form['user'] == "":
        abort(403,description = "L'email ou le mot de passe est vide")
    if db_users.check_token(request.cookies.get('user_token')) and 'user_token' in request.cookies:
        return render_template('administration.html')
    if db_users.check_token(request.cookies.get('user_token')) is not False or 'user_token' not in request.cookies:
        return render_template('index.html')
    
    email = request.form['email']
    pwsd = request.form['mdp']
    user = request.form['user']

    if db_users.check_user(email) == False:
        db_users.add_user(user,email,pwsd)
        return render_template('index.html')
    else:
        flash('Ce compte existe déjà')
        return redirect(url_for('administration'))
    
@users.route(f"{router}connect",methods=['POST'])
def connect_user():
    if request.method != "POST":
        return abort(404,description = "La page n'a pas été trouvée !")
    if request.form['email'] == "" or request.form['mdp'] == "":
        return abort(403,description = "L'email ou le mot de passe est vide")
    if db_users.check_token(request.cookies.get('user_token')) and 'user_token' in request.cookies:
        return render_template('administration.html')
    if db_users.check_token(request.cookies.get('user_token')) is not False or 'user_token' not in request.cookies:
        return render_template('index.html')
    
    email = request.form['email']
    pwsd = request.form['mdp']

    if db_users.check_user(email,pwsd):
        user_email = request.form['email']
        resp = redirect(url_for('dictionnary.render_words'))
        resp.set_cookie('user_email', user_email)
        resp.set_cookie('user_token', db_users.connect_user(email,pwsd))
        return resp
    else:
        return redirect(url_for('connexion'))
