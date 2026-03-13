import math
from abc import ABC, abstractmethod


class Fuerza(ABC):

    @abstractmethod
    def calcular(self) -> float:
        pass

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

    @staticmethod
    def newtons_a_kg_fuerza(n: float) -> float:
        return n / 9.8

    @staticmethod
    def newtons_a_libras(n: float) -> float:
        return n * 0.2248

    @staticmethod
    def libras_a_newtons(lb: float) -> float:
        return lb / 0.2248


class FuerzaPeso(Fuerza):

    G_TIERRA = 9.8
    G_LUNA   = 1.62
    G_MARTE  = 3.72

    def __init__(self, masa: float, g: float = 9.8):
        self.masa = masa
        self.g = g

    @property
    def masa(self) -> float:
        return self._masa

    @masa.setter
    def masa(self, valor: float):
        if valor <= 0:
            raise ValueError(f"La masa debe ser positiva, se recibio {valor}")
        self._masa = valor

    @property
    def g(self) -> float:
        return self._g

    @g.setter
    def g(self, valor: float):
        if valor < 0:
            raise ValueError(f"La gravedad no puede ser negativa, se recibio {valor}")
        self._g = valor

    @classmethod
    def desde_gramos(cls, gramos: float, g: float = 9.8) -> "FuerzaPeso":
        return cls(masa=gramos / 1000, g=g)

    @classmethod
    def en_luna(cls, masa: float) -> "FuerzaPeso":
        return cls(masa=masa, g=cls.G_LUNA)

    @classmethod
    def en_marte(cls, masa: float) -> "FuerzaPeso":
        return cls(masa=masa, g=cls.G_MARTE)

    def calcular(self) -> float:
        return self._masa * self._g

    def descripcion(self) -> str:
        return (f"FuerzaPeso: masa={self._masa} kg  g={self._g} m/s^2  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaResorte(Fuerza):

    def __init__(self, k: float, x: float):
        self.k = k
        self.x = x

    @property
    def k(self) -> float:
        return self._k

    @k.setter
    def k(self, valor: float):
        if valor <= 0:
            raise ValueError(f"La constante del resorte debe ser positiva, se recibio {valor}")
        self._k = valor

    @property
    def energia_potencial(self) -> float:
        return 0.5 * self._k * self.x**2

    @classmethod
    def desde_masa_y_periodo(cls, masa: float, periodo: float) -> "FuerzaResorte":
        k = (2 * math.pi / periodo)**2 * masa
        return cls(k=k, x=0.1)

    def es_estiramiento(self) -> bool:
        return self.x > 0

    def calcular(self) -> float:
        return self._k * abs(self.x)

    def descripcion(self) -> str:
        tipo = "estiramiento" if self.es_estiramiento() else "compresion"
        return (f"FuerzaResorte: k={self._k} N/m  x={self.x} m  ({tipo})  "
                f"-> F = {self.calcular():.4f} N  Ep = {self.energia_potencial:.4f} J")


class FuerzaRozamiento(Fuerza):

    MATERIALES = {
        "madera_madera": 0.20,
        "goma_asfalto":  0.70,
        "hielo_hielo":   0.03,
        "acero_acero":   0.15,
    }

    def __init__(self, mu: float, normal: float):
        self.mu = mu
        self.normal = normal

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, valor: float):
        if not (0 <= valor <= 1):
            raise ValueError(f"El coeficiente mu debe estar entre 0 y 1, se recibio {valor}")
        self._mu = valor

    @property
    def normal(self) -> float:
        return self._normal

    @normal.setter
    def normal(self, valor: float):
        if valor < 0:
            raise ValueError(f"La fuerza normal no puede ser negativa, se recibio {valor}")
        self._normal = valor

    @classmethod
    def desde_material(cls, material: str, normal: float) -> "FuerzaRozamiento":
        if material not in cls.MATERIALES:
            raise ValueError(f"Material desconocido. Opciones: {list(cls.MATERIALES.keys())}")
        return cls(mu=cls.MATERIALES[material], normal=normal)

    def calcular(self) -> float:
        return self._mu * self._normal

    def descripcion(self) -> str:
        return (f"FuerzaRozamiento: mu={self._mu}  N={self._normal:.2f} N  "
                f"-> F = {self.calcular():.4f} N")


