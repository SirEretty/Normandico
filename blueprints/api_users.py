from flask import Flask,Blueprint, request, jsonify, render_template, make_response,abort,redirect,flash,url_for
from model.db_users import Users
from blueprints.api_dictionnary import api_dictionnary
from markupsafe import escape
import os

api_users = Blueprint('api_users', __name__)
router = "/api/users/"

db_users = Users(os.environ['HOST'],os.environ['USER'],os.environ['PASSWORD'],os.environ['DATABASE'])

@api_users.route(f"{router}add",methods=['POST'])
def add_user(user,email,pwsd):
    if request.method != "POST":
        return abort(404)
    if request.form['email'] == "" or request.form['mdp'] == "" or request.form['user'] == "":
        return abort(403)
    if db_users.check_token(request.cookies.get('user_token')) is not False or 'user_token' not in request.cookies:
        return abort(401)
    
    email = request.form['email']
    pwsd = request.form['mdp']
    user = request.form['user']

    if db_users.check_user(email) == False:
        db_users.add_user(user,email,pwsd)
        return jsonify(True)
    else:
        return jsonify(False)
    
@api_users.route(f"{router}connect",methods=['POST'])
def connect_user(email=None,pwsd=None):
    if request.method != "POST":
        return abort(404)
    if email == None or pwsd == None:
        return abort(403)
    
    email = request.form['email']
    pwsd = request.form['mdp']

    if db_users.check_user(email,pwsd):
        resp = jsonify(True)
        resp.set_cookie('user_token', db_users.connect_user(email,pwsd))
        return jsonify (db_users.connect_user(email,pwsd))
    else:
        return jsonify(False)

@api_users.route(f"{router}token")
def has_token(token=None):
    if 'user_token' in request.cookies:
        token = request.cookies.get('user_token')
    if db_users.check_token(token) is False:
        return (jsonify(False))
    return (jsonify(True))

@api_users.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'page_not_found'}), 404)

@api_users.errorhandler(401)
def user_not_authenfication(error):
    return make_response(jsonify({'error': 'user_not_authenfication'}), 401)

@api_users.errorhandler(403)
def access_refused(error):
    return make_response(jsonify({'error': 'access_refused'}), 403)