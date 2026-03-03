"""
Herencia — Ejemplo 2: Jerarquía de cuerpos celestes
====================================================
Un planeta hereda todo lo que tiene un cuerpo celeste y añade
lunas y período orbital. Un planeta habitable hereda todo lo
del planeta y añade temperatura y agua. Tres niveles en cadena.

    CuerpoCeleste          (masa, posición, velocidad)
    ├── Planeta            (lunas, periodo orbital)
    │   └── PlanetaHabitable (temperatura, atmósfera)
    └── Estrella           (temperatura, luminosidad)
        └── NanaBranca     (masa límite Chandrasekhar)

Para practicar:
1. Agrega Cometa que herede de CuerpoCeleste y tenga excentricidad orbital.
2. Sobrescribe __repr__ en cada nivel y observa cómo super() encadena las representaciones.
3. ¿Qué ventaja tiene usar super().__init__() en lugar de llamar al padre por su nombre?
"""

import math


# todo objeto astronómico tiene masa, posición y velocidad

class CuerpoCeleste:
    """Objeto astronómico con masa, posición heliocéntrica y velocidad."""

    G = 6.674e-11  # m³ kg⁻¹ s⁻² — constante gravitacional

    def __init__(self, nombre: str, masa: float,
                 distancia_al_sol: float, velocidad_orbital: float):
        self.nombre            = nombre
        self.masa              = masa               # kg
        self.distancia_al_sol  = distancia_al_sol   # m
        self.velocidad_orbital = velocidad_orbital  # m/s

    def energia_cinetica_orbital(self) -> float:
        """Ec = ½ m v²  (J)."""
        return 0.5 * self.masa * self.velocidad_orbital**2

    def energia_potencial_gravitacional(self, masa_central: float) -> float:
        """Ep = −G·M·m / r  (J)."""
        return -self.G * masa_central * self.masa / self.distancia_al_sol

    def __repr__(self):
        return (f"CuerpoCeleste('{self.nombre}', "
                f"m={self.masa:.2e} kg, d={self.distancia_al_sol:.2e} m)")


# un planeta agrega lunas, anillos y período orbital

MASA_SOL = 1.989e30  # kg

class Planeta(CuerpoCeleste):
    """Cuerpo que orbita una estrella; puede tener lunas y anillos."""

    def __init__(self, nombre: str, masa: float,
                 distancia_al_sol: float, velocidad_orbital: float,
                 num_lunas: int = 0, tiene_anillos: bool = False):
        super().__init__(nombre, masa, distancia_al_sol, velocidad_orbital)
        self.num_lunas     = num_lunas
        self.tiene_anillos = tiene_anillos

    def periodo_orbital(self) -> float:
        """T = 2π r / v  (s) — período orbital kepleriano."""
        return 2 * math.pi * self.distancia_al_sol / self.velocidad_orbital

    def periodo_orbital_anios(self) -> float:
        return self.periodo_orbital() / (365.25 * 24 * 3600)

    def energia_total_orbital(self) -> float:
        """Energía mecánica total en órbita circular: E = −G M m / (2r)."""
        return -self.G * MASA_SOL * self.masa / (2 * self.distancia_al_sol)

    def __repr__(self):
        anillos = "con anillos" if self.tiene_anillos else "sin anillos"
        return (f"Planeta('{self.nombre}', "
                f"lunas={self.num_lunas}, {anillos}, "
                f"T={self.periodo_orbital_anios():.2f} años)")


# añade temperatura promedio y presencia de agua para evaluar habitabilidad

class PlanetaHabitable(Planeta):
    """Planeta dentro de la zona de habitabilidad de su estrella."""

    def __init__(self, nombre: str, masa: float,
                 distancia_al_sol: float, velocidad_orbital: float,
                 num_lunas: int, tiene_anillos: bool,
                 temp_promedio: float, tiene_agua: bool):
        super().__init__(nombre, masa, distancia_al_sol, velocidad_orbital,
                         num_lunas, tiene_anillos)
        self.temp_promedio = temp_promedio  # °C
        self.tiene_agua    = tiene_agua

    def indice_habitabilidad(self) -> float:
        """Heurística simplificada (0–1): temperatura + agua."""
        if not (-50 <= self.temp_promedio <= 60):
            return 0.0
        t_score = 1 - abs(self.temp_promedio - 15) / 65
        return 0.7 * t_score + 0.3 * int(self.tiene_agua)

    def __repr__(self):
        agua = "con agua" if self.tiene_agua else "sin agua"
        return (f"PlanetaHabitable('{self.nombre}', "
                f"T_prom={self.temp_promedio}°C, {agua}, "
                f"IH={self.indice_habitabilidad():.2f})")


# una estrella tiene temperatura superficial y luminosidad propias

