"""
Tests unitarios para algoritmos de ordenamiento.

Cubre: bubble sort, selection sort, insertion sort y merge sort.
Ejecutar con: pytest tests.py -v
"""

import pytest


# ── Implementaciones ──────────────────────────────────────────────────────────

def bubble_sort(lista: list) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(lista: list) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(lista: list) -> list:
    arr = lista[:]
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
    return arr


def merge_sort(lista: list) -> list:
    if len(lista) <= 1:
        return lista[:]
    mid = len(lista) // 2
    izquierda = merge_sort(lista[:mid])
    derecha = merge_sort(lista[mid:])
    return _merge(izquierda, derecha)


def _merge(izquierda: list, derecha: list) -> list:
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


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def lista_normal():
    return [5, 3, 8, 1, 9, 2, 7, 4, 6]

@pytest.fixture
def lista_ya_ordenada():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def lista_orden_inverso():
    return [5, 4, 3, 2, 1]

@pytest.fixture
def lista_con_duplicados():
    return [4, 2, 4, 1, 3, 2]

@pytest.fixture
def lista_un_elemento():
    return [42]

@pytest.fixture
def lista_vacia():
    return []

@pytest.fixture
def lista_negativos():
    return [-3, -1, -7, -2, -5]

@pytest.fixture
def lista_mixta():
    return [0, -3, 5, -1, 2]


# ── Parametrize: corre los mismos casos en los 4 algoritmos ──────────────────

ALGORITMOS = [bubble_sort, selection_sort, insertion_sort, merge_sort]
IDS = ["bubble_sort", "selection_sort", "insertion_sort", "merge_sort"]


@pytest.mark.parametrize("algoritmo", ALGORITMOS, ids=IDS)
class TestOrdenamientoGeneral:
    """Suite compartida que todos los algoritmos deben superar."""

    def test_lista_normal(self, algoritmo, lista_normal):
        # Arrange-Act-Assert (AAA): el patrón clásico de un unit test
        resultado = algoritmo(lista_normal)
        assert resultado == sorted(lista_normal)

    def test_lista_ya_ordenada_no_cambia(self, algoritmo, lista_ya_ordenada):
        resultado = algoritmo(lista_ya_ordenada)
        assert resultado == lista_ya_ordenada

    def test_lista_orden_inverso(self, algoritmo, lista_orden_inverso):
        resultado = algoritmo(lista_orden_inverso)
        assert resultado == [1, 2, 3, 4, 5]

    def test_lista_con_duplicados(self, algoritmo, lista_con_duplicados):
        resultado = algoritmo(lista_con_duplicados)
        assert resultado == sorted(lista_con_duplicados)

    def test_lista_un_elemento(self, algoritmo, lista_un_elemento):
        resultado = algoritmo(lista_un_elemento)
        assert resultado == [42]

    def test_lista_vacia(self, algoritmo, lista_vacia):
        resultado = algoritmo(lista_vacia)
        assert resultado == []

    def test_lista_negativos(self, algoritmo, lista_negativos):
        resultado = algoritmo(lista_negativos)
        assert resultado == [-7, -5, -3, -2, -1]

    def test_lista_mixta_con_cero_y_negativos(self, algoritmo, lista_mixta):
        resultado = algoritmo(lista_mixta)
        assert resultado == [-3, -1, 0, 2, 5]

    def test_no_modifica_lista_original(self, algoritmo, lista_normal):
        copia = lista_normal[:]
        algoritmo(lista_normal)
        assert lista_normal == copia

    def test_mantiene_todos_los_elementos(self, algoritmo, lista_con_duplicados):
        resultado = algoritmo(lista_con_duplicados)
        assert sorted(resultado) == sorted(lista_con_duplicados)
        assert len(resultado) == len(lista_con_duplicados)

    def test_lista_grande(self, algoritmo):
        import random
        lista = random.sample(range(1000), 500)
        resultado = algoritmo(lista)
        assert resultado == sorted(lista)

    def test_lista_dos_elementos_ordenados(self, algoritmo):
        assert algoritmo([1, 2]) == [1, 2]

    def test_lista_dos_elementos_desordenados(self, algoritmo):
        assert algoritmo([2, 1]) == [1, 2]

    def test_todos_iguales(self, algoritmo):
        assert algoritmo([7, 7, 7, 7]) == [7, 7, 7, 7]

    def test_retorna_nueva_lista(self, algoritmo, lista_normal):
        resultado = algoritmo(lista_normal)
        assert resultado is not lista_normal


# ── Tests específicos de Merge Sort ──────────────────────────────────────────

class TestMergeSortEspecifico:

    def test_helper_merge_dos_listas_ordenadas(self):
        assert _merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

    def test_helper_merge_primera_lista_vacia(self):
        assert _merge([], [1, 2, 3]) == [1, 2, 3]

    def test_helper_merge_segunda_lista_vacia(self):
        assert _merge([1, 2, 3], []) == [1, 2, 3]

    def test_helper_merge_listas_de_un_elemento(self):
        assert _merge([2], [1]) == [1, 2]

    def test_recursion_lista_profunda(self):
        lista = list(range(100, 0, -1))
        assert merge_sort(lista) == list(range(1, 101))


# ── Tests de tipo de datos / edge cases ──────────────────────────────────────

class TestTiposDeDatos:

    def test_bubble_sort_strings(self):
        resultado = bubble_sort(["banana", "apple", "cherry"])
        assert resultado == ["apple", "banana", "cherry"]

    def test_insertion_sort_floats(self):
        resultado = insertion_sort([3.14, 1.41, 2.71, 0.57])
        assert resultado == pytest.approx([0.57, 1.41, 2.71, 3.14])

    def test_selection_sort_strings_un_elemento(self):
        assert selection_sort(["solo"]) == ["solo"]


# ── Tests de invariantes (propiedades que siempre deben cumplirse) ────────────

class TestInvariantesDeOrdenamiento:
    """
    Property-based thinking sin hypothesis: verificamos propiedades
    matemáticas del ordenamiento en lugar de valores exactos.
    """

    def test_resultado_esta_ordenado(self, lista_normal):
        resultado = merge_sort(lista_normal)
        for i in range(len(resultado) - 1):
            assert resultado[i] <= resultado[i + 1], (
                f"No ordenado en posición {i}: {resultado[i]} > {resultado[i+1]}"
            )

    def test_longitud_se_preserva(self, lista_con_duplicados):
        assert len(bubble_sort(lista_con_duplicados)) == len(lista_con_duplicados)

    def test_elementos_se_preservan(self, lista_normal):
        resultado = selection_sort(lista_normal)
        assert set(resultado) == set(lista_normal)

    def test_idempotente_doble_ordenamiento(self, lista_normal):
        primera_pasada = merge_sort(lista_normal)
        segunda_pasada = merge_sort(primera_pasada)
        assert primera_pasada == segunda_pasada
