from flask import Flask,request,jsonify,render_template,redirect,url_for
from blueprints.dictionnary import dict
from blueprints.users import users
from markupsafe import escape

app = Flask(__name__)
app.register_blueprint(dict)
app.register_blueprint(users)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def main():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('errors/403.html'), 403
    