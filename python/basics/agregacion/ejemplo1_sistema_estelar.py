"""
Agregación — Ejemplo 1: Sistema estelar
========================================
Conceptos OOP: agregación ("usa/contiene"), ciclo de vida independiente,
               diferencia clave con composición.

Idea central
------------
La agregación es una relación TIENE-UN donde las partes PUEDEN EXISTIR
DE FORMA INDEPENDIENTE del contenedor.

    SistemaEstelar ──(agrega)──► Estrella  (existe por sí sola)
                   ──(agrega)──► [Planeta, Planeta, ...]

La diferencia con composición:
  - Composición: si destruyes el Átomo, el Núcleo desaparece.
  - Agregación:  si destruyes el SistemaEstelar, los Planeta y Estrella
                 siguen existiendo (pueden pertenecer a otro catálogo).

Tareas para el estudiante
-------------------------
1. Agrega el método `agregar_luna(planeta_idx, luna)` al sistema.
2. Implementa `planetas_habitables()` que retorne los planetas
   con temperatura entre −50 y 60 °C.
3. ¿Puede un mismo planeta pertenecer a dos sistemas a la vez?
   ¿Qué implicaría eso para el modelado?
"""

import math


# ---------------------------------------------------------------------------
# Clases independientes (pueden existir sin el sistema)
# ---------------------------------------------------------------------------

class Estrella:
    """Estrella que puede pertenecer o no a un sistema."""

    SIGMA = 5.67e-8  # W m⁻² K⁻⁴

    def __init__(self, nombre: str, masa: float, radio: float,
                 temperatura: float):
        self.nombre      = nombre
        self.masa        = masa          # kg (masas solares × 1.989e30)
        self.radio       = radio         # m
        self.temperatura = temperatura   # K

    @property
    def luminosidad(self) -> float:
        """L = 4πR²σT⁴ (W)."""
        return 4 * math.pi * self.radio**2 * self.SIGMA * self.temperatura**4

    @property
    def zona_habitabilidad(self) -> tuple[float, float]:
        """Límites interior y exterior de la zona habitable (UA)."""
        L_sol = 3.828e26   # W
        L_rel = self.luminosidad / L_sol
        inner = math.sqrt(L_rel / 1.1)
        outer = math.sqrt(L_rel / 0.53)
        return round(inner, 3), round(outer, 3)

    def __repr__(self):
        return f"Estrella('{self.nombre}', T={self.temperatura} K)"


class Planeta:
    """Planeta que puede pertenecer o no a un sistema estelar."""

    G = 6.674e-11  # m³ kg⁻¹ s⁻²
    UA = 1.496e11  # m

    def __init__(self, nombre: str, masa: float, radio: float,
                 semieje_mayor_ua: float, velocidad_orbital: float):
        self.nombre              = nombre
        self.masa                = masa                # kg
        self.radio               = radio               # m
        self.semieje_mayor_ua    = semieje_mayor_ua    # UA
        self.velocidad_orbital   = velocidad_orbital   # m/s
        self._lunas: list        = []

    @property
    def semieje_mayor_m(self) -> float:
        return self.semieje_mayor_ua * self.UA

    def agregar_luna(self, luna: "Planeta") -> None:
        self._lunas.append(luna)

    @property
    def n_lunas(self) -> int:
        return len(self._lunas)

    def temperatura_equilibrio(self, luminosidad_estrella: float,
                               albedo: float = 0.3) -> float:
        """T_eq = [L(1−A) / (16πσd²)]^{1/4}  (K)."""
        SIGMA = 5.67e-8
        d = self.semieje_mayor_m
        return (luminosidad_estrella * (1 - albedo)
                / (16 * math.pi * SIGMA * d**2)) ** 0.25

    def __repr__(self):
        return (f"Planeta('{self.nombre}', "
                f"a={self.semieje_mayor_ua} UA, "
                f"lunas={self.n_lunas})")


# ---------------------------------------------------------------------------
# Clase que agrega: Sistema Estelar
# ---------------------------------------------------------------------------

