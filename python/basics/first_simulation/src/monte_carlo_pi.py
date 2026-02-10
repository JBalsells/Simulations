import time
import math
import random
from multiprocessing import Pool, cpu_count


def estimate_pi_sequential(n_samples: int) -> float:
    """Estimación secuencial usando random de stdlib."""
    inside = 0
    for _ in range(n_samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n_samples


def _worker(n_samples: int) -> int:
    """Worker para multiprocessing. Retorna conteo de puntos dentro del círculo."""
    inside = 0
    for _ in range(n_samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return inside


def estimate_pi_parallel(n_samples: int, n_workers: int | None = None) -> float:
    """Estimación usando multiprocessing para dividir el trabajo."""
    if n_workers is None:
        n_workers = cpu_count() or 4

    samples_per_worker = n_samples // n_workers
    remainder = n_samples % n_workers
    chunks = [samples_per_worker + (1 if i < remainder else 0) for i in range(n_workers)]

    with Pool(processes=n_workers) as pool:
        results = pool.map(_worker, chunks)

    total_inside = sum(results)
    return 4.0 * total_inside / n_samples


def estimate_pi_numpy(n_samples: int) -> float:
    """Estimación vectorizada con NumPy (mucho más rápida)."""
    import numpy as np

    x = np.random.random(n_samples)
    y = np.random.random(n_samples)
    inside = np.sum(x * x + y * y <= 1.0)
    return 4.0 * inside / n_samples


def benchmark(n_samples: int, method: str = "sequential", n_workers: int | None = None) -> dict:
    """Ejecuta una estimación y retorna métricas de rendimiento."""
    methods = {
        "sequential": lambda: estimate_pi_sequential(n_samples),
        "parallel": lambda: estimate_pi_parallel(n_samples, n_workers),
        "numpy": lambda: estimate_pi_numpy(n_samples),
    }

    if method not in methods:
        raise ValueError(f"Método '{method}' no reconocido. Opciones: {list(methods.keys())}")

    start = time.perf_counter()
    pi_estimate = methods[method]()
    elapsed = time.perf_counter() - start

    return {
        "method": method,
        "n_samples": n_samples,
        "pi_estimate": pi_estimate,
        "error": abs(pi_estimate - math.pi),
        "elapsed_seconds": elapsed,
        "samples_per_second": n_samples / elapsed if elapsed > 0 else float("inf"),
    }


def run_full_benchmark():
    sample_sizes = [10000, 100000, 1000000, 10000000]
    methods = ["sequential", "parallel", "numpy"]
    n_workers = cpu_count()

    print(f"CPUs disponibles: {n_workers}")
    print(f"Valor real de π: {math.pi}")

    print("=" * 90)

    print(f"{'Método':<14} {'Muestras':>12} {'π estimado':>12} {'Error':>12} "
          f"{'Tiempo (s)':>12} {'Muestras/s':>14}")

    print("-" * 90)

    results = []
    for n in sample_sizes:
        for method in methods:
            result = benchmark(n, method, n_workers)
            results.append(result)
            print(f"{result['method']:<14} {result['n_samples']:>12,.0f} "
                  f"{result['pi_estimate']:>12.8f} {result['error']:>12.8f} "
                  f"{result['elapsed_seconds']:>12.6f} "
                  f"{result['samples_per_second']:>14,.0f}")
        print("-" * 90)

    return results


if __name__ == "__main__":
    run_full_benchmark()
