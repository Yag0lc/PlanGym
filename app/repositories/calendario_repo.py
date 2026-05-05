from database.db import db
from models.calendario_db import DiaCompletado


def obtenerDiasCompletados(id_usuario, mes, anio):
    dias = DiaCompletado.query.filter_by(
        id_usuario=id_usuario, mes=mes, anio=anio
    ).all()
    return [d.dia for d in dias]


def marcarDia(id_usuario, dia, mes, anio):
    existe = DiaCompletado.query.filter_by(
        id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
    ).first()
    if not existe:
        nuevo = DiaCompletado(id_usuario=id_usuario, dia=dia, mes=mes, anio=anio)
        db.session.add(nuevo)
        db.session.commit()
        return True
    return False


def desmarcarDia(id_usuario, dia, mes, anio):
    dia_obj = DiaCompletado.query.filter_by(
        id_usuario=id_usuario, dia=dia, mes=mes, anio=anio
    ).first()
    if dia_obj:
        db.session.delete(dia_obj)
        db.session.commit()
        return True
    return False