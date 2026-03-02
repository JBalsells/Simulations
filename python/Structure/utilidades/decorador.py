import functools
import sys
import time


def mediciones(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        tiempo_total = time.perf_counter() - inicio
        memoria_bytes = sys.getsizeof(resultado)
        return resultado, tiempo_total, memoria_bytes
    return wrapper
