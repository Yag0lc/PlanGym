from datetime import date
import repositories.rutina_repo as rutina_repo

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def limpiarEjercicios(ejercicios):
    if not isinstance(ejercicios, list):
        return []

    resultado = []
    for ejercicio in ejercicios:
        if isinstance(ejercicio, dict):
            nombre = str(ejercicio.get("nombre", "")).strip()
            dia_semana = str(ejercicio.get("dia_semana", "lunes")).strip().lower()
        else:
            nombre = str(ejercicio).strip()
            dia_semana = "lunes"

        if nombre:
            if dia_semana not in DIAS_SEMANA:
                dia_semana = "lunes"
            resultado.append({"nombre": nombre, "dia_semana": dia_semana})

    return resultado


def crearRutina(nombre, id_usuario, ejercicios):
    ejercicios = limpiarEjercicios(ejercicios)
    if not nombre or len(nombre) < 3 or not ejercicios:
        return None
    return rutina_repo.crearRutina(nombre, id_usuario, ejercicios)


def obtenerRutinas(id_usuario):
    return rutina_repo.obtenerRutinasPorUsuario(id_usuario)


def actualizarRutina(id_rutina, id_usuario, nombre, ejercicios):
    ejercicios = limpiarEjercicios(ejercicios)
    if not nombre or len(nombre) < 3 or not ejercicios:
        return None
    return rutina_repo.actualizarRutina(id_rutina, id_usuario, nombre, ejercicios)


def activarRutina(id_rutina, id_usuario):
    return rutina_repo.activarRutina(id_rutina, id_usuario)


def eliminarRutina(id_rutina, id_usuario):
    return rutina_repo.eliminarRutina(id_rutina, id_usuario)


def guardarRegistroEjercicio(id_usuario, id_rutina_ejercicio, fecha, series, repeticiones, peso):
    if not isinstance(id_rutina_ejercicio, int) or not isinstance(fecha, str):
        return None
    try:
        date.fromisoformat(fecha)
        series = int(series)
        repeticiones = int(repeticiones)
        peso = float(peso)
    except (TypeError, ValueError):
        return None

    if series < 1 or series > 50 or repeticiones < 1 or repeticiones > 500 or peso < 0 or peso > 1000:
        return None
    return rutina_repo.guardarRegistro(
        id_usuario, id_rutina_ejercicio, fecha, series, repeticiones, peso
    )


def obtenerRegistrosEjercicio(id_usuario, fecha):
    try:
        date.fromisoformat(fecha)
    except (TypeError, ValueError):
        return None
    return rutina_repo.obtenerRegistrosPorFecha(id_usuario, fecha)
