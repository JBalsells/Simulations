import math


class Fuerza:

    def calcular(self) -> float:
        raise NotImplementedError(f"{self.__class__.__name__} debe implementar calcular()")

    def descripcion(self) -> str:
        return f"{self.__class__.__name__}: {self.calcular():.4f} N"

    def __abs__(self) -> float:
        return abs(self.calcular())

    def __add__(self, otra: "Fuerza") -> float:
        return self.calcular() + otra.calcular()

    def __sub__(self, otra: "Fuerza") -> float:
        return self.calcular() - otra.calcular()

    def __mul__(self, escalar: float) -> float:
        return self.calcular() * escalar

    def __rmul__(self, escalar: float) -> float:
        return self.__mul__(escalar)

    def __eq__(self, otra: "Fuerza") -> bool:
        return math.isclose(self.calcular(), otra.calcular(), abs_tol=1e-6)

    def __lt__(self, otra: "Fuerza") -> bool:
        return self.calcular() < otra.calcular()

    def __gt__(self, otra: "Fuerza") -> bool:
        return self.calcular() > otra.calcular()

    def __le__(self, otra: "Fuerza") -> bool:
        return self.calcular() <= otra.calcular()

    def __ge__(self, otra: "Fuerza") -> bool:
        return self.calcular() >= otra.calcular()

    def __str__(self) -> str:
        return self.descripcion()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} | {self.calcular():.4f} N>"


