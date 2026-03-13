import threading

contador = 0

def sumar_sin_lock():
    global contador
    for _ in range(1000000):
        contador += 1

contador = 0
hilos = [threading.Thread(target=sumar_sin_lock) for _ in range(5)]

for h in hilos:
    h.start()
for h in hilos:
    h.join()

print(f"Resultado SIN lock (esperado 5000000): {contador}")
print("  -> Puede dar un numero menor porque los hilos se interfieren\n")


lock = threading.Lock()

def sumar_con_lock():
    global contador
    for _ in range(1000000):
        with lock:       # Solo un hilo entra aqui a la vez
            contador += 1

contador = 0
hilos = [threading.Thread(target=sumar_con_lock) for _ in range(5)]

for h in hilos:
    h.start()
for h in hilos:
    h.join()

print(f"Resultado CON lock (esperado 5000000): {contador}")
print("  -> Siempre correcto porque el lock protege la variable")