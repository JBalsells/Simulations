"""
Observer - Patron de Comportamiento
======================================
Define una relacion uno-a-muchos: cuando un objeto cambia de estado,
todos sus "suscriptores" son notificados automaticamente.

Ejemplo de fisica:
    Un detector de colisiones de particulas notifica a distintos
    instrumentos (contador Geiger, pantalla de energia, logger)
    cada vez que ocurre una colision. Cada instrumento reacciona a su manera.
"""


class DetectorColisiones:
    def __init__(self):
        self._observadores = []

    def suscribir(self, observador):
        self._observadores.append(observador)

    def desuscribir(self, observador):
        self._observadores.remove(observador)

    def _notificar(self, particula1, particula2, energia_eV):
        for obs in self._observadores:
            obs.actualizar(particula1, particula2, energia_eV)

    def registrar_colision(self, particula1, particula2, energia_eV):
        print(f"\n[DETECTOR] Colision: {particula1} + {particula2} | E = {energia_eV} eV")
        self._notificar(particula1, particula2, energia_eV)


class ContadorGeiger:
    def __init__(self):
        self._conteo = 0

    def actualizar(self, particula1, particula2, energia_eV):
        self._conteo += 1
        print(f"  [GEIGER]  Evento #{self._conteo} detectado")


class PantallaEnergia:
    UMBRAL_eV = 500

    def actualizar(self, particula1, particula2, energia_eV):
        alerta = " *** ALTA ENERGIA ***" if energia_eV > self.UMBRAL_eV else ""
        print(f"  [PANTALLA] Energia registrada: {energia_eV} eV{alerta}")


class LoggerArchivo:
    def actualizar(self, particula1, particula2, energia_eV):
        entrada = f"{particula1}-{particula2} @ {energia_eV} eV"
        print(f"  [LOG]     Guardando en archivo: '{entrada}'")


detector = DetectorColisiones()

geiger   = ContadorGeiger()
pantalla = PantallaEnergia()
logger   = LoggerArchivo()

detector.suscribir(geiger)
detector.suscribir(pantalla)
detector.suscribir(logger)

detector.registrar_colision("proton",    "proton",    energia_eV=300)
detector.registrar_colision("electron", "positron", energia_eV=1020)

detector.desuscribir(logger)

detector.registrar_colision("neutron", "neutron", energia_eV=50)
