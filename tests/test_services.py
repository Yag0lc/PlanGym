import sys
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from services.calendario_service import validarFecha, validarMesAnio
from services.rutina_service import _normalizarEjercicios


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
        ejercicios = _normalizarEjercicios([" Sentadilla ", "", "Plancha"])
        self.assertEqual(ejercicios, [
            {"nombre": "Sentadilla", "dia_semana": "lunes"},
            {"nombre": "Plancha", "dia_semana": "lunes"}
        ])

    def test_normalizar_ejercicios_rechaza_no_lista(self):
        self.assertEqual(_normalizarEjercicios("Sentadilla"), [])

    def test_normalizar_ejercicios_guarda_dia_semana(self):
        ejercicios = _normalizarEjercicios([
            {"nombre": "Press banca", "dia_semana": "martes"},
            {"nombre": "Remo", "dia_semana": "dia raro"}
        ])
        self.assertEqual(ejercicios, [
            {"nombre": "Press banca", "dia_semana": "martes"},
            {"nombre": "Remo", "dia_semana": "lunes"}
        ])


if __name__ == "__main__":
    unittest.main()
