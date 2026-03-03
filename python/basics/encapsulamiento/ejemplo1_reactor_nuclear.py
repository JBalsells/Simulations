"""
Encapsulamiento — Ejemplo 1: Reactor Nuclear
=============================================
En un reactor, temperatura y potencia son valores críticos. Si alguien
los modifica sin validación puede llevar el sistema a un estado imposible
o peligroso. El encapsulamiento resuelve eso: oculta el estado interno
y obliga a pasar por una interfaz que valida antes de cambiar nada.

Convenciones en Python:
  _atributo  → protegido (convención, no forzado)
  __atributo → privado con name-mangling (_Clase__atributo)
  @property  → getter público
  @x.setter  → setter con validación

Para practicar:
1. Agrega __presion (MPa) con su propiedad y setter que rechace valores > 16 MPa.
2. ¿Qué pasa si intentas acceder a reactor.__temperatura desde fuera de la clase?
3. Implementa estado_seguro() que devuelva True solo si todo está en rango.
"""


# acceso controlado: todo pasa por @property y setters con validación

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

    # getters: permiten leer sin exponer el atributo directamente

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

    # setters: validan el valor antes de almacenarlo

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

    # operaciones que el exterior puede invocar

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

    # método privado: solo lo usa la propia clase

    def __registrar(self, mensaje: str) -> None:
        self.__historial.append(mensaje)


# --- demo ---

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
