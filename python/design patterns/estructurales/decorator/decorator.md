# Decorator — Patron Estructural

## Que problema resuelve

En fisica, sobre un cuerpo pueden actuar muchas fuerzas a la vez: gravedad, friccion, resistencia del aire. En lugar de crear una funcion distinta para cada combinacion posible, **Decorator** permite agregar fuerzas como capas sobre una funcion base, usando la sintaxis `@decorador` de Python.

---

## Cuando usarlo

- Cuando necesitas agregar comportamiento a una funcion sin modificarla
- Cuando quieres combinar efectos de forma flexible
- Para reutilizar logica en distintas combinaciones sin duplicar codigo

---

## Como funciona el `@decorador` en Python

Un decorador es una **funcion que recibe una funcion y devuelve otra funcion** con comportamiento adicional.

```
@con_gravedad           <- se aplica de ultimo (capa mas externa)
@con_friccion(mu=0.3)   <- se aplica segundo
@con_resistencia_aire(velocidad_ms=5)  <- se aplica primero (capa mas interna)
def cuerpo_libre(masa_kg):
    ...
```

Python los aplica **de abajo hacia arriba**, por eso en la salida el orden de descripcion es: Aire → Friccion → Gravedad.

### Flujo de ejecucion

```
cuerpo_libre(10)
      |
      v
con_resistencia_aire  ->  fuerza - F_aire
      |
      v
con_friccion          ->  fuerza - F_friccion
      |
      v
con_gravedad          ->  fuerza + F_gravedad
      |
      v
resultado final: 60.94 N
```

---

## El codigo, linea por linea

### Decorador simple (sin parametros)

```python
def con_gravedad(calcular_fuerza):   # Recibe la funcion a decorar
    def wrapper(masa_kg):            # La nueva funcion que la reemplaza
        fuerza, desc = calcular_fuerza(masa_kg)  # Llama a la original
        fg = masa_kg * 9.8
        return fuerza + fg, desc + " + Gravedad" # Agrega su efecto
    return wrapper                   # Devuelve la funcion envuelta
```

### Decorador con parametros (necesita una capa extra)

```python
def con_friccion(mu):                # 1. Recibe el parametro
    def decorador(calcular_fuerza):  # 2. Recibe la funcion a decorar
        def wrapper(masa_kg):        # 3. La nueva funcion
            fuerza, desc = calcular_fuerza(masa_kg)
            ff = mu * masa_kg * 9.8
            return fuerza - ff, desc + f" + Friccion(mu={mu})"
        return wrapper
    return decorador
```

La capa extra existe porque `@con_friccion(mu=0.3)` primero evalua `con_friccion(0.3)` y el resultado de eso es el decorador real.

### Funcion base con los tres decoradores aplicados

```python
@con_gravedad
@con_friccion(mu=0.3)
@con_resistencia_aire(velocidad_ms=5)
def cuerpo_libre(masa_kg):
    return 0.0, f"Cuerpo libre (m={masa_kg} kg)"
```

Esto es equivalente a escribir:

```python
cuerpo_libre = con_gravedad(con_friccion(0.3)(con_resistencia_aire(5)(cuerpo_libre)))
```

El `@` es solo una forma mas limpia de expresar eso.

---

## Salida del programa

```
Cuerpo libre (m=10 kg) + Aire(v=5 m/s) + Friccion(mu=0.3) + Gravedad
Fuerza neta: 60.94 N
```

---

## Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| No modifica la funcion original | Los decoradores se aplican en orden inverso al escrito |
| Se pueden combinar libremente | Muchas capas dificultan el debug |
| Sintaxis limpia con `@` | Los decoradores con parametros son menos intuitivos al principio |

---

## Analogia del mundo real

Es como vestirse para el frio: partes de una camiseta (funcion base), luego agregas un sueter (`@con_friccion`), luego un abrigo (`@con_gravedad`). Cada prenda agrega su efecto sin modificar las anteriores. El orden en que te vistes importa.
