# Strategy — Patron de Comportamiento

## Que problema resuelve

Hay multiples formas de integrar numericamente las ecuaciones de movimiento: Euler, Euler-Cromer, Verlet... Cada metodo tiene diferente precision y costo computacional. Sin Strategy, el simulador tendria un `if/elif` largo que crece con cada metodo nuevo.

**Strategy encapsula cada algoritmo en su propia clase** y los hace intercambiables sin tocar el simulador.

---

## Cuando usarlo

- Multiples algoritmos para resolver el mismo problema (integracion, ordenamiento, compresion)
- Cuando el usuario debe poder elegir el metodo en tiempo de ejecucion
- Para evitar condicionales que crecen con el tiempo

---

## Diagrama de funcionamiento

```
                    +----------------------+
                    | MetodoEuler          |
SimuladorMovimiento | MetodoEulerCromer    |
        |           | MetodoVerlet         |
        | .integrar() ---> elige uno       |
        |           +----------------------+
        |
   usa la estrategia inyectada, sin saber cual es
```

---

## El codigo, linea por linea

### La interfaz base con ABC

```python
from abc import ABC, abstractmethod

class MetodoIntegracion(ABC):
    nombre: str

    @abstractmethod
    def integrar(self, x, v, a, dt) -> tuple[float, float]:
        pass
```

`ABC` + `@abstractmethod` garantiza que cualquier estrategia concreta **debe** implementar `integrar`. Si alguien crea `MetodoRungeKutta` y olvida ese metodo, Python lanza un error al instanciarla.

### Estrategias concretas

```python
class MetodoEuler(MetodoIntegracion):
    nombre = "Euler"

    def integrar(self, x, v, a, dt):
        x_nuevo = x + v * dt       # Posicion con velocidad actual
        v_nuevo = v + a * dt       # Velocidad con aceleracion actual
        return x_nuevo, v_nuevo

class MetodoEulerCromer(MetodoIntegracion):
    nombre = "Euler-Cromer"

    def integrar(self, x, v, a, dt):
        v_nuevo = v + a * dt           # Primero actualiza v
        x_nuevo = x + v_nuevo * dt     # Luego usa v ya actualizada
        return x_nuevo, v_nuevo
```

`MetodoVerlet` necesita guardar `_x_anterior` entre pasos, por eso es una clase y no una funcion simple.

### El simulador (contexto)

```python
class SimuladorMovimiento:
    def __init__(self, metodo: MetodoIntegracion):
        self._metodo = metodo        # Recibe la estrategia

    def cambiar_metodo(self, metodo: MetodoIntegracion):
        self._metodo = metodo        # La cambia en tiempo de ejecucion

    def simular(self, x0, v0, aceleracion, dt, pasos):
        x, v = x0, v0
        for i in range(pasos):
            x, v = self._metodo.integrar(x, v, aceleracion, dt)  # Delega
```

---

## Salida del programa (caida libre, g = -9.8 m/s²)

```
Metodo: Euler | a=-9.8 m/s^2 | dt=0.1 s
  Paso  x (m)        v (m/s)
  1     0.0000       -0.9800
  2     -0.0980      -1.9600
  ...

Metodo: Euler-Cromer | a=-9.8 m/s^2 | dt=0.1 s
  1     -0.0980      -0.9800
  ...

Metodo: Verlet | a=-9.8 m/s^2 | dt=0.1 s
  1     0.0000       0.0000
  ...
```

Cada metodo produce trayectorias ligeramente distintas con la misma interfaz.

---

## Sin Strategy (como NO hacerlo)

```python
def simular(self, metodo_nombre, ...):
    if metodo_nombre == "euler":
        x_nuevo = x + v * dt
        v_nuevo = v + a * dt
    elif metodo_nombre == "euler-cromer":
        v_nuevo = v + a * dt
        x_nuevo = x + v_nuevo * dt
    # Agregar Verlet o Runge-Kutta requiere modificar este metodo
```

Con Strategy, agregar Runge-Kutta es solo crear `MetodoRungeKutta(MetodoIntegracion)` — el simulador no cambia.

---

## Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| Elimina condicionales largos | Mas clases en el proyecto |
| ABC garantiza que todos los metodos implementen `integrar` | El cliente debe conocer las estrategias disponibles |
| Cambia el metodo en tiempo de ejecucion | Puede ser excesivo si solo hay 1 o 2 algoritmos |

---

## Analogia del mundo real

Es como elegir la ruta para llegar a un destino: autopista (Euler, rapido pero menos preciso), carretera (Euler-Cromer, mas estable) o camino de montana (Verlet, mas preciso pero mas complejo). El destino es el mismo, solo cambia el algoritmo para llegar.
