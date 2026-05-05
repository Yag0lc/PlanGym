import repositories.rutina_repo as rutina_repo


def crearRutina(nombre, id_usuario, ejercicios):
    if not nombre or not ejercicios:
        return None
    return rutina_repo.crearRutina(nombre, id_usuario, ejercicios)


def obtenerRutinas(id_usuario):
    return rutina_repo.obtenerRutinasPorUsuario(id_usuario)


def activarRutina(id_rutina, id_usuario):
    rutina_repo.activarRutina(id_rutina, id_usuario)


def eliminarRutina(id_rutina, id_usuario):
    return rutina_repo.eliminarRutina(id_rutina, id_usuario)