class FuerzaCoulomb(Fuerza):

    K_E = 8.9875e9

    def __init__(self, q1: float, q2: float, r: float):
        self.q1 = q1
        self.q2 = q2
        self.r = r

    @property
    def r(self) -> float:
        return self._r

    @r.setter
    def r(self, valor: float):
        if valor <= 0:
            raise ValueError(f"La distancia r debe ser mayor que cero, se recibio {valor}")
        self._r = valor

    @classmethod
    def desde_microcoulombs(cls, q1_uc: float, q2_uc: float, r: float) -> "FuerzaCoulomb":
        return cls(q1=q1_uc * 1e-6, q2=q2_uc * 1e-6, r=r)

    @staticmethod
    def campo_electrico(q: float, r: float) -> float:
        return FuerzaCoulomb.K_E * abs(q) / r**2

    def es_atractiva(self) -> bool:
        return self.q1 * self.q2 < 0

    def calcular(self) -> float:
        return self.K_E * abs(self.q1 * self.q2) / self._r**2

    def descripcion(self) -> str:
        tipo = "ATRACTIVA" if self.es_atractiva() else "REPULSIVA"
        return (f"FuerzaCoulomb [{tipo}]: q1={self.q1} C  q2={self.q2} C  "
                f"r={self._r} m  -> F = {self.calcular():.4e} N")


class FuerzaCentripeta(Fuerza):

    def __init__(self, masa: float, v: float, r: float):
        self.masa = masa
        self.v = v
        self.r = r

    @property
    def masa(self) -> float:
        return self._masa

    @masa.setter
    def masa(self, valor: float):
        if valor <= 0:
            raise ValueError(f"La masa debe ser positiva, se recibio {valor}")
        self._masa = valor

    @property
    def r(self) -> float:
        return self._r

    @r.setter
    def r(self, valor: float):
        if valor <= 0:
            raise ValueError(f"El radio debe ser positivo, se recibio {valor}")
        self._r = valor

    @classmethod
    def desde_rpm(cls, masa: float, rpm: float, r: float) -> "FuerzaCentripeta":
        v = (2 * math.pi * r * rpm) / 60
        return cls(masa=masa, v=v, r=r)

    def aceleracion_centripeta(self) -> float:
        return self.v**2 / self._r

    def calcular(self) -> float:
        return self._masa * self.v**2 / self._r

    def descripcion(self) -> str:
        return (f"FuerzaCentripeta: m={self._masa} kg  v={self.v} m/s  r={self._r} m  "
                f"-> F = {self.calcular():.4f} N  (a_c = {self.aceleracion_centripeta():.4f} m/s^2)")


class FuerzaElasticaAmortiguada(FuerzaResorte, FuerzaRozamiento):

    def __init__(self, k: float, x: float, mu: float, normal: float):
        FuerzaResorte.__init__(self, k=k, x=x)
        FuerzaRozamiento.__init__(self, mu=mu, normal=normal)

    def calcular(self) -> float:
        return FuerzaResorte.calcular(self) + FuerzaRozamiento.calcular(self)

    def descripcion(self) -> str:
        return (f"FuerzaElasticaAmortiguada: "
                f"F_resorte={FuerzaResorte.calcular(self):.4f} N  "
                f"F_rozamiento={FuerzaRozamiento.calcular(self):.4f} N  "
                f"-> F_total = {self.calcular():.4f} N")


