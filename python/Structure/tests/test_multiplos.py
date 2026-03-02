import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problemas.multiplos import encontrar_multiplos, main


class TestMultiplos(unittest.TestCase):

    def test_resultado_correcto(self):
        resultado, _, _ = main(10, 3, 5)
        self.assertEqual(resultado, 23)

    def test_n_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            main(-1, 3, 5)

    def test_encontrar_multiplos_caso_base(self):
        self.assertEqual(encontrar_multiplos(10, 3, 5), [3, 5, 6, 9])


if __name__ == "__main__":
    unittest.main(verbosity=2)
