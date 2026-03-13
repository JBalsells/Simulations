import math
from abc import ABC, abstractmethod


class Figura(ABC):

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimetro(self) -> float:
        pass

    def describir(self):
        nombre = self.__class__.__name__
        print(f"[{nombre}]  Area = {self.area():.4f}  |  Perimetro = {self.perimetro():.4f}")
        print(f"  {self}")


class Circulo(Figura):
    def __init__(self, radio: float):
        self.radio = radio

    def area(self) -> float:
        return math.pi * self.radio ** 2

    def perimetro(self) -> float:
        return 2 * math.pi * self.radio

    def __str__(self) -> str:
        return f"Circulo de radio {self.radio} cm"


class Rectangulo(Figura):
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return self.base * self.altura

    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

    def __str__(self) -> str:
        return f"Rectangulo de {self.base} x {self.altura} cm"


class TrianguloRectangulo(Figura):
    def __init__(self, cateto_a: float, cateto_b: float):
        self.cateto_a = cateto_a
        self.cateto_b = cateto_b

    def hipotenusa(self) -> float:
        return math.sqrt(self.cateto_a**2 + self.cateto_b**2)

    def area(self) -> float:
        return (self.cateto_a * self.cateto_b) / 2

    def perimetro(self) -> float:
        return self.cateto_a + self.cateto_b + self.hipotenusa()

    def __str__(self) -> str:
        return (f"Triangulo rectangulo: catetos={self.cateto_a},{self.cateto_b} "
                f"| hipotenusa={self.hipotenusa():.4f} cm")


class TrianguloEquilatero(Figura):
    def __init__(self, lado: float):
        self.lado = lado

    def area(self) -> float:
        return (math.sqrt(3) / 4) * self.lado ** 2

    def perimetro(self) -> float:
        return 3 * self.lado

    def __str__(self) -> str:
        return f"Triangulo equilatero de lado {self.lado} cm"

if __name__ == "__main__":
    figuras = [
        Circulo(radio=5),
        Rectangulo(base=4, altura=7),
        TrianguloRectangulo(cateto_a=3, cateto_b=4),
        TrianguloEquilatero(lado=6),
    ]

    print("=" * 60)
    print("   CALCULO DE FIGURAS GEOMETRICAS (Polimorfismo)")
    print("=" * 60)

    for figura in figuras:   # polimorfismo: mismo bucle, distintos objetos
        figura.describir()
        print()

    print("=" * 60)
    print("Resultados:")
    print("  Circulo(r=5)            -> Area=78.5398  Perim=31.4159")
    print("  Rectangulo(4x7)         -> Area=28.0000  Perim=22.0000")
    print("  TrianguloRectangulo(3,4)-> Area=6.0000   Perim=12.0000")
    print("  TrianguloEquilatero(6)  -> Area=15.5885  Perim=18.0000")
