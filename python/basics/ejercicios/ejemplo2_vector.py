"""
Ejemplo 2: Clase Vector 3D
===========================
Con OOP podemos hacer que operar con vectores sea tan natural como
escribir las ecuaciones: v3 = v1 + v2, W = F.punto(d), τ = r.cruz(F).
"""

import math


class Vector3D:
    """Vector en tres dimensiones."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # sobrecarga: permite escribir v3 = v1 + v2 en lugar de sumar componente a componente

    def __add__(self, otro):
        """v1 + v2"""
        return Vector3D(self.x + otro.x, self.y + otro.y, self.z + otro.z)

    def __sub__(self, otro):
        """v1 - v2"""
        return Vector3D(self.x - otro.x, self.y - otro.y, self.z - otro.z)

    def __mul__(self, escalar):
        """v * escalar (producto por escalar)"""
        return Vector3D(self.x * escalar, self.y * escalar, self.z * escalar)

    def __rmul__(self, escalar):
        """escalar * v (permite escribir 3 * v)"""
        return self.__mul__(escalar)

    # --- Métodos de física vectorial ---

    def magnitud(self):
        """|v| = sqrt(x² + y² + z²)"""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def unitario(self):
        """Devuelve el vector unitario v̂ = v / |v|"""
        mag = self.magnitud()
        if mag == 0:
            raise ValueError("El vector nulo no tiene dirección.")
        return self * (1 / mag)

    def punto(self, otro):
        """Producto punto: a · b = ax*bx + ay*by + az*bz"""
        return self.x * otro.x + self.y * otro.y + self.z * otro.z

    def cruz(self, otro):
        """Producto cruz: a × b"""
        return Vector3D(
            self.y * otro.z - self.z * otro.y,
            self.z * otro.x - self.x * otro.z,
            self.x * otro.y - self.y * otro.x
        )

    def angulo_entre(self, otro):
        """Ángulo entre dos vectores en radianes: cos(θ) = (a·b)/(|a||b|)"""
        cos_theta = self.punto(otro) / (self.magnitud() * otro.magnitud())
        # Clamp para evitar errores numéricos en acos
        cos_theta = max(-1, min(1, cos_theta))
        return math.acos(cos_theta)

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


# --- Uso: aplicaciones de física ---

if __name__ == "__main__":

    # 1) Suma de fuerzas
    print("=== Suma de fuerzas ===")
    F1 = Vector3D(3, 0, 0)    # 3 N en x
    F2 = Vector3D(0, 4, 0)    # 4 N en y
    F_neta = F1 + F2
    print(f"F1 = {F1}")
    print(f"F2 = {F2}")
    print(f"F_neta = F1 + F2 = {F_neta}")
    print(f"|F_neta| = {F_neta.magnitud():.2f} N")   # debe dar 5

    # 2) Trabajo: W = F · d
    print("\n=== Trabajo (W = F · d) ===")
    F = Vector3D(10, 0, 0)          # Fuerza de 10 N en x
    d = Vector3D(5, 3, 0)           # Desplazamiento
    W = F.punto(d)
    print(f"F = {F}")
    print(f"d = {d}")
    print(f"W = F · d = {W:.2f} J")

    # 3) Torque: τ = r × F
    print("\n=== Torque (τ = r × F) ===")
    r = Vector3D(0, 2, 0)           # Brazo de palanca: 2 m en y
    F = Vector3D(5, 0, 0)           # Fuerza: 5 N en x
    torque = r.cruz(F)
    print(f"r = {r}")
    print(f"F = {F}")
    print(f"τ = r × F = {torque}")
    print(f"|τ| = {torque.magnitud():.2f} N·m")

    # 4) Ángulo entre vectores
    print("\n=== Ángulo entre vectores ===")
    a = Vector3D(1, 0, 0)
    b = Vector3D(1, 1, 0)
    angulo = a.angulo_entre(b)
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"θ = {angulo:.4f} rad = {math.degrees(angulo):.2f}°")  # debe dar 45°
