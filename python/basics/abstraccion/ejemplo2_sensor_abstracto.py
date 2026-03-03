"""
Abstracción — Ejemplo 2: Sensores físicos con interfaz abstracta
================================================================
Todos los sensores hacen lo mismo en el mismo orden:
inicializar → leer valor crudo → calibrar → validar → reportar.

El método medir() está en la clase base y orquesta esos pasos.
Cada sensor concreto solo se preocupa por sus propios detalles
(cómo leer, qué corrección aplicar, qué rango es válido).

Esto se llama patrón Template Method: el "molde" está arriba,
los detalles abajo.

Para practicar:
1. Agrega SensorCampoMagnetico que mida en Teslas.
2. Modifica medir() para registrar el tiempo de cada lectura.
3. Crea un SensorCompuesto que promedia dos sensores distintos.
"""

from abc import ABC, abstractmethod
import random
import math


# La clase base define el flujo completo, las subclases solo llenan los huecos

class Sensor(ABC):
    """Base para cualquier sensor. Define el ciclo completo de medición."""

    def __init__(self, id_sensor: str):
        self.id_sensor    = id_sensor
        self._inicializado = False
        self._n_lecturas  = 0

    # cada subclase tiene que definir estos tres pasos

    @property
    @abstractmethod
    def unidad(self) -> str:
        """Unidad física de la medición."""

    @property
    @abstractmethod
    def grandeza(self) -> str:
        """Nombre de la magnitud medida (p.ej. 'temperatura')."""

    @abstractmethod
    def _leer_crudo(self) -> float:
        """Lee el valor crudo del hardware del sensor."""

    @abstractmethod
    def _calibrar(self, valor_crudo: float) -> float:
        """Aplica correcciones de calibración al valor crudo."""

    @abstractmethod
    def _validar(self, valor_calibrado: float) -> bool:
        """Devuelve True si el valor está en el rango físico válido."""

    # este método no se toca en las subclases, solo los pasos que llama

    def medir(self) -> float | None:
        """Lee el sensor de principio a fin. Devuelve None si el valor no es válido."""
        if not self._inicializado:
            self._inicializar()

        crudo      = self._leer_crudo()
        calibrado  = self._calibrar(crudo)
        valido     = self._validar(calibrado)
        self._n_lecturas += 1

        if not valido:
            print(f"  [{self.id_sensor}] ADVERTENCIA: lectura fuera de rango "
                  f"({calibrado:.3f} {self.unidad})")
            return None

        return calibrado

    def _inicializar(self) -> None:
        """Se llama automáticamente la primera vez que alguien use el sensor."""
        self._inicializado = True
        print(f"  [{self.id_sensor}] Inicializado ({self.grandeza})")

    def reportar(self) -> None:
        """Resumen del sensor."""
        valor = self.medir()
        if valor is not None:
            print(f"  [{self.id_sensor}] {self.grandeza.capitalize()}: "
                  f"{valor:.4f} {self.unidad}  (lectura #{self._n_lecturas})")

    def __repr__(self):
        return f"{self.__class__.__name__}(id='{self.id_sensor}')"


# Sensor 1: temperatura con error sistemático y algo de ruido

class SensorTemperatura(Sensor):
    """Simula un termopar: tiene un offset fijo y ruido aleatorio en cada lectura."""

    def __init__(self, id_sensor: str, temp_real: float,
                 offset: float = 0.5, ruido: float = 0.2):
        super().__init__(id_sensor)
        self._temp_real  = temp_real   # °C — temperatura real que queremos medir
        self._offset     = offset      # el sensor siempre mide un poco más/menos
        self._ruido      = ruido       # variación aleatoria en cada lectura

    @property
    def unidad(self) -> str: return "°C"

    @property
    def grandeza(self) -> str: return "temperatura"

    def _leer_crudo(self) -> float:
        return self._temp_real + self._offset + random.gauss(0, self._ruido)

    def _calibrar(self, valor_crudo: float) -> float:
        return valor_crudo - self._offset   # restamos el error que ya conocemos

    def _validar(self, valor: float) -> bool:
        return -273.15 <= valor <= 1_000.0   # rango físico razonable


