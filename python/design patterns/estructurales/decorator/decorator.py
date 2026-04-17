"""
Decorator - Patron Estructural
================================
Agrega comportamiento a una funcion envolviendola en capas.
En Python se aplica con la sintaxis @nombre_decorador encima de la funcion.

Ejemplo de fisica:
    Una funcion calcula la fuerza base de un cuerpo. Los decoradores
    agregan capas de fuerzas: gravedad, friccion, resistencia del aire.
    Cada @decorador envuelve a la funcion anterior y suma su efecto.
"""

G = 9.8  # m/s^2, constante gravitacional


# --- Decoradores: funciones que reciben una funcion y devuelven otra ---

def con_gravedad(calcular_fuerza):
    def wrapper(masa_kg):
        fuerza, desc = calcular_fuerza(masa_kg)
        fg = masa_kg * G
        return fuerza + fg, desc + " + Gravedad"
    return wrapper


def con_friccion(mu):
    """Este decorador recibe un parametro, por eso tiene una capa extra."""
    def decorador(calcular_fuerza):
        def wrapper(masa_kg):
            fuerza, desc = calcular_fuerza(masa_kg)
            ff = mu * masa_kg * G
            return fuerza - ff, desc + f" + Friccion(mu={mu})"
        return wrapper
    return decorador


def con_resistencia_aire(velocidad_ms, cd=0.5):
    """Decorador con parametros para la resistencia del aire."""
    def decorador(calcular_fuerza):
        def wrapper(masa_kg):
            fuerza, desc = calcular_fuerza(masa_kg)
            rho  = 1.225  # kg/m^3, densidad del aire
            fair = 0.5 * cd * rho * velocidad_ms ** 2
            return fuerza - fair, desc + f" + Aire(v={velocidad_ms} m/s)"
        return wrapper
    return decorador


# --- Funcion base decorada con las tres capas de fuerza ---

@con_gravedad
@con_friccion(mu=0.3)
@con_resistencia_aire(velocidad_ms=5)
def cuerpo_libre(masa_kg):
    """Cuerpo sin fuerzas: fuerza base = 0."""
    return 0.0, f"Cuerpo libre (m={masa_kg} kg)"


# --- Demostracion ---
fuerza, descripcion = cuerpo_libre(masa_kg=10)
print(descripcion)
print(f"Fuerza neta: {fuerza:.2f} N")
