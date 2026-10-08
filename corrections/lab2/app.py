"""SunuPay API - version corrigee (formateur)."""
import hashlib
import os
import sqlite3

import yaml
from flask import Flask, jsonify, request

app = Flask(__name__)

# Secrets fournis par l'environnement (coffre ou secrets du pipeline), jamais dans le code
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
PAYMENT_GATEWAY_TOKEN = os.environ.get("PAYMENT_GATEWAY_TOKEN", "")

DB = os.environ.get("SUNUPAY_DB", "sunupay.db")


def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER)")
    if con.execute("SELECT COUNT(*) FROM accounts").fetchone()[0] == 0:
        con.executemany("INSERT INTO accounts (owner, balance) VALUES (?, ?)",
                        [("awa", 150000), ("moussa", 82000), ("fatou", 430000)])
    con.commit()
    con.close()


@app.route("/")
def index():
    return jsonify(service="sunupay-api", version="0.2.0")


@app.route("/accounts")
def accounts():
    owner = request.args.get("owner", "")
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id, owner, balance FROM accounts WHERE owner = ?", (owner,)).fetchall()  # requete parametree
    con.close()
    return jsonify(rows)


# Lab 2 corrige : la fonction /ping a ete supprimee. Elle ne servait pas au metier
# et permettait d'executer des commandes sur le serveur. Moins de code = moins de risque.


@app.route("/import", methods=["POST"])
def import_config():
    return jsonify(yaml.safe_load(request.data))


@app.route("/hash")
def strong_hash():
    return hashlib.sha256(request.args.get("pin", "").encode()).hexdigest()


if __name__ == "__main__":
    init_db()
    app.run(host=os.environ.get("BIND", "127.0.0.1"), port=5000, debug=False)
