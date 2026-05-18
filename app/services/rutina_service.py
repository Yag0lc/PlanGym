import repositories.rutina_repo as rutina_repo


def _normalizarEjercicios(ejercicios):
    if not isinstance(ejercicios, list):
        return []
    return [str(e).strip() for e in ejercicios if str(e).strip()]


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
