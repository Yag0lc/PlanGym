from calendar import monthrange
import repositories.calendario_repo as calendario_repo


def validarMesAnio(mes, anio):
    if not isinstance(mes, int) or not isinstance(anio, int):
        return False

    if mes < 1 or mes > 12:
        return False

    if anio < 2000 or anio > 2100:
        return False

    return True


def validarFecha(dia, mes, anio):
    if not isinstance(dia, int):
        return False

    if not validarMesAnio(mes, anio):
        return False

    dias_del_mes = monthrange(anio, mes)[1]

    if dia < 1 or dia > dias_del_mes:
        return False

    return True


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
