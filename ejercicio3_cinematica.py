import math


class Movimiento:

    G = 9.8  # aceleracion de la gravedad (m/s^2)

    def __init__(self, x0: float, v0: float, nombre: str = "Movimiento"):
        self.x0 = x0      # posicion inicial (m)
        self.v0 = v0      # velocidad inicial (m/s)
        self.nombre = nombre

    def posicion(self, t: float) -> float:
        """Retorna la posicion x en el instante t."""
        raise NotImplementedError("Subclase debe implementar posicion(t)")

    def velocidad(self, t: float) -> float:
        """Retorna la velocidad v en el instante t."""
        raise NotImplementedError("Subclase debe implementar velocidad(t)")

    def tiempo_detencion(self) -> float:
        """Retorna el tiempo en que el objeto se detiene (si aplica)."""
        return float("inf")

    def energia_cinetica(self, masa: float, t: float) -> float:
        """
        Energia cinetica en el instante t: Ec = 0.5 * m * v^2
        Este metodo es HEREDADO por todas las subclases sin cambios.
        """
        v = self.velocidad(t)
        return 0.5 * masa * v**2

    def tabla(self, t_max: float, pasos: int = 5):
        """Imprime una tabla de posicion y velocidad en el tiempo."""
        print(f"\n--- {self.nombre} ---")
        print(f"{'t (s)':>8} {'x (m)':>10} {'v (m/s)':>10}")
        print("-" * 30)
        t_stop = self.tiempo_detencion()
        for i in range(pasos + 1):
            t = i * t_max / pasos
            if t > t_stop:
                t = t_stop
            x = self.posicion(t)
            v = self.velocidad(t)
            print(f"{t:>8.2f} {x:>10.3f} {v:>10.3f}")
            if t >= t_stop:
                print("  (objeto detenido)")
                break

class MRU(Movimiento):
    """Movimiento Rectilineo Uniforme: velocidad constante, a = 0."""

    def __init__(self, x0: float, v0: float):
        super().__init__(x0, v0, nombre="MRU (a=0)")

    def posicion(self, t: float) -> float:
        return self.x0 + self.v0 * t

    def velocidad(self, t: float) -> float:
        return self.v0   # constante

class MRUA(Movimiento):

    def __init__(self, x0: float, v0: float, a: float):
        super().__init__(x0, v0, nombre=f"MRUA (a={a} m/s^2)")
        self.a = a

    def posicion(self, t: float) -> float:
        """x(t) = x0 + v0*t + 0.5*a*t^2"""
        return self.x0 + self.v0 * t + 0.5 * self.a * t**2

    def velocidad(self, t: float) -> float:
        """v(t) = v0 + a*t"""
        return self.v0 + self.a * t

    def tiempo_detencion(self) -> float:
        """El objeto se detiene cuando v(t) = 0: t = -v0/a"""
        if self.a == 0:
            return float("inf")
        t = -self.v0 / self.a
        return t if t > 0 else float("inf")


class MRP(Movimiento):
    def __init__(self, x0: float, v0: float, mu: float):
        super().__init__(x0, v0, nombre=f"MRP (mu={mu})")
        self.mu = mu
        self._a = -mu * self.G   # desaceleracion negativa

    def posicion(self, t: float) -> float:
        """
        Si el objeto ya se detuvo (t >= t_stop), x permanece constante.
        x(t) = x0 + v0*t + 0.5*a*t^2   con  a = -mu*g
        """
        t = min(t, self.tiempo_detencion())
        return self.x0 + self.v0 * t + 0.5 * self._a * t**2

    def velocidad(self, t: float) -> float:
        """
        Si el objeto ya se detuvo, v = 0.
        v(t) = v0 + a*t   con a = -mu*g
        """
        t = min(t, self.tiempo_detencion())
        return self.v0 + self._a * t

    def tiempo_detencion(self) -> float:
        """El objeto se detiene cuando v = 0: t = v0 / (mu*g)"""
        if self.mu == 0:
            return float("inf")
        return self.v0 / (self.mu * self.G)

