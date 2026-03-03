"""
Abstracción — Ejemplo 1: Ecuaciones de estado de un gas
========================================================
Conceptos OOP: ABC (Abstract Base Class), @abstractmethod,
               interfaz obligatoria, polimorfismo por herencia.

Idea central
------------
La abstracción define QUÉ debe hacer un objeto sin especificar CÓMO.
Usando `abc.ABC` forzamos que toda subclase implemente los métodos
abstractos; si no lo hace, Python impide instanciarla.

Física
------
Tres modelos para la presión de un gas:

  Gas Ideal:      PV = nRT          → P = nRT / V
  Van der Waals:  (P + an²/V²)(V−nb) = nRT
  Virial (2.º):   PV/(nRT) = 1 + B(T)·n/V

Todos comparten la interfaz:
    presion(V, T, n) → float (Pa)
    nombre           → str
    descripcion()    → str

Tareas para el estudiante
-------------------------
1. Agrega el modelo de Redlich-Kwong con sus constantes.
2. Implementa `temperatura_critica()` y `presion_critica()` como
   métodos abstractos (las constantes dependen del modelo).
3. Traza P(V) para los tres modelos con matplotlib y compáralos.
"""

from abc import ABC, abstractmethod
import math


# ---------------------------------------------------------------------------
# Clase base abstracta — define la interfaz
# ---------------------------------------------------------------------------

