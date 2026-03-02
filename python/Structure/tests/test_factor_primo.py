import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problemas.factor_primo import factor_primo_maximo, main


class TestFactorPrimo(unittest.TestCase):

    def test_resultado_correcto(self):
        resultado, _, _ = main(13195)
        self.assertEqual(resultado, 29)

    def test_n_menor_a_2_lanza_error(self):
        with self.assertRaises(ValueError):
            main(1)

    def test_numero_primo_es_su_propio_factor(self):
        self.assertEqual(factor_primo_maximo(13), 13)


if __name__ == "__main__":
    unittest.main(verbosity=2)
