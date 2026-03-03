"""
Polimorfismo — Ejemplo 1: Fuerzas físicas
==========================================
Conceptos OOP: polimorfismo, duck typing, lista de objetos
               heterogéneos tratados con la misma interfaz.

Idea central
------------
Distintos tipos de fuerza (gravedad, eléctrica, fricción, resorte)
comparten la interfaz:

    calcular(distancia_o_contexto)  → float  (N)
    descripcion()                   → str

Podemos meterlos en una lista y llamar al mismo método
sin saber de qué tipo concreto es cada objeto.

Tareas para el estudiante
-------------------------
1. Agrega una clase `FuerzaMagnética` con F = q·v·B·sin(θ).
2. Ordena la lista `fuerzas` por magnitud usando sorted()
   y un lambda. ¿Qué método usas como clave?
3. Implementa `__lt__` en la clase base para hacer los
   objetos comparables directamente.
"""


# ---------------------------------------------------------------------------
# Clase base (interfaz informal — duck typing)
# ---------------------------------------------------------------------------

class Fuerza:
    """Interfaz común para cualquier tipo de fuerza."""

    def calcular(self, param: float) -> float:
        """Devuelve la magnitud de la fuerza en Newtons."""
        raise NotImplementedError("Implementar en subclase")

    def descripcion(self) -> str:
        raise NotImplementedError("Implementar en subclase")

    def __repr__(self):
        return f"{self.__class__.__name__}()"


# ---------------------------------------------------------------------------
# Subclases concretas
# ---------------------------------------------------------------------------

class FuerzaGravitacional(Fuerza):
    """F = G · m₁ · m₂ / r²  — ley de gravitación de Newton."""

    G = 6.674e-11  # m³ kg⁻¹ s⁻²

    def __init__(self, masa1: float, masa2: float):
        self.masa1 = masa1  # kg
        self.masa2 = masa2  # kg

    def calcular(self, distancia: float) -> float:
        """param = distancia entre masas (m)."""
        return self.G * self.masa1 * self.masa2 / distancia**2

    def descripcion(self) -> str:
        return (f"Gravedad entre {self.masa1:.2e} kg y {self.masa2:.2e} kg"
                f" — siempre atractiva")


class FuerzaElectrica(Fuerza):
    """F = k · q₁ · q₂ / r²  — ley de Coulomb."""

    K = 8.988e9  # N·m²/C²

    def __init__(self, carga1: float, carga2: float):
        self.carga1 = carga1  # C
        self.carga2 = carga2  # C

    def calcular(self, distancia: float) -> float:
        """param = distancia entre cargas (m); negativo = atractiva."""
        return self.K * self.carga1 * self.carga2 / distancia**2

    def descripcion(self) -> str:
        tipo = "atractiva" if self.carga1 * self.carga2 < 0 else "repulsiva"
        return (f"Coulomb q₁={self.carga1:.2e} C, q₂={self.carga2:.2e} C"
                f" — {tipo}")


class FuerzaFriccion(Fuerza):
    """F_f = μ · N  — fricción cinética (no depende de la distancia)."""

    def __init__(self, coeficiente_mu: float, fuerza_normal: float):
        self.mu = coeficiente_mu
        self.N  = fuerza_normal  # N

    def calcular(self, velocidad: float = 1.0) -> float:
        """param = velocidad relativa (ignorada en el modelo clásico)."""
        return self.mu * self.N

    def descripcion(self) -> str:
        return (f"Fricción cinética μ={self.mu}, N={self.N} N"
                f" — se opone al movimiento")


class FuerzaResorte(Fuerza):
    """F = −k · x  — Ley de Hooke (tomamos el módulo)."""

    def __init__(self, constante_k: float):
        self.k = constante_k  # N/m

    def calcular(self, desplazamiento: float) -> float:
        """param = desplazamiento del equilibrio (m); devuelve módulo."""
        return abs(self.k * desplazamiento)

    def descripcion(self) -> str:
        return f"Resorte k={self.k} N/m — proporcional al desplazamiento"


# ---------------------------------------------------------------------------
# Función polimórfica: trabaja con cualquier Fuerza
# ---------------------------------------------------------------------------

def analizar_fuerza(fuerza: Fuerza, param: float) -> None:
    """Calcula y muestra la magnitud de cualquier fuerza."""
    magnitud = fuerza.calcular(param)
    print(f"  {fuerza.descripcion()}")
    print(f"    → F = {magnitud:.4e} N  (param={param})")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Parámetro de cada fuerza (distancia, desplazamiento, etc.)
    escenarios: list[tuple[Fuerza, float]] = [
        (FuerzaGravitacional(5.972e24, 70.0),      6.371e6),   # Tierra-persona
        (FuerzaElectrica(-1.602e-19, 1.602e-19),   5.29e-11),  # e⁻ — p⁺ en Bohr
        (FuerzaFriccion(0.3, 700.0),               2.0),       # bloque sobre piso
        (FuerzaResorte(200.0),                     0.05),      # resorte 5 cm
    ]

    print("=" * 60)
    print("ANÁLISIS DE FUERZAS — polimorfismo en acción")
    print("=" * 60)
    print()

    for fuerza, param in escenarios:
        analizar_fuerza(fuerza, param)
        print()

    # -- Polimorfismo: misma función, distintos tipos --
    print("--- Ordenando fuerzas por magnitud (mayor a menor) ---")
    fuerzas = [f for f, _ in escenarios]
    params  = [p for _, p in escenarios]

    magnitudes = [(f.calcular(p), f) for f, p in zip(fuerzas, params)]
    magnitudes.sort(key=lambda t: t[0], reverse=True)

    for mag, f in magnitudes:
        print(f"  {mag:.3e} N  ←  {f.__class__.__name__}")
