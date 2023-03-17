from flask import Flask,request,jsonify,render_template,redirect,url_for
from blueprints.router import router
from blueprints.api_dictionnary import api_dictionnary
from blueprints.api_users import api_users
from markupsafe import escape

app = Flask(__name__)
app.register_blueprint(router)
app.register_blueprint(api_users)
app.register_blueprint(api_dictionnary)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
