import repositories.rutina_repo as rutina_repo

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def _normalizarEjercicios(ejercicios):
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
    ejercicios = _normalizarEjercicios(ejercicios)
    if not nombre or len(nombre) < 3 or not ejercicios:
        return None
    return rutina_repo.crearRutina(nombre, id_usuario, ejercicios)


def obtenerRutinas(id_usuario):
    return rutina_repo.obtenerRutinasPorUsuario(id_usuario)


def actualizarRutina(id_rutina, id_usuario, nombre, ejercicios):
    ejercicios = _normalizarEjercicios(ejercicios)
    if not nombre or len(nombre) < 3 or not ejercicios:
        return None
    return rutina_repo.actualizarRutina(id_rutina, id_usuario, nombre, ejercicios)


def activarRutina(id_rutina, id_usuario):
    return rutina_repo.activarRutina(id_rutina, id_usuario)


def eliminarRutina(id_rutina, id_usuario):
    return rutina_repo.eliminarRutina(id_rutina, id_usuario)
