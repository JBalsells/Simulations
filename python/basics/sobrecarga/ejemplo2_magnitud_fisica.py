"""
Sobrecarga — Ejemplo 2: Magnitud física con unidades
=====================================================
¿Qué pasa si sumas 5 metros y 3 segundos? En física eso no tiene
sentido, y aquí tampoco: los operadores sobrecargados detectan
unidades incompatibles y lanzan un error antes de seguir.

Para practicar:
1. __pow__ ya está implementado — verifica que (magnitud)**2 funcione.
2. Implementa conversión de unidades (m → km, J → kJ).
3. ¿Cómo representarías unidades compuestas como m/s²?
"""


class Magnitud:
    """Valor numérico con una unidad física asociada."""

    def __init__(self, valor: float, unidad: str):
        self.valor  = float(valor)
        self.unidad = unidad

    def __repr__(self):
        return f"Magnitud({self.valor}, '{self.unidad}')"

    def __str__(self):
        return f"{self.valor:.4g} {self.unidad}"

    # suma y resta: solo si las unidades coinciden

    def __add__(self, otra: "Magnitud") -> "Magnitud":
        self._verificar_unidad(otra, "+")
        return Magnitud(self.valor + otra.valor, self.unidad)

    def __sub__(self, otra: "Magnitud") -> "Magnitud":
        self._verificar_unidad(otra, "-")
        return Magnitud(self.valor - otra.valor, self.unidad)

    # multiplicar combina las unidades: m × m = m·m

    def __mul__(self, otro) -> "Magnitud":
        if isinstance(otro, Magnitud):
            nueva_unidad = f"{self.unidad}·{otro.unidad}"
            return Magnitud(self.valor * otro.valor, nueva_unidad)
        # escalar × magnitud
        return Magnitud(self.valor * otro, self.unidad)

    def __rmul__(self, escalar: float) -> "Magnitud":
        return self.__mul__(escalar)

    # dividir también combina: m / s = m/s

    def __truediv__(self, otro) -> "Magnitud":
        if isinstance(otro, Magnitud):
            if otro.valor == 0:
                raise ZeroDivisionError("División por magnitud cero.")
            nueva_unidad = f"{self.unidad}/{otro.unidad}"
            return Magnitud(self.valor / otro.valor, nueva_unidad)
        if otro == 0:
            raise ZeroDivisionError("División por cero.")
        return Magnitud(self.valor / otro, self.unidad)

    def __pow__(self, exp: int) -> "Magnitud":
        """m ** n — potencia con unidad elevada."""
        nueva_unidad = f"{self.unidad}^{exp}" if exp != 1 else self.unidad
        return Magnitud(self.valor ** exp, nueva_unidad)

    # invertir signo conservando unidad

    def __neg__(self) -> "Magnitud":
        return Magnitud(-self.valor, self.unidad)

    # comparar: solo si las unidades coinciden

    def __eq__(self, otra: object) -> bool:
        if not isinstance(otra, Magnitud):
            return NotImplemented
        self._verificar_unidad(otra, "==")
        return abs(self.valor - otra.valor) < 1e-10

    def __lt__(self, otra: "Magnitud") -> bool:
        self._verificar_unidad(otra, "<")
        return self.valor < otra.valor

    def __le__(self, otra: "Magnitud") -> bool:
        return self < otra or self == otra

    def __gt__(self, otra: "Magnitud") -> bool:
        return not self.__le__(otra)

    # verifica unidades antes de operar

    def _verificar_unidad(self, otra: "Magnitud", operacion: str) -> None:
        if self.unidad != otra.unidad:
            raise TypeError(
                f"Unidades incompatibles para '{operacion}': "
                f"'{self.unidad}' y '{otra.unidad}'"
            )


# atajos para crear magnitudes sin repetir el nombre de la unidad

def metros(valor: float)    -> Magnitud: return Magnitud(valor, "m")
def segundos(valor: float)  -> Magnitud: return Magnitud(valor, "s")
def kilogramos(valor: float)-> Magnitud: return Magnitud(valor, "kg")
def newtons(valor: float)   -> Magnitud: return Magnitud(valor, "N")
def joules(valor: float)    -> Magnitud: return Magnitud(valor, "J")
def kelvin(valor: float)    -> Magnitud: return Magnitud(valor, "K")


# --- demo ---

if __name__ == "__main__":
    print("=" * 55)
    print("MAGNITUDES FÍSICAS CON UNIDADES — sobrecarga")
    print("=" * 55)

    # Cinemática
    d = metros(100.0)
    t = segundos(9.58)    # récord 100 m Usain Bolt
    v = d / t
    print(f"\nVelocidad media: {d} / {t} = {v}")

    # Segunda ley de Newton: F = m * a
    m   = kilogramos(70.0)
    a   = Magnitud(9.8, "m/s^2")
    F   = m * a
    print(f"Fuerza peso: {m} × {a} = {F}")

    # Trabajo: W = F · d
    fuerza = newtons(500.0)
    despl  = metros(10.0)
    W      = fuerza * despl
    print(f"Trabajo: {fuerza} × {despl} = {W}")

    # Energía cinética: Ec = ½ m v²
    masa  = kilogramos(2.0)
    veloc = Magnitud(5.0, "m/s")
    Ec    = 0.5 * masa * veloc ** 2
    print(f"Energía cinética: ½ × {masa} × ({veloc})² = {Ec}")

    # Suma de fuerzas paralelas
    F1 = newtons(30.0)
    F2 = newtons(20.0)
    print(f"\nF1 + F2 = {F1 + F2}")
    print(f"F1 > F2 → {F1 > F2}")

    # Error esperado: suma de unidades distintas
    print("\n--- Suma de unidades incompatibles (debe fallar) ---")
    try:
        resultado = metros(5.0) + segundos(3.0)
    except TypeError as e:
        print(f"  Error capturado: {e}")

    # Comparación para encontrar la mayor velocidad
    velocidades = [Magnitud(v, "m/s") for v in [30.0, 15.5, 45.2, 22.1]]
    mayor = max(velocidades, key=lambda v: v.valor)
    print(f"\nVelocidades: {[str(v) for v in velocidades]}")
    print(f"Mayor: {mayor}")
