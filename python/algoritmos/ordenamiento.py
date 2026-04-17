"""
Algoritmos de ordenamiento — del más lento al más rápido.

1. Bubble Sort     O(n²)      — compara e intercambia pares adyacentes repetidamente
2. Selection Sort  O(n²)      — busca el mínimo y lo coloca en su posición
3. Insertion Sort  O(n²)      — inserta cada elemento en su lugar dentro de la parte ordenada
4. Merge Sort      O(n log n) — divide la lista, ordena cada mitad y las fusiona
5. Quick Sort      O(n log n) — elige un pivote y particiona en menores/mayores

Cada algoritmo está instrumentado para recolectar una métrica única que se
grafica en una figura de 2×3 subplots. El subplot (1,2) muestra el tiempo de
ejecución de todos los algoritmos en función del tamaño de la entrada.
"""

import random
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ─────────────────────────────────────────────────────────────────────────────
# 1. Bubble Sort — O(n²)
#    Métrica: intercambios realizados en cada pasada.
#    Muestra cómo el algoritmo "converge": las pasadas finales hacen cada vez
#    menos intercambios hasta llegar a cero.
# ─────────────────────────────────────────────────────────────────────────────
def bubble_sort(arr: list) -> tuple[list, list]:
    arr = arr[:]
    n = len(arr)
    swaps_per_pass = []
    for i in range(n):
        swaps = 0
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
        swaps_per_pass.append(swaps)
        if swaps == 0:
            break
    return arr, swaps_per_pass


# ─────────────────────────────────────────────────────────────────────────────
# 2. Selection Sort — O(n²)
#    Métrica: comparaciones realizadas en cada iteración.
#    Demuestra la reducción lineal: la i-ésima iteración hace exactamente n-i-1
#    comparaciones, independientemente del orden de los datos.
# ─────────────────────────────────────────────────────────────────────────────
def selection_sort(arr: list) -> tuple[list, list]:
    arr = arr[:]
    n = len(arr)
    comparisons_per_iter = []
    for i in range(n):
        min_idx = i
        comparisons = 0
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        comparisons_per_iter.append(comparisons)
    return arr, comparisons_per_iter


# ─────────────────────────────────────────────────────────────────────────────
# 3. Insertion Sort — O(n²)
#    Métrica: desplazamientos necesarios para insertar cada elemento.
#    Refleja el "costo" de cada inserción: elementos muy fuera de orden generan
#    picos altos; la curva decae cuando la lista está casi ordenada.
# ─────────────────────────────────────────────────────────────────────────────
def insertion_sort(arr: list) -> tuple[list, list]:
    arr = arr[:]
    shifts_per_element = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        shifts = 0
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            shifts += 1
        arr[j + 1] = key
        shifts_per_element.append(shifts)
    return arr, shifts_per_element


# ─────────────────────────────────────────────────────────────────────────────
# 4. Merge Sort — O(n log n)
#    Métrica: comparaciones totales por nivel de profundidad de recursión.
#    Evidencia la propiedad O(n log n): hay ~log₂(n) niveles y cada nivel
#    acumula ~n comparaciones, dando una distribución casi uniforme.
# ─────────────────────────────────────────────────────────────────────────────
def merge_sort(arr: list, depth_counts: dict = None, depth: int = 0) -> list:
    if depth_counts is None:
        depth_counts = {}
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], depth_counts, depth + 1)
    right = merge_sort(arr[mid:], depth_counts, depth + 1)
    return _merge(left, right, depth_counts, depth)


def _merge(left: list, right: list, depth_counts: dict, depth: int) -> list:
    result, i, j, comparisons = [], 0, 0, 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    depth_counts[depth] = depth_counts.get(depth, 0) + comparisons
    return result


def merge_sort_tracked(arr: list) -> tuple[list, dict]:
    depth_counts = {}
    return merge_sort(arr, depth_counts), depth_counts


# ─────────────────────────────────────────────────────────────────────────────
# 5. Quick Sort — O(n log n) promedio
#    Métrica: tamaño promedio de las sub-listas procesadas en cada nivel.
#    Ilustra la estrategia "divide y vencerás": cada nivel maneja subarreglos
#    cada vez más pequeños hasta llegar a tamaño 1.
# ─────────────────────────────────────────────────────────────────────────────
def quick_sort(arr: list, depth_sizes: list = None, depth: int = 0) -> list:
    if depth_sizes is None:
        depth_sizes = []
    if len(arr) <= 1:
        return arr[:]
    while len(depth_sizes) <= depth:
        depth_sizes.append([])
    depth_sizes[depth].append(len(arr))
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return (
        quick_sort(left, depth_sizes, depth + 1)
        + middle
        + quick_sort(right, depth_sizes, depth + 1)
    )


def quick_sort_tracked(arr: list) -> tuple[list, list]:
    depth_sizes = []
    return quick_sort(arr, depth_sizes), depth_sizes


