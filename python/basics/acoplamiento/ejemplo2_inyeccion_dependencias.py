"""
Acoplamiento — Ejemplo 2: Inyección de dependencias en experimento
===================================================================
Conceptos OOP: inyección de dependencias (DI), bajo acoplamiento,
               intercambiabilidad de componentes, ABC como contrato.

Idea central
------------
En lugar de que cada clase CREE sus dependencias (acoplamiento fuerte),
las recibe desde fuera (inyección). Esto permite:
  1. Cambiar el sensor sin tocar el experimento.
  2. Cambiar el integrador numérico sin tocar la física.
  3. Testear cada componente de forma aislada.

Escenario: experimento de caída libre con distintos "sensores"
(real/simulado) y distintos "integradores" (Euler/RK2).

Tareas para el estudiante
-------------------------
1. Crea `SensorRuidos` que añade errores aleatorios a los valores.
2. Implementa `IntegradorRK4` y compara la precisión con Euler.
3. ¿Cuántas líneas hay que cambiar para usar el nuevo sensor?
   (Respuesta esperada: 1 línea en main)
"""

from abc import ABC, abstractmethod
import math


# ---------------------------------------------------------------------------
# Contratos (interfaces abstractas) — definen QUÉ se espera
# ---------------------------------------------------------------------------

class SensorAltitud(ABC):
    """Contrato para cualquier sensor que mida altura."""

    @abstractmethod
    def medir(self, altura_real: float) -> float:
        """Devuelve la lectura del sensor (puede incluir error)."""


class IntegradorNumerica(ABC):
    """Contrato para cualquier método de integración numérica."""

    @abstractmethod
    def paso(self, y: list[float], dydt_fn, dt: float) -> list[float]:
        """Avanza el estado y = [pos, vel] un paso dt."""


# ---------------------------------------------------------------------------
# Implementaciones de SensorAltitud
# ---------------------------------------------------------------------------

class SensorIdeal(SensorAltitud):
    """Sensor perfecto: devuelve el valor real sin error."""

    def medir(self, altura_real: float) -> float:
        return altura_real

    def __repr__(self): return "SensorIdeal"


class SensorGPS(SensorAltitud):
    """Sensor GPS con resolución ±0.5 m (redondea a la resolución)."""

    RESOLUCION = 0.5  # m

    def medir(self, altura_real: float) -> float:
        return round(altura_real / self.RESOLUCION) * self.RESOLUCION

    def __repr__(self): return f"SensorGPS(±{self.RESOLUCION} m)"


class SensorBarometrico(SensorAltitud):
    """Sensor barométrico: introduce drift lineal de 0.1 m/s."""

    def __init__(self):
        self._t = 0.0

    def medir(self, altura_real: float) -> float:
        lectura = altura_real + 0.1 * self._t   # drift con el tiempo
        self._t += 0.01
        return lectura

    def __repr__(self): return "SensorBarometrico(drift=0.1m/s)"


# ---------------------------------------------------------------------------
# Implementaciones de IntegradorNumerica
# ---------------------------------------------------------------------------

class IntegradorEuler(IntegradorNumerica):
    """Método de Euler (1.er orden): y(t+dt) = y(t) + f(y,t)·dt."""

    def paso(self, y: list[float], dydt_fn, dt: float) -> list[float]:
        derivadas = dydt_fn(y)
        return [y[i] + derivadas[i] * dt for i in range(len(y))]

    def __repr__(self): return "IntegradorEuler(orden=1)"


class IntegradorRK2(IntegradorNumerica):
    """Método de Runge-Kutta de 2.º orden (Heun)."""

    def paso(self, y: list[float], dydt_fn, dt: float) -> list[float]:
        k1 = dydt_fn(y)
        y_pred = [y[i] + k1[i] * dt for i in range(len(y))]
        k2 = dydt_fn(y_pred)
        return [y[i] + 0.5 * (k1[i] + k2[i]) * dt for i in range(len(y))]

    def __repr__(self): return "IntegradorRK2(orden=2)"


