"""SunuPay API - application volontairement vulnerable (formation DevSecOps Foundation).
NE JAMAIS deployer en production."""
import hashlib
import sqlite3
import subprocess

import yaml
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lab 1 : secrets en dur dans le code
DB_PASSWORD = "Sunu!Pay#Pr0d-2026-xK9vQ2mZ7tLw"
PAYMENT_GATEWAY_TOKEN = "spg_live_8f3b2c1d9e7a6f5b4c3d2e1f0a9b8c7d"

DB = "/tmp/sunupay.db"


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
    return jsonify(service="sunupay-api", version="0.1.0")


@app.route("/accounts")
def accounts():
    # Lab 2 : injection SQL (concatenation de l'entree utilisateur)
    owner = request.args.get("owner", "")
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id, owner, balance FROM accounts WHERE owner = '" + owner + "'").fetchall()
    con.close()
    return jsonify(rows)


@app.route("/ping")
def ping():
    # Lab 2 : injection de commande
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return out.decode()


@app.route("/import", methods=["POST"])
def import_config():
    # Lab 2 : deserialisation non sure
    return jsonify(yaml.load(request.data, Loader=yaml.Loader))


@app.route("/hash")
def weak_hash():
    # Lab 2 : algorithme de hachage faible
    return hashlib.md5(request.args.get("pin", "").encode()).hexdigest()


if __name__ == "__main__":
    init_db()
    # Lab 2 : mode debug expose
    app.run(host="0.0.0.0", port=5000, debug=True)
