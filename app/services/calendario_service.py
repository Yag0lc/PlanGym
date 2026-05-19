from calendar import monthrange
import repositories.calendario_repo as calendario_repo


def validarMesAnio(mes, anio):
    return isinstance(mes, int) and isinstance(anio, int) and 1 <= mes <= 12 and 2000 <= anio <= 2100


def validarFecha(dia, mes, anio):
    if not validarMesAnio(mes, anio) or not isinstance(dia, int):
        return False
    return 1 <= dia <= monthrange(anio, mes)[1]


def obtenerDias(id_usuario, mes, anio):
    if not validarMesAnio(mes, anio):
        return None
    return calendario_repo.obtenerDiasCompletados(id_usuario, mes, anio)


def marcarDia(id_usuario, dia, mes, anio):
    if not validarFecha(dia, mes, anio):
        return None
    return calendario_repo.marcarDia(id_usuario, dia, mes, anio)


def desmarcarDia(id_usuario, dia, mes, anio):
    if not validarFecha(dia, mes, anio):
        return None
    return calendario_repo.desmarcarDia(id_usuario, dia, mes, anio)
