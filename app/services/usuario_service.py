import repositories.usuario_repo as usuario_repo


def registrarUsuario(nombre, email, password):
    if usuario_repo.buscarUsuarioPorEmail(email) is None:
        return usuario_repo.crearUsuario(nombre, email, password)
    return None


def comprobarUsuario(email, password):
    return usuario_repo.autenticarUsuario(email, password)