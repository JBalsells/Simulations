"""
Strategy - Patron de Comportamiento
======================================
Define una familia de algoritmos, los encapsula y los hace intercambiables.
El cliente puede elegir y cambiar el algoritmo en tiempo de ejecucion.

Ejemplo de fisica:
    Para simular el movimiento de un cuerpo, hay distintos metodos de
    integracion numerica: Euler, Euler-Cromer, Verlet. Cada uno tiene
    diferente precision y costo. Strategy permite cambiar el metodo
    sin modificar el simulador.
"""

from abc import ABC, abstractmethod


# --- Interfaz comun: todas las estrategias deben implementar integrar() ---
class MetodoIntegracion(ABC):
    nombre: str

    @abstractmethod
    def integrar(self, x: float, v: float, a: float, dt: float) -> tuple[float, float]:
        """Dado x, v, a y dt, devuelve (x_nuevo, v_nuevo)."""
        pass


# --- Estrategias concretas: cada una es un metodo de integracion ---
class MetodoEuler(MetodoIntegracion):
    """Metodo de Euler: rapido pero poco preciso."""
    nombre = "Euler"

    def integrar(self, x, v, a, dt):
        x_nuevo = x + v * dt
        v_nuevo = v + a * dt
        return x_nuevo, v_nuevo


class MetodoEulerCromer(MetodoIntegracion):
    """Euler-Cromer: actualiza v primero, luego x. Mas estable."""
    nombre = "Euler-Cromer"

    def integrar(self, x, v, a, dt):
        v_nuevo = v + a * dt        # Primero la velocidad
        x_nuevo = x + v_nuevo * dt  # Luego la posicion con v ya actualizada
        return x_nuevo, v_nuevo


class MetodoVerlet(MetodoIntegracion):
    """Verlet: mas preciso, conserva energia mejor."""
    nombre = "Verlet"

    def __init__(self):
        self._x_anterior = None

    def integrar(self, x, v, a, dt):
        if self._x_anterior is None:
            # Primer paso: no hay x_anterior, arrancamos con Euler
            self._x_anterior = x
            return x + v * dt, v
        x_nuevo = 2 * x - self._x_anterior + a * dt ** 2
        v_nuevo = (x_nuevo - self._x_anterior) / (2 * dt)
        self._x_anterior = x
        return x_nuevo, v_nuevo


# --- Contexto: el simulador que usa la estrategia ---
class SimuladorMovimiento:
    def __init__(self, metodo: MetodoIntegracion):
        self._metodo = metodo

    def cambiar_metodo(self, metodo: MetodoIntegracion):
        self._metodo = metodo

    def simular(self, x0: float, v0: float, aceleracion: float, dt: float, pasos: int):
        x, v = x0, v0
        print(f"\nMetodo: {self._metodo.nombre} | a={aceleracion} m/s^2 | dt={dt} s")
        print(f"  {'Paso':<5} {'x (m)':<12} {'v (m/s)':<10}")
        for i in range(pasos):
            x, v = self._metodo.integrar(x, v, aceleracion, dt)
            print(f"  {i+1:<5} {x:<12.4f} {v:<10.4f}")


# --- Demostracion: caida libre, g = -9.8 m/s^2 ---
sim = SimuladorMovimiento(MetodoEuler())
sim.simular(x0=0, v0=0, aceleracion=-9.8, dt=0.1, pasos=5)

sim.cambiar_metodo(MetodoEulerCromer())
sim.simular(x0=0, v0=0, aceleracion=-9.8, dt=0.1, pasos=5)

sim.cambiar_metodo(MetodoVerlet())
sim.simular(x0=0, v0=0, aceleracion=-9.8, dt=0.1, pasos=5)
