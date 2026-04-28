"""
Ejemplos de linting y análisis estático en Python.

Cada sección muestra código con problemas comunes y su versión corregida,
explicando qué herramienta detectaría cada problema y por qué importa.

Ejecutar el linter sobre este mismo archivo:
    pip install ruff mypy
    ruff check ejemplos.py
    mypy ejemplos.py
"""

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1: Errores que flake8/ruff detectan (pyflakes)
# ════════════════════════════════════════════════════════════════════════════

import hashlib
import json  # noqa: F401  ← esto suprime el warning de import no usado
import os
import secrets
import subprocess
from dataclasses import dataclass
from typing import Optional


# F401 — import sin usar
# import math  # ← ruff/flake8: 'math' imported but unused


# F811 — redefinición de nombre ya importado
# import os  # ← ruff: redefinition of unused 'os'


# F821 — uso de variable no definida
# print(variable_inexistente)  # ← ruff: undefined name 'variable_inexistente'


# F841 — variable asignada pero nunca usada
def ejemplo_variable_sin_usar() -> None:
    resultado = 42  # noqa: F841  ← en código real, esto sería un bug silencioso
    print("esta función no usa 'resultado'")


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2: Violaciones de PEP 8 (pycodestyle / ruff E/W)
# ════════════════════════════════════════════════════════════════════════════

# ── Espaciado ────────────────────────────────────────────────────────────────

# ❌ E225: falta espacio alrededor de operador
# x=5+3

# ✅ Correcto
x = 5 + 3


# ❌ E231: falta espacio después de coma
# def mal(a,b,c): ...

# ✅ Correcto
def bien(a, b, c) -> int:
    return a + b + c


# ❌ E251: espacio innecesario alrededor de = en parámetros por defecto
# def funcion(x =5): ...

# ✅ Correcto
def funcion_con_default(x=5) -> int:
    return x * 2


# ── Comparaciones ────────────────────────────────────────────────────────────

def comparaciones_correctas(valor: Optional[str], activo: bool) -> None:
    # ❌ E711: comparar con None usando == en lugar de is
    # if valor == None: ...
    # if valor != None: ...

    # ✅ Correcto
    if valor is None:
        print("valor es None")
    if valor is not None:
        print(f"valor: {valor}")

    # ❌ E712: comparar booleano con == True/False
    # if activo == True: ...
    # if activo == False: ...

    # ✅ Correcto
    if activo:
        print("activo")
    if not activo:
        print("inactivo")


# ── Imports ──────────────────────────────────────────────────────────────────

# ❌ E401: múltiples imports en una línea
# import os, sys  ← ruff/isort lo separará automáticamente

# ✅ Correcto: ya importados arriba, uno por línea


# ── Líneas en blanco ─────────────────────────────────────────────────────────

# ❌ E302: se esperan 2 líneas en blanco antes de una función de nivel superior
# def mal_espaciado():
#     pass
# def otra_funcion():  ← solo 1 línea en blanco
#     pass

# ✅ Las funciones en este archivo tienen 2 líneas en blanco entre ellas


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3: Type hints y mypy
# ════════════════════════════════════════════════════════════════════════════

# ── Sin type hints: mypy no puede verificar nada ─────────────────────────────

def calcular_descuento_sin_tipos(precio, porcentaje):
    return precio * (1 - porcentaje / 100)


# ── Con type hints: mypy detecta errores de tipo antes de ejecutar ───────────

def calcular_descuento(precio: float, porcentaje: float) -> float:
    return precio * (1 - porcentaje / 100)


# Esto mypy lo detectaría como error:
# resultado = calcular_descuento("caro", 10)
# error: Argument 1 to "calcular_descuento" has incompatible type "str"; expected "float"


# ── Optional: cuando algo puede ser None ────────────────────────────────────

def buscar_usuario(user_id: int) -> Optional[str]:
    usuarios = {1: "Ana", 2: "Pedro"}
    return usuarios.get(user_id)


def saludar(user_id: int) -> None:
    nombre = buscar_usuario(user_id)

    # Sin verificar None mypy advierte: Item "None" of "str | None" has no attribute "upper"
    # print(nombre.upper())  ← potencial AttributeError en runtime

    # ✅ Verificar antes de usar
    if nombre is not None:
        print(f"Hola, {nombre.upper()}")
    else:
        print("Usuario no encontrado")


