import functools

def fibonacci_lento(n):
    if n <= 1:          # Caso base
        return n
    return fibonacci_lento(n - 1) + fibonacci_lento(n - 2)  # Caso recursivo

print("Fibonacci (primeros 10 numeros):")
for i in range(10):
    print(f"  fib({i}) = {fibonacci_lento(i)}")

@functools.cache
def fibonacci_rapido(n):
    if n <= 1:
        return n
    return fibonacci_rapido(n - 1) + fibonacci_rapido(n - 2)

print(f"\nfibonacci_rapido(30) = {fibonacci_rapido(30)}")
print(f"fibonacci_rapido(50) = {fibonacci_rapido(50)}")
print("(El lento tardaria mucho en calcular fib(50)!)")


def busqueda_binaria(lista, objetivo, inicio=0, fin=None):
    if fin is None:
        fin = len(lista) - 1

    if inicio > fin:
        return -1

    medio = (inicio + fin) // 2

    if lista[medio] == objetivo:
        return medio

    elif objetivo < lista[medio]:
        return busqueda_binaria(lista, objetivo, inicio, medio - 1)
    else:
        return busqueda_binaria(lista, objetivo, medio + 1, fin)


numeros = list(range(0, 100, 2))  # [0, 2, 4, 6, ..., 98]
print(f"\nBusqueda binaria en lista de {len(numeros)} numeros pares:")
print(f"  Buscando 42 -> posicion: {busqueda_binaria(numeros, 42)}")
print(f"  Buscando 7  -> posicion: {busqueda_binaria(numeros, 7)} (no existe)")
print(f"  Buscando 0  -> posicion: {busqueda_binaria(numeros, 0)}")