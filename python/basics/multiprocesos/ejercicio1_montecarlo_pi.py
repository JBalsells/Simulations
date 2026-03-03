"""
Ejercicio 1 — Multiprocesos: Estimación de π por Monte Carlo
=============================================================
Conceptos: multiprocessing.Pool, Pool.map, división de trabajo,
           combinación de resultados entre procesos.

Contexto físico
---------------
El método de Monte Carlo usa números aleatorios para resolver problemas
deterministas. Aquí estimamos π aprovechando la relación geométrica
entre un cuadrado de lado 2 y el círculo inscrito de radio 1:

      Área del círculo    π · 1²   π
      ─────────────────  = ─────  = ─
      Área del cuadrado    2 · 2    4

Algoritmo:
  1. Generar N puntos (x, y) con x, y ∈ [−1, 1].
  2. Contar cuántos caen dentro del círculo: x² + y² ≤ 1.
  3. π ≈ 4 · (puntos_dentro / N_total).

Con múltiples procesos repartimos los N puntos entre los núcleos
disponibles, cada proceso trabaja en su propio espacio de memoria
(sin GIL), y al final sumamos los conteos parciales.

Error esperado
--------------
El error estadístico del método de Monte Carlo escala como 1/√N,
así que para ganar un decimal extra de precisión necesitamos
100 veces más puntos.

Tareas para el estudiante
-------------------------
1. Ejecuta con N_PUNTOS = 10_000_000. ¿Cuántos decimales correctos?
2. Compara el tiempo con N_PROCESOS = 1 vs. N_PROCESOS = 4.
3. ¿Por qué con threading en Python esto NO daría speedup,
   pero con multiprocessing SÍ? (pista: GIL)
"""

import math
import multiprocessing
import random
import time


# ---------------------------------------------------------------------------
# Parámetros
# ---------------------------------------------------------------------------

N_PUNTOS   = 4_000_000   # total de puntos aleatorios
N_PROCESOS = 4            # número de procesos worker


# ---------------------------------------------------------------------------
# Función worker: cuenta puntos dentro del círculo
# ---------------------------------------------------------------------------

def contar_dentro(args: tuple) -> int:
    """Genera 'n' puntos aleatorios y cuenta cuántos caen en el círculo.

    Parámetros
    ----------
    args : (n, semilla) — número de puntos y semilla para reproducibilidad.

    Retorna
    -------
    Número de puntos con x² + y² ≤ 1.
    """
    n, semilla = args
    rng = random.Random(semilla)
    dentro = 0
    for _ in range(n):
        x = rng.uniform(-1, 1)
        y = rng.uniform(-1, 1)
        if x * x + y * y <= 1.0:
            dentro += 1
    return dentro


# ---------------------------------------------------------------------------
# Estimación secuencial (línea de base)
# ---------------------------------------------------------------------------

def estimar_secuencial(n_total: int) -> tuple:
    inicio = time.perf_counter()
    dentro = contar_dentro((n_total, 42))
    pi_est = 4 * dentro / n_total
    return pi_est, time.perf_counter() - inicio


# ---------------------------------------------------------------------------
# Estimación con múltiples procesos
# ---------------------------------------------------------------------------

def estimar_paralelo(n_total: int, n_procesos: int) -> tuple:
    # Repartir los puntos entre procesos (puede haber residuo)
    puntos_por_proceso = n_total // n_procesos
    residuo = n_total % n_procesos

    tareas = [
        (puntos_por_proceso + (1 if i < residuo else 0), i * 17)
        for i in range(n_procesos)
    ]

    inicio = time.perf_counter()
    with multiprocessing.Pool(processes=n_procesos) as pool:
        conteos = pool.map(contar_dentro, tareas)
    elapsed = time.perf_counter() - inicio

    total_dentro = sum(conteos)
    pi_est = 4 * total_dentro / n_total
    return pi_est, elapsed


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ESTIMACIÓN DE π — Método de Monte Carlo")
    print("=" * 60)
    print(f"\n  Puntos totales : {N_PUNTOS:,}")
    print(f"  Procesos       : {N_PROCESOS}")
    print(f"  π real         : {math.pi:.8f}")

    print("\n>>> Modo SECUENCIAL")
    pi_seq, t_seq = estimar_secuencial(N_PUNTOS)
    error_seq = abs(pi_seq - math.pi)
    print(f"  π estimado : {pi_seq:.8f}")
    print(f"  Error abs. : {error_seq:.2e}")
    print(f"  Tiempo     : {t_seq:.3f} s")

    print(f"\n>>> Modo PARALELO  ({N_PROCESOS} procesos)")
    pi_par, t_par = estimar_paralelo(N_PUNTOS, N_PROCESOS)
    error_par = abs(pi_par - math.pi)
    print(f"  π estimado : {pi_par:.8f}")
    print(f"  Error abs. : {error_par:.2e}")
    print(f"  Tiempo     : {t_par:.3f} s")

    speedup = t_seq / t_par
    print(f"\n  Speedup    : {speedup:.1f}x  (ideal ≈ {N_PROCESOS}x)")
    print(f"\n  Error teórico ~ 1/√N = {1/math.sqrt(N_PUNTOS):.2e}")
