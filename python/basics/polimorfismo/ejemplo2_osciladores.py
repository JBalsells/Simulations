"""
Polimorfismo — Ejemplo 2: Familia de osciladores
=================================================
Tres osciladores muy distintos en física, pero todos responden
a posicion(t), velocidad(t) y energia_total(t). Eso permite
meterlos en una lista y tratarlos igual, sin preguntar de qué tipo es cada uno.

  Armónico    : x(t) = A·cos(ω₀·t)
  Amortiguado : x(t) = A·e^{−γt}·cos(ω_d·t)
  Forzado     : x(t) = B·cos(ω_f·t − φ)  [régimen estacionario]

Para practicar:
1. Agrega OsciladorNoLineal con potencial cúbico.
2. Calcula en qué tiempo el amortiguado pierde el 50% de su energía.
3. Grafica posicion(t) para los tres con matplotlib.
"""

import math


# interfaz común: todos los osciladores implementan estos métodos

class Oscilador:
    """Interfaz base para cualquier oscilador mecánico."""

    def __init__(self, masa: float, amplitud: float, omega0: float):
        self.masa     = masa      # kg
        self.amplitud = amplitud  # m
        self.omega0   = omega0    # rad/s — frecuencia natural

    @property
    def nombre(self) -> str:
        return self.__class__.__name__

    def posicion(self, t: float) -> float:
        raise NotImplementedError

    def velocidad(self, t: float) -> float:
        """Derivada numérica centrada de posición."""
        dt = 1e-6
        return (self.posicion(t + dt) - self.posicion(t - dt)) / (2 * dt)

    def energia_total(self, t: float) -> float:
        """E = ½mv² + ½mω₀²x²  (válido para el caso armónico)."""
        x = self.posicion(t)
        v = self.velocidad(t)
        return 0.5 * self.masa * (v**2 + self.omega0**2 * x**2)

    def __repr__(self):
        return (f"{self.nombre}(m={self.masa} kg, "
                f"A={self.amplitud} m, ω₀={self.omega0:.2f} rad/s)")


# sin pérdidas: oscila para siempre con la misma amplitud

class OsciladorArmonico(Oscilador):
    """x(t) = A·cos(ω₀·t) — sin pérdidas de energía."""

    def posicion(self, t: float) -> float:
        return self.amplitud * math.cos(self.omega0 * t)

    def frecuencia_hz(self) -> float:
        return self.omega0 / (2 * math.pi)

    def periodo(self) -> float:
        return 2 * math.pi / self.omega0


# pierde energía al medio: la amplitud decae exponencialmente

class OsciladorAmortiguado(Oscilador):
    """x(t) = A·e^{−γt}·cos(ω_d·t) — pierde energía al medio."""

    def __init__(self, masa: float, amplitud: float, omega0: float,
                 gamma: float):
        super().__init__(masa, amplitud, omega0)
        if gamma >= omega0:
            raise ValueError("γ debe ser < ω₀ para régimen subamortiguado.")
        self.gamma   = gamma                          # coeficiente de amortiguación (1/s)
        self.omega_d = math.sqrt(omega0**2 - gamma**2)  # frecuencia amortiguada

    def posicion(self, t: float) -> float:
        return self.amplitud * math.exp(-self.gamma * t) * math.cos(self.omega_d * t)

    def factor_calidad(self) -> float:
        """Q = ω₀ / (2γ) — número de oscilaciones antes de agotar energía."""
        return self.omega0 / (2 * self.gamma)

    def energia_total(self, t: float) -> float:
        """Energía decae como E(t) = E₀·e^{−2γt}."""
        e0 = 0.5 * self.masa * self.omega0**2 * self.amplitud**2
        return e0 * math.exp(-2 * self.gamma * t)


# fuerza externa que impulsa el sistema; cerca de ω₀ aparece la resonancia

class OsciladorForzado(Oscilador):
    """Sistema amortiguado con fuerza externa F₀·cos(ω_f·t).

    Solución estacionaria:
        x(t) = B·cos(ω_f·t − φ)
    donde B = F₀/m / √((ω₀²−ω_f²)² + (2γω_f)²)
    """

    def __init__(self, masa: float, amplitud_fuerza: float,
                 omega0: float, omega_f: float, gamma: float):
        # amplitud estacionaria calculada internamente
        self.gamma   = gamma
        self.omega_f = omega_f
        denominador  = math.sqrt(
            (omega0**2 - omega_f**2)**2 + (2 * gamma * omega_f)**2
        )
        B = (amplitud_fuerza / masa) / denominador
        super().__init__(masa, B, omega0)
        self.fase = math.atan2(2 * gamma * omega_f, omega0**2 - omega_f**2)

    def posicion(self, t: float) -> float:
        return self.amplitud * math.cos(self.omega_f * t - self.fase)

    def en_resonancia(self) -> bool:
        """Resonancia cuando ω_f ≈ ω₀."""
        return abs(self.omega_f - self.omega0) < 0.01 * self.omega0


# imprime la tabla de cualquier oscilador — no importa cuál sea

def tabla_temporal(oscilador: Oscilador, tiempos: list[float]) -> None:
    print(f"\n  [{oscilador}]")
    print(f"  {'t (s)':>8}  {'x (m)':>10}  {'v (m/s)':>10}  {'E (J)':>12}")
    print("  " + "-" * 46)
    for t in tiempos:
        x = oscilador.posicion(t)
        v = oscilador.velocidad(t)
        e = oscilador.energia_total(t)
        print(f"  {t:>8.2f}  {x:>10.4f}  {v:>10.4f}  {e:>12.6f}")


# --- demo ---

if __name__ == "__main__":
    m, A, w0 = 0.5, 0.1, 2 * math.pi  # masa, amplitud, ω₀ = 1 Hz

    osc_a = OsciladorArmonico(m, A, w0)
    osc_d = OsciladorAmortiguado(m, A, w0, gamma=0.3)
    osc_f = OsciladorForzado(m, amplitud_fuerza=1.0, omega0=w0,
                              omega_f=0.9 * w0, gamma=0.3)

    osciladores: list[Oscilador] = [osc_a, osc_d, osc_f]
    tiempos = [0.0, 0.25, 0.5, 1.0, 2.0]

    print("=" * 60)
    print("OSCILADORES MECÁNICOS — polimorfismo en acción")
    print("=" * 60)

    for osc in osciladores:
        tabla_temporal(osc, tiempos)

    # Info específica de cada tipo
    print(f"\n--- Datos adicionales ---")
    print(f"  Armónico   — período       : {osc_a.periodo():.4f} s")
    print(f"  Amortiguado— factor Q      : {osc_d.factor_calidad():.2f}")
    print(f"  Forzado    — en resonancia : {osc_f.en_resonancia()}")

    # Energía relativa del amortiguado a t=5 s
    t_ref = 5.0
    e_ini = osc_d.energia_total(0)
    e_fin = osc_d.energia_total(t_ref)
    print(f"\n  Energía amortiguado en t={t_ref}s: "
          f"{e_fin/e_ini*100:.1f}% de la inicial")
