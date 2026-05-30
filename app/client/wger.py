import json
import time
import requests

CACHE = {}
CACHE_TTL = 60

BASE_URL = "https://wger.de/api/v2"
IDIOMA_ESPANOL = 4
IDIOMA_INGLES = 2

CATEGORIAS = {
    10: "Abdominales",
    8:  "Brazos",
    12: "Piernas",
    11: "Pecho",
    13: "Espalda",
    14: "Hombros",
    9:  "Gluteos",
}

EJERCICIOS_LOCALES = [
    {
        "id": 10001,
        "nombre": "Press banca",
        "descripcion": "Ejercicio de pecho con barra o mancuernas.",
        "categoria_id": 11,
        "imagen_url": None,
        "musculos": ["Pecho", "Triceps", "Hombros"],
    },
    {
        "id": 10002,
        "nombre": "Sentadilla",
        "descripcion": "Ejercicio principal de pierna.",
        "categoria_id": 12,
        "imagen_url": None,
        "musculos": ["Piernas", "Gluteos"],
    },
    {
        "id": 10003,
        "nombre": "Jalon al pecho",
        "descripcion": "Ejercicio de espalda en polea.",
        "categoria_id": 13,
        "imagen_url": None,
        "musculos": ["Espalda", "Biceps"],
    },
    {
        "id": 10004,
        "nombre": "Curl de biceps",
        "descripcion": "Ejercicio para trabajar el biceps.",
        "categoria_id": 8,
        "imagen_url": None,
        "musculos": ["Biceps"],
    },
]


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
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        data = respuesta.json()
        set_cache(cache_key, data)
        return data
    except Exception:
        return None


def get_ejercicios(categoria_id=None, pagina=1):
    limite = 20
    offset = (pagina - 1) * limite
    params = {"format": "json", "language": IDIOMA_ESPANOL, "limit": limite, "offset": offset}
    if categoria_id:
        params["category"] = categoria_id

    data = fetch_wger(f"{BASE_URL}/exerciseinfo/", params)
    if data is None:
        return get_ejercicios_locales(categoria_id)

    ejercicios = []
    for ej in data.get("results", []):
        ejercicios.append(adaptar_ejercicio(ej, categoria_id))

    return ejercicios


def get_ejercicio_id(ejercicio_id):
    data = fetch_wger(f"{BASE_URL}/exerciseinfo/{ejercicio_id}/?format=json")
    if data is None:
        return get_ejercicio_local_id(ejercicio_id)

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
        "categoria": CATEGORIAS.get(categoria_id, obtener_categoria(data)),
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
    traducciones = data.get("translations")

    for traduccion in traducciones:
        if traduccion.get("language") == IDIOMA_ESPANOL:
            return traduccion

    for traduccion in traducciones:
        if traduccion.get("language") == IDIOMA_INGLES:
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
    descripcion = descripcion.replace("<ol>", "").replace("</ol>", " ")
    descripcion = descripcion.replace("<ul>", "").replace("</ul>", " ")
    descripcion = descripcion.replace("<li>", "- ").replace("</li>", " ")
    descripcion = descripcion.replace("\u200b", "")
    return descripcion.strip()


def get_ejercicios_locales(categoria_id=None):
    ejercicios = EJERCICIOS_LOCALES
    if categoria_id:
        ejercicios = [ej for ej in ejercicios if ej["categoria_id"] == categoria_id]

    return [
        {
            "id": ej["id"],
            "nombre": ej["nombre"],
            "descripcion": ej["descripcion"],
            "categoria": CATEGORIAS.get(ej["categoria_id"], "General"),
            "imagen_url": ej["imagen_url"],
        }
        for ej in ejercicios
    ]


def get_ejercicio_local_id(ejercicio_id):
    for ej in EJERCICIOS_LOCALES:
        if ej["id"] == ejercicio_id:
            return {
                "id": ej["id"],
                "nombre": ej["nombre"],
                "descripcion": ej["descripcion"],
                "categoria": CATEGORIAS.get(ej["categoria_id"], "General"),
                "imagen_url": ej["imagen_url"],
                "musculos": ej["musculos"],
            }

    return None