# ─────────────────────────────────────────────────────────────────────────────
# Benchmark — tiempo vs tamaño de entrada para los 5 algoritmos
# ─────────────────────────────────────────────────────────────────────────────
_SORT_FNS = {
    "Bubble":    lambda d: bubble_sort(d)[0],
    "Selection": lambda d: selection_sort(d)[0],
    "Insertion": lambda d: insertion_sort(d)[0],
    "Merge":     lambda d: merge_sort_tracked(d)[0],
    "Quick":     lambda d: quick_sort_tracked(d)[0],
}


def run_benchmark(sizes: list[int]) -> dict[str, list[float]]:
    times = {name: [] for name in _SORT_FNS}
    for n in sizes:
        data = random.sample(range(n * 10), n)
        for name, fn in _SORT_FNS.items():
            t0 = time.perf_counter()
            fn(data)
            times[name].append((time.perf_counter() - t0) * 1000)
    return times


# ─────────────────────────────────────────────────────────────────────────────
# Visualización
# ─────────────────────────────────────────────────────────────────────────────
COLORS = {
    "Bubble":    "#e74c3c",
    "Selection": "#e67e22",
    "Insertion": "#f1c40f",
    "Merge":     "#2ecc71",
    "Quick":     "#3498db",
}


def plot_all(n: int = 300) -> None:
    data = random.sample(range(n * 10), n)

    _, swaps          = bubble_sort(data)
    _, comparisons    = selection_sort(data)
    _, shifts         = insertion_sort(data)
    _, depth_counts   = merge_sort_tracked(data)
    _, depth_sizes    = quick_sort_tracked(data)

    bench_sizes = [50, 100, 200, 400, 600, 800, 1000]
    bench_times = run_benchmark(bench_sizes)

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle("Algoritmos de Ordenamiento — Métricas por Algoritmo", fontsize=15, fontweight="bold")

    # ── 1. Bubble Sort: intercambios por pasada ──────────────────────────────
    ax = axes[0, 0]
    passes = range(1, len(swaps) + 1)
    ax.bar(passes, swaps, color=COLORS["Bubble"], edgecolor="white", linewidth=0.5)
    ax.set_title("Bubble Sort  O(n²)\nIntercambios por pasada", fontsize=10)
    ax.set_xlabel("Pasada #")
    ax.set_ylabel("Intercambios")
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # ── 2. Selection Sort: comparaciones por iteración ───────────────────────
    ax = axes[0, 1]
    iters = range(1, len(comparisons) + 1)
    ax.plot(iters, comparisons, color=COLORS["Selection"], linewidth=1.8)
    ax.fill_between(iters, comparisons, alpha=0.25, color=COLORS["Selection"])
    ax.set_title("Selection Sort  O(n²)\nComparaciones por iteración", fontsize=10)
    ax.set_xlabel("Iteración #")
    ax.set_ylabel("Comparaciones")

    # ── 3. Insertion Sort: desplazamientos por elemento ──────────────────────
    ax = axes[0, 2]
    elems = range(1, len(shifts) + 1)
    ax.scatter(elems, shifts, color=COLORS["Insertion"], s=6, alpha=0.7)
    window = 15
    moving_avg = [
        sum(shifts[max(0, i - window): i + 1]) / len(shifts[max(0, i - window): i + 1])
        for i in range(len(shifts))
    ]
    ax.plot(elems, moving_avg, color="black", linewidth=1.5, label=f"Media móvil ({window})")
    ax.set_title("Insertion Sort  O(n²)\nDesplazamientos por elemento insertado", fontsize=10)
    ax.set_xlabel("Elemento #")
    ax.set_ylabel("Desplazamientos")
    ax.legend(fontsize=8)

    # ── 4. Merge Sort: comparaciones por nivel de recursión ──────────────────
    ax = axes[1, 0]
    levels = sorted(depth_counts.keys())
    comp_vals = [depth_counts[l] for l in levels]
    ax.bar(levels, comp_vals, color=COLORS["Merge"], edgecolor="white", linewidth=0.5)
    ax.set_title("Merge Sort  O(n log n)\nComparaciones por nivel de recursión", fontsize=10)
    ax.set_xlabel("Nivel de profundidad")
    ax.set_ylabel("Comparaciones totales")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # ── 5. Quick Sort: tamaño promedio de particiones por nivel ──────────────
    ax = axes[1, 1]
    avg_sizes = [sum(s) / len(s) for s in depth_sizes]
    depths = range(len(avg_sizes))
    ax.plot(depths, avg_sizes, marker="o", color=COLORS["Quick"], linewidth=1.8, markersize=5)
    ax.set_title("Quick Sort  O(n log n)\nTamaño promedio de particiones por nivel", fontsize=10)
    ax.set_xlabel("Nivel de recursión")
    ax.set_ylabel("Tamaño promedio de sub-lista")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # ── 6. Benchmark: tiempo vs tamaño de entrada ────────────────────────────
    ax = axes[1, 2]
    for name, times in bench_times.items():
        ax.plot(bench_sizes, times, marker="o", label=name,
                color=COLORS[name], linewidth=1.8, markersize=5)
    ax.set_title("Benchmark\nTiempo de ejecución vs tamaño de entrada", fontsize=10)
    ax.set_xlabel("Tamaño de lista (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    plot_all(n=300)
