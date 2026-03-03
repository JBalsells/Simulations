"""
Ejercicio 2 — Multihilos: Movimiento Browniano de N partículas
==============================================================
Conceptos: threading.Thread, threading.Lock, estado compartido,
           condición de carrera (race condition).

Contexto físico
---------------
El movimiento Browniano describe el desplazamiento aleatorio de una
partícula suspendida en un fluido, debido a los choques con las
moléculas del medio (Einstein, 1905).

Cada partícula sigue una caminata aleatoria 2D:
    x(t+1) = x(t) + dx   donde dx ~ N(0, σ)
    y(t+1) = y(t) + dy   donde dy ~ N(0, σ)

El desplazamiento cuadrático medio (MSD) teórico es:
    <r²> = 4 D t          (en 2D)
donde D = σ² / 2 es el coeficiente de difusión efectivo.

Simulamos varias partículas en paralelo (un hilo por partícula) y
luego comparamos el MSD numérico con la predicción teórica.

Tareas para el estudiante
-------------------------
1. Aumenta N_PASOS a 1000. ¿Cómo cambia el MSD final?
2. Cambia SIGMA de 1.0 a 2.0. ¿Cómo afecta al MSD y al tiempo?
3. Quita el Lock y ejecuta varias veces. ¿Obtienes resultados
   distintos? ¿Por qué puede fallar sin el Lock?
"""

import threading
import math
import random


# ---------------------------------------------------------------------------
# Parámetros de la simulación
# ---------------------------------------------------------------------------

N_PARTICULAS = 8      # número de partículas (hilos)
N_PASOS      = 500    # pasos de tiempo por partícula
SIGMA        = 1.0    # desviación estándar del desplazamiento (m)
D_EFECTIVO   = SIGMA**2 / 2  # coeficiente de difusión (m²/paso)


# ---------------------------------------------------------------------------
# Tarea de un hilo: evolucionar una partícula
# ---------------------------------------------------------------------------

def simular_particula(
    pid: int,
    n_pasos: int,
    sigma: float,
    resultados: list,
    lock: threading.Lock,
) -> None:
    """Realiza la caminata aleatoria 2D de una partícula.

    Parámetros
    ----------
    pid       : identificador de la partícula.
    n_pasos   : número de pasos de tiempo.
    sigma     : desv. estándar del desplazamiento por paso.
    resultados: lista compartida donde se guarda el MSD final.
    lock      : cerrojo para acceso seguro a 'resultados'.
    """
    rng = random.Random(pid * 13)  # RNG independiente por partícula
    x, y = 0.0, 0.0

    for _ in range(n_pasos):
        x += rng.gauss(0, sigma)
        y += rng.gauss(0, sigma)

    msd = x**2 + y**2  # desplazamiento cuadrático al final

    # -- sección crítica: escribir en la lista compartida --
    with lock:
        resultados.append({"pid": pid, "x_final": x, "y_final": y, "msd": msd})


# ---------------------------------------------------------------------------
# Simulación con hilos
# ---------------------------------------------------------------------------

def simular_browniano(n_particulas: int, n_pasos: int, sigma: float) -> list:
    """Lanza un hilo por partícula y espera a que todos terminen."""
    resultados: list = []
    lock  = threading.Lock()
    hilos = []

    for pid in range(1, n_particulas + 1):
        hilo = threading.Thread(
            target=simular_particula,
            args=(pid, n_pasos, sigma, resultados, lock),
            name=f"Particula-{pid}",
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return resultados


# ---------------------------------------------------------------------------
# Análisis estadístico
# ---------------------------------------------------------------------------

def analizar_resultados(resultados: list, n_pasos: int) -> None:
    msds = [r["msd"] for r in resultados]
    msd_promedio = sum(msds) / len(msds)
    msd_teorico  = 4 * D_EFECTIVO * n_pasos

    print(f"  {'PID':>4}  {'x final':>10}  {'y final':>10}  {'r (m)':>10}  {'MSD (m²)':>12}")
    print("  " + "-" * 55)
    for r in sorted(resultados, key=lambda d: d["pid"]):
        r_mag = math.sqrt(r["x_final"]**2 + r["y_final"]**2)
        print(f"  {r['pid']:>4}  {r['x_final']:>10.2f}  {r['y_final']:>10.2f}  "
              f"{r_mag:>10.2f}  {r['msd']:>12.2f}")

    print(f"\n  MSD promedio (numérico)  : {msd_promedio:.2f} m²")
    print(f"  MSD teórico  4·D·t       : {msd_teorico:.2f} m²")
    error_rel = abs(msd_promedio - msd_teorico) / msd_teorico * 100
    print(f"  Error relativo           : {error_rel:.1f} %")
    print(f"  (El error disminuye al aumentar N_PARTICULAS — ley de grandes números)")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("SIMULACIÓN: Movimiento Browniano — caminata aleatoria 2D")
    print("=" * 60)
    print(f"\n  Partículas : {N_PARTICULAS}")
    print(f"  Pasos      : {N_PASOS}")
    print(f"  σ          : {SIGMA} m/paso")
    print(f"  D efectivo : {D_EFECTIVO} m²/paso")
    print()

    resultados = simular_browniano(N_PARTICULAS, N_PASOS, SIGMA)

    print("\n--- Resultados ---")
    analizar_resultados(resultados, N_PASOS)
