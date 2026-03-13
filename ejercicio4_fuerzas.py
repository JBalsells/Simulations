"""
EJERCICIO 4 - Sistema de Fuerzas con Polimorfismo y Sobrecarga de Metodos
==========================================================================
Tema: Polimorfismo, herencia, sobrecarga de operadores y metodos especiales
Nivel: Avanzado

Conceptos demostrados:
    - Polimorfismo: calcular() tiene distinta logica en cada tipo de fuerza
    - Sobrecarga de operadores: +, -, *, ==, <, >, abs()
    - Herencia: todos los tipos de fuerza comparten la misma interfaz
    - Clase contenedora SistemaFuerzas que opera sobre cualquier tipo

Tipos de fuerza implementados:
    - FuerzaPeso        : F = m * g
    - FuerzaResorte     : F = -k * x          (Ley de Hooke)
    - FuerzaRozamiento  : F = mu * N          (rozamiento cinetico)
    - FuerzaCoulomb     : F = k * q1*q2 / r^2 (ley de Coulomb)
    - FuerzaCentripeta  : F = m * v^2 / r

Operadores sobrecargados en la clase base Fuerza:
    +   suma de magnitudes (composicion de fuerzas colineales)
    -   diferencia de magnitudes
    *   multiplicacion por escalar (amplificar/reducir una fuerza)
    ==  dos fuerzas son iguales si tienen la misma magnitud
    <   comparacion de magnitudes
    >   comparacion de magnitudes
    abs() retorna la magnitud absoluta
    str() representacion legible
"""

import math


# =========================================================================== #
#  CLASE BASE
# =========================================================================== #

class Fuerza:
    """
    Clase base abstracta para todas las fuerzas fisicas.
    Define la interfaz comun y los operadores sobrecargados.
    """

    def calcular(self) -> float:
        """
        Calcula y retorna la magnitud de la fuerza en Newtons.
        Cada subclase implementa su propia formula (polimorfismo).
        """
        raise NotImplementedError(f"{self.__class__.__name__} debe implementar calcular()")

    def descripcion(self) -> str:
        """Retorna una descripcion fisica de la fuerza (override opcional)."""
        return f"{self.__class__.__name__}: {self.calcular():.4f} N"

    # ----------------------------------------------------------------------- #
    #  SOBRECARGA DE OPERADORES
    # ----------------------------------------------------------------------- #

    def __abs__(self) -> float:
        """abs(f) -> magnitud en Newtons. Ejemplo: abs(FuerzaPeso(10))"""
        return abs(self.calcular())

    def __add__(self, otra: "Fuerza") -> float:
        """
        Suma de fuerzas colineales (mismo eje).
        Retorna la magnitud resultante (float).
        Ejemplo: peso + normal -> fuerza neta vertical
        """
        return self.calcular() + otra.calcular()

    def __sub__(self, otra: "Fuerza") -> float:
        """Diferencia entre fuerzas. Util para calcular fuerza neta."""
        return self.calcular() - otra.calcular()

    def __mul__(self, escalar: float) -> float:
        """
        Escala la magnitud de la fuerza.
        Ejemplo: fuerza * 2  -> doble de fuerza
        """
        return self.calcular() * escalar

    def __rmul__(self, escalar: float) -> float:
        """Permite escribir: 3 * fuerza"""
        return self.__mul__(escalar)

    def __eq__(self, otra: "Fuerza") -> bool:
        """Dos fuerzas son iguales si tienen la misma magnitud (tolerancia 1e-6 N)."""
        return math.isclose(self.calcular(), otra.calcular(), abs_tol=1e-6)

    def __lt__(self, otra: "Fuerza") -> bool:
        """f1 < f2 si la magnitud de f1 es menor."""
        return self.calcular() < otra.calcular()

    def __gt__(self, otra: "Fuerza") -> bool:
        """f1 > f2 si la magnitud de f1 es mayor."""
        return self.calcular() > otra.calcular()

    def __le__(self, otra: "Fuerza") -> bool:
        return self.calcular() <= otra.calcular()

    def __ge__(self, otra: "Fuerza") -> bool:
        return self.calcular() >= otra.calcular()

    def __str__(self) -> str:
        return self.descripcion()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} | {self.calcular():.4f} N>"


