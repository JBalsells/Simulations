import multiprocessing
import time
import random
import statistics


def simular_lecturas_historial(cantidad):
    return [random.gauss(25.0, 3.0) for _ in range(cantidad)]


def leer_y_procesar_sensor(nombre, demora_segundos, n_muestras):

    print(f"  [Proceso-{nombre}] Iniciando lectura...")
    time.sleep(demora_segundos) 

    historial = simular_lecturas_historial(n_muestras)
    valor_actual = round(historial[-1], 2)

    promedio    = round(statistics.mean(historial), 3)
    desv_std    = round(statistics.stdev(historial), 3)
    valor_min   = round(min(historial), 3)
    valor_max   = round(max(historial), 3)

    anomalias = [round(v, 2) for v in historial if abs(v - promedio) > 2 * desv_std]

    reporte = {
        "sensor":        nombre,
        "valor_actual":  valor_actual,
        "promedio":      promedio,
        "desv_std":      desv_std,
        "minimo":        valor_min,
        "maximo":        valor_max,
        "anomalias":     len(anomalias),
        "muestras":      n_muestras,
    }

    print(f"  [Proceso-{nombre}] Listo. Valor={valor_actual}, "
          f"Prom={promedio}, Anomalias={len(anomalias)}")
    return reporte


sensores = [
    ("Temperatura", 1.0, 200_000),
    ("Humedad",     1.5, 200_000),
    ("Presion",     1.0, 200_000),
    ("Viento",      2.0, 200_000),
]


if __name__ == "__main__":

    print("=" * 55)
    print("LECTURA + PROCESAMIENTO SECUENCIAL:")
    print("=" * 55)
    inicio = time.time()

    resultados_sec = []
    for nombre, demora, muestras in sensores:
        r = leer_y_procesar_sensor(nombre, demora, muestras)
        resultados_sec.append(r)

    tiempo_secuencial = time.time() - inicio
    print(f"\nTiempo total secuencial: {tiempo_secuencial:.2f}s\n")


    print("=" * 55)
    print("LECTURA + PROCESAMIENTO CON MULTIPROCESSING:")
    print("=" * 55)
    inicio = time.time()

    with multiprocessing.Pool(processes=len(sensores)) as pool:
        # starmap permite pasar multiples argumentos por elemento
        resultados_mp = pool.starmap(leer_y_procesar_sensor, sensores)

    tiempo_mp = time.time() - inicio
    print(f"\nTiempo total con multiprocessing: {tiempo_mp:.2f}s")
    print(f"Aceleracion: {tiempo_secuencial / tiempo_mp:.1f}x mas rapido")
    print(f"Nucleos utilizados: {multiprocessing.cpu_count()}")

    print("\n--- REPORTE FINAL ---")
    print(f"{'Sensor':<13} {'Valor':>7} {'Promedio':>9} {'Std':>6} {'Anomalias':>10}")
    print("-" * 50)
    for r in resultados_mp:
        print(f"{r['sensor']:<13} {r['valor_actual']:>7} "
              f"{r['promedio']:>9} {r['desv_std']:>6} {r['anomalias']:>10}")