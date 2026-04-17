"""
Singleton - Patron Creacional (sin cls)
========================================
Garantiza que una clase tenga UNA SOLA instancia en toda la aplicacion.

Ejemplo de fisica:
    Las constantes fisicas universales (c, G, h) no deben cambiar
    ni duplicarse en distintas partes del programa. Con Singleton,
    todos los modulos comparten exactamente el mismo objeto de constantes.

Diferencia con singleton.py:
    En lugar de usar __new__ con cls, se usa una funcion fabrica
    y una variable global para controlar que solo exista una instancia.
"""

_instancia = None


class ConstantesFisicas:

    def __init__(self):
        self.c = 3e8          # Velocidad de la luz (m/s)
        self.G = 6.674e-11    # Constante gravitacional (N m^2/kg^2)
        self.h = 6.626e-34    # Constante de Planck (J·s)

    def mostrar(self):
        print(f"  c = {self.c} m/s")
        print(f"  G = {self.G} N m^2/kg^2")
        print(f"  h = {self.h} J·s")


def obtener_constantes():
    global _instancia

    if _instancia is None:
        _instancia = ConstantesFisicas()

    return _instancia


constantes_modulo_A = obtener_constantes()
constantes_modulo_B = obtener_constantes()

print("Son el mismo objeto:", constantes_modulo_A is constantes_modulo_B)  # True

print("\nConstantes desde modulo A:")
constantes_modulo_A.mostrar()

print("\nConstantes desde modulo B (mismo objeto):")
constantes_modulo_B.mostrar()