class SistemaFuerzas:

    def __init__(self, nombre: str = "Sistema"):
        self.nombre = nombre
        self._fuerzas: list[Fuerza] = []

    def agregar(self, fuerza: Fuerza) -> "SistemaFuerzas":
        self._fuerzas.append(fuerza)
        return self

    def __iadd__(self, fuerza: Fuerza) -> "SistemaFuerzas":
        return self.agregar(fuerza)

    def __len__(self) -> int:
        return len(self._fuerzas)

    def __iter__(self):
        return iter(self._fuerzas)

    def __contains__(self, fuerza: Fuerza) -> bool:
        return fuerza in self._fuerzas

    def __getitem__(self, indice: int) -> Fuerza:
        return self._fuerzas[indice]

    def fuerza_neta(self) -> float:
        return sum(f.calcular() for f in self)

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
        print(f"  SISTEMA: {self.nombre}  ({len(self)} fuerzas)")
        print(f"{'=' * 60}")
        for i, f in enumerate(self, 1):
            print(f"  [{i}] {f}")
        print(f"{'-' * 60}")
        print(f"  Fuerza neta        : {self.fuerza_neta():.4f} N")
        print(f"  Fuerza maxima      : {self.fuerza_maxima().calcular():.4f} N  ({self.fuerza_maxima().__class__.__name__})")
        print(f"  Fuerza minima      : {self.fuerza_minima().calcular():.4f} N  ({self.fuerza_minima().__class__.__name__})")
        print(f"  En equilibrio?     : {self.esta_en_equilibrio()}")
        print(f"{'=' * 60}")


class Cuerpo:

    def __init__(self, nombre: str, masa: float):
        self.nombre = nombre
        self.masa = masa
        self.sistema = SistemaFuerzas(nombre)

    @property
    def masa(self) -> float:
        return self._masa

    @masa.setter
    def masa(self, valor: float):
        if valor <= 0:
            raise ValueError(f"La masa debe ser positiva, se recibio {valor}")
        self._masa = valor

    def aplicar(self, fuerza: Fuerza) -> "Cuerpo":
        self.sistema.agregar(fuerza)
        return self

    def aceleracion(self) -> float:
        return self.sistema.fuerza_neta() / self._masa

    def energia_cinetica(self, v: float) -> float:
        return 0.5 * self._masa * v**2

    def __str__(self) -> str:
        return (f"Cuerpo '{self.nombre}': masa={self._masa} kg  "
                f"F_neta={self.sistema.fuerza_neta():.4f} N  "
                f"a={self.aceleracion():.4f} m/s^2")


