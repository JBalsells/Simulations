"""
Ordenamiento con decoradores.

Los mismos 5 algoritmos, ahora decorados con:
  @medir_tiempo  — mide y muestra el tiempo de ejecución del algoritmo puro.
  @graficar(...) — captura la métrica retornada y genera su gráfico automáticamente.

Orden de apilado (de adentro hacia afuera):
    @graficar(...)   ← externo: recibe (resultado, métrica) y grafica
    @medir_tiempo    ← interno: mide el tiempo antes de graficar
    def algoritmo(...) -> (lista_ordenada, métrica)
"""

import random
import time
from functools import wraps
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ─────────────────────────────────────────────────────────────────────────────
# Decoradores
# ─────────────────────────────────────────────────────────────────────────────

def medir_tiempo(fn):
    """
    Mide el tiempo de ejecución de la función decorada.
    Imprime el resultado y lo almacena en wrapper.ultimo_tiempo_ms.
    Pasa el valor de retorno original sin modificarlo.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        resultado = fn(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000
        wrapper.ultimo_tiempo_ms = elapsed
        print(f"  [{fn.__name__}]  {elapsed:.3f} ms")
        return resultado
    wrapper.ultimo_tiempo_ms = None
    return wrapper


def graficar(titulo: str, xlabel: str, ylabel: str, color: str, plot_fn):
    """
    Captura la métrica retornada por el algoritmo y la grafica.

    Contrato con el algoritmo decorado:
        entrada : cualquier argumento
        salida  : (lista_ordenada, métrica)

    plot_fn(ax, metrica, color) es la función que dibuja la métrica en el eje.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            resultado, metrica = fn(*args, **kwargs)
            fig, ax = plt.subplots(figsize=(9, 5))
            plot_fn(ax, metrica, color)
            ax.set_title(titulo, fontsize=12, fontweight="bold")
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.tight_layout()
            plt.show()
            return resultado, metrica
        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────────────────────
# Funciones de graficado — una por algoritmo
# ─────────────────────────────────────────────────────────────────────────────

def _plot_bubble(ax, swaps_per_pass, color):
    passes = range(1, len(swaps_per_pass) + 1)
    ax.bar(passes, swaps_per_pass, color=color, edgecolor="white", linewidth=0.4)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))


def _plot_selection(ax, comparisons_per_iter, color):
    iters = range(1, len(comparisons_per_iter) + 1)
    ax.plot(iters, comparisons_per_iter, color=color, linewidth=1.8)
    ax.fill_between(iters, comparisons_per_iter, alpha=0.25, color=color)


def _plot_insertion(ax, shifts, color):
    elems = range(1, len(shifts) + 1)
    ax.scatter(elems, shifts, color=color, s=6, alpha=0.7)
    window = 15
    moving_avg = [
        sum(shifts[max(0, i - window): i + 1]) / len(shifts[max(0, i - window): i + 1])
        for i in range(len(shifts))
    ]
    ax.plot(elems, moving_avg, color="black", linewidth=1.5, label=f"Media móvil ({window})")
    ax.legend(fontsize=8)


def _plot_merge(ax, depth_counts, color):
    levels = sorted(depth_counts.keys())
    comp_vals = [depth_counts[lvl] for lvl in levels]
    ax.bar(levels, comp_vals, color=color, edgecolor="white", linewidth=0.4)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))


def _plot_quick(ax, depth_sizes, color):
    avg_sizes = [sum(s) / len(s) for s in depth_sizes]
    depths = range(len(avg_sizes))
    ax.plot(depths, avg_sizes, marker="o", color=color, linewidth=1.8, markersize=5)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))


# ─────────────────────────────────────────────────────────────────────────────
# Algoritmos decorados
# ─────────────────────────────────────────────────────────────────────────────

@graficar(
    titulo="Bubble Sort  O(n²) — Intercambios por pasada",
    xlabel="Pasada #",
    ylabel="Intercambios",
    color="#e74c3c",
    plot_fn=_plot_bubble,
)
@medir_tiempo
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


@graficar(
    titulo="Selection Sort  O(n²) — Comparaciones por iteración",
    xlabel="Iteración #",
    ylabel="Comparaciones",
    color="#e67e22",
    plot_fn=_plot_selection,
)
@medir_tiempo
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


@graficar(
    titulo="Insertion Sort  O(n²) — Desplazamientos por elemento insertado",
    xlabel="Elemento #",
    ylabel="Desplazamientos",
    color="#f39c12",
    plot_fn=_plot_insertion,
)
@medir_tiempo
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


@graficar(
    titulo="Merge Sort  O(n log n) — Comparaciones por nivel de recursión",
    xlabel="Nivel de profundidad",
    ylabel="Comparaciones totales",
    color="#2ecc71",
    plot_fn=_plot_merge,
)
@medir_tiempo
def merge_sort(arr: list) -> tuple[list, dict]:
    depth_counts = {}
    return _merge_sort(arr, depth_counts), depth_counts


def _merge_sort(arr: list, depth_counts: dict, depth: int = 0) -> list:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = _merge_sort(arr[:mid], depth_counts, depth + 1)
    right = _merge_sort(arr[mid:], depth_counts, depth + 1)
    return _do_merge(left, right, depth_counts, depth)


def _do_merge(left, right, depth_counts, depth):
    result, i, j, comparisons = [], 0, 0, 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    depth_counts[depth] = depth_counts.get(depth, 0) + comparisons
    return result


@graficar(
    titulo="Quick Sort  O(n log n) — Tamaño promedio de particiones por nivel",
    xlabel="Nivel de recursión",
    ylabel="Tamaño promedio de sub-lista",
    color="#3498db",
    plot_fn=_plot_quick,
)
@medir_tiempo
def quick_sort(arr: list) -> tuple[list, list]:
    depth_sizes = []
    return _quick_sort(arr, depth_sizes), depth_sizes


def _quick_sort(arr: list, depth_sizes: list, depth: int = 0) -> list:
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
        _quick_sort(left, depth_sizes, depth + 1)
        + middle
        + _quick_sort(right, depth_sizes, depth + 1)
    )


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    n = 300
    data = random.sample(range(n * 10), n)

    print(f"\nOrdenando {n} elementos — cada algoritmo mostrará su gráfico al terminar\n")

    for fn in [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort]:
        resultado, _ = fn(data)
        assert resultado == sorted(data), f"{fn.__name__} produce resultado incorrecto"

    print("\nTodos los algoritmos verificados correctamente.")
