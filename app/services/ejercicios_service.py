import client.wger as wger

CATEGORIAS = wger.CATEGORIAS


def listarEjercicios(categoria_id=None, pagina=1):
    limite = 20
    offset = (pagina - 1) * limite
    return wger.obtenerEjercicios(categoria_id=categoria_id, limite=limite, offset=offset)


def detalleEjercicio(ejercicio_id):
    return wger.obtenerDetalleEjercicio(ejercicio_id)