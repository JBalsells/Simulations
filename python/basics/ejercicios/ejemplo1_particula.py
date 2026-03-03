"""
Ejemplo 1: Clase Partícula
==========================
Una partícula puntual en 1D: tiene masa, posición y velocidad.
A partir de ahí se calculan energía cinética, momentum y movimiento.
"""


class Particula:
    """Representa una partícula puntual en una dimensión."""

    def __init__(self, masa, posicion, velocidad):
        self.masa = masa            # kg
        self.posicion = posicion    # m
        self.velocidad = velocidad  # m/s

    def energia_cinetica(self):
        """K = ½mv²"""
        return 0.5 * self.masa * self.velocidad ** 2

    def momentum(self):
        """p = mv"""
        return self.masa * self.velocidad

    def mover(self, dt):
        """Avanza la partícula un intervalo de tiempo dt (MRU)."""
        self.posicion += self.velocidad * dt

    def aplicar_fuerza(self, fuerza, dt):
        """Aplica una fuerza constante durante un intervalo dt.
        Actualiza velocidad y posición (MRUA)."""
        aceleracion = fuerza / self.masa  # F = ma → a = F/m
        self.posicion += self.velocidad * dt + 0.5 * aceleracion * dt ** 2
        self.velocidad += aceleracion * dt

    def __repr__(self):
        return (f"Partícula(m={self.masa} kg, "
                f"x={self.posicion:.2f} m, "
                f"v={self.velocidad:.2f} m/s)")


# --- Uso ---

if __name__ == "__main__":
    # Crear dos partículas
    electron = Particula(masa=9.109e-31, posicion=0, velocidad=1e6)
    bola = Particula(masa=0.5, posicion=0, velocidad=10)

    print("=== Estado inicial ===")
    print(f"Electrón: {electron}")
    print(f"  Energía cinética: {electron.energia_cinetica():.2e} J")
    print(f"  Momentum: {electron.momentum():.2e} kg·m/s")
    print()
    print(f"Bola: {bola}")
    print(f"  Energía cinética: {bola.energia_cinetica():.2f} J")
    print(f"  Momentum: {bola.momentum():.2f} kg·m/s")

    # Simular movimiento de la bola con gravedad (caída libre horizontal + gravedad)
    print("\n=== Aplicar fuerza de frenado (-1 N) durante 3 segundos ===")
    for t in range(3):
        bola.aplicar_fuerza(fuerza=-1.0, dt=1.0)
        print(f"  t={t + 1}s → {bola}")
