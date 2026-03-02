# Tarea 1 de Métodos Numéricos

[Ver enunciados](enunciados.pdf)

Colección de algoritmos numéricos implementados en Python.

## Estructura del proyecto

- **`problemas/`** — algoritmos principales (multiplos, fibonacci, factor primo)
- **`utilidades/`** — herramientas compartidas (decorador, gráficas, operaciones)
- **`tests/`** — pruebas unitarias de cada módulo
- **`Makefile`** — comandos para correr y testear el proyecto
- **`requirements.txt`** — dependencias del proyecto

---

## Problemas

### Problema 1 — Múltiplos de 3 y 5 (`multiplos.py`)

Cada nuevo término de la secuencia se genera sumando los múltiplos de 3 o 5 menores que N.
Por ejemplo, para N=10: los múltiplos son {3, 5, 6, 9}, cuya suma es **23**.

**a) Algoritmo:** implementado en `problemas/multiplos.py` mediante iteración de 1 a N comprobando divisibilidad con el operador módulo `%`.

**b) y c) Suma, tiempo de cálculo y memoria RAM:**

| N | Suma | Tiempo (s) | Memoria (bytes) |
|---|---|---|---|
| 100 | 2,318 | 0.000011 | 28 |
| 1,000 | 233,168 | 0.000076 | 28 |
| 10,000 | 23,331,668 | 0.000762 | 28 |
| 100,000 | 2,333,316,668 | 0.008104 | 32 |

**d) Gráficas:** generadas con `matplotlib` mostrando N vs tiempo y N vs memoria al ejecutar `make run_multiplos`.

**e) ¿Se puede calcular para N=1,000,000?**
Sí. El resultado es **233,333,166,668** en **0.080726 s** con 32 bytes de memoria. El algoritmo escala linealmente O(n), por lo que valores grandes son viables.

---

### Problema 2 — Serie de Fibonacci (`fibonacci.py`)

Cada nuevo término se genera sumando los dos anteriores: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
Se suman únicamente los términos **pares** menores que N.
Por ejemplo, para N=100: términos pares = {2, 8, 34}, suma = **44**.

**a) Algoritmo:** implementado en `problemas/fibonacci.py` generando la secuencia con un bucle `while a < n` y filtrando pares con `sumar_pares`.

**b) y c) Suma, tiempo de cálculo y memoria RAM:**

| N | Términos pares | Suma | Tiempo (s) | Memoria (bytes) |
|---|---|---|---|---|
| 100 | {2, 8, 34} | 44 | 0.000004 | 28 |
| 1,000 | {2, 8, 34, 144, 610} | 798 | 0.000003 | 28 |
| 10,000 | {2, 8, 34, 144, 610, 2584} | 3,382 | 0.000003 | 28 |
| 100,000 | {2, 8, 34, 144, 610, 2584, 10946, 46368} | 60,696 | 0.000004 | 28 |

**d) Gráficas:** generadas con `matplotlib` al ejecutar `make run_fibonacci`.

**e) ¿Se puede calcular para N=1,000,000?**
Sí. Los términos pares son {2, 8, 34, 144, 610, 2584, 10946, 46368, 196418, 832040} y la suma es **1,089,154** en **0.000005 s**. La secuencia de Fibonacci crece exponencialmente, por lo que hay muy pocos términos menores a 1,000,000.

---

### Problema 3 — Factor primo máximo (`factor_primo.py`)

Encuentra el factor primo más grande de un número entero N.
Por ejemplo, los factores primos de 13195 son {5, 7, 13, 29}, siendo **29** el mayor.

**a) Algoritmo:** implementado en `problemas/factor_primo.py`. Divide sucesivamente N entre 2 y luego entre divisores impares hasta √N. Si al finalizar N > 1, ese residuo es primo y es el factor máximo.

**b) y c) Factor primo máximo, tiempo de cálculo y memoria RAM:**

| N | Factor primo máximo | Tiempo (s) | Memoria (bytes) |
|---|---|---|---|
| 13,195 | 29 | 0.000003 | 28 |
| 600,851,475,143 | 6,857 | 0.000064 | 28 |
| 9,999,999,999,971 | 9,999,999,999,971 | 0.161479 | 32 |
| 999,999,999,999,989 | 999,999,999,999,989 | 1.616140 | 32 |

> Los dos últimos valores son números primos, lo que representa el peor caso para el algoritmo ya que debe iterar hasta √N sin encontrar divisores.

**d) Gráficas:** generadas con `matplotlib` al ejecutar `make run_factor_primo`.

**e) ¿Se puede calcular para N=600,851,475,143?**
Sí. El factor primo máximo es **6,857** y se calcula en **0.000064 s**. El tiempo es tan bajo porque 600,851,475,143 tiene factores pequeños que lo descomponen rápidamente.

---

### Instalar dependencias
```bash
make install
```

## Comandos del Makefile

| Comando | Descripción |
|---|---|
| `make install` | Instala las dependencias del proyecto |
| `make run_multiplos` | Ejecuta multiplos.py (pide N, X, Y interactivamente) |
| `make run_fibonacci` | Ejecuta fibonacci.py (pide N o usa lista interna) |
| `make run_factor_primo` | Ejecuta factor_primo.py (pide N o usa lista interna) |
| `make test` | Corre todos los tests |
| `make help` | Muestra la ayuda de cada problema |
