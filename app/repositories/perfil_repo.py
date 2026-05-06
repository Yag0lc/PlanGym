from models.usuario_db import Usuario
from models.rutina_db import Rutina
from models.calendario_db import DiaCompletado
from database.db import db
from werkzeug.security import generate_password_hash


def obtenerUsuario(id_usuario):
    return Usuario.query.filter_by(id=id_usuario).first()


def obtenerEstadisticas(id_usuario):
    total_rutinas = Rutina.query.filter_by(id_usuario=id_usuario).count()
    total_dias = DiaCompletado.query.filter_by(id_usuario=id_usuario).count()
    return {
        'total_rutinas': total_rutinas,
        'total_dias': total_dias
    }


def cambiarPassword(id_usuario, nueva_password):
    usuario = Usuario.query.filter_by(id=id_usuario).first()
    if usuario:
        usuario.password = generate_password_hash(nueva_password)
        db.session.commit()
        return True
    return False


def cambiarNombre(id_usuario, nuevo_nombre):
    usuario = Usuario.query.filter_by(id=id_usuario).first()
    if usuario:
        usuario.nombre = nuevo_nombre
        db.session.commit()
        return True
    return False