class FuerzaPeso(Fuerza):

    G_TIERRA = 9.8
    G_LUNA   = 1.62
    G_MARTE  = 3.72

    def __init__(self, masa: float, g: float = 9.8):
        self.masa = masa
        self.g = g

    def calcular(self) -> float:
        return self.masa * self.g

    def descripcion(self) -> str:
        return (f"FuerzaPeso: masa={self.masa} kg  g={self.g} m/s^2  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaResorte(Fuerza):

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

    MADERA_MADERA = 0.20
    GOMA_ASFALTO  = 0.70
    HIELO_HIELO   = 0.03
    ACERO_ACERO   = 0.15

    def __init__(self, mu: float, normal: float):
        self.mu = mu
        self.normal = normal

    def calcular(self) -> float:
        return self.mu * self.normal

    def descripcion(self) -> str:
        return (f"FuerzaRozamiento: mu={self.mu}  N={self.normal:.2f} N  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaCoulomb(Fuerza):

    K_E = 8.9875e9

    def __init__(self, q1: float, q2: float, r: float):
        if r <= 0:
            raise ValueError("La distancia r debe ser mayor que cero.")
        self.q1 = q1
        self.q2 = q2
        self.r = r

    def calcular(self) -> float:
        return self.K_E * abs(self.q1 * self.q2) / self.r**2

    def es_atractiva(self) -> bool:
        return self.q1 * self.q2 < 0

    def descripcion(self) -> str:
        tipo = "ATRACTIVA" if self.es_atractiva() else "REPULSIVA"
        return (f"FuerzaCoulomb [{tipo}]: q1={self.q1} C  q2={self.q2} C  "
                f"r={self.r} m  -> F = {self.calcular():.4e} N")


class FuerzaCentripeta(Fuerza):

    def __init__(self, masa: float, v: float, r: float):
        if r <= 0:
            raise ValueError("El radio r debe ser mayor que cero.")
        self.masa = masa
        self.v = v
        self.r = r

    def calcular(self) -> float:
        return self.masa * self.v**2 / self.r

    def aceleracion_centripeta(self) -> float:
        return self.v**2 / self.r

    def descripcion(self) -> str:
        return (f"FuerzaCentripeta: m={self.masa} kg  v={self.v} m/s  r={self.r} m  "
                f"-> F = {self.calcular():.4f} N  (a_c = {self.aceleracion_centripeta():.4f} m/s^2)")


class SistemaFuerzas:

    def __init__(self, nombre: str = "Sistema"):
        self.nombre = nombre
        self._fuerzas: list[Fuerza] = []

    def agregar(self, fuerza: Fuerza) -> "SistemaFuerzas":
        self._fuerzas.append(fuerza)
        return self

    def fuerza_neta(self) -> float:
        return sum(f.calcular() for f in self._fuerzas)

    def fuerza_maxima(self) -> Fuerza:
        return max(self._fuerzas, key=lambda f: f.calcular())

    def fuerza_minima(self) -> Fuerza:
        return min(self._fuerzas, key=lambda f: f.calcular())

    def ordenar_por_magnitud(self) -> list[Fuerza]:
        return sorted(self._fuerzas)

    def esta_en_equilibrio(self, tolerancia: float = 1e-4) -> bool:
        return abs(self.fuerza_neta()) < tolerancia

    def informe(self):
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


if __name__ == "__main__":

    peso       = FuerzaPeso(masa=10)
    resorte    = FuerzaResorte(k=200, x=0.5)
    rozamiento = FuerzaRozamiento(mu=0.3, normal=98)
    electrica  = FuerzaCoulomb(q1=2e-6, q2=-3e-6, r=0.05)
    centripeta = FuerzaCentripeta(masa=5, v=10, r=2)

    fuerzas = [peso, resorte, rozamiento, electrica, centripeta]

    print("=" * 60)
    print("  CALCULO POLIMORFICO DE FUERZAS")
    print("=" * 60)
    for f in fuerzas:
        print(f"  {f}")

    print("\n" + "=" * 60)
    print("  SOBRECARGA DE OPERADORES")
    print("=" * 60)

    print(f"\n  abs(peso)                = {abs(peso):.4f} N")
    print(f"  peso + resorte           = {peso + resorte:.4f} N")
    print(f"  resorte - rozamiento     = {resorte - rozamiento:.4f} N")
    print(f"  centripeta * 2           = {centripeta * 2:.4f} N")
    print(f"  3 * rozamiento           = {3 * rozamiento:.4f} N")
    print(f"  peso == resorte?         {peso == resorte}")
    print(f"  rozamiento < centripeta? {rozamiento < centripeta}")
    print(f"  centripeta > peso?       {centripeta > peso}")

    peso_tierra = FuerzaPeso(masa=70, g=FuerzaPeso.G_TIERRA)
    peso_luna   = FuerzaPeso(masa=70, g=FuerzaPeso.G_LUNA)
    peso_marte  = FuerzaPeso(masa=70, g=FuerzaPeso.G_MARTE)

    print(f"\n  Peso 70 kg en la Tierra : {abs(peso_tierra):.2f} N")
    print(f"  Peso 70 kg en la Luna   : {abs(peso_luna):.2f} N")
    print(f"  Peso 70 kg en Marte     : {abs(peso_marte):.2f} N")
    print(f"  Tierra > Luna?          : {peso_tierra > peso_luna}")

    planetas = [peso_marte, peso_tierra, peso_luna]
    print(f"\n  Fuerzas ordenadas de menor a mayor:")
    for f in sorted(planetas):
        print(f"    {f.calcular():.2f} N  (g={f.g})")

    masa   = 5
    angulo = 30
    componente_paralela = FuerzaPeso(masa=masa * math.sin(math.radians(angulo)))
    normal_rampa        = FuerzaPeso(masa=masa * math.cos(math.radians(angulo)))
    roza_rampa          = FuerzaRozamiento(mu=0.25, normal=normal_rampa.calcular())

    sistema_rampa = SistemaFuerzas("Objeto en rampa inclinada 30 deg")
    sistema_rampa.agregar(componente_paralela)
    sistema_rampa.agregar(roza_rampa)
    sistema_rampa.informe()

    aceleracion = sistema_rampa.fuerza_neta() / masa
    print(f"  Aceleracion neta: {aceleracion:.4f} m/s^2")

    resorte_b = FuerzaResorte(k=500, x=0.2)
    aplicada  = FuerzaPeso(masa=10.204, g=9.8)

    sistema_resorte = SistemaFuerzas("Resorte en equilibrio")
    sistema_resorte.agregar(resorte_b)
    sistema_resorte.agregar(aplicada)
    sistema_resorte.informe()

    sistema_general = SistemaFuerzas("Sistema general - comparacion de fuerzas")
    for f in fuerzas:
        sistema_general.agregar(f)
    sistema_general.informe()

    print("\n  Fuerzas ordenadas de menor a mayor magnitud:")
    for f in sistema_general.ordenar_por_magnitud():
        print(f"    {f.__class__.__name__:<22} {f.calcular():.4e} N")
