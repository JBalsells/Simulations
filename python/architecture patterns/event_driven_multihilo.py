"""
Patron Observer + Event-Driven con multihilos.

Idea:
  - El Sensor (Subject) tiene una temperatura que cambia cada cierto tiempo.
  - Los Observers se suscriben al Sensor y son notificados cuando cambia.
  - Monitor: solo muestra el valor.
  - Alerta: si la temperatura supera un umbral, dispara un evento.
  - Bombero: hilo aparte que espera el evento y reacciona.
"""

import threading
import random
import time
from abc import ABC, abstractmethod


# ---------- Patron Observer ----------

class Observer(ABC):
    """Interfaz que deben cumplir todos los observadores."""

    @abstractmethod
    def update(self, valor: float) -> None:
        ...


class Subject:
    """Sujeto observable: mantiene una lista de observadores y los notifica."""

    def __init__(self):
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, valor: float) -> None:
        for obs in self._observers:
            obs.update(valor)


# ---------- Sensor (Subject concreto) ----------

class Sensor(Subject):
    """Genera valores de temperatura en su propio hilo."""

    def __init__(self):
        super().__init__()
        self.temperatura = 20.0
        self._detener = threading.Event()

    def run(self, ticks: int = 10) -> None:
        for _ in range(ticks):
            if self._detener.is_set():
                break
            self.temperatura = random.uniform(20.0, 100.0)
            print(f"[Sensor]   nueva temperatura = {self.temperatura:5.2f}")
            self.notify(self.temperatura)
            time.sleep(0.5)

    def stop(self) -> None:
        self._detener.set()


# ---------- Observers concretos ----------

class Monitor(Observer):
    """Solo registra el valor que recibe."""

    def update(self, valor: float) -> None:
        print(f"[Monitor]  registro temperatura = {valor:.2f}")


class Alerta(Observer):
    """Dispara un evento cuando la temperatura supera el umbral."""

    def __init__(self, umbral: float, evento: threading.Event):
        self.umbral = umbral
        self.evento = evento

    def update(self, valor: float) -> None:
        if valor >= self.umbral:
            print(f"[Alerta]   {valor:.2f} >= {self.umbral} -> disparo evento")
            self.evento.set()


# ---------- Hilo que espera el evento ----------

class Bombero(threading.Thread):
    """Hilo bloqueado en evento.wait() hasta que la Alerta lo dispare."""

    def __init__(self, evento: threading.Event):
        super().__init__(daemon=True)
        self.evento = evento
        self.activo = True

    def run(self) -> None:
        while self.activo:
            if self.evento.wait(timeout=1.0):
                print("[Bombero]  !! evento recibido, apagando incendio")
                self.evento.clear()

    def detener(self) -> None:
        self.activo = False


# ---------- Programa principal ----------

def main():
    evento_alerta = threading.Event()

    sensor = Sensor()
    sensor.subscribe(Monitor())
    sensor.subscribe(Alerta(umbral=80.0, evento=evento_alerta))

    bombero = Bombero(evento_alerta)
    bombero.start()

    hilo_sensor = threading.Thread(target=sensor.run, args=(12,))
    hilo_sensor.start()
    hilo_sensor.join()

    bombero.detener()
    bombero.join(timeout=2.0)
    print("[main]     simulacion terminada")


if __name__ == "__main__":
    main()
