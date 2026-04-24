# Guía de Linting y Análisis Estático de Código

## ¿Qué es el linting?

Un **linter** es una herramienta que analiza el código fuente *sin ejecutarlo* y reporta errores, malas prácticas, inconsistencias de estilo y posibles bugs. El nombre viene de una herramienta llamada `lint` creada en 1978 para el lenguaje C.

El **análisis estático** es el término más amplio: engloba linting, verificación de tipos, detección de vulnerabilidades de seguridad y cualquier inspección del código que no requiera ejecutarlo.

```
Tu código fuente  →  [Linter/Analizador]  →  Lista de problemas
                                              (sin ejecutar el código)
```

---

## ¿Por qué usar linters?

- **Detectan bugs antes de ejecutar** — variables no definidas, imports no usados, comparaciones que siempre son falsas.
- **Imponen un estilo consistente** — todo el equipo escribe código que parece escrito por la misma persona.
- **Educan** — los mensajes del linter enseñan mejores prácticas mientras escribes.
- **Reducen el tiempo en code review** — el linter señala lo mecánico para que los humanos revisen lo importante.
- **Documentan convenciones** — la configuración del linter *es* el documento de estándares del equipo.

---

## Categorías de herramientas

### 1. Formateadores de código

No reportan problemas: directamente **reescriben el código** para que cumpla el estilo. Son deterministas: siempre producen el mismo resultado.

#### Black

El formateador más popular de Python. Sin opciones (deliberadamente). Elimina toda discusión sobre estilo.

```bash
pip install black

# Formatear un archivo
black mi_archivo.py

# Ver qué cambiaría sin modificar
black --check --diff mi_archivo.py
```

**Antes:**
```python
x = {'a':1,'b':   2, 'c': 3}
def funcion( x,y ):
    return x+y
```

**Después de `black`:**
```python
x = {"a": 1, "b": 2, "c": 3}


def funcion(x, y):
    return x + y
```

#### isort

Ordena y agrupa los imports automáticamente.

```bash
pip install isort

isort mi_archivo.py
```

**Antes:**
```python
import os
from mi_modulo import cosa
import sys
import json
from collections import defaultdict
```

**Después de `isort`:**
```python
import json
import os
import sys
from collections import defaultdict

from mi_modulo import cosa
```

---

### 2. Linters de estilo y errores

Reportan problemas pero no modifican el código. Tú decides qué arreglar.

#### Flake8

Combina tres herramientas: **pycodestyle** (PEP 8), **pyflakes** (errores lógicos) y **mccabe** (complejidad ciclomática).

```bash
pip install flake8

flake8 mi_archivo.py
```

**Ejemplo de salida:**
```
mi_archivo.py:3:1  E302 expected 2 blank lines, found 1
mi_archivo.py:7:12 E711 comparison to None (use "is" or "is not")
mi_archivo.py:12:1 F401 'os' imported but unused
mi_archivo.py:15:5 W291 trailing whitespace
```

Cada código tiene una letra que indica la categoría:
| Prefijo | Categoría |
|---------|-----------|
| `E` | Error de estilo (PEP 8) |
| `W` | Warning de estilo |
| `F` | Error lógico (pyflakes) |
| `C` | Complejidad ciclomática |

#### Pylint

El linter más completo y estricto. Detecta más cosas que flake8 pero también genera más falsos positivos.

```bash
pip install pylint

pylint mi_archivo.py
```

Asigna una **puntuación de 0 a 10** al código y muestra qué tan bien escrito está.

```
Your code has been rated at 7.50/10 (previous run: 6.00/10, +1.50)
```

---

### 3. Ruff — el moderno todo-en-uno

Linter extremadamente rápido escrito en Rust que reemplaza flake8, isort, pyupgrade y docenas de plugins. Es el estándar moderno.

```bash
pip install ruff

# Analizar
ruff check mi_archivo.py

# Corregir automáticamente lo que puede
ruff check --fix mi_archivo.py

# Formatear (reemplaza a black)
ruff format mi_archivo.py
```

**Configuración en `pyproject.toml`:**
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # naming conventions
    "UP",  # pyupgrade (modernizar sintaxis)
    "B",   # bugbear (bugs comunes)
    "SIM", # simplify (código innecesariamente complejo)
]
ignore = ["E501"]  # ignorar líneas largas si usas black

[tool.ruff.lint.per-file-ignores]
"tests/*.py" = ["S101"]  # permitir assert en tests
```

---

### 4. Verificadores de tipos (Type Checkers)

Python es de tipado dinámico, pero desde Python 3.5 puedes agregar **type hints** opcionales. Los type checkers verifican que los tipos sean consistentes sin ejecutar el código.

#### Type Hints básicos

```python
# Sin type hints
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)

# Con type hints
def calcular_descuento(precio: float, porcentaje: float) -> float:
    return precio * (1 - porcentaje / 100)

# Tipos más complejos
from typing import Optional, Union

def buscar_usuario(id: int) -> Optional[str]:
    ...  # puede retornar str o None

def procesar(valor: Union[int, str]) -> str:
    ...  # acepta int o str

# Python 3.10+: sintaxis más limpia
def buscar_usuario(id: int) -> str | None:
    ...
```

#### Mypy

El verificador de tipos más utilizado y maduro.

```bash
pip install mypy

mypy mi_archivo.py
```

**Ejemplo de lo que detecta:**
```python
def sumar(a: int, b: int) -> int:
    return a + b

