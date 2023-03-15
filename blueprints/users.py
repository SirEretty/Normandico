from flask import Blueprint, request, jsonify, render_template, make_response,abort,redirect,flash,url_for
from model.db_users import Users
from markupsafe import escape
import json

users = Blueprint('users', __name__)
router = "/api/users/"

#Instance de la base de donnée
connect = None
with open("database.json","r") as f:
    connect = json.loads(f.read())
    f.close()
db = Users(connect['host'],connect['user'],connect['password'],connect['database'])

@users.route(f"{router}add",methods=['POST'])
def add_user():
        if request.method != "POST":
            abort(404,description = "La page n'a pas été trouvée !")
        if request.form['email'] == "" or request.form['mdp'] == "" or request.form['user'] == "":
            abort(403,description = "L'email ou le mot de passe est vide")

        email = request.form['email']
        pwsd = request.form['mdp']
        user = request.form['user']

        if db.check_user(email) == False:
            db.add_user(user,email,pwsd)
            return render_template('index.html')
        else:
            flash('Ce compte existe déjà')
            return redirect(url_for('inscription'))
@users.route(f"{router}connect",methods=['POST'])
def connect_user():
    if request.method != "POST":
        return render_template('404.html',reason = "L'email ou le mot de passe est vide"), 404
    if request.form['email'] == "" or request.form['mdp'] == "":
        return render_template('404.html',reason = "L'email ou le mot de passe est vide"), 404

    email = request.form['email']
    pwsd = request.form['mdp']

    if db.check_user(email,pwsd):
        user_email = request.form['email']
        resp = make_response(render_template('index.html'))
        resp.set_cookie('user_email', user_email)
        resp.set_cookie('user_token', db.connect_user(email,pwsd))
        return resp
