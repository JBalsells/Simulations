# Pi Estimation - Monte Carlo Simulation

Estimación del valor de Pi mediante simulación Monte Carlo. El programa lanza puntos aleatorios dentro de un cuadrado unitario y cuenta cuántos caen dentro de un cuarto de círculo de radio 1. La razón entre puntos dentro del círculo y el total de puntos converge a `π/4`.

## Método

```
  1 ┌─────────────────┐
    │ ·  ·            │
    │    ·  ·  ·      │
    │  ·  ·  ·  ·     │
    │ ·  ·  ·  ·      │
    │  ·  ·  ·        │
    │   ·  ·          │
    │    ·            │
  0 └─────────────────┘
    0                  1

π ≈ 4 × (puntos dentro del círculo / puntos totales)
```

## Estrategias de ejecución

| Método | Descripción |
|---|---|
| `sequential` | Loop en Python puro con `random`. Baseline de rendimiento. |
| `parallel` | Divide las muestras entre los CPUs disponibles con `multiprocessing.Pool`. |
| `numpy` | Genera todos los puntos de forma vectorizada con NumPy. |

## Requisitos

- Python >= 3.10
- NumPy >= 1.23.0

## Instalación

```bash
poetry install
```

## Uso

### Ejecutar benchmark completo

```bash
PYTHONPATH=src python -m first_simulation.monte_carlo_pi
```

Salida ejemplo (16 CPUs):

```
Método             Muestras   π estimado        Error   Tiempo (s)     Muestras/s
------------------------------------------------------------------------------------------
sequential       10,000,000   3.14144040   0.00015225     1.764223      5,668,219
parallel         10,000,000   3.14142560   0.00016705     0.362735     27,568,365
numpy            10,000,000   3.14172440   0.00013175     0.332128     30,108,877
```

### Usar como librería

```python
from first_simulation.monte_carlo_pi import benchmark, estimate_pi_numpy

# Benchmark individual
result = benchmark(1_000_000, method="numpy")
print(result)
# {'method': 'numpy', 'n_samples': 1000000, 'pi_estimate': 3.14..., 'error': 0.00..., ...}

# Estimación directa
pi = estimate_pi_numpy(5_000_000)
print(f"π ≈ {pi}")
```

## Observaciones

- **sequential** es el más lento pero sirve como referencia para medir la mejora de los otros métodos.
- **parallel** tiene overhead de creación de procesos, por lo que solo supera a sequential con muestras grandes (>100K).
- **numpy** es consistentemente rápido gracias a operaciones vectorizadas en C. Es el método recomendado para uso general.
- A mayor cantidad de muestras, menor el error de estimación (convergencia ∝ `1/√n`).
