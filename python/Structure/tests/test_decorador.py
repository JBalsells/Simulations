import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utilidades.decorador import mediciones


@mediciones
def sumar(a, b):
    return a + b


@mediciones
def retornar_lista():
    return [1, 2, 3]


@mediciones
def retornar_string():
    return "hola"


class TestMediciones(unittest.TestCase):

    def test_retorna_tres_valores(self):
        resultado = sumar(2, 3)
        self.assertEqual(len(resultado), 3)

    def test_resultado_correcto(self):
        resultado, _, _ = sumar(2, 3)
        self.assertEqual(resultado, 5)

    def test_tiempo_es_float(self):
        _, tiempo, _ = sumar(2, 3)
        self.assertIsInstance(tiempo, float)

    def test_tiempo_es_positivo(self):
        _, tiempo, _ = sumar(2, 3)
        self.assertGreater(tiempo, 0)

    def test_memoria_es_entero(self):
        _, _, memoria = sumar(2, 3)
        self.assertIsInstance(memoria, int)

    def test_memoria_es_positiva(self):
        _, _, memoria = sumar(2, 3)
        self.assertGreater(memoria, 0)

    def test_preserva_nombre_funcion(self):
        self.assertEqual(sumar.__name__, "sumar")

    def test_funciona_con_lista(self):
        resultado, _, _ = retornar_lista()
        self.assertEqual(resultado, [1, 2, 3])

    def test_memoria_refleja_tipo(self):
        _, _, mem_int = sumar(1, 2)
        _, _, mem_lista = retornar_lista()
        self.assertLess(mem_int, mem_lista)

    def test_funciona_con_string(self):
        resultado, _, _ = retornar_string()
        self.assertEqual(resultado, "hola")


if __name__ == "__main__":
    unittest.main(verbosity=2)
