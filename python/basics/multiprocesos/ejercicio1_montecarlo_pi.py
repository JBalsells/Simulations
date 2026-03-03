"""
Ejercicio 1 — Multiprocesos: Estimación de π por Monte Carlo
=============================================================
Tiramos puntos aleatorios en un cuadrado y contamos cuántos caen
dentro del círculo inscrito. La proporción nos da π/4.

      Área círculo / Área cuadrado = π/4

Con múltiples procesos repartimos los puntos entre núcleos; cada
proceso trabaja en su propia memoria (sin GIL) y al final sumamos.
El error escala como 1/√N — para ganar un decimal necesitas 100× más puntos.

Para practicar:
1. Ejecuta con N_PUNTOS = 10_000_000. ¿Cuántos decimales correctos?
2. Compara el tiempo con N_PROCESOS = 1 vs. 4.
3. ¿Por qué con threading no habría speedup pero con multiprocessing sí?
"""

import math
import multiprocessing
import random
import time


# parámetros de la simulación

N_PUNTOS   = 4_000_000   # total de puntos aleatorios
N_PROCESOS = 4            # número de procesos worker


# worker: recibe n puntos y una semilla, devuelve cuántos cayeron dentro

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


# versión secuencial para comparar tiempos

def estimar_secuencial(n_total: int) -> tuple:
    inicio = time.perf_counter()
    dentro = contar_dentro((n_total, 42))
    pi_est = 4 * dentro / n_total
    return pi_est, time.perf_counter() - inicio


# versión paralela: reparte los puntos entre procesos y suma los conteos

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


# --- demo ---

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
