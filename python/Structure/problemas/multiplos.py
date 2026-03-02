import argparse
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utilidades.decorador import mediciones
from utilidades.operaciones import Operaciones

def encontrar_multiplos(n: int, x: int, y: int) -> list:
    resultado = []
    for i in range(1, n):
        if i % x == 0 or i % y == 0:
            resultado.append(i)
    return resultado

@mediciones
def algoritmo(n: int, x: int, y: int) -> int:
    return Operaciones.sumar_lista(encontrar_multiplos(n, x, y))

def main(n: int, x: int, y: int) -> int:
    if n <= 0:
        raise ValueError("N debe ser un entero positivo.")
    if x <= 0 or y <= 0:
        raise ValueError("X e Y deben ser enteros positivos.")

    return algoritmo(n, x, y)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suma los múltiplos de X o Y desde 1 hasta N.")
    parser.add_argument("--n", type=int, required=True, help="Límite superior")
    parser.add_argument("--x", type=int, required=True, help="Primer divisor")
    parser.add_argument("--y", type=int, required=True, help="Segundo divisor")
    args = parser.parse_args()

    try:
        resultado, tiempo, memoria = main(args.n, args.x, args.y)
        print(f"Suma de múltiplos de {args.x} o {args.y} hasta {args.n}: {resultado}")
        print(f"Tiempo de ejecución : {tiempo:.6f} s")
        print(f"Memoria de respuesta: {memoria} bytes")
    except ValueError as e:
        print(f"Error: {e}")
