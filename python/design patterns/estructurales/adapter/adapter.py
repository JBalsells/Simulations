"""
Adapter - Patron Estructural
================================
Permite que dos clases con interfaces incompatibles trabajen juntas.
Actua como un "traductor" entre dos sistemas.

Ejemplo de fisica:
    Un sensor de velocidad antiguo reporta en pies/segundo.
    Nuestra simulacion trabaja en metros/segundo (SI).
    No podemos modificar el sensor. El Adapter traduce las unidades.
"""

from abc import ABC, abstractmethod


# --- Sistema externo: sensor antiguo que NO podemos modificar ---
class SensorVelocidadLegacy:
    """Sensor que mide velocidad en pies por segundo."""
    def __init__(self, velocidad_fps):
        self._velocidad_fps = velocidad_fps

    def leer_fps(self):
        return self._velocidad_fps


# --- Interfaz que ESPERA nuestra simulacion ---
class SensorVelocidad(ABC):
    """Todo sensor en nuestra simulacion debe poder dar velocidad en m/s."""
    @abstractmethod
    def leer_ms(self) -> float:
        pass


# --- Sensor moderno (compatible directamente) ---
class SensorModerno(SensorVelocidad):
    def __init__(self, velocidad_ms):
        self._velocidad_ms = velocidad_ms

    def leer_ms(self) -> float:
        return self._velocidad_ms


# --- Adapter: adapta el sensor legacy a la interfaz de la simulacion ---
class AdapterSensorLegacy(SensorVelocidad):
    FPS_A_MS = 0.3048  # 1 pie/s = 0.3048 m/s

    def __init__(self, sensor_legacy: SensorVelocidadLegacy):
        self._sensor = sensor_legacy  # Guarda el objeto externo

    def leer_ms(self) -> float:
        fps = self._sensor.leer_fps()   # Llama al sensor externo
        return fps * self.FPS_A_MS      # Traduce la unidad


# --- Simulacion: solo conoce SensorVelocidad (la interfaz comun) ---
def simular_movimiento(sensor: SensorVelocidad, tiempo_s: float):
    v = sensor.leer_ms()
    distancia = v * tiempo_s
    print(f"  Velocidad: {v:.2f} m/s | Tiempo: {tiempo_s} s | Distancia: {distancia:.2f} m")


# --- Demostracion ---
sensor_nuevo    = SensorModerno(velocidad_ms=20)
sensor_viejo    = SensorVelocidadLegacy(velocidad_fps=100)
sensor_adaptado = AdapterSensorLegacy(sensor_viejo)

print("Sensor moderno:")
simular_movimiento(sensor_nuevo, tiempo_s=3)

print("\nSensor legacy (adaptado a m/s):")
simular_movimiento(sensor_adaptado, tiempo_s=3)
