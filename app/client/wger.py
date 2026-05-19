import requests
import time

CACHE = {}
CACHE_TTL = 60

BASE_URL = "https://wger.de/api/v2"

CATEGORIAS = {
    10: "Abdominales",
    8:  "Brazos",
    12: "Piernas",
    11: "Pecho",
    13: "Espalda",
    14: "Hombros",
    9:  "Gluteos",
}


def get_cache(key):
    if key in CACHE:
        data, caduca = CACHE[key]
        if time.time() < caduca:
            return data
    return None


def set_cache(key, data):
    CACHE[key] = (data, time.time() + CACHE_TTL)


def fetch_wger(url, params=None):
    cache_key = url + str(params)
    cache_data = get_cache(cache_key)
    if cache_data:
        return cache_data

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        set_cache(cache_key, data)
        return data
    except Exception:
        return None


def get_ejercicios(categoria_id=None, pagina=1):
    limite = 20
    offset = (pagina - 1) * limite
    params = {"format": "json", "language": 2, "limit": limite, "offset": offset}
    if categoria_id:
        params["category"] = categoria_id

    data = fetch_wger(f"{BASE_URL}/exerciseinfo/", params)
    if data is None:
        return []

    ejercicios = []
    for ej in data.get("results", []):
        ejercicios.append(adaptar_ejercicio(ej, categoria_id))

    return ejercicios


def get_ejercicio_id(ejercicio_id):
    data = fetch_wger(f"{BASE_URL}/exerciseinfo/{ejercicio_id}/?format=json")
    if data is None:
        return None

    return adaptar_ejercicio_detalle(data)


def obtenerEjercicios(categoria_id=None, limite=20, offset=0):
    pagina = (offset // limite) + 1
    return get_ejercicios(categoria_id, pagina)


def obtenerDetalleEjercicio(ejercicio_id):
    return get_ejercicio_id(ejercicio_id)


def adaptar_ejercicio(data, categoria_id=None):
    traduccion = obtener_traduccion(data)
    descripcion = limpiar_descripcion(traduccion.get("description"))

    return {
        "id": data.get("id"),
        "nombre": traduccion.get("name") or "Sin nombre",
        "descripcion": descripcion,
        "categoria": CATEGORIAS.get(categoria_id, "General"),
        "imagen_url": obtener_imagen(data),
    }


def adaptar_ejercicio_detalle(data):
    traduccion = obtener_traduccion(data)
    descripcion = limpiar_descripcion(traduccion.get("description"))

    return {
        "id": data.get("id"),
        "nombre": traduccion.get("name") or "Sin nombre",
        "descripcion": descripcion or "Sin descripcion disponible.",
        "categoria": obtener_categoria(data),
        "imagen_url": obtener_imagen(data),
        "musculos": obtener_musculos(data),
    }


def obtener_traduccion(data):
    traducciones = data.get("translations") or []

    for traduccion in traducciones:
        if traduccion.get("language") == 2:
            return traduccion

    if traducciones:
        return traducciones[0]

    return {}


def obtener_categoria(data):
    categoria = data.get("category")

    if isinstance(categoria, dict):
        return categoria.get("name") or "General"

    return CATEGORIAS.get(categoria, "General")


def obtener_imagen(data):
    imagenes = data.get("images") or []

    for imagen in imagenes:
        if imagen.get("is_main") and imagen.get("image"):
            return imagen.get("image")

    if imagenes:
        return imagenes[0].get("image")

    return None


def obtener_musculos(data):
    musculos = []

    for musculo in data.get("muscles") or []:
        if isinstance(musculo, dict):
            nombre = musculo.get("name_en") or musculo.get("name")
            if nombre:
                musculos.append(nombre)

    return musculos


def limpiar_descripcion(descripcion):
    descripcion = descripcion or ""
    descripcion = descripcion.replace("<p>", "").replace("</p>", " ")
    descripcion = descripcion.replace("<br>", " ").replace("<br/>", " ")
    descripcion = descripcion.replace("<br />", " ")
    return descripcion.strip()