# =========================================================================== #
#  SUBCLASES — una por cada ley fisica
# =========================================================================== #

class FuerzaPeso(Fuerza):
    """
    Fuerza gravitacional terrestre sobre un objeto.
    Formula: F = m * g
    Parametros:
        masa  : masa del objeto en kg
        g     : aceleracion gravitacional (por defecto 9.8 m/s^2)
    """

    G_TIERRA = 9.8    # m/s^2
    G_LUNA   = 1.62   # m/s^2
    G_MARTE  = 3.72   # m/s^2

    def __init__(self, masa: float, g: float = 9.8):
        self.masa = masa
        self.g = g

    def calcular(self) -> float:
        return self.masa * self.g

    def descripcion(self) -> str:
        return (f"FuerzaPeso: masa={self.masa} kg  g={self.g} m/s^2  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaResorte(Fuerza):
    """
    Fuerza elastica segun la Ley de Hooke.
    Formula: F = k * |x|
    (El signo negativo indica restauracion; aqui se retorna la magnitud)
    Parametros:
        k : constante del resorte en N/m
        x : deformacion respecto al equilibrio en metros (+ estiramiento, - compresion)
    """

    def __init__(self, k: float, x: float):
        self.k = k
        self.x = x

    def calcular(self) -> float:
        return self.k * abs(self.x)

    def es_estiramiento(self) -> bool:
        return self.x > 0

    def descripcion(self) -> str:
        tipo = "estiramiento" if self.es_estiramiento() else "compresion"
        return (f"FuerzaResorte: k={self.k} N/m  x={self.x} m  ({tipo})  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaRozamiento(Fuerza):
    """
    Fuerza de rozamiento cinetico.
    Formula: F = mu * N
    Parametros:
        mu     : coeficiente de rozamiento cinetico (adimensional)
        normal : fuerza normal en N (generalmente el peso del objeto)
    """

    # Coeficientes de rozamiento tipicos (mu cinetico)
    MADERA_MADERA   = 0.20
    GOMA_ASFALTO    = 0.70
    HIELO_HIELO     = 0.03
    ACERO_ACERO     = 0.15

    def __init__(self, mu: float, normal: float):
        self.mu = mu
        self.normal = normal

    def calcular(self) -> float:
        return self.mu * self.normal

    def descripcion(self) -> str:
        return (f"FuerzaRozamiento: mu={self.mu}  N={self.normal:.2f} N  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaCoulomb(Fuerza):
    """
    Fuerza electrica entre dos cargas puntuales (Ley de Coulomb).
    Formula: F = k_e * |q1 * q2| / r^2
    Parametros:
        q1, q2 : cargas en Coulombs (pueden ser negativas)
        r      : distancia entre las cargas en metros
    """

    K_E = 8.9875e9   # constante de Coulomb en N*m^2/C^2

    def __init__(self, q1: float, q2: float, r: float):
        if r <= 0:
            raise ValueError("La distancia r debe ser mayor que cero.")
        self.q1 = q1
        self.q2 = q2
        self.r = r

    def calcular(self) -> float:
        return self.K_E * abs(self.q1 * self.q2) / self.r**2

    def es_atractiva(self) -> bool:
        """La fuerza es atractiva si las cargas tienen signos opuestos."""
        return self.q1 * self.q2 < 0

    def descripcion(self) -> str:
        tipo = "ATRACTIVA" if self.es_atractiva() else "REPULSIVA"
        return (f"FuerzaCoulomb [{tipo}]: q1={self.q1} C  q2={self.q2} C  "
                f"r={self.r} m  -> F = {self.calcular():.4e} N")


class FuerzaCentripeta(Fuerza):
    """
    Fuerza centripeta en movimiento circular uniforme.
    Formula: F = m * v^2 / r
    Parametros:
        masa : masa del objeto en kg
        v    : velocidad tangencial en m/s
        r    : radio de la trayectoria circular en metros
    """

    def __init__(self, masa: float, v: float, r: float):
        if r <= 0:
            raise ValueError("El radio r debe ser mayor que cero.")
        self.masa = masa
        self.v = v
        self.r = r

    def calcular(self) -> float:
        return self.masa * self.v**2 / self.r

    def aceleracion_centripeta(self) -> float:
        """a_c = v^2 / r"""
        return self.v**2 / self.r

    def descripcion(self) -> str:
        return (f"FuerzaCentripeta: m={self.masa} kg  v={self.v} m/s  r={self.r} m  "
                f"-> F = {self.calcular():.4f} N  (a_c = {self.aceleracion_centripeta():.4f} m/s^2)")


# =========================================================================== #
#  CLASE CONTENEDORA
# =========================================================================== #

class SistemaFuerzas:
    """
    Agrupa multiples fuerzas y calcula propiedades del sistema.
    Demuestra polimorfismo: opera sobre cualquier subclase de Fuerza
    sin conocer su tipo concreto.
    """

    def __init__(self, nombre: str = "Sistema"):
        self.nombre = nombre
        self._fuerzas: list[Fuerza] = []

    def agregar(self, fuerza: Fuerza) -> "SistemaFuerzas":
        """Agrega una fuerza al sistema. Retorna self para encadenamiento."""
        self._fuerzas.append(fuerza)
        return self

    def fuerza_neta(self) -> float:
        """
        Suma algebraica de todas las fuerzas (asume fuerzas colineales).
        Polimorfismo: llama a calcular() sin importar el tipo de fuerza.
        """
        return sum(f.calcular() for f in self._fuerzas)

    def fuerza_maxima(self) -> Fuerza:
        """Retorna la fuerza de mayor magnitud usando el operador >."""
        return max(self._fuerzas, key=lambda f: f.calcular())

    def fuerza_minima(self) -> Fuerza:
        """Retorna la fuerza de menor magnitud usando el operador <."""
        return min(self._fuerzas, key=lambda f: f.calcular())

    def ordenar_por_magnitud(self) -> list[Fuerza]:
        """Lista de fuerzas ordenadas de menor a mayor usando comparadores."""
        return sorted(self._fuerzas)

    def esta_en_equilibrio(self, tolerancia: float = 1e-4) -> bool:
        """
        Un sistema esta en equilibrio si la fuerza neta es ~0.
        (Requiere que algunas fuerzas sean negativas / en sentido opuesto)
        """
        return abs(self.fuerza_neta()) < tolerancia

    def informe(self):
        """Imprime un resumen completo del sistema."""
        print(f"\n{'=' * 60}")
        print(f"  SISTEMA: {self.nombre}")
        print(f"{'=' * 60}")
        for i, f in enumerate(self._fuerzas, 1):
            print(f"  [{i}] {f}")
        print(f"{'-' * 60}")
        print(f"  Fuerza neta        : {self.fuerza_neta():.4f} N")
        print(f"  Fuerza maxima      : {self.fuerza_maxima().calcular():.4f} N  "
              f"({self.fuerza_maxima().__class__.__name__})")
        print(f"  Fuerza minima      : {self.fuerza_minima().calcular():.4f} N  "
              f"({self.fuerza_minima().__class__.__name__})")
        print(f"  En equilibrio?     : {self.esta_en_equilibrio()}")
        print(f"{'=' * 60}")


# =========================================================================== #
#  PROGRAMA PRINCIPAL
# =========================================================================== #

if __name__ == "__main__":

    # ----------------------------------------------------------------------- #
    # 1. CREACION DE FUERZAS (polimorfismo: misma interfaz, distintas formulas)
    # ----------------------------------------------------------------------- #
    peso        = FuerzaPeso(masa=10)                        # 98 N
    resorte     = FuerzaResorte(k=200, x=0.5)               # 100 N
    rozamiento  = FuerzaRozamiento(mu=0.3, normal=98)        # 29.4 N
    electrica   = FuerzaCoulomb(q1=2e-6, q2=-3e-6, r=0.05)  # atractiva
    centripeta  = FuerzaCentripeta(masa=5, v=10, r=2)        # 250 N

    fuerzas = [peso, resorte, rozamiento, electrica, centripeta]

    # ----------------------------------------------------------------------- #
    # 2. POLIMORFISMO: mismo metodo calcular() en todos los tipos
    # ----------------------------------------------------------------------- #
    print("=" * 60)
    print("  CALCULO POLIMORFICO DE FUERZAS")
    print("=" * 60)
    for f in fuerzas:
        print(f"  {f}")   # llama a __str__ -> descripcion() sobreescrito

    # ----------------------------------------------------------------------- #
    # 3. SOBRECARGA DE OPERADORES
    # ----------------------------------------------------------------------- #
    print("\n" + "=" * 60)
    print("  SOBRECARGA DE OPERADORES")
    print("=" * 60)

    print(f"\n  abs(peso)              = {abs(peso):.4f} N")
    print(f"  peso + resorte         = {peso + resorte:.4f} N")
    print(f"  resorte - rozamiento   = {resorte - rozamiento:.4f} N")
    print(f"  centripeta * 2         = {centripeta * 2:.4f} N")
    print(f"  3 * rozamiento         = {3 * rozamiento:.4f} N")
    print(f"  peso == resorte?       {peso == resorte}")
    print(f"  rozamiento < centripeta? {rozamiento < centripeta}")
    print(f"  centripeta > peso?     {centripeta > peso}")

    # Comparacion en diferentes planetas
    peso_tierra = FuerzaPeso(masa=70, g=FuerzaPeso.G_TIERRA)
    peso_luna   = FuerzaPeso(masa=70, g=FuerzaPeso.G_LUNA)
    peso_marte  = FuerzaPeso(masa=70, g=FuerzaPeso.G_MARTE)
    print(f"\n  Peso 70 kg en la Tierra : {abs(peso_tierra):.2f} N")
    print(f"  Peso 70 kg en la Luna   : {abs(peso_luna):.2f} N")
    print(f"  Peso 70 kg en Marte     : {abs(peso_marte):.2f} N")
    print(f"  Tierra > Luna?          : {peso_tierra > peso_luna}")

    # Ordenamiento usando los operadores de comparacion
    planetas = [peso_marte, peso_tierra, peso_luna]
    ordenados = sorted(planetas)
    print(f"\n  Fuerzas ordenadas de menor a mayor:")
    for f in ordenados:
        print(f"    {f.calcular():.2f} N  ({f.__class__.__name__} g={f.g})")

    # ----------------------------------------------------------------------- #
    # 4. SISTEMA DE FUERZAS (clase contenedora polimorfica)
    # ----------------------------------------------------------------------- #

    # Escenario A: objeto sobre una rampa (peso vs rozamiento)
    masa = 5       # kg
    angulo = 30    # grados
    peso_rampa = FuerzaPeso(masa=masa)
    componente_paralela  = FuerzaPeso(masa=masa * math.sin(math.radians(angulo)))
    normal_rampa         = FuerzaPeso(masa=masa * math.cos(math.radians(angulo)))
    roza_rampa           = FuerzaRozamiento(mu=0.25, normal=normal_rampa.calcular())

    sistema_rampa = SistemaFuerzas("Objeto en rampa inclinada 30 deg")
    sistema_rampa.agregar(componente_paralela)
    sistema_rampa.agregar(roza_rampa)
    sistema_rampa.informe()

    aceleracion = sistema_rampa.fuerza_neta() / masa
    print(f"  Aceleracion neta: {aceleracion:.4f} m/s^2 "
          f"({'baja' if aceleracion > 0 else 'no se mueve o sube'})")

    # Escenario B: resorte vs fuerza aplicada (equilibrio)
    resorte_b = FuerzaResorte(k=500, x=0.2)          # 100 N restauradora
    aplicada  = FuerzaPeso(masa=10.204, g=9.8)        # ~100 N aplicada

    sistema_resorte = SistemaFuerzas("Resorte en equilibrio")
    sistema_resorte.agregar(resorte_b)
    sistema_resorte.agregar(aplicada)
    sistema_resorte.informe()

    # Escenario C: sistema general con todas las fuerzas
    sistema_general = SistemaFuerzas("Sistema general - comparacion de fuerzas")
    for f in fuerzas:
        sistema_general.agregar(f)
    sistema_general.informe()

    print("\n  Fuerzas ordenadas de menor a mayor magnitud:")
    for f in sistema_general.ordenar_por_magnitud():
        print(f"    {f.__class__.__name__:<22} {f.calcular():.4e} N")
