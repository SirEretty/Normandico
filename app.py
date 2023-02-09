from flask import Flask,request,jsonify,render_template
import requests as req
from blueprints.dictionnary import appdict
from markupsafe import escape
import json


app = Flask(__name__)
app.register_blueprint(appdict)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/words/")
def renderWords():
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