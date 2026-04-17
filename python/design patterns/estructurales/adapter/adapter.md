# Adapter — Patron Estructural

## Que problema resuelve

Tu simulacion trabaja en el Sistema Internacional (m/s). Tienes un sensor antiguo que reporta velocidad en **pies por segundo**. No puedes modificar el sensor. El **Adapter** actua como un conector que traduce las llamadas de un sistema al otro.

---

## Cuando usarlo

- Al integrar instrumentos o librerias que usan unidades o interfaces diferentes
- Al reutilizar codigo heredado (legacy) que no puedes modificar
- Cuando dos sistemas necesitan comunicarse pero "hablan distinto"

---

## Diagrama de funcionamiento

```
Simulacion (cliente)
       |
       | sensor.leer_ms()              <- solo conoce esta interfaz
       v
  AdapterSensorLegacy
       |
       | self._sensor.leer_fps()       <- llama al sensor externo
       | resultado * 0.3048            <- convierte fps -> m/s
       |
       v
  Devuelve metros/segundo a la simulacion
```

---

## El codigo, linea por linea

### La interfaz con ABC

```python
from abc import ABC, abstractmethod

class SensorVelocidad(ABC):
    @abstractmethod
    def leer_ms(self) -> float:
        pass
```

Usar `ABC` y `@abstractmethod` en lugar de `raise NotImplementedError` tiene una ventaja: si alguien crea una subclase y olvida implementar `leer_ms`, Python lanza un error **al instanciar**, no al llamar al metodo. Falla rapido y con un mensaje claro.

### El sensor externo (no lo podemos tocar)

```python
class SensorVelocidadLegacy:
    def leer_fps(self):           # Interfaz diferente: fps, no m/s
        return self._velocidad_fps
```

### El Adapter

```python
class AdapterSensorLegacy(SensorVelocidad):   # Implementa la interfaz de TU sistema
    FPS_A_MS = 0.3048

    def __init__(self, sensor_legacy):
        self._sensor = sensor_legacy           # Envuelve el objeto externo

    def leer_ms(self) -> float:
        fps = self._sensor.leer_fps()          # Habla con el sensor en fps
        return fps * self.FPS_A_MS             # Devuelve m/s
```

La funcion `simular_movimiento` nunca sabe que por dentro hay un sensor en pies.

---

## Salida del programa

```
Sensor moderno:
  Velocidad: 20.00 m/s | Tiempo: 3 s | Distancia: 60.00 m

Sensor legacy (adaptado a m/s):
  Velocidad: 30.48 m/s | Tiempo: 3 s | Distancia: 91.44 m
```

100 pies/s = 30.48 m/s. La conversion es transparente para la simulacion.

---

## Por que ABC y no solo `raise NotImplementedError`

```python
# Sin ABC: el error aparece tarde (al llamar el metodo)
class SensorRoto(SensorVelocidad):
    pass

s = SensorRoto()       # No falla aqui...
s.leer_ms()            # Falla aqui: NotImplementedError

# Con ABC: el error aparece temprano (al crear el objeto)
class SensorRoto(SensorVelocidad):
    pass

s = SensorRoto()       # TypeError inmediato: no implemento leer_ms
```

---

## Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| Integra sistemas sin modificarlos | Agrega una capa de indirección |
| Reutiliza instrumentos o codigo existente | Puede ocultar la conversion si no esta documentada |
| ABC garantiza que la interfaz se cumpla | |

---

## Analogia del mundo real

Es exactamente como un adaptador de enchufes de viaje: tu laptop tiene un enchufe europeo, el hotel tiene tomacorriente americano. El adaptador no cambia ni la laptop ni la pared — solo hace que los dos sean compatibles entre si.
