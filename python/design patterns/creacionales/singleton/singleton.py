"""
Singleton - Patron Creacional
================================
Garantiza que una clase tenga UNA SOLA instancia en toda la aplicacion.

Ejemplo de fisica:
    Las constantes fisicas universales (c, G, h) no deben cambiar
    ni duplicarse en distintas partes del programa. Con Singleton,
    todos los modulos comparten exactamente el mismo objeto de constantes.
"""


class ConstantesFisicas:
    _instancia = None

    def __new__(cls):

        cls._instancia = super().__new__(cls)

        cls._instancia.c = 3e8          # Velocidad de la luz (m/s)
        cls._instancia.G = 6.674e-11    # Constante gravitacional (N m^2/kg^2)
        cls._instancia.h = 6.626e-34    # Constante de Planck (J·s)
        return cls._instancia
    
    
    def mostrar(self):
        print(f"  c = {self.c} m/s")
        print(f"  G = {self.G} N m^2/kg^2")
        print(f"  h = {self.h} J·s")


constantes_modulo_A = ConstantesFisicas()
constantes_modulo_B = ConstantesFisicas()

print("Son el mismo objeto:", constantes_modulo_A is constantes_modulo_B)  # True

print("\nConstantes desde modulo A:")
constantes_modulo_A.mostrar()

print("\nConstantes desde modulo B (mismo objeto):")
constantes_modulo_B.mostrar()
