"""
Cohesión — Ejemplo 2: Simulador de partículas
==============================================
Cada clase tiene un único trabajo bien definido:
  - Particula: guarda posición, velocidad y masa. Nada más.
  - CalculadorFuerzas: calcula la gravedad entre partículas.
  - IntegradorVerlet: avanza el tiempo un paso.
  - Monitor: mide energía, momento, centro de masa.

Si quieres cambiar la física, solo tocas CalculadorFuerzas.
Si quieres otro algoritmo, solo tocas el integrador.
El resto no se entera.

Para practicar:
1. Implementa IntegradorRK4 como alternativa. ¿Necesitas tocar otras clases?
2. Agrega en Monitor el cálculo del momento de inercia.
3. ¿Qué cambiarías para simular cargas eléctricas en vez de masas?
"""

import math
import random


# 1. Solo datos: posición, velocidad, masa y la fuerza que actúa sobre ella

class Particula:
    """Guarda el estado de una partícula. No calcula nada por sí sola."""

    def __init__(self, masa: float, x: float, y: float,
                 vx: float = 0.0, vy: float = 0.0):
        self.masa = masa
        self.x  = x;  self.y  = y
        self.vx = vx; self.vy = vy
        self.fx = 0.0; self.fy = 0.0   # fuerza resultante en este instante

    @property
    def velocidad(self) -> float:
        return math.sqrt(self.vx**2 + self.vy**2)

    @property
    def posicion(self) -> tuple:
        return (self.x, self.y)

    def energia_cinetica(self) -> float:
        return 0.5 * self.masa * self.velocidad**2

    def __repr__(self):
        return (f"Particula(m={self.masa:.2f}, "
                f"x={self.x:.3f}, y={self.y:.3f}, "
                f"v={self.velocidad:.3f})")


# 2. Solo física: sabe calcular la gravedad entre partículas, nada más

class CalculadorFuerzas:
    """Calcula la fuerza gravitacional entre cada par de partículas.

    No sabe de posiciones futuras ni de tiempo. Solo física del instante actual.
    """

    G     = 6.674e-11   # constante gravitacional
    R_MIN = 1e-3        # distancia mínima (evita singularidad)

    def calcular_y_asignar(self, particulas: list[Particula]) -> None:
        """Calcula todas las fuerzas y las asigna a cada partícula."""
        # Reiniciar fuerzas
        for p in particulas:
            p.fx = p.fy = 0.0

        # calculamos cada par una sola vez y aplicamos la 3a ley de Newton
        n = len(particulas)
        for i in range(n):
            for j in range(i + 1, n):
                pi, pj = particulas[i], particulas[j]
                dx = pj.x - pi.x
                dy = pj.y - pi.y
                r  = max(math.sqrt(dx**2 + dy**2), self.R_MIN)
                F  = self.G * pi.masa * pj.masa / r**2
                fx = F * dx / r
                fy = F * dy / r
                pi.fx += fx;  pi.fy += fy
                pj.fx -= fx;  pj.fy -= fy


# 3. Solo matemáticas: avanza posiciones y velocidades un paso de tiempo

class IntegradorVerlet:
    """Avanza el sistema un paso dt usando el método de Verlet.

    No sabe qué tipo de fuerzas hay, solo recibe una función que las calcula.
    """

    def __init__(self, dt: float):
        self.dt = dt

    def paso(self, particulas: list[Particula],
             calcular_fuerzas_fn) -> None:
        """Avanza un paso: primero posiciones, luego recalcula fuerzas, luego velocidades."""
        dt = self.dt

        # guardamos la aceleración antes de mover
        ax_old = [p.fx / p.masa for p in particulas]
        ay_old = [p.fy / p.masa for p in particulas]

        # movemos las partículas con la aceleración actual
        for i, p in enumerate(particulas):
            p.x += p.vx * dt + 0.5 * ax_old[i] * dt**2
            p.y += p.vy * dt + 0.5 * ay_old[i] * dt**2

        # con las nuevas posiciones, recalculamos las fuerzas
        calcular_fuerzas_fn(particulas)

        # ahora sí actualizamos velocidades con el promedio de aceleraciones
        for i, p in enumerate(particulas):
            ax_new = p.fx / p.masa
            ay_new = p.fy / p.masa
            p.vx += 0.5 * (ax_old[i] + ax_new) * dt
            p.vy += 0.5 * (ay_old[i] + ay_new) * dt


