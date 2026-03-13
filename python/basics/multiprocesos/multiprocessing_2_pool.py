import multiprocessing
import time

def procesar_numero(n):
    resultado = sum(i * i for i in range(n))
    return resultado

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":

    numeros = list(range(1, 10000001))

    #print("Buscando numeros primos SIN Pool...")
    #inicio = time.time()
    #primos_sin_pool = [n for n in numeros if es_primo(n)]
    #print(f"Encontrados: {len(primos_sin_pool)} primos")
    #print(f"Tiempo: {time.time() - inicio:.3f} segundos\n")

    print("Buscando numeros primos CON Pool...")
    inicio = time.time()

    # Pool crea tantos procesos como nucleos tenga tu computadora
    with multiprocessing.Pool() as pool:
        # map() aplica la funcion a cada elemento de la lista
        resultados = pool.map(es_primo, numeros)

    primos_con_pool = [n for n, es_p in zip(numeros, resultados) if es_p]
    print(f"Encontrados: {len(primos_con_pool)} primos")
    print(f"Tiempo: {time.time() - inicio:.3f} segundos")

    print(f"\nNucleos de CPU disponibles: {multiprocessing.cpu_count()}")
    print("El Pool usa todos los nucleos disponibles automaticamente!")
