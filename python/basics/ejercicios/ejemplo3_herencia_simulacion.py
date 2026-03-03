"""
Ejemplo 3: Herencia y Polimorfismo — Simulación de cuerpos celestes
====================================================================
Todos los cuerpos celestes tienen masa y gravedad. Las estrellas
además tienen luminosidad. Los planetas tienen período orbital.
Los satélites orbitan un planeta concreto. Eso es herencia.
"""

import math


# todo cuerpo celeste tiene masa, posición y puede calcular la fuerza gravitacional

class CuerpoCeleste:
    """Clase base para cualquier cuerpo celeste."""

    G = 6.674e-11  # Constante de gravitación universal (N·m²/kg²)

    def __init__(self, nombre, masa, posicion_x, posicion_y):
        self.nombre = nombre
        self.masa = masa          # kg
        self.x = posicion_x       # m
        self.y = posicion_y       # m
        self.vx = 0.0             # m/s
        self.vy = 0.0             # m/s

    def distancia_a(self, otro):
        """Distancia euclidiana entre dos cuerpos."""
        dx = otro.x - self.x
        dy = otro.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def fuerza_gravitacional(self, otro):
        """Magnitud de la fuerza gravitacional: F = G·m1·m2 / r²"""
        r = self.distancia_a(otro)
        if r == 0:
            return 0.0
        return self.G * self.masa * otro.masa / r ** 2

    def info(self):
        """Información básica del cuerpo. Las subclases pueden extenderla."""
        return f"{self.nombre} (m={self.masa:.2e} kg)"

    def __repr__(self):
        return self.info()


# cada subclase agrega lo que la distingue

class Estrella(CuerpoCeleste):
    """Una estrella: tiene luminosidad y temperatura superficial."""

    def __init__(self, nombre, masa, posicion_x, posicion_y,
                 luminosidad, temperatura):
        super().__init__(nombre, masa, posicion_x, posicion_y)
        self.luminosidad = luminosidad      # en luminosidades solares (L☉)
        self.temperatura = temperatura      # K

    def clasificacion_espectral(self):
        """Clasificación simplificada por temperatura."""
        T = self.temperatura
        if T >= 30000:
            return "O (azul)"
        elif T >= 10000:
            return "B (azul-blanco)"
        elif T >= 7500:
            return "A (blanco)"
        elif T >= 6000:
            return "F (amarillo-blanco)"
        elif T >= 5200:
            return "G (amarillo)"
        elif T >= 3700:
            return "K (naranja)"
        else:
            return "M (rojo)"

    def info(self):
        base = super().info()
        return (f"⭐ {base}, T={self.temperatura} K, "
                f"L={self.luminosidad} L☉, "
                f"Tipo {self.clasificacion_espectral()}")


class Planeta(CuerpoCeleste):
    """Un planeta: orbita una estrella."""

    def __init__(self, nombre, masa, posicion_x, posicion_y, radio_orbital):
        super().__init__(nombre, masa, posicion_x, posicion_y)
        self.radio_orbital = radio_orbital  # m

    def periodo_orbital(self, estrella):
        """Tercera ley de Kepler: T² = (4π²/GM) · r³"""
        T_squared = (4 * math.pi ** 2 / (self.G * estrella.masa)) * self.radio_orbital ** 3
        return math.sqrt(T_squared)

    def velocidad_orbital(self, estrella):
        """Velocidad orbital circular: v = sqrt(GM/r)"""
        return math.sqrt(self.G * estrella.masa / self.radio_orbital)

    def info(self):
        base = super().info()
        r_ua = self.radio_orbital / 1.496e11  # convertir a UA
        return f"🪐 {base}, r={r_ua:.2f} UA"


class Satelite(CuerpoCeleste):
    """Un satélite natural: orbita un planeta."""

    def __init__(self, nombre, masa, posicion_x, posicion_y,
                 radio_orbital, planeta_huesped):
        super().__init__(nombre, masa, posicion_x, posicion_y)
        self.radio_orbital = radio_orbital
        self.planeta_huesped = planeta_huesped

    def periodo_orbital(self):
        """Periodo orbital alrededor de su planeta huésped."""
        T_sq = (4 * math.pi ** 2 / (self.G * self.planeta_huesped.masa)) * self.radio_orbital ** 3
        return math.sqrt(T_sq)

    def info(self):
        base = super().info()
        r_km = self.radio_orbital / 1000
        return f"🌙 {base}, orbita {self.planeta_huesped.nombre}, r={r_km:.0f} km"


# --- demo: mini sistema solar ---

if __name__ == "__main__":

    # Crear objetos
    sol = Estrella(
        nombre="Sol",
        masa=1.989e30,
        posicion_x=0, posicion_y=0,
        luminosidad=1.0,
        temperatura=5778
    )

    tierra = Planeta(
        nombre="Tierra",
        masa=5.972e24,
        posicion_x=1.496e11, posicion_y=0,
        radio_orbital=1.496e11
    )

    luna = Satelite(
        nombre="Luna",
        masa=7.342e22,
        posicion_x=1.496e11 + 3.844e8, posicion_y=0,
        radio_orbital=3.844e8,
        planeta_huesped=tierra
    )

    marte = Planeta(
        nombre="Marte",
        masa=6.417e23,
        posicion_x=2.279e11, posicion_y=0,
        radio_orbital=2.279e11
    )

    # --- Polimorfismo: todos responden a info() de forma distinta ---
    print("=== Sistema Solar (polimorfismo con info()) ===")
    cuerpos = [sol, tierra, luna, marte]
    for cuerpo in cuerpos:
        print(f"  {cuerpo.info()}")

    # --- Fuerza gravitacional (método heredado) ---
    print("\n=== Fuerza gravitacional ===")
    F_sol_tierra = sol.fuerza_gravitacional(tierra)
    print(f"F(Sol → Tierra) = {F_sol_tierra:.2e} N")

    F_tierra_luna = tierra.fuerza_gravitacional(luna)
    print(f"F(Tierra → Luna) = {F_tierra_luna:.2e} N")

    # --- Periodo orbital (Tercera ley de Kepler) ---
    print("\n=== Periodos orbitales (3ra ley de Kepler) ===")
    T_tierra = tierra.periodo_orbital(sol)
    print(f"Tierra alrededor del Sol: {T_tierra:.2e} s "
          f"= {T_tierra / (3600 * 24):.1f} días")

    T_marte = marte.periodo_orbital(sol)
    print(f"Marte alrededor del Sol:  {T_marte:.2e} s "
          f"= {T_marte / (3600 * 24):.1f} días")

    T_luna = luna.periodo_orbital()
    print(f"Luna alrededor de Tierra: {T_luna:.2e} s "
          f"= {T_luna / (3600 * 24):.1f} días")

    # --- Velocidades orbitales ---
    print("\n=== Velocidades orbitales ===")
    v_tierra = tierra.velocidad_orbital(sol)
    print(f"Tierra: {v_tierra:.2f} m/s = {v_tierra / 1000:.2f} km/s")

    v_marte = marte.velocidad_orbital(sol)
    print(f"Marte:  {v_marte:.2f} m/s = {v_marte / 1000:.2f} km/s")
