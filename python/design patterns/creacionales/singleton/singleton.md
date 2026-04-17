# Singleton — Patron Creacional

## Que problema resuelve

En una simulacion de fisica, las constantes universales como la velocidad de la luz `c`, la constante gravitacional `G` o la constante de Planck `h` deben ser **unicas y consistentes** en todo el programa. Si cada modulo creara su propio objeto de constantes, podria haber valores distintos en distintas partes del codigo, lo cual introduce errores silenciosos.

**Singleton garantiza que solo exista UN objeto de esa clase en toda la aplicacion.**

---

## Cuando usarlo

- Constantes o parametros globales de una simulacion
- Conexion a base de datos o archivo de resultados (solo una)
- Logger que escribe en un unico archivo de salida

---

## Diagrama de funcionamiento

```
Primera llamada:              Segunda llamada:
ConstantesFisicas()           ConstantesFisicas()
        |                             |
¿_instancia es None?          ¿_instancia es None?
        |                             |
       SI                            NO
        |                             |
  Crea el objeto               Devuelve el objeto
  y lo guarda                      existente
        |                             |
        +-----------> mismo objeto <--+
```

---

## El codigo, linea por linea

```python
class ConstantesFisicas:
    _instancia = None          # Variable compartida por TODA la clase

    def __new__(cls):
        # __new__ se ejecuta ANTES de __init__, cuando se "construye" el objeto
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)   # Crea el objeto una sola vez
            cls._instancia.c = 3e8                  # Velocidad de la luz
            cls._instancia.G = 6.674e-11            # Constante gravitacional
            cls._instancia.h = 6.626e-34            # Constante de Planck
        return cls._instancia  # Siempre devuelve la misma referencia
```

> `__new__` es el metodo que Python llama para *construir* un objeto antes de inicializarlo.
> Al controlarlo, decidimos no crear uno nuevo si ya existe uno guardado.

---

## Salida del programa

```
Son el mismo objeto: True

Constantes desde modulo A:
  c = 300000000.0 m/s
  G = 6.674e-11 N m^2/kg^2
  h = 6.626e-34 J·s

Constantes desde modulo B (mismo objeto):
  c = 300000000.0 m/s
  G = 6.674e-11 N m^2/kg^2
  h = 6.626e-34 J·s
```

Aunque se llama `ConstantesFisicas()` dos veces, ambas variables apuntan al **mismo objeto en memoria**.

---

## Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| Un solo punto de verdad para datos globales | Dificulta las pruebas unitarias |
| Evita inconsistencias entre modulos | Puede ocultar dependencias entre clases |
| Ahorra memoria al no duplicar objetos | No es seguro en programas con hilos sin proteccion adicional |

---

## Analogia del mundo real

Es como las leyes de la fisica del universo: no importa desde que laboratorio del mundo se mida la velocidad de la luz, siempre es la misma. No existe una "velocidad de la luz diferente para cada pais".
