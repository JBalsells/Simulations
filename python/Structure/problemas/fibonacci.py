import argparse
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utilidades.decorador import mediciones
from utilidades.graficas import Graficas
from utilidades.operaciones import Operaciones

def secuencia_fibonacci(n: int) -> list:
    serie = []
    a, b = 1, 2
    for _ in range(n):
        serie.append(a)
        a, b = b, a + b
    return serie


@mediciones
def algoritmo(n: int):
    return Operaciones.sumar_pares(secuencia_fibonacci(n))


def main(n: int):
    if n <= 0:
        raise ValueError("N debe ser un entero positivo.")
    return algoritmo(n)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suma los términos pares de los primeros N números de Fibonacci.")
    parser.add_argument("--n", type=int, help="Cantidad de términos (opcional, usa lista interna si se omite)")
    args = parser.parse_args()

    try:
        valores_n = [args.n] if args.n is not None else [100, 1000, 10000, 100000]
        tiempos, memorias = [], []

        for n in valores_n:
            res, t, m = main(n)
            tiempos.append(t)
            memorias.append(m)
            try:
                print(f"n={n}: resultado={res}, tiempo={t:.6f}s, memoria={m}B")
            except ValueError:
                print(f"n={n}: resultado=(número muy grande), tiempo={t:.6f}s, memoria={m}B")

        Graficas(valores_n, tiempos, memorias).graficar()

    except ValueError as e:
        print(f"Error: {e}")
