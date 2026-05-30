import sys
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from services.calendario_service import validarFecha, validarMesAnio
from services.perfil_service import actualizarNombre, actualizarPassword
from services.rutina_service import limpiarEjercicios
from client.wger import limpiar_descripcion, get_ejercicios_locales, get_ejercicio_local_id


class CalendarioServiceTest(unittest.TestCase):
    def test_mes_y_anio_validos(self):
        self.assertTrue(validarMesAnio(5, 2026))

    def test_mes_invalido(self):
        self.assertFalse(validarMesAnio(13, 2026))

    def test_fecha_valida(self):
        self.assertTrue(validarFecha(29, 2, 2024))

    def test_fecha_invalida(self):
        self.assertFalse(validarFecha(31, 2, 2026))


class RutinaServiceTest(unittest.TestCase):
    def test_normalizar_ejercicios_limpia_textos_vacios(self):
        ejercicios = limpiarEjercicios([" Sentadilla ", "", "Plancha"])
        self.assertEqual(ejercicios, [
            {"nombre": "Sentadilla", "dia_semana": "lunes"},
            {"nombre": "Plancha", "dia_semana": "lunes"}
        ])

    def test_normalizar_ejercicios_rechaza_no_lista(self):
        self.assertEqual(limpiarEjercicios("Sentadilla"), [])

    def test_normalizar_ejercicios_guarda_dia_semana(self):
        ejercicios = limpiarEjercicios([
            {"nombre": "Press banca", "dia_semana": "martes"},
            {"nombre": "Remo", "dia_semana": "dia raro"}
        ])
        self.assertEqual(ejercicios, [
            {"nombre": "Press banca", "dia_semana": "martes"},
            {"nombre": "Remo", "dia_semana": "lunes"}
        ])


class PerfilServiceTest(unittest.TestCase):
    def test_actualizar_nombre_rechaza_texto_corto(self):
        self.assertFalse(actualizarNombre(1, "Ya"))

    def test_actualizar_nombre_rechaza_espacios(self):
        self.assertFalse(actualizarNombre(1, "   "))

    def test_actualizar_password_rechaza_texto_corto(self):
        self.assertFalse(actualizarPassword(1, "123"))

    def test_actualizar_password_rechaza_none(self):
        self.assertFalse(actualizarPassword(1, None))


class EjerciciosServiceTest(unittest.TestCase):
    def test_limpiar_descripcion_quita_html_basico(self):
        texto = limpiar_descripcion("<p>Hola</p><ol><li>Paso 1</li></ol>")
        self.assertEqual(texto, "Hola - Paso 1")

    def test_ejercicios_locales_filtra_categoria(self):
        ejercicios = get_ejercicios_locales(11)
        self.assertEqual(len(ejercicios), 1)
        self.assertEqual(ejercicios[0]["categoria"], "Pecho")

    def test_detalle_local_devuelve_musculos(self):
        ejercicio = get_ejercicio_local_id(10001)
        self.assertIn("Pecho", ejercicio["musculos"])


if __name__ == "__main__":
    unittest.main()
