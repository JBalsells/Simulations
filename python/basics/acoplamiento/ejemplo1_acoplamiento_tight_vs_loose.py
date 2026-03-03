"""
Acoplamiento — Ejemplo 1: Acoplamiento fuerte vs. débil
=========================================================
El acoplamiento mide cuánto sabe una clase sobre las otras.

Cuando una clase crea y conoce exactamente sus dependencias (acoplamiento
fuerte), es difícil cambiarlas sin tocar esa clase. Cuando recibe sus
dependencias desde fuera (acoplamiento débil), podemos cambiarlas
sin tocar nada.

El ejemplo: un simulador de péndulo que muestra resultados.
  - Versión fuerte: el simulador crea su propio presentador. No puedes
    cambiarlo sin modificar el simulador.
  - Versión débil: el presentador se pasa desde fuera. Puedes usar
    texto, CSV, JSON o lo que sea, sin tocar el simulador.

Para practicar:
1. Agrega PresentadorJSON que devuelva un diccionario con los datos.
2. Cambia el presentador en tiempo de ejecución y confirma que
   SimuladorPendulo no necesita ningún cambio.
"""

import math


# --- ACOPLAMIENTO FUERTE: el simulador decide cómo mostrar los datos ---

class PresentadorImpresiónFuerte:
    """Muestra resultados sólo por pantalla."""

    def mostrar(self, t: float, theta: float, omega: float) -> None:
        print(f"    t={t:.2f}s  θ={math.degrees(theta):+.3f}°  "
              f"ω={math.degrees(omega):+.3f} °/s")


class SimuladorPenduloAcoplado:
    """⚠ Ejemplo de lo que NO se debe hacer: el presentador está hardcodeado.

    Para usar CSV o cualquier otra salida, habría que editar esta clase.
    """

    G = 9.8

    def __init__(self, longitud: float, theta0: float, dt: float):
        self.L     = longitud
        self.theta = theta0
        self.omega = 0.0
        self.dt    = dt
        # el presentador está fijo aquí adentro, no hay forma de cambiarlo
        self._presentador = PresentadorImpresiónFuerte()

    def simular(self, n_pasos: int) -> None:
        t = 0.0
        for _ in range(n_pasos):
            alpha       = -(self.G / self.L) * math.sin(self.theta)
            self.omega += alpha * self.dt
            self.theta += self.omega * self.dt
            t          += self.dt
            self._presentador.mostrar(t, self.theta, self.omega)


# --- ACOPLAMIENTO DÉBIL: el simulador no sabe ni le importa qué presentador recibe ---

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
    """Solo sabe simular el péndulo. Cómo mostrar los datos es problema del presentador.

    Para cambiar la salida basta pasar otro objeto con mostrar(dict).
    Este simulador no necesita tocarse nunca.
    """

    G = 9.8

    def __init__(self, longitud: float, theta0_deg: float, dt: float):
        self.L     = longitud
        self.theta = math.radians(theta0_deg)
        self.omega = 0.0
        self.dt    = dt

    def simular(self, n_pasos: int, presentador) -> None:
        """Corre la simulación y le pasa cada resultado al presentador."""
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


# El mismo simulador con tres presentadores distintos, sin tocar nada

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
