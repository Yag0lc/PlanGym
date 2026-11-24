from datetime import date
from calendar import monthrange
from database.db import db
from models.calendario_db import DiaCompletado, DiaDescartado
from models.rutina_db import Rutina


def obtenerDiasCompletados(id_usuario, mes, anio):
    dias = DiaCompletado.query.filter_by(
        id_usuario=id_usuario, mes=mes, anio=anio
    ).all()
    return [d.dia for d in dias]


def marcarDia(id_usuario, dia, mes, anio):
    DiaDescartado.query.filter_by(
        id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
    ).delete()
    existe = DiaCompletado.query.filter_by(
        id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
    ).first()
    if not existe:
        nuevo = DiaCompletado(id_usuario=id_usuario, dia=dia, mes=mes, anio=anio)
        db.session.add(nuevo)
    db.session.commit()
    return True


def desmarcarDia(id_usuario, dia, mes, anio):
    dia_obj = DiaCompletado.query.filter_by(
        id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
    ).first()
    if dia_obj:
        db.session.delete(dia_obj)
    descartado = DiaDescartado.query.filter_by(
        id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
    ).first()
    if not descartado:
        db.session.add(DiaDescartado(
            id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
        ))
    db.session.commit()
    return True


def obtenerEstadosCalendario(id_usuario, mes, anio):
    completados = set(obtenerDiasCompletados(id_usuario, mes, anio))
    descartados = {
        dia.dia for dia in DiaDescartado.query.filter_by(
            id_usuario=id_usuario, mes=mes, anio=anio
        ).all()
    }
    estados = {str(dia): "completado" for dia in completados}
    rutina = Rutina.query.filter_by(id_usuario=id_usuario, activa=True).first()
    if not rutina:
        return estados

    dias_entreno = {ejercicio.dia_semana for ejercicio in rutina.ejercicios}
    nombres_dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    hoy = date.today()
    for dia in range(1, monthrange(anio, mes)[1] + 1):
        fecha = date(anio, mes, dia)
        if (fecha < hoy and nombres_dias[fecha.weekday()] in dias_entreno
                and dia not in completados and dia not in descartados):
            estados[str(dia)] = "pendiente"
    return estados
