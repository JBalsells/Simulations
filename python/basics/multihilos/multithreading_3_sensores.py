import threading
import time
import random

lecturas = {}
lock = threading.Lock()


def leer_sensor(nombre, demora_segundos):
    """
    Simula la lectura de un sensor que tarda 'demora_segundos'.
    En la vida real aqui iria: serial.read(), requests.get(), i2c.read(), etc.
    """
    print(f"  [{nombre}] Consultando sensor...")
    time.sleep(demora_segundos) 

    if nombre == "Temperatura":
        valor = round(random.uniform(18.0, 35.0), 1)
        unidad = "°C"
    elif nombre == "Humedad":
        valor = round(random.uniform(40.0, 90.0), 1)
        unidad = "%"
    elif nombre == "Presion":
        valor = round(random.uniform(1000.0, 1025.0), 1)
        unidad = "hPa"
    else: 
        valor = round(random.uniform(0.0, 80.0), 1)
        unidad = "km/h"

    with lock:
        lecturas[nombre] = {"valor": valor, "unidad": unidad}

    print(f"  [{nombre}] Listo: {valor} {unidad}")

sensores = [
    ("Temperatura", 2.0),
    ("Humedad",     3.0),
    ("Presion",     1.5),
    ("Viento",      2.5),
]

print("LECTURA SECUENCIAL (un sensor a la vez):")
inicio = time.time()

for nombre, demora in sensores:
    leer_sensor(nombre, demora)

tiempo_secuencial = time.time() - inicio
print(f"\nTiempo total secuencial: {tiempo_secuencial:.1f}s")
print(f"Lecturas: {lecturas}\n")

print("=" * 50)

lecturas.clear()
print("LECTURA CON MULTITHREADING (todos a la vez):")
inicio = time.time()

hilos = []
for nombre, demora in sensores:
    hilo = threading.Thread(target=leer_sensor, args=(nombre, demora))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

tiempo_threading = time.time() - inicio
print(f"\nTiempo total con threading: {tiempo_threading:.1f}s")
print(f"Lecturas: {lecturas}")
print(f"\nAhorro de tiempo: {tiempo_secuencial - tiempo_threading:.1f}s "
      f"({(1 - tiempo_threading/tiempo_secuencial)*100:.0f}% mas rapido)")
