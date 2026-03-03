"""
Composición — Ejemplo 1: Átomo
===============================
En la composición, el todo crea y posee sus partes. Si el átomo
desaparece, su núcleo y electrones también.

Esto lo diferencia de la agregación: allá las partes existen
por su cuenta (como planetas sin sistema). Aquí no.

    Atomo crea → Nucleo
    Atomo crea → [Electron, Electron, ...]

Para practicar:
1. Agrega ionizar(n) que retire n electrones del átomo.
2. Implementa __eq__ para comparar átomos por número atómico.
3. Calcula el radio de Bohr del n-ésimo orbital:
   r_n = n²·a₀ / Z  (a₀ = 0.529 Å)
"""

import math


# estas clases no se usan solas, el átomo las crea internamente

class Electron:
    """Electrón en una capa del átomo."""

    MASA   = 9.109e-31   # kg
    CARGA  = -1.602e-19  # C

    def __init__(self, numero_capa: int):
        self.numero_capa = numero_capa   # n = 1, 2, 3, ...

    def energia_bohr(self, Z: int) -> float:
        """Energía en el modelo de Bohr: Eₙ = −13.6·Z² / n²  (eV)."""
        return -13.6 * Z**2 / self.numero_capa**2

    def __repr__(self):
        return f"Electron(capa={self.numero_capa})"


class Nucleo:
    """Núcleo atómico compuesto por protones y neutrones."""

    MASA_PROTON  = 1.673e-27  # kg
    MASA_NEUTRON = 1.675e-27  # kg

    def __init__(self, Z: int, N: int):
        self.Z = Z   # número atómico (protones)
        self.N = N   # número de neutrones

    @property
    def numero_masico(self) -> int:
        """A = Z + N."""
        return self.Z + self.N

    @property
    def masa(self) -> float:
        """Masa aproximada del núcleo (sin energía de ligadura)."""
        return self.Z * self.MASA_PROTON + self.N * self.MASA_NEUTRON

    @property
    def carga(self) -> float:
        """Carga eléctrica total del núcleo (C)."""
        return self.Z * 1.602e-19

    def radio_nuclear(self) -> float:
        """R = R₀ · A^{1/3}, R₀ = 1.2 fm."""
        R0 = 1.2e-15  # m
        return R0 * self.numero_masico ** (1/3)

    def energia_ligadura_aprox(self) -> float:
        """Fórmula de Bethe-Weizsäcker simplificada (MeV)."""
        A, Z, N = self.numero_masico, self.Z, self.N
        if A <= 1:
            return 0.0
        av, as_, ac, aa = 15.85, 18.34, 0.711, 23.21
        Eb = (av * A
              - as_ * A**(2/3)
              - ac * Z**2 / A**(1/3)
              - aa * (A - 2*Z)**2 / A)
        return max(0.0, Eb)

    def __repr__(self):
        return f"Nucleo(Z={self.Z}, N={self.N}, A={self.numero_masico})"


# el átomo crea y controla su núcleo y electrones

class Atomo:
    """Átomo neutro: crea y posee su núcleo y sus electrones."""

    # Tabla parcial de elementos
    SIMBOLOS = {
        1: "H",  2: "He", 3: "Li",  4: "Be",  5: "B",
        6: "C",  7: "N",  8: "O",   9: "F",  10: "Ne",
       11: "Na", 12: "Mg",17: "Cl", 18: "Ar", 26: "Fe",
       29: "Cu", 47: "Ag", 79: "Au", 92: "U",
    }

    def __init__(self, Z: int, N: int):
        if Z <= 0 or N < 0:
            raise ValueError("Z debe ser > 0 y N ≥ 0.")
        # Composición: el átomo CREA sus partes
        self._nucleo     = Nucleo(Z, N)
        self._electrones = self._distribuir_electrones(Z)

    # para consultar Z o A, el átomo le pregunta a su núcleo

    @property
    def numero_atomico(self) -> int:
        return self._nucleo.Z

    @property
    def simbolo(self) -> str:
        return self.SIMBOLOS.get(self._nucleo.Z, f"X{self._nucleo.Z}")

    @property
    def n_electrones(self) -> int:
        return len(self._electrones)

    @property
    def masa_total(self) -> float:
        """Masa núcleo + masa electrones (kg)."""
        return (self._nucleo.masa
                + self.n_electrones * Electron.MASA)

    # asigna los electrones a capas según la regla 2n²

    def _distribuir_electrones(self, Z: int) -> list[Electron]:
        """Llena capas 1→2→3→... con máximos 2n² electrones."""
        electrones = []
        restantes = Z
        capa = 1
        while restantes > 0:
            maximo = 2 * capa**2
            en_capa = min(restantes, maximo)
            electrones.extend([Electron(capa)] * en_capa)
            restantes -= en_capa
            capa += 1
        return electrones

    def configuracion_electronica(self) -> str:
        """Devuelve una representación textual de capas."""
        capas: dict[int, int] = {}
        for e in self._electrones:
            capas[e.numero_capa] = capas.get(e.numero_capa, 0) + 1
        return "  ".join(f"{n}:{cnt}" for n, cnt in sorted(capas.items()))

    # energías usando el modelo de Bohr

    def energia_ionizacion_bohr(self) -> float:
        """Energía para arrancar el electrón más externo (eV)."""
        if not self._electrones:
            return 0.0
        capa_max = max(e.numero_capa for e in self._electrones)
        return abs(Electron(capa_max).energia_bohr(self._nucleo.Z))

    # representación legible del átomo

    def __repr__(self):
        return (f"Atomo({self.simbolo}, Z={self.numero_atomico}, "
                f"A={self._nucleo.numero_masico}, "
                f"e⁻={self.n_electrones})")


# --- demo ---

if __name__ == "__main__":
    elementos = [
        Atomo(1,  0),   # H
        Atomo(2,  2),   # He
        Atomo(6,  6),   # C
        Atomo(8,  8),   # O
        Atomo(26, 30),  # Fe
        Atomo(92, 146), # U-238
    ]

    print("=" * 60)
    print("ÁTOMOS — composición: núcleo + electrones")
    print("=" * 60)

    for atomo in elementos:
        print(f"\n{atomo}")
        nucleo = atomo._nucleo
        print(f"  Núcleo       : {nucleo}")
        print(f"  Config. e⁻   : {atomo.configuracion_electronica()}")
        print(f"  Masa total   : {atomo.masa_total:.4e} kg")
        print(f"  Radio nuclear: {nucleo.radio_nuclear():.3e} m")
        print(f"  Eb (Bethe-W) : {nucleo.energia_ligadura_aprox():.2f} MeV")
        print(f"  E ionización : {atomo.energia_ionizacion_bohr():.3f} eV")
