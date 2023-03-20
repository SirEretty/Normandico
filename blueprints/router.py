from flask import Flask,Blueprint,request,jsonify,render_template,redirect,url_for,make_response,flash,abort
from blueprints.api_dictionnary import getWord, addWord, updateWord,deleteWord
from blueprints.api_users import connect_user, has_token
from markupsafe import escape

router = Blueprint('router', __name__)

@router.route("/")
def main():
    return render_template("dictionnary.html")

@router.route("/rechercher",methods=['POST'])
def rechercher():
    if request.method != 'POST':
        flash("Veuillez remplir la barre de recherche")
        return redirect('/')
    
    if request.form['mot'] == "":
        flash("Veuillez remplir la barre de recherche")
        return redirect('/')

    if getWord(word=request.form['mot']).get_json() != False:
        data = getWord(word=request.form['mot']).get_json()
        match request.form['lang']:
            case "fr":
                response = data['fr']
            case "normand":
                response = data['normand']
            case _:
                response="Le mot recherché n'est pas référencé!"
        flash(response)
        return redirect('/')
    else:
        flash("Le mot recherché n'est pas référencé!")
        return redirect('/')


@router.route("/connexion/",methods=['POST','GET'])
def connexion():
    if has_token(request.cookies.get('user_token')).get_json() != False:
        return redirect("/administration")

    if request.method == "POST":
        if request.form['email'] == "" or request.form['mdp'] == "":
            return render_template("connexion.html")
        
        email=request.form['email']
        mdp=request.form['mdp']
        if connect_user(email,mdp).get_json() == False:
            flash("Veuillez retenter de vous connecter !")
            return render_template("connexion.html")
        
        res = make_response(redirect("/administration"))
        res.set_cookie('user_token', connect_user(email,mdp).get_json())
        return res
    
    return render_template("connexion.html")

@router.route("/administration/",methods=['GET'])
def administration():
    if has_token(request.cookies.get('user_token')).get_json() == False:
        flash("Veuillez vous connecter à votre compte !")
        return redirect('/connexion/')
    
    html = ""
    try:
        for word in getWord().get_json():
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
    return render_template("administration.html", table = html)

@router.route("/administration/ajouter",methods=['POST'])
def ajouter_mot():
    if request.method != 'POST':
        abort(403)
    if has_token(request.cookies.get('user_token')).get_json() == False:
        flash("Veuillez vous connecter à votre compte !")
        return redirect('/connexion/')
    
    if addWord(word_french=request.form['fr'],word_normand=request.form['normand'],token=request.cookies.get('user_token')).get_json():
        flash("Le mot a bien été rajouté !")
        return redirect('/administration/')
    else:
        flash("Le mot n'a pas pu être rajouté !")
        return redirect('/administration/')

@router.route("/administration/modifier",methods=['POST'])
def modifier_mot():
    if request.method != 'POST':
        abort(403)
    if has_token(request.cookies.get('user_token')).get_json() == False:
        flash("Veuillez vous connecter à votre compte !")
        return redirect('/connexion/')
    
    if updateWord(id=request.form['id'],french=request.form['fr'],normand=request.form['normand'],token=request.cookies.get('user_token')).get_json() != False:
        flash("Le mot a bien été modifié !")
        return redirect('/administration/')
    else:
        flash("Le mot n'a pas pu être modifié !")
        return redirect('/administration/')

@router.route("/administration/supprimer",methods=['POST'])
def supprimer_mot():
    if request.method != 'POST':
        abort(403)
    if has_token(request.cookies.get('user_token')).get_json() == False:
        flash("Veuillez vous connecter à votre compte !")
        return redirect('/connexion/')
    
    if deleteWord(id=request.form['id'],token=request.cookies.get('user_token')).get_json() != False:
        flash("Le mot a été supprimé !")
        return redirect('/administration/')
    else:
        flash("Le mot n'a pas pu être supprimé !")
        return redirect('/administration/')

@router.route("/administration/mot",methods=['POST'])
def obtenir_mot():
    if request.method != 'POST':
        abort(403)
    if has_token(request.cookies.get('user_token')).get_json() == False:
        flash("Veuillez vous connecter à votre compte !")
        return redirect('/connexion/')
    
    if getWord(word=request.form['mot']).get_json() != False:
        data = getWord(word=request.form['mot']).get_json()
        flash(f"ID: {data['id']} | Français: {data['fr']} | Normand: {data['normand']}")
        return redirect('/administration/')
    else:
        flash("Le mot n'a pas été trouvé !")
        return redirect('/administration/')