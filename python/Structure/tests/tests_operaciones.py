import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utilidades.operaciones import Operaciones


class TestSumarLista(unittest.TestCase):

    def test_lista_vacia(self):
        self.assertEqual(Operaciones.sumar_lista([]), 0)

    def test_un_elemento(self):
        self.assertEqual(Operaciones.sumar_lista([7]), 7)

    def test_varios_elementos(self):
        self.assertEqual(Operaciones.sumar_lista([1, 2, 3, 4, 5]), 15)

    def test_elementos_negativos(self):
        self.assertEqual(Operaciones.sumar_lista([-3, -2, 5]), 0)

    def test_devuelve_entero(self):
        self.assertIsInstance(Operaciones.sumar_lista([1, 2, 3]), int)


class TestSumarPares(unittest.TestCase):

    def test_lista_vacia(self):
        self.assertEqual(Operaciones.sumar_pares([]), 0)

    def test_sin_pares(self):
        self.assertEqual(Operaciones.sumar_pares([1, 3, 5, 7]), 0)

    def test_solo_pares(self):
        self.assertEqual(Operaciones.sumar_pares([2, 4, 6]), 12)

    def test_mezcla_pares_impares(self):
        self.assertEqual(Operaciones.sumar_pares([1, 2, 3, 4, 5, 6]), 12)

    def test_un_elemento_par(self):
        self.assertEqual(Operaciones.sumar_pares([8]), 8)

    def test_un_elemento_impar(self):
        self.assertEqual(Operaciones.sumar_pares([7]), 0)

    def test_devuelve_entero(self):
        self.assertIsInstance(Operaciones.sumar_pares([1, 2, 3]), int)


if __name__ == "__main__":
    unittest.main(verbosity=2)
