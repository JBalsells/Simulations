"""
Composición — Ejemplo 2: Sistema óptico (telescopio)
=====================================================
Un telescopio está hecho de sus partes: objetivo, ocular y montura.
No tiene sentido hablar del "objetivo" sin el telescopio; es una parte
que el telescopio crea, posee y usa. Eso es composición.

    Telescopio ──► Objetivo    (lente/espejo primario)
               ──► Ocular      (lente eyepiece)
               ──► Montura     (soporte mecánico)

Fórmulas que usamos:
  Aumento angular  : M = f_obj / f_oc
  Límite difracción: θ = 1.22 · λ / D  (rad) — criterio de Rayleigh
  Magnitud límite  : m_lim ≈ 2.1 + 5·log10(D·1000)  (D en m)

Para practicar:
1. Agrega un FiltroSolar que reduzca la apertura efectiva.
2. Implementa la potencia captadora relativa al ojo (pupila ~7 mm): P = (D/0.007)².
3. ¿Qué pasa con el aumento si el ocular tiene f=0?
"""

import math


# estas clases no se usan solas, el telescopio las crea internamente

class Objetivo:
    """Lente o espejo primario que colecta la luz."""

    def __init__(self, diametro: float, focal: float, tipo: str = "refractor"):
        self.diametro = diametro   # m — apertura
        self.focal    = focal      # m — distancia focal
        self.tipo     = tipo       # "refractor" | "reflector" | "catadióptrico"

    @property
    def razon_focal(self) -> float:
        """f/ = F / D."""
        return self.focal / self.diametro

    def area_colectora(self) -> float:
        """Área efectiva de captación de luz (m²)."""
        return math.pi * (self.diametro / 2)**2

    def __repr__(self):
        return (f"Objetivo({self.tipo}, D={self.diametro*100:.1f} cm, "
                f"f={self.focal*100:.1f} cm, f/{self.razon_focal:.1f})")


class Ocular:
    """Lente ocular (eyepiece) donde el observador pone el ojo."""

    def __init__(self, focal: float, campo_aparente: float = 52.0):
        self.focal          = focal           # m
        self.campo_aparente = campo_aparente  # grados

    def __repr__(self):
        return (f"Ocular(f={self.focal*1000:.1f} mm, "
                f"campo={self.campo_aparente}°)")


class Montura:
    """Soporte mecánico del telescopio."""

    TIPOS = {"azimutal", "ecuatorial", "dobsoniana", "goto"}

    def __init__(self, tipo: str, carga_max_kg: float):
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo desconocido. Opciones: {self.TIPOS}")
        self.tipo          = tipo
        self.carga_max_kg  = carga_max_kg

    def soporta(self, peso_tubo_kg: float) -> bool:
        return peso_tubo_kg <= self.carga_max_kg

    def __repr__(self):
        return f"Montura({self.tipo}, max={self.carga_max_kg} kg)"


# el telescopio crea y controla su objetivo, ocular y montura

class Telescopio:
    """Instrumento óptico compuesto por objetivo, ocular y montura."""

    LONGITUD_ONDA_REF = 550e-9  # m — verde (centro del espectro visible)

    def __init__(self, nombre: str,
                 diametro_obj: float, focal_obj: float, tipo_obj: str,
                 focal_oc: float,
                 tipo_montura: str, carga_max_kg: float):
        self.nombre = nombre
        # Composición: el telescopio crea sus propias partes
        self._objetivo = Objetivo(diametro_obj, focal_obj, tipo_obj)
        self._ocular   = Ocular(focal_oc)
        self._montura  = Montura(tipo_montura, carga_max_kg)

    # óptica calculada a partir del objetivo y el ocular

    @property
    def aumento(self) -> float:
        """M = F_obj / F_oc."""
        return self._objetivo.focal / self._ocular.focal

    def cambiar_ocular(self, nueva_focal: float) -> None:
        """Cambia el ocular (única pieza intercambiable en el modelo)."""
        self._ocular = Ocular(nueva_focal)

    def limite_difraccion(self, longitud_onda: float = None) -> float:
        """θ_min = 1.22 λ / D  (radianes) — criterio de Rayleigh."""
        lda = longitud_onda or self.LONGITUD_ONDA_REF
        return 1.22 * lda / self._objetivo.diametro

    def limite_difraccion_arcsec(self) -> float:
        """Límite de resolución en segundos de arco."""
        return math.degrees(self.limite_difraccion()) * 3600

    def campo_real(self) -> float:
        """Campo de visión real (grados) = campo_aparente / aumento."""
        return self._ocular.campo_aparente / self.aumento

    def magnitud_limite(self) -> float:
        """Magnitud estelar límite ≈ 2.1 + 5·log10(D·1000)."""
        D_mm = self._objetivo.diametro * 1000
        return 2.1 + 5 * math.log10(D_mm)

    def potencia_captadora(self, pupila_m: float = 7e-3) -> float:
        """Veces más luz que el ojo desnudo."""
        return (self._objetivo.diametro / pupila_m)**2

    # ficha técnica completa

    def ficha_tecnica(self) -> str:
        lineas = [
            f"Telescopio: {self.nombre}",
            f"  {self._objetivo}",
            f"  {self._ocular}",
            f"  {self._montura}",
            f"  Aumento         : {self.aumento:.1f}×",
            f"  Límite difrac.  : {self.limite_difraccion_arcsec():.2f} \"",
            f"  Campo real      : {self.campo_real():.2f}°",
            f"  Magnitud límite : {self.magnitud_limite():.1f}",
            f"  Captadora (ojo) : {self.potencia_captadora():.0f}×",
        ]
        return "\n".join(lineas)

    def __repr__(self):
        return (f"Telescopio('{self.nombre}', "
                f"D={self._objetivo.diametro*100:.0f} cm, "
                f"M={self.aumento:.0f}×)")


# --- demo ---

if __name__ == "__main__":
    print("=" * 60)
    print("SISTEMA ÓPTICO — composición en un telescopio")
    print("=" * 60)

    # Telescopio refractor pequeño (aficionado)
    refractor = Telescopio(
        nombre="Refractor 80/900",
        diametro_obj=0.080, focal_obj=0.900, tipo_obj="refractor",
        focal_oc=0.025,
        tipo_montura="ecuatorial", carga_max_kg=5.0,
    )

    # Gran telescopio reflector (observatorio)
    reflector = Telescopio(
        nombre="Dobson 400/1800",
        diametro_obj=0.400, focal_obj=1.800, tipo_obj="reflector",
        focal_oc=0.020,
        tipo_montura="dobsoniana", carga_max_kg=40.0,
    )

    for telescopio in [refractor, reflector]:
        print()
        print(telescopio.ficha_tecnica())

    # Cambiar ocular y recalcular
    print("\n--- Cambio de ocular en el Dobson (f=10 mm) ---")
    reflector.cambiar_ocular(0.010)
    print(f"  Nuevo aumento   : {reflector.aumento:.0f}×")
    print(f"  Nuevo campo real: {reflector.campo_real():.3f}°")

    # Comparar resolución angular (luna a 384 400 km)
    d_luna = 384_400e3  # m
    print("\n--- Detalle mínimo separable en la Luna ---")
    for t in [refractor, reflector]:
        theta = t.limite_difraccion()     # rad
        detalle = theta * d_luna / 1000   # km
        print(f"  {t.nombre:20s} → {detalle:.1f} km")
