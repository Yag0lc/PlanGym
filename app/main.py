
# === https://gymtracker.pro/?lng=es// ===

import os
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from database.db import db

app = Flask(__name__)

# === CONFIGURACIÓN DE SESIÓN ===
app.config['SECRET_KEY'] = "PlanGym-Secret-Key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

Session(app)

# === CONFIGURACIÓN DE BASE DE DATOS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'plangym.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# === RUTA PRINCIPAL ===
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/principal')
def dashboard():
    return render_template('calendario.html')

# === COMANDO PARA CREAR TABLAS ===
@app.cli.command("crear-tablas")
def crear_tablas():
    print("Creando estructura de base de datos...")
    db.drop_all()
    db.create_all()
    print("Base de datos creada correctamente.")


# === EJECUCIÓN ===
if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)