import repositories.perfil_repo as perfil_repo


def obtenerPerfil(id_usuario):
    usuario = perfil_repo.obtenerUsuario(id_usuario)
    stats = perfil_repo.obtenerEstadisticas(id_usuario)
    return usuario, stats


def actualizarPassword(id_usuario, nueva_password):
    if len(nueva_password) < 6:
        return False
    return perfil_repo.cambiarPassword(id_usuario, nueva_password)


def actualizarNombre(id_usuario, nuevo_nombre):
    if not nuevo_nombre or len(nuevo_nombre) < 3:
        return False
    return perfil_repo.cambiarNombre(id_usuario, nuevo_nombre)