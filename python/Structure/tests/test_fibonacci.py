import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problemas.fibonacci import main, secuencia_fibonacci


class TestFibonacci(unittest.TestCase):

    def test_resultado_correcto(self):
        resultado, _, _ = main(10)
        self.assertEqual(resultado, 44)

    def test_n_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            main(-1)

    def test_secuencia_primeros_terminos(self):
        self.assertEqual(secuencia_fibonacci(5), [1, 2, 3, 5, 8])


if __name__ == "__main__":
    unittest.main(verbosity=2)
