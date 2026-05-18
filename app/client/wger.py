import requests

BASE_URL = "https://wger.de/api/v2"
TIMEOUT = 5

# Categorías de wger en español (id -> nombre)
CATEGORIAS = {
    10: "Abdominales",
    8:  "Brazos",
    12: "Piernas",
    11: "Pecho",
    13: "Espalda",
    14: "Hombros",
    9:  "Glúteos",
}


def _get(url, params=None):
    """Petición GET con manejo de errores y timeout."""
    try:
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.HTTPError:
        return None
    except Exception:
        return None


def obtenerEjercicios(categoria_id=None, limite=20, offset=0):
    """
    Devuelve lista de ejercicios en inglés (language=2).
    Si se pasa categoria_id filtra por categoría.
    Retorna lista de dicts con: id, nombre, descripcion, categoria.
    """
    params = {
        "format": "json",
        "language": 2,
        "limit": limite,
        "offset": offset,
    }
    if categoria_id:
        params["category"] = categoria_id

    data = _get(f"{BASE_URL}/exercise/", params)
    if data is None:
        return []

    resultado = []
    for ej in data.get("results", []):
        resultado.append({
            "id": ej.get("id"),
            "nombre": ej.get("name") or "Sin nombre",
            "descripcion": _limpiarHtml(ej.get("description") or ""),
            "categoria_id": categoria_id,
            "categoria": CATEGORIAS.get(categoria_id, "General"),
        })
    return resultado


def obtenerDetalleEjercicio(ejercicio_id):
    """
    Devuelve detalle de un ejercicio: nombre, descripcion, categoria, musculos, imagen.
    Retorna None si hay error.
    """
    data = _get(f"{BASE_URL}/exercise/{ejercicio_id}/?format=json")
    if data is None:
        return None

    # Obtener info de la categoría
    categoria_nombre = "General"
    categoria_data = _get(f"{BASE_URL}/exercisecategory/{data.get('category', '')}/?format=json")
    if categoria_data:
        categoria_nombre = categoria_data.get("name", "General")

    # Obtener músculos
    musculos = []
    for m_id in data.get("muscles", []):
        m_data = _get(f"{BASE_URL}/muscle/{m_id}/?format=json")
        if m_data:
            musculos.append(m_data.get("name_en") or m_data.get("name", ""))

    # Obtener imagen si existe
    img_data = _get(f"{BASE_URL}/exerciseimage/?format=json&exercise_base={ejercicio_id}")
    imagen_url = None
    if img_data and img_data.get("results"):
        imagen_url = img_data["results"][0].get("image")

    return {
        "id": ejercicio_id,
        "nombre": data.get("name") or "Sin nombre",
        "descripcion": _limpiarHtml(data.get("description") or "Sin descripción disponible."),
        "categoria": categoria_nombre,
        "musculos": musculos,
        "imagen_url": imagen_url,
    }


def _limpiarHtml(texto):
    """Elimina tags HTML básicos de la descripción."""
    import re
    limpio = re.sub(r"<[^>]+>", " ", texto)
    limpio = re.sub(r"\s+", " ", limpio).strip()
    return limpio