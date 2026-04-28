from typing import Any, Callable
from unittest import TestCase

# ── Implementaciones ──────────────────────────────────────────────────────────

SortFn = Callable[[list[Any]], list[Any]]


def bubble_sort(lista: list[Any]) -> list[Any]:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(lista: list[Any]) -> list[Any]:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(lista: list[Any]) -> list[Any]:
    arr = lista[:]
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
    return arr


def merge_sort(lista: list[Any]) -> list[Any]:
    if len(lista) <= 1:
        return lista[:]
    mid = len(lista) // 2
    izquierda = merge_sort(lista[:mid])
    derecha = merge_sort(lista[mid:])
    return _merge(izquierda, derecha)


def _merge(izquierda: list[Any], derecha: list[Any]) -> list[Any]:
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


# ── Cambia esta línea para probar cualquier algoritmo de ordenamiento ─────────
ALGORITMO: SortFn = bubble_sort
# ALGORITMO = selection_sort
# ALGORITMO = insertion_sort
# ALGORITMO = merge_sort
# -----------------------------------------------------------------------------


class SortingAlgorithmTest(TestCase):

    def setUp(self) -> None:
        self.sort: SortFn = ALGORITMO
        self.lista_normal = [5, 3, 8, 1, 9, 2, 7, 4, 6]
        self.lista_ordenada = [1, 2, 3, 4, 5]
        self.lista_inversa = [5, 4, 3, 2, 1]
        self.lista_duplicados = [4, 2, 4, 1, 3, 2]
        self.lista_negativos = [-3, -1, -7, -2, -5]
        self.lista_mixta = [0, -3, 5, -1, 2]

    def test_lista_normal(self) -> None:
        resultado = self.sort(self.lista_normal)
        self.assertEqual(resultado, sorted(self.lista_normal))

    def test_lista_ya_ordenada_no_cambia(self) -> None:
        resultado = self.sort(self.lista_ordenada)
        self.assertEqual(resultado, self.lista_ordenada)

    def test_lista_orden_inverso(self) -> None:
        resultado = self.sort(self.lista_inversa)
        self.assertEqual(resultado, [1, 2, 3, 4, 5])

    def test_lista_con_duplicados(self) -> None:
        resultado = self.sort(self.lista_duplicados)
        self.assertEqual(resultado, sorted(self.lista_duplicados))

    def test_lista_un_elemento(self) -> None:
        resultado = self.sort([42])
        self.assertEqual(resultado, [42])

    def test_lista_vacia(self) -> None:
        resultado = self.sort([])
        self.assertEqual(resultado, [])

    def test_lista_negativos(self) -> None:
        resultado = self.sort(self.lista_negativos)
        self.assertEqual(resultado, [-7, -5, -3, -2, -1])

    def test_lista_mixta_con_cero_y_negativos(self) -> None:
        resultado = self.sort(self.lista_mixta)
        self.assertEqual(resultado, [-3, -1, 0, 2, 5])

    def test_no_modifica_lista_original(self) -> None:
        copia = self.lista_normal[:]
        self.sort(self.lista_normal)
        self.assertEqual(self.lista_normal, copia)

    def test_retorna_nueva_lista(self) -> None:
        resultado = self.sort(self.lista_normal)
        self.assertIsNot(resultado, self.lista_normal)

    def test_todos_iguales(self) -> None:
        resultado = self.sort([7, 7, 7, 7])
        self.assertEqual(resultado, [7, 7, 7, 7])

    def test_dos_elementos_ordenados(self) -> None:
        self.assertEqual(self.sort([1, 2]), [1, 2])

    def test_dos_elementos_desordenados(self) -> None:
        self.assertEqual(self.sort([2, 1]), [1, 2])

    def test_mantiene_todos_los_elementos(self) -> None:
        resultado = self.sort(self.lista_duplicados)
        self.assertEqual(sorted(resultado), sorted(self.lista_duplicados))
        self.assertEqual(len(resultado), len(self.lista_duplicados))

    def test_resultado_esta_ordenado(self) -> None:
        resultado = self.sort(self.lista_normal)
        for i in range(len(resultado) - 1):
            self.assertLessEqual(
                resultado[i],
                resultado[i + 1],
                f"No ordenado en posición {i}: {resultado[i]} > {resultado[i + 1]}",
            )

    def test_idempotente_doble_ordenamiento(self) -> None:
        primera_pasada = self.sort(self.lista_normal)
        segunda_pasada = self.sort(primera_pasada)
        self.assertEqual(primera_pasada, segunda_pasada)