# ---------------------------------------------------------------------------
# Experimento con inyección de dependencias
# ---------------------------------------------------------------------------

class ExperimentoCaidaLibre:
    """Simula una caída libre con sensor e integrador inyectados.

    La clase no sabe qué tipo concreto de sensor o integrador recibe;
    sólo usa los contratos (medir / paso).
    """

    G = 9.8   # m/s²

    def __init__(self, altura_inicial: float,
                 sensor: SensorAltitud,
                 integrador: IntegradorNumerica,
                 dt: float = 0.05):
        self.h0         = altura_inicial
        self._sensor    = sensor        # inyectado
        self._integrador = integrador   # inyectado
        self.dt         = dt

    def _derivadas(self, estado: list[float]) -> list[float]:
        """dh/dt = v,   dv/dt = -g."""
        _, v = estado
        return [v, -self.G]

    def solucion_analitica(self, t: float) -> float:
        """h(t) = h₀ − ½g·t²."""
        return self.h0 - 0.5 * self.G * t**2

    def ejecutar(self, tiempo_total: float) -> list[dict]:
        """Ejecuta la simulación y devuelve los registros."""
        estado = [self.h0, 0.0]   # [altura, velocidad]
        t      = 0.0
        registros = []

        while estado[0] >= 0 and t <= tiempo_total:
            h_num  = estado[0]
            h_med  = self._sensor.medir(h_num)   # ← usa el sensor inyectado
            h_real = self.solucion_analitica(t)
            error  = abs(h_num - h_real)

            registros.append({
                "t":      t,
                "h_num":  h_num,
                "h_med":  h_med,
                "h_real": h_real,
                "error":  error,
            })

            # ← usa el integrador inyectado
            estado = self._integrador.paso(estado, self._derivadas, self.dt)
            t     += self.dt

        return registros

    def __repr__(self):
        return (f"ExperimentoCaidaLibre("
                f"sensor={self._sensor}, "
                f"integrador={self._integrador})")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def mostrar_resultados(experimento: ExperimentoCaidaLibre,
                       registros: list[dict], n_filas: int = 6) -> None:
    print(f"\n  {experimento}")
    print(f"  {'t (s)':>6}  {'h_num (m)':>10}  {'h_med (m)':>10}  "
          f"{'h_real (m)':>11}  {'error (m)':>10}")
    print("  " + "-" * 55)
    paso = max(1, len(registros) // n_filas)
    for r in registros[::paso]:
        print(f"  {r['t']:>6.2f}  {r['h_num']:>10.4f}  {r['h_med']:>10.4f}  "
              f"{r['h_real']:>11.4f}  {r['error']:>10.4f}")

    error_max = max(r["error"] for r in registros)
    error_med = sum(r["error"] for r in registros) / len(registros)
    print(f"  Error máx = {error_max:.4f} m,  Error medio = {error_med:.4f} m")


if __name__ == "__main__":
    H0      = 100.0   # m
    T_TOTAL = 4.0     # s
    DT      = 0.05    # s

    print("=" * 62)
    print("INYECCIÓN DE DEPENDENCIAS — caída libre")
    print("=" * 62)

    configuraciones = [
        (SensorIdeal(),        IntegradorEuler()),
        (SensorIdeal(),        IntegradorRK2()),
        (SensorGPS(),          IntegradorRK2()),
        (SensorBarometrico(),  IntegradorRK2()),
    ]

    for sensor, integrador in configuraciones:
        exp = ExperimentoCaidaLibre(H0, sensor, integrador, DT)
        reg = exp.ejecutar(T_TOTAL)
        mostrar_resultados(exp, reg)

    print("\n--- Cambiar sensor sin tocar ExperimentoCaidaLibre ---")
    print("  exp = ExperimentoCaidaLibre(100, SensorGPS(), IntegradorRK2())")
    print("  → sólo cambia 1 línea en main; la clase no se modifica.")
