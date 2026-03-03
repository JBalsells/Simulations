"""
Encapsulamiento — Ejemplo 2: Instrumento de medición calibrado
===============================================================
Un sensor devuelve una señal cruda: no es el valor final. Hay que
aplicarle offset, ganancia y filtro antes de mostrársela al usuario.
Esos parámetros internos no deben tocarse desde afuera directamente;
se ocultan con encapsulamiento y se exponen solo a través de la interfaz.

Para practicar:
1. Agrega un atributo unidad y muéstralo en __repr__.
2. Implementa resetear_calibracion() que vuelva a offset=0, ganancia=1.
3. ¿Deberías también vaciar el buffer al resetear? Justifica.
"""

from collections import deque


# sensor con calibración y filtro de promedio

class InstrumentoMedicion:
    """Instrumento con señal cruda, calibración y filtro de promedio.

    Atributos privados:
        __lectura_cruda    — último valor del sensor sin corregir
        __offset           — corrección aditiva de calibración
        __ganancia         — corrección multiplicativa de calibración
        __buffer           — últimas N lecturas para promedio
    """

    def __init__(self, nombre: str, rango_min: float, rango_max: float,
                 n_promedio: int = 5):
        self.nombre     = nombre
        self._rango_min = rango_min    # protegido: lo usan subclases
        self._rango_max = rango_max
        self.__offset   = 0.0
        self.__ganancia = 1.0
        self.__lectura_cruda: float | None = None
        self.__buffer: deque[float] = deque(maxlen=n_promedio)

    # ajuste de offset y ganancia

    @property
    def offset(self) -> float:
        return self.__offset

    @offset.setter
    def offset(self, valor: float) -> None:
        self.__offset = float(valor)
        print(f"  [{self.nombre}] Offset ajustado a {self.__offset}")

    @property
    def ganancia(self) -> float:
        return self.__ganancia

    @ganancia.setter
    def ganancia(self, valor: float) -> None:
        if valor == 0:
            raise ValueError("La ganancia no puede ser 0.")
        self.__ganancia = float(valor)
        print(f"  [{self.nombre}] Ganancia ajustada a {self.__ganancia}")

    # lectura calibrada y filtrada

    def registrar_lectura_cruda(self, valor: float) -> None:
        """Recibe la señal del sensor y aplica calibración."""
        self.__lectura_cruda = valor
        calibrado = (valor + self.__offset) * self.__ganancia
        self.__buffer.append(calibrado)

    @property
    def lectura(self) -> float:
        """Última lectura calibrada (sin filtrar)."""
        if self.__lectura_cruda is None:
            raise RuntimeError("No hay lecturas registradas aún.")
        return (self.__lectura_cruda + self.__offset) * self.__ganancia

    @property
    def lectura_filtrada(self) -> float:
        """Promedio de las últimas N lecturas calibradas."""
        if not self.__buffer:
            raise RuntimeError("Buffer vacío.")
        return sum(self.__buffer) / len(self.__buffer)

    @property
    def en_rango(self) -> bool:
        """True si la última lectura calibrada está dentro del rango."""
        return self._rango_min <= self.lectura <= self._rango_max

    def __repr__(self):
        try:
            valor = f"{self.lectura:.3f}"
        except RuntimeError:
            valor = "sin datos"
        return f"{self.__class__.__name__}('{self.nombre}', lectura={valor})"


# sensores concretos: cada uno tiene su rango y operaciones propias

class Termometro(InstrumentoMedicion):
    """Sensor de temperatura: rango típico −50 a 500 °C."""

    def __init__(self, nombre: str = "Termómetro"):
        super().__init__(nombre, rango_min=-50.0, rango_max=500.0)

    def en_zona_critica(self) -> bool:
        """Alerta si supera el 90 % del rango máximo."""
        return self.lectura > 0.9 * self._rango_max


class Manometro(InstrumentoMedicion):
    """Sensor de presión: rango 0 a 200 bar."""

    def __init__(self, nombre: str = "Manómetro"):
        super().__init__(nombre, rango_min=0.0, rango_max=200.0)

    def presion_relativa(self, p_atm: float = 1.01325) -> float:
        """Presión manométrica = medida − presión atmosférica."""
        return self.lectura - p_atm


class Galvanometro(InstrumentoMedicion):
    """Sensor de corriente: rango −10 a 10 A."""

    def __init__(self, nombre: str = "Galvanómetro"):
        super().__init__(nombre, rango_min=-10.0, rango_max=10.0)

    def potencia_disipada(self, resistencia: float) -> float:
        """P = I² · R (W)."""
        return self.lectura**2 * resistencia


# --- demo ---

if __name__ == "__main__":
    print("=" * 55)
    print("INSTRUMENTOS DE MEDICIÓN — encapsulamiento")
    print("=" * 55)

    # -- Termómetro --
    print("\n--- Termómetro de horno ---")
    termo = Termometro("Horno-1")
    termo.offset  = 2.5    # el sensor sobreestima 2.5 °C
    termo.ganancia = 0.98  # factor de escala

    for cruda in [200.0, 201.5, 199.8, 202.0, 200.5]:
        termo.registrar_lectura_cruda(cruda)

    print(f"  Última lectura  : {termo.lectura:.3f} °C")
    print(f"  Lectura filtrada: {termo.lectura_filtrada:.3f} °C")
    print(f"  En rango        : {termo.en_rango}")
    print(f"  Zona crítica    : {termo.en_zona_critica()}")

    # -- Manómetro --
    print("\n--- Manómetro de caldera ---")
    mano = Manometro("Caldera-A")
    for cruda in [8.5, 8.7, 8.6, 8.8, 8.7]:
        mano.registrar_lectura_cruda(cruda)
    print(f"  Presión medida   : {mano.lectura:.3f} bar")
    print(f"  Presión relativa : {mano.presion_relativa():.3f} bar")
    print(f"  Filtrada         : {mano.lectura_filtrada:.3f} bar")

    # -- Galvanómetro --
    print("\n--- Galvanómetro de circuito ---")
    galv = Galvanometro("Circuito-RC")
    galv.offset = -0.05   # pequeño offset del cero
    for cruda in [3.0, 3.02, 2.98, 3.01, 2.99]:
        galv.registrar_lectura_cruda(cruda)
    R = 10.0  # Ω
    print(f"  Corriente       : {galv.lectura:.4f} A")
    print(f"  Potencia (R={R}Ω): {galv.potencia_disipada(R):.4f} W")

    # -- Intento de acceso directo --
    print("\n--- Acceso directo (debe fallar) ---")
    try:
        print(termo.__offset)
    except AttributeError as e:
        print(f"  Atributo privado protegido: {e}")
