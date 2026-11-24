from database.db import db
from models.rutina_db import Rutina
from models.ejercicio_db import RutinaEjercicio, RegistroEjercicio


def crearRutina(nombre, id_usuario, ejercicios):
    # Desactivar todas las rutinas del usuario antes de crear una nueva
    rutinas = Rutina.query.filter_by(id_usuario=id_usuario).all()
    for r in rutinas:
        r.activa = False

    rutina_nueva = Rutina(nombre=nombre, id_usuario=id_usuario, activa=False)
    db.session.add(rutina_nueva)
    db.session.flush()  # Para obtener el id antes del commit

    for ejercicio_datos in ejercicios:
        ejercicio = RutinaEjercicio(
            nombre=ejercicio_datos["nombre"],
            dia_semana=ejercicio_datos["dia_semana"],
            id_rutina=rutina_nueva.id
        )
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

    for ejercicio_datos in ejercicios:
        ejercicio = RutinaEjercicio(
            nombre=ejercicio_datos["nombre"],
            dia_semana=ejercicio_datos["dia_semana"],
            id_rutina=rutina.id
        )
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


def guardarRegistro(id_usuario, id_rutina_ejercicio, fecha, series, repeticiones, peso):
    ejercicio = RutinaEjercicio.query.join(Rutina).filter(
        RutinaEjercicio.id == id_rutina_ejercicio,
        Rutina.id_usuario == id_usuario
    ).first()
    if not ejercicio:
        return None

    registro = RegistroEjercicio.query.filter_by(
        id_usuario=id_usuario,
        id_rutina_ejercicio=id_rutina_ejercicio,
        fecha=fecha
    ).first()
    if not registro:
        registro = RegistroEjercicio(
            id_usuario=id_usuario,
            id_rutina_ejercicio=id_rutina_ejercicio,
            fecha=fecha,
            series=series,
            repeticiones=repeticiones,
            peso=peso
        )
        db.session.add(registro)
    else:
        registro.series = series
        registro.repeticiones = repeticiones
        registro.peso = peso

    db.session.commit()
    return registro


def obtenerRegistrosPorFecha(id_usuario, fecha):
    registros = RegistroEjercicio.query.filter_by(
        id_usuario=id_usuario, fecha=fecha
    ).all()
    return {registro.id_rutina_ejercicio: registro for registro in registros}