class Estrella(CuerpoCeleste):
    """Estrella con luminosidad y temperatura superficial."""

    SIGMA = 5.67e-8  # W m⁻² K⁻⁴ — constante de Stefan-Boltzmann

    def __init__(self, nombre: str, masa: float, radio: float,
                 temperatura_superficial: float):
        # Las estrellas no "orbitan" otro cuerpo en este modelo
        super().__init__(nombre, masa,
                         distancia_al_sol=0.0, velocidad_orbital=0.0)
        self.radio                  = radio                  # m
        self.temperatura_superficial = temperatura_superficial  # K

    def luminosidad(self) -> float:
        """L = 4π R² σ T⁴  (W) — ley de Stefan-Boltzmann."""
        return 4 * math.pi * self.radio**2 * self.SIGMA * self.temperatura_superficial**4

    def clase_espectral(self) -> str:
        """Clasificación Harvard simplificada por temperatura."""
        T = self.temperatura_superficial
        if   T >= 30_000: return "O"
        elif T >= 10_000: return "B"
        elif T >=  7_500: return "A"
        elif T >=  6_000: return "F"
        elif T >=  5_200: return "G"
        elif T >=  3_700: return "K"
        else:             return "M"

    def __repr__(self):
        return (f"Estrella('{self.nombre}', "
                f"T={self.temperatura_superficial} K, "
                f"clase={self.clase_espectral()}, "
                f"L={self.luminosidad():.3e} W)")


# remanente estelar: muy denso, ya no fusiona hidrógeno

class NanaBranca(Estrella):
    """Remanente estelar denso y compacto; no fusiona más hidrógeno."""

    LIMITE_CHANDRASEKHAR = 1.44 * 1.989e30  # kg (~1.44 masas solares)

    def __init__(self, nombre: str, masa: float, radio: float,
                 temperatura_superficial: float):
        super().__init__(nombre, masa, radio, temperatura_superficial)

    def densidad_media(self) -> float:
        """ρ = M / (4/3 π R³)  (kg/m³)."""
        volumen = (4 / 3) * math.pi * self.radio**3
        return self.masa / volumen

    def es_estable(self) -> bool:
        """Estable si está por debajo del límite de Chandrasekhar."""
        return self.masa < self.LIMITE_CHANDRASEKHAR

    def __repr__(self):
        estable = "estable" if self.es_estable() else "INESTABLE → SN Ia"
        return (f"NanaBranca('{self.nombre}', "
                f"ρ={self.densidad_media():.2e} kg/m³, {estable})")


# --- demo ---

if __name__ == "__main__":
    # --- Planetas del sistema solar ---
    tierra = PlanetaHabitable(
        nombre="Tierra", masa=5.972e24,
        distancia_al_sol=1.496e11, velocidad_orbital=29_783,
        num_lunas=1, tiene_anillos=False,
        temp_promedio=15, tiene_agua=True,
    )
    saturno = Planeta(
        nombre="Saturno", masa=5.683e26,
        distancia_al_sol=1.427e12, velocidad_orbital=9_690,
        num_lunas=146, tiene_anillos=True,
    )

    # --- Estrellas ---
    sol = Estrella(
        nombre="Sol", masa=1.989e30,
        radio=6.96e8, temperatura_superficial=5_778,
    )
    sirio = Estrella(
        nombre="Sirio A", masa=4.018e30,
        radio=1.19e9, temperatura_superficial=9_940,
    )
    sirio_b = NanaBranca(
        nombre="Sirio B", masa=2.0e30,
        radio=5.85e6, temperatura_superficial=25_200,
    )

    objetos = [tierra, saturno, sol, sirio, sirio_b]

    print("=" * 60)
    print("SISTEMA SOLAR Y MÁS — herencia de cuerpos celestes")
    print("=" * 60)

    for obj in objetos:
        print(f"\n{obj}")
        ec = obj.energia_cinetica_orbital()
        if ec > 0:
            print(f"  Ec orbital      : {ec:.3e} J")
        if isinstance(obj, Planeta):
            print(f"  Período orbital : {obj.periodo_orbital_anios():.2f} años")
            print(f"  Energía total   : {obj.energia_total_orbital():.3e} J")
        if isinstance(obj, PlanetaHabitable):
            print(f"  Índice habitab. : {obj.indice_habitabilidad():.2f}")
        if isinstance(obj, Estrella):
            print(f"  Luminosidad     : {obj.luminosidad():.3e} W")
            print(f"  Clase espectral : {obj.clase_espectral()}")
        if isinstance(obj, NanaBranca):
            print(f"  Densidad media  : {obj.densidad_media():.2e} kg/m³")
            print(f"  ¿Estable?       : {obj.es_estable()}")
