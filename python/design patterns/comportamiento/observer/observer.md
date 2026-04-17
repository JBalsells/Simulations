# Observer — Patron de Comportamiento

## Que problema resuelve

En un experimento de fisica de particulas, cuando ocurre una colision, varios instrumentos deben reaccionar: el contador Geiger registra el evento, la pantalla muestra la energia, el logger guarda el registro. Si el detector conoce directamente a cada instrumento, agregar uno nuevo requiere modificar el detector. 

**Observer desacopla el emisor de los receptores**: el detector solo avisa que algo ocurrio; cada instrumento decide que hacer.

---

## Cuando usarlo

- Sistemas de eventos y notificaciones en tiempo real
- Cuando multiples objetos deben reaccionar al cambio de estado de otro
- Para desacoplar el objeto que genera datos de los que los consumen

---

## Diagrama de funcionamiento

```
DetectorColisiones (Sujeto)
         |
         | registrar_colision()
         |
         +----> _notificar() -----> ContadorGeiger.actualizar()
         |                    \---> PantallaEnergia.actualizar()
         |                     \--> LoggerArchivo.actualizar()
```

El detector no sabe si los observadores son Geiger, pantallas, loggers... solo llama `actualizar()`.

---

## El codigo, linea por linea

```python
class DetectorColisiones:
    def __init__(self):
        self._observadores = []       # Lista de quien escucha

    def suscribir(self, observador):
        self._observadores.append(observador)

    def _notificar(self, particula1, particula2, energia_eV):
        for obs in self._observadores:
            obs.actualizar(particula1, particula2, energia_eV)  # Avisa a todos

    def registrar_colision(self, particula1, particula2, energia_eV):
        # ... registra ...
        self._notificar(particula1, particula2, energia_eV)  # Dispara el evento


# Cada observador decide como reaccionar
class ContadorGeiger:
    def actualizar(self, particula1, particula2, energia_eV):
        self._conteo += 1
        print(f"Evento #{self._conteo} detectado")

class PantallaEnergia:
    def actualizar(self, particula1, particula2, energia_eV):
        print(f"Energia: {energia_eV} eV")
```

---

## Salida del programa

```
[DETECTOR] Colision: proton + proton | E = 300 eV
  [GEIGER]  Evento #1 detectado
  [PANTALLA] Energia registrada: 300 eV
  [LOG]     Guardando en archivo: 'proton-proton @ 300 eV'

[DETECTOR] Colision: electron + positron | E = 1020 eV
  [GEIGER]  Evento #2 detectado
  [PANTALLA] Energia registrada: 1020 eV *** ALTA ENERGIA ***
  [LOG]     Guardando en archivo: 'electron-positron @ 1020 eV'

[DETECTOR] Colision: neutron + neutron | E = 50 eV
  [GEIGER]  Evento #3 detectado
  [PANTALLA] Energia registrada: 50 eV
              <- el logger ya no recibe notificaciones
```

---

## Agregar un nuevo instrumento (sin tocar el detector)

```python
class AlertaSonora:
    UMBRAL = 800

    def actualizar(self, particula1, particula2, energia_eV):
        if energia_eV > self.UMBRAL:
            print("  [ALARMA]  BEEP BEEP — energia critica!")

detector.suscribir(AlertaSonora())  # Una sola linea, nada mas cambia
```

---

## Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| El emisor no depende de los receptores concretos | Orden de notificacion no garantizado |
| Agregar o quitar observadores en tiempo de ejecucion | Muchos observadores pueden hacer el flujo dificil de seguir |
| Principio de responsabilidad unica bien aplicado | Referencias circulares pueden causar problemas |

---

## Analogia del mundo real

Es como suscribirse a alertas de un sismografo: el sismografo (sujeto) detecta el temblor y avisa a todos los sistemas que se suscribieron (alarmas, centros de emergencia, apps del celular). Cada sistema reacciona a su manera. El sismografo no sabe ni le importa cuantos hay.
