"""
Sobrecarga — Ejemplo 1: Vector 3D con operadores sobrecargados
==============================================================
En física es natural escribir u + v, 3 * u, u · v. Python permite
definir exactamente eso para clases propias usando métodos dunder
(__add__, __mul__, __abs__, etc.).

Para practicar:
1. __rmul__ ya está implementado — verifica que 3 * v funcione.
2. Agrega angulo_con(otro) usando el producto punto.
3. Implementa proyeccion_sobre(otro) que devuelva el escalar.
"""

import math


class Vector3D:
    """Vector tridimensional con operadores aritméticos sobrecargados."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    # suma, resta, negación y escala

    def __add__(self, otro: "Vector3D") -> "Vector3D":
        """u + v — suma componente a componente."""
        return Vector3D(self.x + otro.x, self.y + otro.y, self.z + otro.z)

    def __sub__(self, otro: "Vector3D") -> "Vector3D":
        """u − v — resta componente a componente."""
        return Vector3D(self.x - otro.x, self.y - otro.y, self.z - otro.z)

    def __neg__(self) -> "Vector3D":
        """−v — vector opuesto."""
        return Vector3D(-self.x, -self.y, -self.z)

    def __mul__(self, escalar: float) -> "Vector3D":
        """v * k — escalado (producto por escalar)."""
        return Vector3D(self.x * escalar, self.y * escalar, self.z * escalar)

    def __rmul__(self, escalar: float) -> "Vector3D":
        """k * v — escalado (conmutatividad)."""
        return self.__mul__(escalar)

    def __truediv__(self, escalar: float) -> "Vector3D":
        """v / k — división por escalar."""
        if escalar == 0:
            raise ZeroDivisionError("No se puede dividir un vector por cero.")
        return Vector3D(self.x / escalar, self.y / escalar, self.z / escalar)

    # igualdad con tolerancia numérica (float no es exacto)

    def __eq__(self, otro: object) -> bool:
        """u == v — igualdad con tolerancia numérica."""
        if not isinstance(otro, Vector3D):
            return NotImplemented
        eps = 1e-10
        return (abs(self.x - otro.x) < eps and
                abs(self.y - otro.y) < eps and
                abs(self.z - otro.z) < eps)

    # |v| con abs(v)

    def __abs__(self) -> float:
        """|v| — norma euclidiana (operador abs())."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    # producto punto (escalar) y producto cruz (vector)

    def punto(self, otro: "Vector3D") -> float:
        """u · v = ux·vx + uy·vy + uz·vz — producto escalar."""
        return self.x * otro.x + self.y * otro.y + self.z * otro.z

    def cruz(self, otro: "Vector3D") -> "Vector3D":
        """u × v — producto vectorial (regla de la mano derecha)."""
        return Vector3D(
            self.y * otro.z - self.z * otro.y,
            self.z * otro.x - self.x * otro.z,
            self.x * otro.y - self.y * otro.x,
        )

    # normalizar y ángulo entre vectores

    def normalizar(self) -> "Vector3D":
        """û = v / |v| — vector unitario."""
        norma = abs(self)
        if norma == 0:
            raise ValueError("No se puede normalizar el vector cero.")
        return self / norma

    def angulo_con(self, otro: "Vector3D") -> float:
        """θ = arccos(u·v / |u||v|) en grados."""
        cos_theta = self.punto(otro) / (abs(self) * abs(otro))
        cos_theta = max(-1.0, min(1.0, cos_theta))   # clamp numérico
        return math.degrees(math.acos(cos_theta))


# --- demo: fuerza, trabajo, torque y momento angular ---

if __name__ == "__main__":
    print("=" * 55)
    print("VECTOR 3D — operadores sobrecargados en física")
    print("=" * 55)

    # Vectores de fuerza
    F1 = Vector3D(3.0, 0.0, 0.0)   # 3 N en x
    F2 = Vector3D(0.0, 4.0, 0.0)   # 4 N en y

    print(f"\nF1 = {F1}")
    print(f"F2 = {F2}")
    print(f"F1 + F2 = {F1 + F2}   (fuerza resultante)")
    print(f"|F1 + F2| = {abs(F1 + F2):.4f} N")
    print(f"2 * F1 = {2 * F1}")
    print(f"-F2 = {-F2}")

    # Trabajo W = F · d
    desplazamiento = Vector3D(5.0, 3.0, 0.0)   # m
    fuerza = Vector3D(10.0, 2.0, 0.0)          # N
    trabajo = fuerza.punto(desplazamiento)
    print(f"\nFuerza  = {fuerza}")
    print(f"Desplaz = {desplazamiento}")
    print(f"Trabajo W = F · d = {trabajo:.2f} J")

    # Torque τ = r × F
    r = Vector3D(0.5, 0.0, 0.0)    # brazo de palanca (m)
    F = Vector3D(0.0, 10.0, 0.0)   # fuerza (N)
    torque = r.cruz(F)
    print(f"\nr = {r},  F = {F}")
    print(f"τ = r × F = {torque}")
    print(f"|τ| = {abs(torque):.4f} N·m")

    # Momento angular L = r × p
    v_part = Vector3D(0.0, 2.0, 0.0)    # m/s
    masa = 0.5                           # kg
    p = masa * v_part                    # momento lineal
    r_part = Vector3D(1.0, 0.0, 0.0)
    L = r_part.cruz(p)
    print(f"\nMomento angular L = r × p = {L}")

    # Ángulo entre dos vectores del campo eléctrico
    E1 = Vector3D(1.0, 0.0, 0.0)
    E2 = Vector3D(1.0, 1.0, 0.0)
    print(f"\nÁngulo entre E1={E1} y E2={E2}: "
          f"{E1.angulo_con(E2):.2f}°")
