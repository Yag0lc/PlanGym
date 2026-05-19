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
    9:  "Glúteos",
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

    data = fetch_wger(f"{BASE_URL}/exercise/", params)
    if data is None:
        return []

    ejercicios = []
    for ej in data.get("results", []):
        ejercicios.append(adaptar_ejercicio(ej, categoria_id))

    return ejercicios


def get_ejercicio_id(ejercicio_id):
    data = fetch_wger(f"{BASE_URL}/exercise/{ejercicio_id}/?format=json")
    if data is None:
        return None

    img_data = fetch_wger(f"{BASE_URL}/exerciseimage/?format=json&exercise_base={ejercicio_id}")
    imagen_url = None
    if img_data and img_data.get("results"):
        imagen_url = img_data["results"][0].get("image")

    return adaptar_ejercicio_detalle(data, imagen_url)


def obtenerEjercicios(categoria_id=None, limite=20, offset=0):
    pagina = (offset // limite) + 1
    return get_ejercicios(categoria_id, pagina)


def obtenerDetalleEjercicio(ejercicio_id):
    return get_ejercicio_id(ejercicio_id)


def adaptar_ejercicio(data, categoria_id=None):
    descripcion = data.get("description") or ""
    descripcion = descripcion.replace("<p>", "").replace("</p>", " ")
    descripcion = descripcion.replace("<br>", " ").replace("<br/>", " ")
    descripcion = descripcion.strip()

    return {
        "id": data.get("id"),
        "nombre": data.get("name") or "Sin nombre",
        "descripcion": descripcion,
        "categoria": CATEGORIAS.get(categoria_id, "General"),
    }


def adaptar_ejercicio_detalle(data, imagen_url=None):
    descripcion = data.get("description") or ""
    descripcion = descripcion.replace("<p>", "").replace("</p>", " ")
    descripcion = descripcion.replace("<br>", " ").replace("<br/>", " ")
    descripcion = descripcion.strip()

    return {
        "id": data.get("id"),
        "nombre": data.get("name") or "Sin nombre",
        "descripcion": descripcion or "Sin descripción disponible.",
        "categoria": CATEGORIAS.get(data.get("category"), "General"),
        "imagen_url": imagen_url,
    }