resultado = sumar("hola", 5)  # mypy detecta: Argument 1 has incompatible type "str"; expected "int"
```

#### Pyright / Pylance

Verificador de tipos de Microsoft, muy rápido. Es el que usa VS Code por defecto (como Pylance).

```bash
pip install pyright
pyright mi_archivo.py
```

---

### 5. Análisis de seguridad

#### Bandit

Detecta vulnerabilidades de seguridad comunes en código Python.

```bash
pip install bandit

bandit -r mi_proyecto/
```

**Ejemplos de lo que detecta:**
```python
import subprocess
subprocess.call(comando)          # B603: subprocess sin shell=False
import pickle
pickle.loads(datos)               # B301: deserialización insegura
password = "admin123"             # B105: contraseña hardcodeada
eval(input("Ingresa código: "))   # B307: uso de eval
```

---

### 6. Complejidad de código

#### Radon

Calcula métricas de complejidad: complejidad ciclomática, índice de mantenibilidad, etc.

```bash
pip install radon

# Complejidad ciclomática
radon cc mi_archivo.py -s

# Índice de mantenibilidad (A=mejor, F=peor)
radon mi mi_archivo.py
```

**Complejidad ciclomática:** cuenta cuántos caminos de ejecución tiene una función. Más de 10 es señal de que la función debe dividirse.

```
mi_archivo.py
    F 15:0 procesar_pedido - D (complexity: 12)
    F 45:0 validar_datos   - B (complexity: 4)
    F 67:0 formatear       - A (complexity: 1)
```

---

## PEP 8 — La guía de estilo oficial de Python

PEP 8 es el documento que define las convenciones de estilo del lenguaje Python. Los linters lo usan como referencia.

**Las reglas más importantes:**

```python
# ✅ Nombres: snake_case para variables y funciones
nombre_usuario = "Ana"
def calcular_total(): ...

# ✅ Nombres: PascalCase para clases
class UsuarioActivo: ...

# ✅ Nombres: UPPER_CASE para constantes
MAX_REINTENTOS = 3
URL_BASE = "https://api.ejemplo.com"

# ✅ 2 líneas en blanco entre funciones/clases de nivel superior
def funcion_a():
    ...


def funcion_b():
    ...

# ✅ 1 línea en blanco entre métodos de una clase
class MiClase:
    def metodo_a(self):
        ...

    def metodo_b(self):
        ...

# ✅ Espacios alrededor de operadores
x = 5 + 3
if x == 8:

# ✅ Sin espacios dentro de paréntesis/corchetes
lista[1:3]
funcion(arg1, arg2)

# ✅ Máximo 79 caracteres por línea (o 88/100 con Black)
# ✅ Imports uno por línea
import os
import sys  # no: import os, sys

# ✅ Comparar con None usando is/is not
if valor is None: ...    # no: if valor == None
if valor is not None: ...

# ✅ Comparar booleanos directamente
if activo: ...           # no: if activo == True
if not activo: ...       # no: if activo == False
```

---

## Pre-commit hooks

Un **git hook** es un script que se ejecuta automáticamente antes o después de un comando git. Los pre-commit hooks se ejecutan *antes de cada commit*, bloqueándolo si el código no pasa las verificaciones.

```bash
pip install pre-commit
```

**Archivo `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
```

```bash
# Instalar los hooks en el repo
pre-commit install

# Ahora cada git commit ejecutará los linters automáticamente
git commit -m "mi cambio"
# Si el linter falla, el commit se bloquea

# Correr manualmente sobre todos los archivos
pre-commit run --all-files
```

---

## Integración con editores

### VS Code

Instalar extensiones: **Pylance** (tipos), **Ruff** (linting/formato)

Configuración en `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "charliermarsh.ruff",
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  }
}
```

### PyCharm

Incluye su propio analizador estático. También tiene integración nativa con mypy y puede correr ruff como external tool.

---

## Configuración recomendada para un proyecto nuevo

**`pyproject.toml`:**
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "SIM", "UP"]

[tool.mypy]
python_version = "3.11"
strict = false
ignore_missing_imports = true
warn_unused_ignores = true

[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]  # permitir assert
```

---

## Comparativa de herramientas

| Herramienta | Categoría | Velocidad | Autocorrige | Cuándo usar |
|---|---|---|---|---|
| `black` | Formateo | Rápida | ✅ | Siempre (o `ruff format`) |
| `isort` | Imports | Rápida | ✅ | Siempre (o `ruff --select I`) |
| `flake8` | Estilo + errores | Rápida | ❌ | Proyectos legacy |
| `pylint` | Estilo + errores | Lenta | ❌ | Cuando necesitas máxima cobertura |
| `ruff` | Todo-en-uno | Muy rápida | ✅ | Proyectos nuevos — reemplaza todo |
| `mypy` | Tipos | Media | ❌ | Cuando usas type hints |
| `pyright` | Tipos | Rápida | ❌ | Alternativa a mypy, mejor en VS Code |
| `bandit` | Seguridad | Media | ❌ | APIs, código que maneja datos sensibles |
| `radon` | Complejidad | Rápida | ❌ | Cuando el código crece mucho |

---

## Flujo de trabajo recomendado

```
Escribes código
      ↓
Editor formatea al guardar (ruff format)
      ↓
git commit
      ↓
pre-commit hook corre: ruff check + mypy
      ↓
¿Hay errores? → Sí → Corrige y vuelve a commitear
              → No → Commit exitoso
                        ↓
                   CI/CD pipeline
                   (GitHub Actions)
                   corre todo de nuevo
                   en un entorno limpio
```
