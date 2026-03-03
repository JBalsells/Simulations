"""
Encapsulamiento — Ejemplo 1: Reactor Nuclear
=============================================
Conceptos OOP: atributos privados (__), atributos protegidos (_),
               @property, setters con validación, acceso controlado.

Idea central
------------
El encapsulamiento oculta el estado interno y controla el acceso
a través de una interfaz pública segura. En un reactor nuclear,
los valores de temperatura y potencia son críticos: modificarlos
sin validación podría llevar a estados físicamente imposibles
o peligrosos.

Convenciones en Python
----------------------
  _atributo   → protegido (por convención, no forzado)
  __atributo  → privado con name-mangling (_Clase__atributo)
  @property   → getter público que accede al atributo privado
  @x.setter   → setter con lógica de validación

Tareas para el estudiante
-------------------------
1. Agrega un atributo `__presion` (MPa) con su propiedad y
   setter que lance ValueError si supera 16 MPa.
2. ¿Qué pasa si intentas acceder a `reactor.__temperatura`
   desde fuera de la clase?
3. Implementa un método `estado_seguro()` que devuelva True
   sólo si temperatura, potencia y presión están en rango.
"""


# ---------------------------------------------------------------------------
# Clase principal con encapsulamiento
# ---------------------------------------------------------------------------

class ReactorNuclear:
    """Modelo simplificado de un reactor de fisión.

    Atributos privados controlados con @property:
        __temperatura   (°C)
        __potencia_mw   (MW)
        __barras_control (0–100 %)

    Nunca modifiques __temperatura directamente desde fuera.
    Usa `reactor.temperatura = valor` para pasar por el setter.
    """

    # Límites de operación segura
    T_MAX     = 330.0    # °C — temperatura máxima del refrigerante
    T_MIN     =  20.0    # °C — temperatura mínima de operación
    P_MAX     = 3_200.0  # MW — potencia nominal máxima
    BARRAS_MIN = 0.0
    BARRAS_MAX = 100.0

    def __init__(self, nombre: str, potencia_nominal_mw: float):
        self.nombre = nombre
        self.__temperatura    = 25.0       # °C — valor inicial seguro
        self.__potencia_mw    = 0.0        # MW — apagado inicialmente
        self.__barras_control = 100.0      # % — 100 = completamente insertadas
        self._potencia_nominal = potencia_nominal_mw
        self.__historial: list[str] = []   # registro de cambios

    # ---- Propiedades (getters) ----

    @property
    def temperatura(self) -> float:
        """Temperatura actual del refrigerante (°C) — sólo lectura externa."""
        return self.__temperatura

    @property
    def potencia_mw(self) -> float:
        """Potencia actual generada (MW)."""
        return self.__potencia_mw

    @property
    def barras_control(self) -> float:
        """Posición de las barras de control (%). 100 = insertas = apagado."""
        return self.__barras_control

    @property
    def historial(self) -> list:
        """Historial de operaciones (sólo lectura — copia defensiva)."""
        return list(self.__historial)   # copia, no referencia

    # ---- Setters con validación ----

    @temperatura.setter
    def temperatura(self, valor: float) -> None:
        if not (self.T_MIN <= valor <= self.T_MAX):
            raise ValueError(
                f"Temperatura {valor}°C fuera de rango "
                f"[{self.T_MIN}, {self.T_MAX}] °C"
            )
        anterior = self.__temperatura
        self.__temperatura = valor
        self.__registrar(f"Temperatura: {anterior:.1f} → {valor:.1f} °C")

    @barras_control.setter
    def barras_control(self, porcentaje: float) -> None:
        if not (self.BARRAS_MIN <= porcentaje <= self.BARRAS_MAX):
            raise ValueError(
                f"Posición de barras {porcentaje}% fuera de [0, 100]"
            )
        anterior = self.__barras_control
        self.__barras_control = porcentaje
        # La potencia varía inversamente con la inserción de barras
        self.__potencia_mw = self._potencia_nominal * (1 - porcentaje / 100)
        self.__registrar(
            f"Barras: {anterior:.1f}% → {porcentaje:.1f}%  "
            f"| Potencia → {self.__potencia_mw:.1f} MW"
        )

    # ---- Métodos públicos ----

    def arrancar(self) -> None:
        """Retira barras al 70 % para iniciar reacción en cadena."""
        self.barras_control = 70.0
        self.__registrar("ARRANQUE del reactor")

    def apagar_emergencia(self) -> None:
        """SCRAM: inserta barras al 100 % inmediatamente."""
        self.__barras_control = 100.0
        self.__potencia_mw    = 0.0
        self.__registrar("*** APAGADO DE EMERGENCIA (SCRAM) ***")

    def estado(self) -> str:
        return (
            f"Reactor '{self.nombre}'\n"
            f"  Temperatura   : {self.__temperatura:.1f} °C\n"
            f"  Potencia      : {self.__potencia_mw:.1f} MW "
            f"({self.__potencia_mw / self._potencia_nominal * 100:.1f}%)\n"
            f"  Barras control: {self.__barras_control:.1f}%\n"
            f"  Estado        : {'OPERATIVO' if self.__potencia_mw > 0 else 'APAGADO'}"
        )

    # ---- Método privado: solo para uso interno ----

    def __registrar(self, mensaje: str) -> None:
        self.__historial.append(mensaje)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    reactor = ReactorNuclear("R-1 Atucha", potencia_nominal_mw=357.0)

    print("=" * 50)
    print("SIMULACIÓN: Control de un reactor nuclear")
    print("=" * 50)

    print("\n--- Estado inicial ---")
    print(reactor.estado())

    print("\n--- Arranque ---")
    reactor.arrancar()
    reactor.temperatura = 150.0
    print(reactor.estado())

    print("\n--- Operación a plena potencia ---")
    reactor.barras_control = 10.0
    reactor.temperatura = 300.0
    print(reactor.estado())

    print("\n--- Intento de sobretemperatura (debe fallar) ---")
    try:
        reactor.temperatura = 400.0   # > T_MAX
    except ValueError as e:
        print(f"  ERROR capturado: {e}")

    print("\n--- Apagado de emergencia ---")
    reactor.apagar_emergencia()
    reactor.temperatura = 25.0
    print(reactor.estado())

    print("\n--- Historial de operaciones ---")
    for entrada in reactor.historial:
        print(f"  · {entrada}")

    # Demostración de name-mangling
    print("\n--- Acceso directo al atributo privado ---")
    try:
        print(reactor.__temperatura)
    except AttributeError as e:
        print(f"  No se puede acceder: {e}")
    # Pero el name-mangling permite (no recomendado):
    print(f"  Via name-mangling: {reactor._ReactorNuclear__temperatura:.1f} °C  "
          f"(¡no hacer esto en producción!)")