if __name__ == "__main__":

    peso        = FuerzaPeso(masa=10)
    resorte     = FuerzaResorte(k=200, x=0.5)
    rozamiento  = FuerzaRozamiento(mu=0.3, normal=98)
    electrica   = FuerzaCoulomb(q1=2e-6, q2=-3e-6, r=0.05)
    centripeta  = FuerzaCentripeta(masa=5, v=10, r=2)
    amortiguada = FuerzaElasticaAmortiguada(k=300, x=0.2, mu=0.1, normal=50)

    fuerzas = [peso, resorte, rozamiento, electrica, centripeta, amortiguada]

    print("=" * 60)
    print("  POLIMORFISMO + ABC - calcular() en cada tipo")
    print("=" * 60)
    for f in fuerzas:
        print(f"  {f}")

    print("\n" + "=" * 60)
    print("  CLASSMETHOD - constructores alternativos")
    print("=" * 60)
    print(f"  {FuerzaPeso.desde_gramos(500)}")
    print(f"  {FuerzaPeso.en_luna(70)}")
    print(f"  {FuerzaPeso.en_marte(70)}")
    print(f"  {FuerzaRozamiento.desde_material('goma_asfalto', 200)}")
    print(f"  {FuerzaCoulomb.desde_microcoulombs(2, -3, 0.05)}")
    print(f"  {FuerzaCentripeta.desde_rpm(masa=2, rpm=120, r=0.5)}")
    print(f"  {FuerzaResorte.desde_masa_y_periodo(masa=1, periodo=2)}")

    print("\n" + "=" * 60)
    print("  STATICMETHOD - utilidades sin instancia")
    print("=" * 60)
    print(f"  980 N = {Fuerza.newtons_a_kg_fuerza(980):.4f} kgf")
    print(f"  980 N = {Fuerza.newtons_a_libras(980):.4f} lb")
    print(f"  220 lb = {Fuerza.libras_a_newtons(220):.4f} N")
    print(f"  Campo electrico (q=1e-6 C, r=0.1 m) = {FuerzaCoulomb.campo_electrico(1e-6, 0.1):.4e} N/C")

    print("\n" + "=" * 60)
    print("  PROPERTY - validacion de atributos")
    print("=" * 60)
    r = FuerzaResorte(k=100, x=0.3)
    print(f"  Resorte inicial      : {r}")
    r.x = -0.5
    print(f"  Resorte comprimido   : {r}")
    r.k = 400
    print(f"  Resorte k modificado : {r}")
    try:
        r.k = -10
    except ValueError as e:
        print(f"  Error esperado       : {e}")
    try:
        FuerzaRozamiento(mu=1.5, normal=100)
    except ValueError as e:
        print(f"  Error esperado       : {e}")

    print("\n" + "=" * 60)
    print("  SOBRECARGA DE OPERADORES")
    print("=" * 60)
    print(f"  abs(peso)                = {abs(peso):.4f} N")
    print(f"  peso + resorte           = {peso + resorte:.4f} N")
    print(f"  resorte - rozamiento     = {resorte - rozamiento:.4f} N")
    print(f"  centripeta * 2           = {centripeta * 2:.4f} N")
    print(f"  3 * rozamiento           = {3 * rozamiento:.4f} N")
    print(f"  peso == resorte?         {peso == resorte}")
    print(f"  rozamiento < centripeta? {rozamiento < centripeta}")
    print(f"  centripeta > peso?       {centripeta > peso}")

    print("\n" + "=" * 60)
    print("  HERENCIA MULTIPLE - FuerzaElasticaAmortiguada")
    print("=" * 60)
    print(f"  MRO: {[c.__name__ for c in FuerzaElasticaAmortiguada.__mro__]}")
    print(f"  {amortiguada}")
    print(f"  F_resorte pura    : {FuerzaResorte.calcular(amortiguada):.4f} N")
    print(f"  F_rozamiento pura : {FuerzaRozamiento.calcular(amortiguada):.4f} N")

    print("\n" + "=" * 60)
    print("  PROTOCOLO CONTENEDOR - __iter__, __len__, __contains__, __getitem__, +=")
    print("=" * 60)
    sistema = SistemaFuerzas("Demo contenedor")
    sistema += peso
    sistema += resorte
    sistema += rozamiento

    print(f"  len(sistema)           = {len(sistema)}")
    print(f"  sistema[0]             = {sistema[0]}")
    print(f"  sistema[1]             = {sistema[1]}")
    print(f"  peso in sistema?       {peso in sistema}")
    print(f"  centripeta in sistema? {centripeta in sistema}")
    print("  Iteracion con for:")
    for f in sistema:
        print(f"    {f.__class__.__name__:<28} {f.calcular():.4f} N")
    sistema.informe()

    print("\n" + "=" * 60)
    print("  COMPOSICION - clase Cuerpo contiene SistemaFuerzas")
    print("=" * 60)

    bloque = Cuerpo(nombre="Bloque en rampa 30 deg", masa=5)
    bloque.aplicar(FuerzaPeso(masa=5 * math.sin(math.radians(30))))
    bloque.aplicar(FuerzaRozamiento.desde_material(
        "madera_madera",
        FuerzaPeso(masa=5 * math.cos(math.radians(30))).calcular()
    ))
    print(f"  {bloque}")
    bloque.sistema.informe()

    auto = Cuerpo(nombre="Auto en curva", masa=1200)
    auto.aplicar(FuerzaCentripeta(masa=1200, v=20, r=50))
    auto.aplicar(FuerzaRozamiento.desde_material(
        "goma_asfalto",
        FuerzaPeso(masa=1200).calcular()
    ))
    print(f"  {auto}")
    auto.sistema.informe()

    print("\n" + "=" * 60)
    print("  ORDENAMIENTO POLIMORFICO CON OPERADORES DE COMPARACION")
    print("=" * 60)
    sistema_general = SistemaFuerzas("Todas las fuerzas")
    for f in fuerzas:
        sistema_general.agregar(f)
    print("  Fuerzas ordenadas de menor a mayor magnitud:")
    for f in sistema_general.ordenar_por_magnitud():
        print(f"    {f.__class__.__name__:<30} {f.calcular():.4e} N")