class SistemaEstelar:
    """Colección de una estrella y sus planetas orbitantes.

    Recibe objetos ya creados (no los crea): si el sistema desaparece,
    estrella y planetas siguen existiendo como objetos Python.
    """

    def __init__(self, nombre: str, estrella: Estrella):
        self.nombre    = nombre
        self._estrella = estrella   # referencia, no copia
        self._planetas: list[Planeta] = []

    def agregar_planeta(self, planeta: Planeta) -> None:
        self._planetas.append(planeta)

    def retirar_planeta(self, nombre: str) -> Planeta | None:
        """Retira un planeta del sistema (el objeto sigue existiendo)."""
        for i, p in enumerate(self._planetas):
            if p.nombre == nombre:
                return self._planetas.pop(i)
        return None

    @property
    def n_planetas(self) -> int:
        return len(self._planetas)

    def planetas_en_zona_habitable(self) -> list[Planeta]:
        """Planetas cuyo semieje cae dentro de la zona habitable."""
        inner, outer = self._estrella.zona_habitabilidad
        return [p for p in self._planetas
                if inner <= p.semieje_mayor_ua <= outer]

    def masa_total(self) -> float:
        """Masa del sistema: estrella + planetas (kg)."""
        return self._estrella.masa + sum(p.masa for p in self._planetas)

    def resumen(self) -> None:
        hz_inner, hz_outer = self._estrella.zona_habitabilidad
        print(f"\nSistema: {self.nombre}")
        print(f"  Estrella   : {self._estrella}")
        print(f"  Luminosidad: {self._estrella.luminosidad:.3e} W")
        print(f"  Zona hab.  : {hz_inner}–{hz_outer} UA")
        print(f"  Planetas   : {self.n_planetas}")
        print(f"  {'Nombre':12} {'a (UA)':>8} {'T_eq (K)':>10} {'¿Zona hab?':>12}")
        print("  " + "-" * 48)
        for p in sorted(self._planetas, key=lambda x: x.semieje_mayor_ua):
            T = p.temperatura_equilibrio(self._estrella.luminosidad)
            zh = "Sí" if hz_inner <= p.semieje_mayor_ua <= hz_outer else "No"
            print(f"  {p.nombre:12} {p.semieje_mayor_ua:>8.3f} "
                  f"{T:>10.1f} {zh:>12}")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Crear objetos independientes
    sol = Estrella("Sol", masa=1.989e30, radio=6.96e8, temperatura=5_778)

    mercurio = Planeta("Mercurio", 3.3e23, 2.44e6, semieje_mayor_ua=0.387, velocidad_orbital=47_870)
    venus    = Planeta("Venus",    4.87e24, 6.05e6, semieje_mayor_ua=0.723, velocidad_orbital=35_020)
    tierra   = Planeta("Tierra",   5.97e24, 6.37e6, semieje_mayor_ua=1.000, velocidad_orbital=29_783)
    marte    = Planeta("Marte",    6.39e23, 3.39e6, semieje_mayor_ua=1.524, velocidad_orbital=24_130)
    jupiter  = Planeta("Júpiter",  1.90e27, 6.99e7, semieje_mayor_ua=5.204, velocidad_orbital=13_070)

    luna = Planeta("Luna", 7.34e22, 1.74e6, semieje_mayor_ua=0.00257, velocidad_orbital=1_022)
    tierra.agregar_luna(luna)

    # Construir el sistema
    sistema_solar = SistemaEstelar("Sistema Solar", sol)
    for planeta in [mercurio, venus, tierra, marte, jupiter]:
        sistema_solar.agregar_planeta(planeta)

    print("=" * 55)
    print("SISTEMA ESTELAR — agregación")
    print("=" * 55)

    sistema_solar.resumen()

    # Los planetas existen de forma independiente del sistema
    print(f"\n--- Los objetos siguen existiendo tras retirarse ---")
    jupiter_retirado = sistema_solar.retirar_planeta("Júpiter")
    print(f"  Júpiter fuera del sistema: {jupiter_retirado}")
    print(f"  Sistema ahora: {sistema_solar.n_planetas} planetas")
    print(f"  Júpiter sigue siendo: {jupiter}")   # el objeto persiste

    # Segundo sistema que reusa el mismo objeto planeta
    print(f"\n--- Usar Júpiter en un segundo catálogo ---")
    catalogo_gigantes = SistemaEstelar("Catálogo Gigantes", sol)
    catalogo_gigantes.agregar_planeta(jupiter_retirado)
    print(f"  Catálogo contiene: {catalogo_gigantes.n_planetas} planeta(s)")
    print(f"  Es el mismo objeto: {jupiter is jupiter_retirado}")
