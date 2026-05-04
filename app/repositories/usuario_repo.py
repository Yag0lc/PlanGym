from models.usuario_db import Usuario
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


def crearUsuario(nombre, email, password):
    hash_password = generate_password_hash(password)
    usuario_nuevo = Usuario(nombre=nombre, email=email, password=hash_password)
    db.session.add(usuario_nuevo)
    db.session.commit()
    return usuario_nuevo


def buscarUsuarioPorEmail(email):
    return Usuario.query.filter_by(email=email).first()


def buscarUsuarioPorId(id):
    return Usuario.query.filter_by(id=id).first()


def comprobarPassword(usuario, password):
    return check_password_hash(usuario.password, password)


def autenticarUsuario(email, password):
    usuario = buscarUsuarioPorEmail(email)
    if usuario and comprobarPassword(usuario, password):
        return usuario
    return None