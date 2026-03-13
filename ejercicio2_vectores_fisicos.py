import math


class Vector2D:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self) -> str:
        signo = "+" if self.y >= 0 else "-"
        return f"({self.x}i {signo} {abs(self.y)}j)"

    def __add__(self, otro: "Vector2D") -> "Vector2D":
        """Suma componente a componente: (a,b) + (c,d) = (a+c, b+d)"""
        return Vector2D(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro: "Vector2D") -> "Vector2D":
        """Resta componente a componente: (a,b) - (c,d) = (a-c, b-d)"""
        return Vector2D(self.x - otro.x, self.y - otro.y)

    def __mul__(self, escalar: float) -> "Vector2D":
        """
        Multiplicacion por escalar: k * (a,b) = (k*a, k*b)
        Ejemplo: Vector2D(2,3) * 4  ->  Vector2D(8, 12)
        """
        return Vector2D(self.x * escalar, self.y * escalar)

    def __rmul__(self, escalar: float) -> "Vector2D":
        """Permite escribir: 4 * v  (ademas de v * 4)"""
        return self.__mul__(escalar)

    def __neg__(self) -> "Vector2D":
        """Negacion: -(a,b) = (-a,-b)"""
        return Vector2D(-self.x, -self.y)

    def __eq__(self, otro: "Vector2D") -> bool:
        """Igualdad entre vectores."""
        return self.x == otro.x and self.y == otro.y

    def magnitud(self) -> float:
        """Modulo o norma del vector: |v| = sqrt(x^2 + y^2)"""
        return math.sqrt(self.x**2 + self.y**2)

    def unitario(self) -> "Vector2D":
        """Vector unitario: v / |v|  (magnitud = 1, misma direccion)"""
        mag = self.magnitud()
        if mag == 0:
            raise ValueError("El vector nulo no tiene direccion unitaria.")
        return Vector2D(self.x / mag, self.y / mag)

    def producto_punto(self, otro: "Vector2D") -> float:
        """Producto escalar: v1 . v2 = x1*x2 + y1*y2"""
        return self.x * otro.x + self.y * otro.y

    def es_ortogonal(self, otro: "Vector2D") -> bool:
        """Dos vectores son ortogonales si su producto punto es 0."""
        return math.isclose(self.producto_punto(otro), 0, abs_tol=1e-9)

    def angulo_entre(self, otro: "Vector2D") -> float:
        """
        Angulo en grados entre dos vectores.
        cos(theta) = (v1 . v2) / (|v1| * |v2|)
        Se usa clip para evitar errores numericos en arccos (dominio [-1, 1]).
        """
        cos_theta = self.producto_punto(otro) / (self.magnitud() * otro.magnitud())
        cos_theta = max(-1.0, min(1.0, cos_theta))   # clip por seguridad numerica
        return math.degrees(math.acos(cos_theta))


if __name__ == "__main__":
    print("=" * 55)
    print("   OPERACIONES CON VECTORES FISICOS 2D")
    print("=" * 55)

    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, -2)

    print(f"\nv1 = {v1}")
    print(f"v2 = {v2}")

    print(f"\nSuma:             v1 + v2  = {v1 + v2}")
    print(f"Resta:            v1 - v2  = {v1 - v2}")
    print(f"Escalar x3:       v1 * 3   = {v1 * 3}")
    print(f"Escalar (izq):    4 * v2   = {4 * v2}")
    print(f"Negacion:         -v2      = {-v2}")
    print(f"Magnitud v1:      |v1|     = {v1.magnitud():.4f}")
    print(f"Vector unitario:  v1/|v1|  = {v1.unitario()}")
    print(f"Producto punto:   v1 . v2  = {v1.producto_punto(v2):.4f}")
    print(f"Son ortogonales (v1,v2)?   {v1.es_ortogonal(v2)}")
    print(f"Angulo entre v1 y v2:      {v1.angulo_entre(v2):.2f} grados")

    ex = Vector2D(1, 0)
    ey = Vector2D(0, 1)
    print(f"\nex = {ex},  ey = {ey}")
    print(f"Son ortogonales ex, ey?    {ex.es_ortogonal(ey)}")
    print(f"Angulo entre ex y ey:      {ex.angulo_entre(ey):.2f} grados")

    fuerza       = Vector2D(10, 0)   # 10 N en direccion x
    desplazamiento = Vector2D(5, 3)  # 5 m en x, 3 m en y
    trabajo = fuerza.producto_punto(desplazamiento)
    print(f"\nEjemplo fisico - Trabajo:")
    print(f"  F = {fuerza},  d = {desplazamiento}")
    print(f"  W = F . d = {trabajo:.2f} J")

    print("\n" + "=" * 55)
    print("Resultados:")
    print("  v1 + v2       ->  (4i + 2j)")
    print("  v1 - v2       ->  (2i + 6j)")
    print("  v1 * 3        ->  (9i + 12j)")
    print("  |v1|          ->  5.0000")
    print("  v1 . v2       ->  -5.0000")
    print("  angulo(v1,v2) ->  ~116.57 grados")
    print("  angulo(ex,ey) ->  90.00 grados")