# 4. Solo medición: energía, momento lineal, centro de masa

class Monitor:
    """Observa el sistema y calcula sus propiedades globales.

    No mueve partículas ni calcula fuerzas. Solo mide.
    """

    G = 6.674e-11

    def energia_cinetica_total(self, particulas: list[Particula]) -> float:
        return sum(p.energia_cinetica() for p in particulas)

    def energia_potencial(self, particulas: list[Particula]) -> float:
        """Energía potencial gravitacional total del sistema (negativa siempre)."""
        U = 0.0
        n = len(particulas)
        for i in range(n):
            for j in range(i + 1, n):
                pi, pj = particulas[i], particulas[j]
                r = math.sqrt((pi.x - pj.x)**2 + (pi.y - pj.y)**2)
                if r > 0:
                    U -= self.G * pi.masa * pj.masa / r
        return U

    def energia_total(self, particulas: list[Particula]) -> float:
        return self.energia_cinetica_total(particulas) + self.energia_potencial(particulas)

    def momento_lineal(self, particulas: list[Particula]) -> tuple:
        px = sum(p.masa * p.vx for p in particulas)
        py = sum(p.masa * p.vy for p in particulas)
        return px, py

    def centro_de_masa(self, particulas: list[Particula]) -> tuple:
        M  = sum(p.masa for p in particulas)
        cx = sum(p.masa * p.x for p in particulas) / M
        cy = sum(p.masa * p.y for p in particulas) / M
        return cx, cy

    def temperatura_cin(self, particulas: list[Particula]) -> float:
        """Temperatura como medida del movimiento promedio de las partículas (en 2D)."""
        k_B = 1.38e-23
        Ec  = self.energia_cinetica_total(particulas)
        N   = len(particulas)
        return 2 * Ec / (N * k_B) if N > 0 else 0.0


# Instanciamos cada clase y las conectamos manualmente

if __name__ == "__main__":
    random.seed(42)

    N_PART = 4
    DT     = 1e6    # s (escala astronómica)
    PASOS  = 5

    # Crear partículas (masas del orden de planetas)
    particulas = [
        Particula(masa=6e24, x= 1e9, y= 0.0,  vx=0.0, vy=1e3),
        Particula(masa=6e24, x=-1e9, y= 0.0,  vx=0.0, vy=-1e3),
        Particula(masa=1e25, x= 0.0, y= 1e9,  vx=1e3, vy=0.0),
        Particula(masa=1e25, x= 0.0, y=-1e9,  vx=-1e3, vy=0.0),
    ]

    # cada clase hace exactamente una cosa
    fuerzas   = CalculadorFuerzas()
    integrador = IntegradorVerlet(dt=DT)
    monitor   = Monitor()

    # antes del primer paso necesitamos calcular las fuerzas iniciales
    fuerzas.calcular_y_asignar(particulas)

    print("=" * 58)
    print("SIMULADOR N-CUERPOS — alta cohesión (SRP)")
    print("=" * 58)
    print(f"\n  Partículas: {N_PART},  dt={DT:.0e} s,  pasos={PASOS}")

    E0 = monitor.energia_total(particulas)
    p0 = monitor.momento_lineal(particulas)
    cm0 = monitor.centro_de_masa(particulas)
    print(f"\n  {'Paso':>5}  {'Ec (J)':>14}  {'E_total (J)':>14}  {'|p| (kg·m/s)':>15}")
    print("  " + "-" * 55)

    for paso in range(PASOS + 1):
        Ec = monitor.energia_cinetica_total(particulas)
        E  = monitor.energia_total(particulas)
        px, py = monitor.momento_lineal(particulas)
        p_mag = math.sqrt(px**2 + py**2)
        print(f"  {paso:>5}  {Ec:>14.4e}  {E:>14.4e}  {p_mag:>15.4e}")

        if paso < PASOS:
            integrador.paso(particulas, fuerzas.calcular_y_asignar)

    print(f"\n  Conservación de energía: ΔE/E₀ = "
          f"{abs(monitor.energia_total(particulas) - E0)/abs(E0):.2e}")
    cm_f = monitor.centro_de_masa(particulas)
    print(f"  Centro de masa inicial: ({cm0[0]:.3e}, {cm0[1]:.3e}) m")
    print(f"  Centro de masa final  : ({cm_f[0]:.3e}, {cm_f[1]:.3e}) m")
