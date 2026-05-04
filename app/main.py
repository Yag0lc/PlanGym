import os
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from database.db import db

from models.usuario_db import Usuario
from models.rutina_db import Rutina
from models.ejercicio_db import RutinaEjercicio
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

# === BLUEPRINTS ===
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

# === MODELOS ===
from models.usuario_db import Usuario

# === DECORADOR LOGIN ===
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated

# === RUTAS ===
@app.route('/')
def home():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('welcome.html')

@app.route('/principal')
@login_required
def dashboard():
    return render_template('calendario.html', nombre=session.get('usuario_nombre'))

# === CREAR TABLAS Y ARRANCAR (igual que el proyecto Pokémon) ===
with app.app_context():
    os.makedirs(os.path.join(BASE_DIR, '..', 'data'), exist_ok=True)
    db.create_all()
    print("Base de datos lista.")

app.run('0.0.0.0', 8080, debug=True)