class Proyectil(Movimiento):
    def __init__(self, v0: float, angulo_grados: float, y0: float = 0):
        angulo_rad = math.radians(angulo_grados)
        self.v0x = v0 * math.cos(angulo_rad)   # componente horizontal
        self.v0y = v0 * math.sin(angulo_rad)   # componente vertical
        super().__init__(x0=y0, v0=self.v0y,
                         nombre=f"Proyectil (v0={v0} m/s, angulo={angulo_grados} deg)")

    def posicion(self, t: float) -> float:
        """Altura y(t) = y0 + v0y*t - 0.5*g*t^2"""
        return self.x0 + self.v0y * t - 0.5 * self.G * t**2

    def posicion_x(self, t: float) -> float:
        """Alcance horizontal x(t) = v0x*t"""
        return self.v0x * t

    def velocidad(self, t: float) -> float:
        """Velocidad vertical vy(t) = v0y - g*t"""
        return self.v0y - self.G * t

    def tiempo_vuelo(self) -> float:
        """Tiempo total en el aire (cuando y=0 de nuevo): t = 2*v0y/g"""
        return 2 * self.v0y / self.G

    def altura_maxima(self) -> float:
        """Altura maxima: y_max = v0y^2 / (2*g)"""
        return self.v0y**2 / (2 * self.G)

    def alcance_maximo(self) -> float:
        """Distancia horizontal total al aterrizar."""
        return self.posicion_x(self.tiempo_vuelo())

    def tabla(self, t_max: float = None, pasos: int = 6):
        """Tabla especial con columnas x e y para el proyectil."""
        if t_max is None:
            t_max = self.tiempo_vuelo()
        print(f"\n--- {self.nombre} ---")
        print(f"{'t (s)':>8} {'x (m)':>10} {'y (m)':>10} {'vy (m/s)':>10}")
        print("-" * 42)
        for i in range(pasos + 1):
            t = i * t_max / pasos
            print(f"{t:>8.2f} {self.posicion_x(t):>10.3f} "
                  f"{self.posicion(t):>10.3f} {self.velocidad(t):>10.3f}")
        print(f"  Altura maxima : {self.altura_maxima():.3f} m")
        print(f"  Alcance total : {self.alcance_maximo():.3f} m")
        print(f"  Tiempo vuelo  : {self.tiempo_vuelo():.3f} s")

if __name__ == "__main__":
    print("=" * 55)
    print("   SIMULACION DE MOVIMIENTO RECTILINEO - Cinematica")
    print("=" * 55)

    movimientos = [
        MRU(x0=0, v0=10),                  # coche a vel constante
        MRUA(x0=0, v0=0, a=3),             # cohete arrancando
        MRUA(x0=100, v0=20, a=-5),         # frenada brusca
        MRP(x0=0, v0=15, mu=0.4),          # objeto sobre superficie rugosa
    ]

    for mov in movimientos:   # polimorfismo: mismo metodo, distintos calculos
        mov.tabla(t_max=4.0, pasos=4)

    # Energia cinetica: metodo heredado, funciona en todos los tipos
    print("\n" + "=" * 55)
    print("Energia cinetica (masa=2 kg) a t=3s:")
    for mov in movimientos:
        ec = mov.energia_cinetica(masa=2, t=3)
        print(f"  {mov.nombre:<30} Ec = {ec:.2f} J")

    # Desafio: proyectil parabolico
    print("\n" + "=" * 55)
    print("   DESAFIO: MOVIMIENTO PARABOLICO (Proyectil)")
    print("=" * 55)
    pelota = Proyectil(v0=20, angulo_grados=45)
    pelota.tabla()

    print("\n" + "=" * 55)
    print("Verificacion de resultados:")
    mrua = MRUA(x0=0, v0=0, a=3)
    print(f"  MRUA(a=3) x(4s) = {mrua.posicion(4):.3f} m  (esperado: 24.000)")
    print(f"  MRUA(a=3) v(4s) = {mrua.velocidad(4):.3f} m/s (esperado: 12.000)")
    mrp = MRP(x0=0, v0=15, mu=0.4)
    print(f"  MRP t_stop      = {mrp.tiempo_detencion():.3f} s  (esperado: 3.827)")
    print(f"  MRP distancia   = {mrp.posicion(mrp.tiempo_detencion()):.3f} m  (esperado: 28.699)")