# ── Union types (Python 3.10+ usa | en lugar de Union) ──────────────────────

def procesar_id(valor: int | str) -> str:
    if isinstance(valor, int):
        return f"ID numérico: {valor}"
    return f"ID de texto: {valor}"


# ── Dataclasses con tipos: documentación gratuita ───────────────────────────


@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    activo: bool = True
    etiquetas: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.etiquetas is None:
            self.etiquetas = []
        if self.precio < 0:
            raise ValueError(f"El precio no puede ser negativo: {self.precio}")

    def precio_con_iva(self, iva: float = 0.12) -> float:
        return round(self.precio * (1 + iva), 2)


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4: Problemas que ruff/bugbear detectan (reglas B)
# ════════════════════════════════════════════════════════════════════════════

# ── B006: argumento mutable por defecto (bug clásico de Python) ───────────────

# ❌ PELIGROSO: la lista se comparte entre todas las llamadas
def agregar_elemento_mal(item: str, lista: list = []) -> list:  # noqa: B006
    lista.append(item)
    return lista


# Demostración del bug:
# >>> agregar_elemento_mal("a")
# ['a']
# >>> agregar_elemento_mal("b")   ← nueva llamada, pero...
# ['a', 'b']                      ← ¡la lista del primer llamado sigue ahí!


# ✅ Correcto: usar None como sentinel
def agregar_elemento_bien(item: str, lista: Optional[list] = None) -> list:
    if lista is None:
        lista = []
    lista.append(item)
    return lista


# ── B007: variable de loop no usada ──────────────────────────────────────────

# ❌ ruff/B007 advierte que 'i' no se usa dentro del loop
# for i in range(5):
#     print("hola")

# ✅ Usar _ cuando el valor no importa
for _ in range(5):
    pass  # convenio: _ significa "no me importa este valor"


# ── B011: no usar assert False, usar raise ────────────────────────────────────

# ❌ assert False, "mensaje"  ← los assert se pueden desactivar con -O

# ✅ Correcto
# raise AssertionError("mensaje")


# ── SIM108: ternario en lugar de if/else de una línea ────────────────────────

estado_verbose = True
# ❌ innecesariamente largo
if estado_verbose:
    etiqueta = "activo"
else:
    etiqueta = "inactivo"

# ✅ ternario (ruff/SIM108 lo sugiere automáticamente)
etiqueta = "activo" if estado_verbose else "inactivo"


# ── SIM118: usar 'in dict' en lugar de 'in dict.keys()' ──────────────────────

config = {"debug": True, "puerto": 8080}

# ❌ redundante
if "debug" in config.keys():  # noqa: SIM118
    pass

# ✅ correcto
if "debug" in config:
    pass


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5: Complejidad ciclomática — cuándo una función es demasiado compleja
# ════════════════════════════════════════════════════════════════════════════

# Complejidad ciclomática = número de caminos de ejecución posibles.
# Cada if, elif, for, while, and, or suma 1 al contador.
# Más de 10 es señal de que la función debe dividirse.

# radon cc ejemplos.py -s  ← para medirlo


# ❌ Complejidad alta (≈ 9): difícil de leer, testear y mantener
def procesar_pedido_complejo(pedido: dict) -> str:
    if pedido.get("activo"):
        if pedido.get("tipo") == "urgente":
            if pedido.get("stock", 0) > 0:
                if pedido.get("cliente_vip"):
                    return "urgente-vip-con-stock"
                else:
                    return "urgente-con-stock"
            else:
                if pedido.get("permite_espera"):
                    return "urgente-sin-stock-espera"
                else:
                    return "urgente-sin-stock-cancelado"
        elif pedido.get("tipo") == "normal":
            if pedido.get("stock", 0) > 0:
                return "normal-con-stock"
            return "normal-sin-stock"
    return "inactivo"


# ✅ Complejidad baja: cada función hace UNA cosa
def _tiene_stock(pedido: dict) -> bool:
    return pedido.get("stock", 0) > 0


def _clasificar_urgente(pedido: dict) -> str:
    if not _tiene_stock(pedido):
        return "urgente-sin-stock-espera" if pedido.get("permite_espera") else "urgente-sin-stock-cancelado"
    return "urgente-vip-con-stock" if pedido.get("cliente_vip") else "urgente-con-stock"