class EcuacionEstado(ABC):
    """Interfaz abstracta para modelos termodinámicos de gases."""

    R = 8.314  # J mol⁻¹ K⁻¹ — constante de los gases ideales

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre del modelo."""

    @abstractmethod
    def presion(self, V: float, T: float, n: float) -> float:
        """Calcula la presión en Pascales.

        Parámetros
        ----------
        V : volumen (m³)
        T : temperatura (K)
        n : cantidad de sustancia (mol)
        """

    @abstractmethod
    def descripcion(self) -> str:
        """Descripción breve del modelo y sus limitaciones."""

    def factor_compresibilidad(self, V: float, T: float, n: float) -> float:
        """Z = PV / nRT — factor de compresibilidad (1 para gas ideal)."""
        P = self.presion(V, T, n)
        return P * V / (n * self.R * T)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.nombre})"


# ---------------------------------------------------------------------------
# Implementación 1: Gas Ideal
# ---------------------------------------------------------------------------

class GasIdeal(EcuacionEstado):
    """PV = nRT — modelo sin interacciones moleculares."""

    @property
    def nombre(self) -> str:
        return "Gas Ideal"

    def presion(self, V: float, T: float, n: float) -> float:
        return n * self.R * T / V

    def descripcion(self) -> str:
        return ("Gas Ideal (PV = nRT): válido a bajas presiones y "
                "altas temperaturas. No considera volumen molecular "
                "ni fuerzas intermoleculares.")


# ---------------------------------------------------------------------------
# Implementación 2: Van der Waals
# ---------------------------------------------------------------------------

class VanDerWaals(EcuacionEstado):
    """(P + an²/V²)(V − nb) = nRT — considera volumen y atracción."""

    # Constantes de Van der Waals para algunos gases
    CONSTANTES = {
        "N2": (0.1370, 3.87e-5),   # a (Pa·m⁶/mol²), b (m³/mol)
        "CO2":(0.3658, 4.29e-5),
        "H2O":(0.5536, 3.05e-5),
        "He": (0.00346, 2.38e-5),
    }

    def __init__(self, gas: str = "N2"):
        if gas not in self.CONSTANTES:
            raise ValueError(f"Gas desconocido. Opciones: {list(self.CONSTANTES)}")
        self.gas = gas
        self.a, self.b = self.CONSTANTES[gas]

    @property
    def nombre(self) -> str:
        return f"Van der Waals ({self.gas})"

    def presion(self, V: float, T: float, n: float) -> float:
        return (n * self.R * T / (V - n * self.b)
                - self.a * n**2 / V**2)

    def descripcion(self) -> str:
        return (f"Van der Waals ({self.gas}): a={self.a:.4f}, b={self.b:.2e}. "
                "Corrige volumen excluido (b) y atracción molecular (a). "
                "Mejor que el gas ideal a presiones moderadas.")

    def temperatura_boyle(self) -> float:
        """T_B = a / (R·b) — temperatura de Boyle (comportamiento ideal)."""
        return self.a / (self.R * self.b)


# ---------------------------------------------------------------------------
# Implementación 3: Virial (segundo coeficiente)
# ---------------------------------------------------------------------------

class Virial(EcuacionEstado):
    """PV/(nRT) = 1 + B(T)·(n/V) — expansión virial de segundo orden."""

    # Segundo coeficiente virial aproximado B(T) = b - a/(RT)
    def __init__(self, a: float = 0.1370, b: float = 3.87e-5):
        self.a = a
        self.b = b

    @property
    def nombre(self) -> str:
        return "Virial (2.º orden)"

    def coeficiente_B(self, T: float) -> float:
        """B(T) = b − a/(RT) — segundo coeficiente virial (m³/mol)."""
        return self.b - self.a / (self.R * T)

    def presion(self, V: float, T: float, n: float) -> float:
        B = self.coeficiente_B(T)
        return n * self.R * T / V * (1 + B * n / V)

    def descripcion(self) -> str:
        return ("Virial (2.º orden): expansión en potencias de densidad. "
                "Preciso a densidades moderadas; el coeficiente B "
                "captura las desviaciones del gas ideal.")


# ---------------------------------------------------------------------------
# Función que trabaja con cualquier EcuacionEstado
# ---------------------------------------------------------------------------

def tabla_pV(modelo: EcuacionEstado, T: float, n: float,
             volumenes: list[float]) -> None:
    """Imprime P, Z para distintos volúmenes."""
    print(f"\n  [{modelo.nombre}]  T={T} K, n={n} mol")
    print(f"  {'V (L)':>8}  {'P (kPa)':>10}  {'Z':>8}")
    print("  " + "-" * 30)
    for V in volumenes:
        V_m3 = V * 1e-3   # L → m³
        P    = modelo.presion(V_m3, T, n)
        Z    = modelo.factor_compresibilidad(V_m3, T, n)
        print(f"  {V:>8.1f}  {P/1000:>10.3f}  {Z:>8.5f}")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ECUACIONES DE ESTADO — abstracción en acción")
    print("=" * 60)

    modelos: list[EcuacionEstado] = [
        GasIdeal(),
        VanDerWaals("CO2"),
        Virial(a=0.3658, b=4.29e-5),
    ]

    for m in modelos:
        print(f"\n{m}")
        print(f"  {m.descripcion()}")

    # Comparar P a T = 300 K, n = 1 mol, distintos volúmenes (litros)
    T  = 300.0   # K
    n  = 1.0     # mol
    Vs = [1.0, 2.0, 5.0, 10.0, 50.0]   # L

    print("\n--- Comparativa P(V) a T=300 K, n=1 mol ---")
    for modelo in modelos:
        tabla_pV(modelo, T, n, Vs)

    # Factor de compresibilidad a alta presión (V pequeño)
    V_peq = 0.5e-3   # 0.5 L en m³
    print("\n--- Factor Z a V=0.5 L (alta presión) ---")
    for modelo in modelos:
        Z = modelo.factor_compresibilidad(V_peq, T, n)
        P = modelo.presion(V_peq, T, n)
        print(f"  {modelo.nombre:30s}  P={P/1e6:.3f} MPa,  Z={Z:.5f}")

    # Demostración: no se puede instanciar EcuacionEstado directamente
    print("\n--- Intentar instanciar clase abstracta ---")
    try:
        EcuacionEstado()
    except TypeError as e:
        print(f"  Error capturado: {e}")
