import repositories.calendario_repo as calendario_repo


def obtenerDias(id_usuario, mes, anio):
    return calendario_repo.obtenerDiasCompletados(id_usuario, mes, anio)


def marcarDia(id_usuario, dia, mes, anio):
    return calendario_repo.marcarDia(id_usuario, dia, mes, anio)


def desmarcarDia(id_usuario, dia, mes, anio):
    return calendario_repo.desmarcarDia(id_usuario, dia, mes, anio)
