import sqlite3
import csv
import requests
from io import StringIO
import os

DB_PATH = "violations_mtl.db"
CSV_URL = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

def import_data():
    if not os.path.exists(DB_PATH):
        print(f"❌ La base '{DB_PATH}' n'existe pas.")
        return

    print("➡️ Téléchargement du CSV...")
    response = requests.get(CSV_URL)
    content = response.content.decode('utf-8')

    csv_data = csv.DictReader(StringIO(content))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    count = 0
    for row in csv_data:
        try:
            cursor.execute("""
                INSERT INTO violations (
                    id_poursuite,
                    business_id,
                    date,
                    description,
                    adresse,
                    date_jugement,
                    etablissement,
                    montant,
                    proprietaire,
                    ville,
                    statut,
                    date_statut,
                    categorie
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get("id_poursuite"),
                row.get("business_id"),
                row.get("date"),
                row.get("description"),
                row.get("adresse"),
                row.get("date_jugement"),
                row.get("etablissement"),
                float(row.get("montant") or 0),
                row.get("proprietaire"),
                row.get("ville"),
                row.get("statut"),
                row.get("date_statut"),
                row.get("categorie")
            ))
            count += 1
        except Exception as e:
            print("⚠️ Erreur d'insertion :", e)
            print("Ligne fautive :", row)

    conn.commit()
    conn.close()
    print(f"✅ Importation terminée. {count} lignes insérées.")


def get_all_violations():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM violations")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_violations(nom=None, proprietaire=None, rue=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM violations WHERE 1=1"
    params = []

    if nom:
        query += " AND LOWER(etablissement) LIKE ?"
        params.append(f"%{nom.lower()}%")

    if proprietaire:
        query += " AND LOWER(proprietaire) LIKE ?"
        params.append(f"%{proprietaire.lower()}%")

    if rue:
        query += " AND LOWER(adresse) LIKE ?"
        params.append(f"%{rue.lower()}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

import sqlite3

def get_contraventions_date(du, au):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    query = """
        SELECT * FROM violations
        WHERE date >= ? AND date <= ?
    """
    cursor.execute(query, (du, au))
    rows = cursor.fetchall()

    result = [dict(row) for row in rows]
    conn.close()
    return result

def get_infractions_by_nom(nom_etablissement):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
        SELECT * FROM violations
        WHERE etablissement = ?
    """
    cur.execute(query, (nom_etablissement,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]



