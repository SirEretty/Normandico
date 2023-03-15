from flask import Flask,request,jsonify,render_template
import requests as req
from blueprints.dictionnary import dict
from blueprints.users import users
from markupsafe import escape
import json


app = Flask(__name__)
app.register_blueprint(dict)
app.register_blueprint(users)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/words/")
def render_words():
    r = req.get(request.environ['HTTP_REFERER']+"api/words/")
    words = r.json()
    html = ""
    for word in words:
        html += f"""
            <tr>
                <td>{word['id']}</td>
                <td>{word['fr']}</td>
                <td>{word['normand']}</td>
            </tr>
        """
    return render_template("dictionnary.html", tableWords = html)

@app.route("/connexion/")
def connexion():
    return render_template("connexion.html")

@app.route("/inscription/")
def inscription():
    return render_template("inscription.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('errors/403.html'), 403
    