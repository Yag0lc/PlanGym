from database.db import db
from models.rutina_db import Rutina
from models.ejercicio_db import RutinaEjercicio


def crearRutina(nombre, id_usuario, ejercicios):
    # Desactivar todas las rutinas del usuario antes de crear una nueva
    rutinas = Rutina.query.filter_by(id_usuario=id_usuario).all()
    for r in rutinas:
        r.activa = False

    rutina_nueva = Rutina(nombre=nombre, id_usuario=id_usuario, activa=False)
    db.session.add(rutina_nueva)
    db.session.flush()  # Para obtener el id antes del commit

    for nombre_ejercicio in ejercicios:
        ejercicio = RutinaEjercicio(nombre=nombre_ejercicio, id_rutina=rutina_nueva.id)
        db.session.add(ejercicio)

    db.session.commit()
    return rutina_nueva


def obtenerRutinasPorUsuario(id_usuario):
    return Rutina.query.filter_by(id_usuario=id_usuario).all()


def obtenerRutinaPorId(id_rutina):
    return Rutina.query.filter_by(id=id_rutina).first()


def actualizarRutina(id_rutina, id_usuario, nombre, ejercicios):
    rutina = Rutina.query.filter_by(id=id_rutina, id_usuario=id_usuario).first()
    if not rutina:
        return None

    rutina.nombre = nombre
    RutinaEjercicio.query.filter_by(id_rutina=rutina.id).delete()

    for nombre_ejercicio in ejercicios:
        ejercicio = RutinaEjercicio(nombre=nombre_ejercicio, id_rutina=rutina.id)
        db.session.add(ejercicio)

    db.session.commit()
    return rutina


def activarRutina(id_rutina, id_usuario):
    rutina_objetivo = Rutina.query.filter_by(id=id_rutina, id_usuario=id_usuario).first()
    if not rutina_objetivo:
        return False

    rutinas = Rutina.query.filter_by(id_usuario=id_usuario).all()
    for r in rutinas:
        r.activa = r.id == id_rutina
    db.session.commit()
    return True


def eliminarRutina(id_rutina, id_usuario):
    rutina = Rutina.query.filter_by(id=id_rutina, id_usuario=id_usuario).first()
    if rutina:
        db.session.delete(rutina)
        db.session.commit()
        return True
    return False
