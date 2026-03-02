import argparse
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utilidades.decorador import mediciones
from utilidades.graficas import Graficas


def factor_primo_maximo(n: int) -> int:
    factor = None

    while n % 2 == 0:
        factor = 2
        n //= 2

    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factor = divisor
            n //= divisor
        divisor += 2

    if n > 1:
        factor = n

    return factor


@mediciones
def algoritmo(n: int) -> int:
    return factor_primo_maximo(n)


def main(n: int):
    if n < 2:
        raise ValueError("N debe ser un entero mayor o igual a 2.")
    return algoritmo(n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encuentra el factor primo máximo de cada número en una lista interna.")
    parser.add_argument("--n", type=int, help="Número entero >= 2 (opcional, usa lista interna si se omite)")
    args = parser.parse_args()

    try:
        valores_n = [args.n] if args.n is not None else [13195, 600851475143, 9999999999971, 999999999999989]
        tiempos = []
        memorias = []

        for n in valores_n:
            resultado, tiempo, memoria = main(n)
            tiempos.append(tiempo)
            memorias.append(memoria)
            print(f"n={n}: factor primo máximo={resultado}, tiempo={tiempo:.6f} s, memoria={memoria} bytes")

        Graficas(valores_n, tiempos, memorias).graficar()

    except ValueError as e:
        print(f"Error: {e}")
