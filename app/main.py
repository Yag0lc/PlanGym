import os
import logging
from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from database.db import db
from routes.perfil_routes import perfil_bp
from models.usuario_db import Usuario
from models.rutina_db import Rutina
from models.ejercicio_db import RutinaEjercicio
from routes.rutinas_routes import rutinas_bp
from models.calendario_db import DiaCompletado
from routes.calendario_routes import calendario_bp
from routes.ejercicios_routes import ejercicios_bp


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


app.config['SECRET_KEY'] = "PlanGym-Secret-Key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = False

Session(app)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'plangym.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.before_request
def registrar_peticion():
    app.logger.info("%s %s", request.method, request.path)


from routes.auth import auth_bp
app.register_blueprint(auth_bp)
app.register_blueprint(rutinas_bp)
app.register_blueprint(calendario_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(ejercicios_bp)





@app.route('/')
def home():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('welcome.html')

@app.route('/principal')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('home'))
    return render_template('calendario.html', nombre=session.get('usuario_nombre'))

with app.app_context():
    os.makedirs(os.path.join(BASE_DIR, '..', 'data'), exist_ok=True)
    db.create_all()
    print("Base de datos lista.")


if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug=True)
