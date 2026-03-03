"""
Acoplamiento — Ejemplo 1: Acoplamiento fuerte vs. débil
=========================================================
Conceptos OOP: acoplamiento (cuánto depende una clase de otra),
               inyección de dependencias, interfaces informales.

Idea central
------------
El acoplamiento mide cuánto conoce una clase sobre los internos
de otra. Un acoplamiento FUERTE crea dependencias difíciles de
cambiar; uno DÉBIL permite reemplazar componentes sin tocar el resto.

Escenario: simular el movimiento de un péndulo y mostrar resultados.
  - Con acoplamiento fuerte:  Simulador crea y conoce el tipo exacto
    del presentador (PrintPresenter).
  - Con acoplamiento débil:   Simulador recibe cualquier objeto con
    el método mostrar(datos), sin importar su clase.

Tareas para el estudiante
-------------------------
1. Agrega `PresentadorCSV` que guarde los resultados en un string CSV.
2. Crea `PresentadorJSON` que produzca un diccionario con los datos.
3. Cambia el presentador en tiempo de ejecución (en el mismo
   simulador) y observa que no hay que tocar SimuladorPendulo.
"""

import math


# ===========================================================================
# ACOPLAMIENTO FUERTE — el simulador sabe exactamente con quién habla
# ===========================================================================

class PresentadorImpresiónFuerte:
    """Muestra resultados sólo por pantalla."""

    def mostrar(self, t: float, theta: float, omega: float) -> None:
        print(f"    t={t:.2f}s  θ={math.degrees(theta):+.3f}°  "
              f"ω={math.degrees(omega):+.3f} °/s")


class SimuladorPenduloAcoplado:
    """⚠ FUERTE ACOPLAMIENTO: crea el presentador internamente.

    Problema: si quieres cambiar a CSV, debes modificar ESTA clase.
    No puedes reutilizarla con otro tipo de presentador.
    """

    G = 9.8

    def __init__(self, longitud: float, theta0: float, dt: float):
        self.L     = longitud
        self.theta = theta0
        self.omega = 0.0
        self.dt    = dt
        # Acoplamiento fuerte: instancia interna fija
        self._presentador = PresentadorImpresiónFuerte()

    def simular(self, n_pasos: int) -> None:
        t = 0.0
        for _ in range(n_pasos):
            alpha       = -(self.G / self.L) * math.sin(self.theta)
            self.omega += alpha * self.dt
            self.theta += self.omega * self.dt
            t          += self.dt
            self._presentador.mostrar(t, self.theta, self.omega)


# ===========================================================================
# ACOPLAMIENTO DÉBIL — el simulador acepta cualquier presentador
# ===========================================================================

class PresentadorTexto:
    """Presentador 1: imprime resultados con formato tabla."""

    def mostrar(self, datos: dict) -> None:
        t, theta, omega = datos["t"], datos["theta_deg"], datos["omega_deg"]
        print(f"  t={t:5.2f}s | θ={theta:+8.3f}° | ω={omega:+8.3f} °/s")


class PresentadorCompacto:
    """Presentador 2: una sola línea CSV por llamada."""

    def __init__(self):
        self._buffer: list[str] = []

    def mostrar(self, datos: dict) -> None:
        linea = f"{datos['t']:.3f},{datos['theta_deg']:.4f},{datos['omega_deg']:.4f}"
        self._buffer.append(linea)

    def csv(self) -> str:
        encabezado = "t,theta_deg,omega_deg"
        return encabezado + "\n" + "\n".join(self._buffer)


class PresentadorEnergia:
    """Presentador 3: calcula y muestra la energía mecánica."""

    def __init__(self, masa: float, longitud: float):
        self.masa = masa
        self.L    = longitud
        self.G    = 9.8

    def mostrar(self, datos: dict) -> None:
        theta = math.radians(datos["theta_deg"])
        omega = math.radians(datos["omega_deg"])
        Ec = 0.5 * self.masa * (self.L * omega)**2
        Ep = self.masa * self.G * self.L * (1 - math.cos(theta))
        E  = Ec + Ep
        print(f"  t={datos['t']:5.2f}s | Ec={Ec:.4f} J | Ep={Ep:.4f} J | "
              f"E={E:.4f} J")


class SimuladorPendulo:
    """Acoplamiento débil: acepta CUALQUIER objeto con método mostrar(dict).

    Para cambiar cómo se presentan los datos basta pasar otro presentador;
    esta clase no necesita modificarse jamás.
    """

    G = 9.8

    def __init__(self, longitud: float, theta0_deg: float, dt: float):
        self.L     = longitud
        self.theta = math.radians(theta0_deg)
        self.omega = 0.0
        self.dt    = dt

    def simular(self, n_pasos: int, presentador) -> None:
        """Ejecuta la simulación y delega la presentación al presentador."""
        t = 0.0
        for _ in range(n_pasos):
            alpha       = -(self.G / self.L) * math.sin(self.theta)
            self.omega += alpha * self.dt
            self.theta += self.omega * self.dt
            t          += self.dt

            datos = {
                "t":          t,
                "theta_deg":  math.degrees(self.theta),
                "omega_deg":  math.degrees(self.omega),
            }
            presentador.mostrar(datos)


# ===========================================================================
# Programa principal
# ===========================================================================

if __name__ == "__main__":
    L      = 1.0    # m
    THETA0 = 15.0   # grados
    DT     = 0.1    # s
    PASOS  = 6

    print("=" * 60)
    print("ACOPLAMIENTO — fuerte vs. débil")
    print("=" * 60)

    # --- Fuerte acoplamiento ---
    print("\n[FUERTE ACOPLAMIENTO]  — presentador fijo dentro del simulador")
    sim_acoplado = SimuladorPenduloAcoplado(L, math.radians(THETA0), DT)
    sim_acoplado.simular(PASOS)

    # --- Débil acoplamiento: presentador como texto ---
    print("\n[DÉBIL ACOPLAMIENTO]  — PresentadorTexto")
    sim = SimuladorPendulo(L, THETA0, DT)
    sim.simular(PASOS, PresentadorTexto())

    # --- Mismo simulador, presentador de energía ---
    print("\n[DÉBIL ACOPLAMIENTO]  — PresentadorEnergia (sin cambiar SimuladorPendulo)")
    sim2 = SimuladorPendulo(L, THETA0, DT)
    sim2.simular(PASOS, PresentadorEnergia(masa=0.5, longitud=L))

    # --- Mismo simulador, presentador CSV (captura datos) ---
    print("\n[DÉBIL ACOPLAMIENTO]  — PresentadorCompacto (CSV)")
    pres_csv = PresentadorCompacto()
    sim3 = SimuladorPendulo(L, THETA0, DT)
    sim3.simular(PASOS, pres_csv)
    print(pres_csv.csv())
