from flask import Flask, render_template, request, redirect, url_for,jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database import import_data  
import database

app = Flask(__name__)

def mise_a_jour_quotidienne():
    print(f"[{datetime.now()}] 🔄 Mise à jour des données...")
    import_data()

scheduler = BackgroundScheduler()
scheduler.add_job(mise_a_jour_quotidienne, trigger='cron', hour=0, minute=0)
scheduler.start()

import atexit
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recherche', methods=['GET'])
def recherche():
    nom = request.args.get("nom")
    proprio = request.args.get("proprietaire")
    rue = request.args.get("rue")
    resultats = database.search_violations(nom, proprio, rue)
    return render_template("resultats.html", violations=resultats)

@app.route('/contrevenants', methods=['GET'])
def liste_contraventions():
    du = request.args.get('du')
    au = request.args.get('au')

    if not du or not au:
        return jsonify({"error": "Paramètres 'du' et 'au' requis"}), 400

    try:
        resultats = database.get_contraventions_date(du, au)
        return jsonify(resultats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/doc')
def documentation():
    with open("static/documentation.raml", "r", encoding="utf-8") as f:
        contenu_raml = f.read()
    return render_template("doc.html", raml=contenu_raml)

@app.route('/infractions')
def infractions_par_nom():
    nom = request.args.get('nom')
    if not nom:
        return jsonify({"error": "Nom requis"}), 400
    try:
        resultats = database.get_infractions_by_nom(nom)
        return jsonify(resultats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
