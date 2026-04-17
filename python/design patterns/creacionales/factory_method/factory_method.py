"""
Factory Method - Patron Creacional
=====================================
Define una "fabrica" que crea objetos sin que el cliente tenga que
conocer la clase exacta. El cliente pide un tipo y la fabrica lo construye.

Ejemplo de fisica:
    En una simulacion de particulas, queremos crear electrones, protones
    y neutrones con sus propiedades correctas (masa, carga). En lugar de
    construirlos manualmente cada vez, una fabrica los crea por nombre.
"""


# --- Clase base: define la interfaz comun de todas las particulas ---
class Particula:
    def __init__(self, nombre, masa_kg, carga_C):
        self.nombre   = nombre
        self.masa_kg  = masa_kg
        self.carga_C  = carga_C

    def info(self):
        signo = "+" if self.carga_C > 0 else ("-" if self.carga_C < 0 else "neutra")
        print(f"  {self.nombre:<10} | masa = {self.masa_kg:.3e} kg | carga = {signo}")


# --- Particulas concretas ---
class Electron(Particula):
    def __init__(self):
        super().__init__("Electron", masa_kg=9.109e-31, carga_C=-1.602e-19)


class Proton(Particula):
    def __init__(self):
        super().__init__("Proton", masa_kg=1.673e-27, carga_C=+1.602e-19)


class Neutron(Particula):
    def __init__(self):
        super().__init__("Neutron", masa_kg=1.675e-27, carga_C=0)


# --- Factory: decide que clase crear segun el nombre ---
class ParticulaFactory:
    _catalogo = {
        "electron": Electron,
        "proton":   Proton,
        "neutron":  Neutron,
    }

    @staticmethod
    def crear(tipo: str) -> Particula:
        clase = ParticulaFactory._catalogo.get(tipo.lower())
        if clase is None:
            raise ValueError(f"Particula desconocida: '{tipo}'")
        return clase()


# --- Demostracion ---
tipos = ["electron", "proton", "neutron"]

print("Particulas creadas por la fabrica:")
for tipo in tipos:
    p = ParticulaFactory.crear(tipo)
    p.info()
