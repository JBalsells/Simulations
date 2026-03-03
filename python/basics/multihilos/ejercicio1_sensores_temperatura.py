"""
Ejercicio 1 — Multihilos: Lectura paralela de sensores de temperatura
======================================================================
Conceptos: threading.Thread, time.sleep, listas compartidas, comparación
           secuencial vs. concurrente.

Contexto físico
---------------
En un experimento colocamos sensores de temperatura en distintos puntos
de un material. Cada sensor tarda un tiempo diferente en estabilizarse
y devolver su lectura (proceso de equilibrio térmico con el entorno).
Hacerlo de forma secuencial llevaría la suma de todos esos tiempos;
con hilos podemos leer todos en paralelo y reducir la espera al tiempo
del sensor más lento.

Diagrama
--------
  Sensor 1 ─── delay 1 s ──► T = 23.4 °C ─┐
  Sensor 2 ─── delay 3 s ──► T = 31.7 °C ─┤─► resultados[]
  Sensor 3 ─── delay 2 s ──► T = 18.9 °C ─┘
  ...

Tareas para el estudiante
-------------------------
1. Ejecuta el script y anota el tiempo secuencial vs. paralelo.
2. Agrega un sensor extra con delay = 4 s y observa cómo cambia
   el tiempo total paralelo (pista: debería quedarse igual al anterior
   si ningún otro sensor supera los 3 s).
3. ¿Por qué el tiempo paralelo ideal es igual al del sensor más lento?
"""

import threading
import time
import random


# ---------------------------------------------------------------------------
# Datos de los sensores
# ---------------------------------------------------------------------------

SENSORES = [
    {"id": 1, "ubicacion": "Centro",        "delay": 1.0},
    {"id": 2, "ubicacion": "Borde Norte",   "delay": 3.0},
    {"id": 3, "ubicacion": "Borde Sur",     "delay": 2.0},
    {"id": 4, "ubicacion": "Interior Alto", "delay": 1.5},
    {"id": 5, "ubicacion": "Interior Bajo", "delay": 2.5},
]

T_AMBIENTE = 20.0  # °C


# ---------------------------------------------------------------------------
# Tarea de un hilo: leer un sensor
# ---------------------------------------------------------------------------

def leer_sensor(sensor: dict, resultados: list) -> None:
    """Simula la lectura de un sensor de temperatura.

    Parámetros
    ----------
    sensor    : dict con 'id', 'ubicacion' y 'delay' (segundos).
    resultados: lista compartida donde se guarda la lectura.
    """
    sensor_id = sensor["id"]
    ubicacion = sensor["ubicacion"]
    delay     = sensor["delay"]

    print(f"  [Sensor {sensor_id} — {ubicacion}] iniciando lectura...")
    time.sleep(delay)  # simula tiempo de equilibrio térmico

    # Temperatura medida: ambiente + variación local reproducible
    random.seed(sensor_id * 7)
    temperatura = T_AMBIENTE + random.uniform(-5.0, 15.0)

    resultados.append({
        "sensor_id": sensor_id,
        "ubicacion": ubicacion,
        "temp_C":    round(temperatura, 2),
    })
    print(f"  [Sensor {sensor_id} — {ubicacion}] "
          f"T = {temperatura:.2f} °C  (delay = {delay} s)")


# ---------------------------------------------------------------------------
# Lectura SECUENCIAL (línea de base)
# ---------------------------------------------------------------------------

def medir_secuencial(sensores: list) -> tuple:
    resultados = []
    inicio = time.perf_counter()
    for s in sensores:
        leer_sensor(s, resultados)
    return resultados, time.perf_counter() - inicio


# ---------------------------------------------------------------------------
# Lectura PARALELA con hilos
# ---------------------------------------------------------------------------

def medir_paralelo(sensores: list) -> tuple:
    resultados = []
    hilos = []

    inicio = time.perf_counter()

    for s in sensores:
        hilo = threading.Thread(
            target=leer_sensor,
            args=(s, resultados),
            name=f"Hilo-Sensor-{s['id']}",
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()  # espera a que todos terminen

    return resultados, time.perf_counter() - inicio


# ---------------------------------------------------------------------------
# Análisis del perfil de temperaturas
# ---------------------------------------------------------------------------

def analizar(resultados: list) -> None:
    temps = [r["temp_C"] for r in resultados]
    t_min = min(temps)
    t_max = max(temps)
    loc_min = next(r["ubicacion"] for r in resultados if r["temp_C"] == t_min)
    loc_max = next(r["ubicacion"] for r in resultados if r["temp_C"] == t_max)

    print(f"  Promedio  : {sum(temps) / len(temps):.2f} °C")
    print(f"  Mínima    : {t_min:.2f} °C  →  {loc_min}")
    print(f"  Máxima    : {t_max:.2f} °C  →  {loc_max}")
    print(f"  Gradiente : {t_max - t_min:.2f} °C  (diferencia máx. entre zonas)")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENTO: Perfil de temperatura de un material")
    print("=" * 60)

    print("\n>>> Modo SECUENCIAL")
    res_seq, t_seq = medir_secuencial(SENSORES)
    print(f"\n  Tiempo total secuencial : {t_seq:.2f} s")
    analizar(res_seq)

    print()

    print(">>> Modo PARALELO  (un hilo por sensor)")
    res_par, t_par = medir_paralelo(SENSORES)
    print(f"\n  Tiempo total paralelo   : {t_par:.2f} s")
    analizar(res_par)

    speedup = t_seq / t_par
    t_ideal = max(s["delay"] for s in SENSORES)
    print(f"\n  Aceleración (speedup)   : {speedup:.1f}x")
    print(f"  Tiempo ahorrado         : {t_seq - t_par:.2f} s")
    print(f"  Tiempo ideal (límite)   : {t_ideal:.1f} s  "
          f"(= delay del sensor más lento)")
