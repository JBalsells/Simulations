import time


def medir_tiempo(funcion):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        print(f"{funcion.__name__} tardo {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

@medir_tiempo
def suma_lenta(n):
    """Suma los primeros n numeros con un pequeño retardo simulado."""
    time.sleep(0.5)
    return sum(range(n))

@medir_tiempo
def suma_rapida(n):
    return n * (n - 1) // 2

resultado1 = suma_lenta(1_000_000)
resultado2 = suma_rapida(1_000_000)
resultado3 = suma_lenta(2_000_000)
resultado4 = suma_rapida(2_000_000)

print(f"suma_lenta  -> {resultado1}")
print(f"suma_rapida -> {resultado2}")
print(f"suma_lenta  -> {resultado3}")
print(f"suma_rapida -> {resultado4}")
