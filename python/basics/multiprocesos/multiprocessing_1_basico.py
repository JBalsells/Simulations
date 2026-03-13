import multiprocessing
import time

def calcular_cuadrados(nombre, inicio, fin):
    """Calcula el cuadrado de un rango de numeros."""
    print(f"[Proceso {nombre}] Empezando con {fin - inicio} numeros...")
    resultados = [n * n for n in range(inicio, fin)]
    print(f"[Proceso {nombre}] Terminado! Primeros 3 resultados: {resultados[:3]}")


if __name__ == "__main__":

    TOTAL = 1000000000
    mitad = TOTAL // 2

    print("SIN multiprocessing:")
    inicio = time.time()
    calcular_cuadrados("A", 0, mitad)
    calcular_cuadrados("B", mitad, TOTAL)
    print(f"Tiempo: {time.time() - inicio:.2f} segundos\n")

    print("=" * 50)

    print("CON multiprocessing:")
    inicio = time.time()

    proceso1 = multiprocessing.Process(target=calcular_cuadrados, args=("A", 0, mitad))
    proceso2 = multiprocessing.Process(target=calcular_cuadrados, args=("B", mitad, TOTAL))

    proceso1.start()
    proceso2.start()

    proceso1.join()
    proceso2.join()

    print(f"Tiempo: {time.time() - inicio:.2f} segundos")
    print("\nCon multiprocessing los dos procesos corrieron en paralelo real!")
