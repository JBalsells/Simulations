"""
Herencia — Ejemplo 1: Jerarquía de partículas subatómicas
==========================================================
Conceptos OOP: herencia simple, herencia múltiple, super(),
               override de métodos, isinstance / issubclass.

Árbol de herencia
-----------------
    Particula
    ├── ParticulaCargada  (agrega: carga eléctrica)
    │   ├── Electron
    │   └── Proton
    └── ParticulaNeutral
        └── Neutron

Una subclase hereda todos los atributos y métodos de su padre
y puede extenderlos o reemplazarlos (override).

Tareas para el estudiante
-------------------------
1. Agrega la clase `Muon` que hereda de `ParticulaCargada`
   con masa = 1.883e-28 kg y carga = -1.
2. Implementa un método `es_antipartícula_de(otra)` en
   `ParticulaCargada` que devuelva True si misma masa,
   carga opuesta.
3. ¿Qué pasa si llamas `Particula.energia_reposo()` directamente?
"""

# ---------------------------------------------------------------------------
# Constantes físicas
# ---------------------------------------------------------------------------

C_LUZ = 2.998e8   # m/s — velocidad de la luz


# ---------------------------------------------------------------------------
# Clase base
# ---------------------------------------------------------------------------

class Particula:
    """Partícula puntual con masa en reposo."""

    def __init__(self, nombre: str, masa: float):
        self.nombre = nombre
        self.masa   = masa      # kg

    def energia_reposo(self) -> float:
        """E₀ = m·c²  (en Joules)."""
        return self.masa * C_LUZ**2

    def __repr__(self):
        return f"{self.nombre}(m={self.masa:.3e} kg)"


# ---------------------------------------------------------------------------
# Primera subclase: partícula con carga eléctrica
# ---------------------------------------------------------------------------

class ParticulaCargada(Particula):
    """Partícula que porta carga eléctrica."""

    CARGA_ELEMENTAL = 1.602e-19  # C

    def __init__(self, nombre: str, masa: float, numero_carga: int):
        super().__init__(nombre, masa)          # delega al padre
        self.numero_carga = numero_carga        # +1, -1, +2, …

    @property
    def carga(self) -> float:
        """Carga real en Coulombs."""
        return self.numero_carga * self.CARGA_ELEMENTAL

    def fuerza_coulomb(self, otra: "ParticulaCargada", distancia: float) -> float:
        """Fuerza electrostática entre dos partículas cargadas (N).
        F = k·q₁·q₂ / r²
        """
        k = 8.988e9  # N·m²/C²
        return k * self.carga * otra.carga / distancia**2

    def __repr__(self):
        signo = "+" if self.numero_carga >= 0 else ""
        return f"{self.nombre}(m={self.masa:.3e} kg, q={signo}{self.numero_carga}e)"


# ---------------------------------------------------------------------------
# Segunda subclase: partícula sin carga
# ---------------------------------------------------------------------------

class ParticulaNeutral(Particula):
    """Partícula sin carga eléctrica neta."""

    def __init__(self, nombre: str, masa: float):
        super().__init__(nombre, masa)

    def puede_ionizar(self) -> bool:
        """Las partículas neutras no ionizan directamente por campo eléctrico."""
        return False


# ---------------------------------------------------------------------------
# Subclases de ParticulaCargada
# ---------------------------------------------------------------------------

class Electron(ParticulaCargada):
    """Electrón: leptón de carga −1."""

    MASA_ELECTRON = 9.109e-31  # kg

    def __init__(self):
        super().__init__("Electrón", self.MASA_ELECTRON, numero_carga=-1)

    def longitud_onda_de_broglie(self, velocidad: float) -> float:
        """λ = h / (m·v) — longitud de onda de De Broglie (m)."""
        h = 6.626e-34  # J·s
        return h / (self.masa * velocidad)


class Proton(ParticulaCargada):
    """Protón: barión de carga +1."""

    MASA_PROTON = 1.673e-27  # kg

    def __init__(self):
        super().__init__("Protón", self.MASA_PROTON, numero_carga=+1)

    def radio_nuclear(self) -> float:
        """Radio clásico del protón (m)."""
        return 8.775e-16


# ---------------------------------------------------------------------------
# Subclase de ParticulaNeutral
# ---------------------------------------------------------------------------

class Neutron(ParticulaNeutral):
    """Neutrón: barión de carga 0."""

    MASA_NEUTRON = 1.675e-27  # kg
    VIDA_MEDIA   = 879.4       # s (fuera del núcleo)

    def __init__(self):
        super().__init__("Neutrón", self.MASA_NEUTRON)

    def decae_en(self) -> str:
        """Decaimiento beta: n → p + e⁻ + antineutrino."""
        return "Protón + Electrón + Antineutrino_e"


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    e  = Electron()
    p  = Proton()
    n  = Neutron()

    particulas = [e, p, n]

    print("=" * 55)
    print("PARTÍCULAS SUBATÓMICAS — herencia en acción")
    print("=" * 55)

    for part in particulas:
        print(f"\n{part}")
        print(f"  Energía en reposo : {part.energia_reposo():.3e} J")

        if isinstance(part, ParticulaCargada):
            print(f"  Carga             : {part.carga:.3e} C")
        if isinstance(part, ParticulaNeutral):
            print(f"  ¿Ioniza directo?  : {part.puede_ionizar()}")

    # Herencia verificada
    print("\n--- Verificación de jerarquía ---")
    print(f"  ¿Electron es Particula?         {isinstance(e, Particula)}")
    print(f"  ¿Electron es ParticulaCargada?  {isinstance(e, ParticulaCargada)}")
    print(f"  ¿Electron es ParticulaNeutral?  {isinstance(e, ParticulaNeutral)}")
    print(f"  ¿Proton subclase de Particula?  {issubclass(Proton, Particula)}")

    # Fuerza entre electrón y protón (radio de Bohr)
    r_bohr = 5.29e-11  # m
    F = e.fuerza_coulomb(p, r_bohr)
    print(f"\n  Fuerza e⁻—p⁺ a r_Bohr = {r_bohr:.2e} m : {F:.3e} N")

    # Longitud de onda del electrón
    v_electron = 2.19e6  # m/s (primer orbital de Bohr)
    lda = e.longitud_onda_de_broglie(v_electron)
    print(f"  λ De Broglie del e⁻ a v={v_electron:.2e} m/s : {lda:.3e} m")

    # Decaimiento del neutrón
    print(f"\n  Neutrón libre decae en: {n.decae_en()}")
    print(f"  Vida media: {Neutron.VIDA_MEDIA} s ≈ {Neutron.VIDA_MEDIA/60:.1f} min")