# Sensor 2: presión con un pequeño error multiplicativo en la escala

class SensorPresion(Sensor):
    """Simula un manómetro que sobreestima un poco (ganancia > 1)."""

    def __init__(self, id_sensor: str, presion_real: float,
                 ganancia: float = 1.02):
        super().__init__(id_sensor)
        self._presion_real = presion_real   # Pa — presión real del sistema
        self._ganancia     = ganancia       # el sensor amplifica un poco la señal

    @property
    def unidad(self) -> str: return "Pa"

    @property
    def grandeza(self) -> str: return "presión"

    def _leer_crudo(self) -> float:
        ruido = random.gauss(0, self._presion_real * 0.001)
        return self._presion_real * self._ganancia + ruido

    def _calibrar(self, valor_crudo: float) -> float:
        return valor_crudo / self._ganancia   # compensamos el factor de escala

    def _validar(self, valor: float) -> bool:
        return 0 <= valor <= 1e8   # 0 a 100 MPa


# Sensor 3: velocidad del viento — mide rpm y las convierte a m/s

class Anemometro(Sensor):
    """Anemómetro de copas: convierte rpm del rotor a velocidad en m/s."""

    def __init__(self, id_sensor: str, velocidad_real: float):
        super().__init__(id_sensor)
        self._v_real = velocidad_real   # m/s

    @property
    def unidad(self) -> str: return "m/s"

    @property
    def grandeza(self) -> str: return "velocidad del viento"

    def _leer_crudo(self) -> float:
        # el sensor devuelve rpm con un poco de ruido
        rpm_crudo = self._v_real * 10 + random.gauss(0, 0.5)
        return rpm_crudo

    def _calibrar(self, valor_crudo: float) -> float:
        return valor_crudo / 10.0   # convertimos rpm a m/s

    def _validar(self, valor: float) -> bool:
        return 0.0 <= valor <= 100.0   # m/s — límite del instrumento

    def fuerza_viento_beaufort(self) -> int:
        """Escala Beaufort aproximada a partir de la lectura."""
        v = self.medir() or 0.0
        escala = [0.5, 1.5, 3.3, 5.4, 7.9, 10.7, 13.8, 17.1, 20.7, 24.4, 28.4, 32.6]
        for i, limite in enumerate(escala):
            if v < limite:
                return i
        return 12


# Creamos varios sensores y los usamos todos igual, sin importar su tipo

if __name__ == "__main__":
    print("=" * 55)
    print("SENSORES FÍSICOS — abstracción y template method")
    print("=" * 55)

    sensores: list[Sensor] = [
        SensorTemperatura("T-01", temp_real=120.0),
        SensorTemperatura("T-02", temp_real=450.0),
        SensorPresion("P-01", presion_real=101_325.0),   # presión atmosférica
        Anemometro("V-01", velocidad_real=8.5),
    ]

    print("\n--- Ronda de mediciones ---")
    for sensor in sensores:
        sensor.reportar()

    print("\n--- Sensor fuera de rango ---")
    t_invalido = SensorTemperatura("T-ERR", temp_real=1100.0, offset=0, ruido=0)
    t_invalido.medir()

    print("\n--- Beaufort del viento ---")
    anemo = Anemometro("V-02", velocidad_real=15.0)
    anemo.medir()
    print(f"  Escala Beaufort: {anemo.fuerza_viento_beaufort()}")

    # esto tiene que fallar: Sensor solo es una plantilla, no se puede usar directamente
    print("\n--- Intentar instanciar Sensor directamente ---")
    try:
        Sensor("X")
    except TypeError as e:
        print(f"  Error: {e}")