def procesar_pedido_simple(pedido: dict) -> str:
    if not pedido.get("activo"):
        return "inactivo"
    if pedido.get("tipo") == "urgente":
        return _clasificar_urgente(pedido)
    return "normal-con-stock" if _tiene_stock(pedido) else "normal-sin-stock"


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6: Vulnerabilidades que bandit detecta
# ════════════════════════════════════════════════════════════════════════════

# ── B303: usar MD5/SHA1 para hashing de passwords ────────────────────────────

# ❌ MD5 y SHA1 son inseguros para passwords (bandit B303)
def hashear_password_inseguro(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()  # noqa: S324


# ✅ Usar hashlib con algoritmos modernos o bcrypt/argon2
def hashear_password_seguro(password: str) -> str:
    salt = secrets.token_hex(16)
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


# ── B602/B603: subprocess con shell=True es peligroso ────────────────────────

# ❌ Si 'nombre_archivo' viene del usuario, puede ejecutar comandos arbitrarios
def listar_archivos_inseguro(directorio: str) -> None:
    # subprocess.call(f"ls {directorio}", shell=True)  # noqa: S602, S605
    pass  # comentado para no ejecutar en el ejemplo


# ✅ Pasar argumentos como lista, nunca como string con shell=True
def listar_archivos_seguro(directorio: str) -> None:
    subprocess.run(["ls", directorio], check=True)  # noqa: S603, S607


# ── B105: password hardcodeada ────────────────────────────────────────────────

# ❌ bandit B105: hardcoded password
# API_KEY = "sk-abc123secreto"  ← bandit lo detecta inmediatamente

# ✅ Leer de variable de entorno
API_KEY = os.environ.get("API_KEY", "")


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7: pyupgrade — modernizar sintaxis automáticamente
# ════════════════════════════════════════════════════════════════════════════

# ruff con la regla UP (pyupgrade) detecta sintaxis antigua y la moderniza.

# ── UP006/UP007: tipos del módulo typing que ya no necesitan importarse ───────

# ❌ Python < 3.9 requería esto
# from typing import List, Dict, Tuple
# def funcion(items: List[str]) -> Dict[str, int]: ...

# ✅ Python 3.9+: usar los built-ins directamente
def contar_palabras(palabras: list[str]) -> dict[str, int]:
    conteo: dict[str, int] = {}
    for palabra in palabras:
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


# ── UP032: f-string en lugar de .format() ─────────────────────────────────────

nombre = "mundo"

# ❌ sintaxis antigua
saludo_viejo = "Hola, {}".format(nombre)  # noqa: UP032

# ✅ f-string (más legible y rápido)
saludo_nuevo = f"Hola, {nombre}"


# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 8: Demostración práctica
# ════════════════════════════════════════════════════════════════════════════

def demo_productos() -> None:
    productos = [
        Producto(1, "Laptop", 8500.0, etiquetas=["electronica", "oferta"]),
        Producto(2, "Mouse", 220.0),
        Producto(3, "Monitor", 3200.0, activo=False),
    ]

    print("Catálogo de productos activos:")
    print("-" * 40)

    for producto in productos:
        if not producto.activo:
            continue

        precio_iva = producto.precio_con_iva()
        etiquetas = ", ".join(producto.etiquetas) if producto.etiquetas else "sin etiquetas"
        print(f"  [{producto.id}] {producto.nombre:<12} Q{precio_iva:>8.2f}  ({etiquetas})")

    print()

    # Demostrar el bug del argumento mutable
    print("Bug del argumento mutable por defecto:")
    lista1 = agregar_elemento_mal("a")
    lista2 = agregar_elemento_mal("b")
    print(f"  Llamada 1: {lista1}")
    print(f"  Llamada 2: {lista2}  ← ¡contiene 'a' aunque no se pasó!")

    print()
    print("Versión corregida:")
    lista3 = agregar_elemento_bien("a")
    lista4 = agregar_elemento_bien("b")
    print(f"  Llamada 1: {lista3}")
    print(f"  Llamada 2: {lista4}  ← independiente, correcto")

    print()
    print("Búsqueda de usuario con Optional:")
    saludar(1)
    saludar(99)

    print()
    print("Conteo de palabras (type hints en acción):")
    texto = "el gato y el perro y el gato".split()
    resultado = contar_palabras(texto)
    for palabra, cantidad in sorted(resultado.items(), key=lambda x: -x[1]):
        print(f"  '{palabra}': {cantidad}")


if __name__ == "__main__":
    demo_productos()
