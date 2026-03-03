"""
Agregación — Ejemplo 2: Laboratorio de física
==============================================
Un laboratorio tiene instrumentos, pero no los posee: los instrumentos
pueden estar en varios laboratorios a la vez, prestarse, o usarse en
distintos experimentos sin que nadie los destruya al terminar.

El cronómetro puede ser del lab de termodinámica Y del lab de mecánica
al mismo tiempo. Eso es la agregación.

Para practicar:
1. Agrega prestamo(instrumento, otro_lab) que lo mueva de un lab a otro.
2. Implementa disponibles() que filtre los instrumentos sin experimento asignado.
3. ¿Qué pasa si borras el laboratorio pero el experimento sigue
   referenciando los mismos instrumentos?
"""


# Un instrumento existe solo, sin depender de ningún lab ni experimento

class Instrumento:
    """Instrumento físico que se puede usar en cualquier experimento."""

    def __init__(self, nombre: str, tipo: str,
                 precision: float, unidad: str):
        self.nombre    = nombre
        self.tipo      = tipo        # "termómetro", "cronómetro", etc.
        self.precision = precision   # ± valor
        self.unidad    = unidad

    def descripcion(self) -> str:
        return (f"{self.nombre} ({self.tipo}) — "
                f"precisión ±{self.precision} {self.unidad}")

    def __repr__(self):
        return f"Instrumento('{self.nombre}', ±{self.precision} {self.unidad})"


# El experimento también solo referencia instrumentos, no los crea

class Experimento:
    """Agrupa los instrumentos necesarios y registra las mediciones."""

    def __init__(self, nombre: str, descripcion: str):
        self.nombre      = nombre
        self.descripcion = descripcion
        self._instrumentos: list[Instrumento] = []
        self._mediciones:   list[dict]        = []

    def asignar_instrumento(self, instrumento: Instrumento) -> None:
        if instrumento not in self._instrumentos:
            self._instrumentos.append(instrumento)

    def registrar_medicion(self, instrumento: Instrumento,
                           valor: float, incertidumbre: float = None) -> None:
        """Guarda un valor medido. Usa la precisión del instrumento si no se indica otra."""
        if instrumento not in self._instrumentos:
            raise ValueError(f"'{instrumento.nombre}' no está asignado "
                             f"a este experimento.")
        inc = incertidumbre if incertidumbre is not None else instrumento.precision
        self._mediciones.append({
            "instrumento": instrumento.nombre,
            "valor":       valor,
            "unidad":      instrumento.unidad,
            "incert":      inc,
        })

    def resultado_promedio(self, nombre_instrumento: str) -> tuple[float, float]:
        """Calcula la media y desviación estándar de todas las lecturas de ese instrumento."""
        datos = [m["valor"] for m in self._mediciones
                 if m["instrumento"] == nombre_instrumento]
        if not datos:
            raise ValueError(f"Sin mediciones de '{nombre_instrumento}'.")
        media = sum(datos) / len(datos)
        var   = sum((x - media)**2 for x in datos) / len(datos)
        return media, var ** 0.5

    def reporte(self) -> None:
        print(f"  Experimento: {self.nombre}")
        print(f"  Descripción: {self.descripcion}")
        print(f"  Instrumentos asignados: "
              f"{[i.nombre for i in self._instrumentos]}")
        print(f"  Mediciones registradas: {len(self._mediciones)}")
        for m in self._mediciones:
            print(f"    {m['instrumento']:20s} "
                  f"{m['valor']:8.3f} ± {m['incert']:.3f} {m['unidad']}")

    def __repr__(self):
        return (f"Experimento('{self.nombre}', "
                f"instrumentos={len(self._instrumentos)})")


# El laboratorio solo lleva la cuenta de qué tiene, no posee nada en exclusiva

class Laboratorio:
    """Lleva el inventario de instrumentos y los experimentos registrados."""

    def __init__(self, nombre: str, departamento: str):
        self.nombre       = nombre
        self.departamento = departamento
        self._inventario:   list[Instrumento] = []
        self._experimentos: list[Experimento] = []

    def incorporar(self, instrumento: Instrumento) -> None:
        """Agrega un instrumento al inventario."""
        self._inventario.append(instrumento)
        print(f"  [{self.nombre}] Incorporado: {instrumento.nombre}")

    def registrar_experimento(self, experimento: Experimento) -> None:
        self._experimentos.append(experimento)

    def inventario(self) -> None:
        print(f"\n  Inventario de {self.nombre} ({self.departamento})")
        for i, inst in enumerate(self._inventario, 1):
            print(f"    {i}. {inst.descripcion()}")

    def estado_general(self) -> None:
        print(f"\n  Lab: {self.nombre}")
        print(f"  Instrumentos: {len(self._inventario)}")
        print(f"  Experimentos: {len(self._experimentos)}")

    def __repr__(self):
        return (f"Laboratorio('{self.nombre}', "
                f"inst={len(self._inventario)}, "
                f"exp={len(self._experimentos)})")


if __name__ == "__main__":
    print("=" * 58)
    print("LABORATORIO DE FÍSICA — agregación")
    print("=" * 58)

    # creamos los instrumentos primero, sin asignarlos a ningún lado
    termometro  = Instrumento("Termómetro digital",  "temperatura",  0.1,  "°C")
    cronometro  = Instrumento("Cronómetro",          "tiempo",       0.01, "s")
    balanza     = Instrumento("Balanza analítica",   "masa",         0.001,"g")
    regla       = Instrumento("Regla de acero",      "longitud",     0.5,  "mm")
    calorim     = Instrumento("Calorímetro Dewar",   "temperatura",  0.2,  "°C")

    # nota: cronómetro y balanza aparecen en los dos laboratorios
    lab_termo = Laboratorio("Lab. Termodinámica", "Física")
    for inst in [termometro, cronometro, balanza, calorim]:
        lab_termo.incorporar(inst)

    lab_mec = Laboratorio("Lab. Mecánica", "Física")
    for inst in [cronometro, regla, balanza]:   # los mismos objetos, no copias
        lab_mec.incorporar(inst)

    lab_termo.inventario()
    lab_mec.inventario()

    # asignamos instrumentos ya existentes al experimento
    exp1 = Experimento("Calor específico del agua",
                       "Calentar 100 g de agua y medir ΔT")
    exp1.asignar_instrumento(termometro)
    exp1.asignar_instrumento(balanza)
    exp1.asignar_instrumento(calorim)

    # Registrar mediciones (T final del agua calentada)
    for T_med in [22.1, 22.0, 22.3, 22.2, 22.1]:
        exp1.registrar_medicion(termometro, T_med)

    media, sigma = exp1.resultado_promedio("Termómetro digital")
    lab_termo.registrar_experimento(exp1)

    print("\n--- Reporte del experimento ---")
    exp1.reporte()
    print(f"\n  Temperatura promedio: ({media:.3f} ± {sigma:.3f}) °C")

    # Experimento 2: péndulo (usa instrumentos del lab de mecánica)
    exp2 = Experimento("Período del péndulo",
                       "Medir T en función de L para g = 4π²L/T²")
    exp2.asignar_instrumento(cronometro)
    exp2.asignar_instrumento(regla)

    for T_period in [1.412, 1.408, 1.415, 1.410, 1.413]:
        exp2.registrar_medicion(cronometro, T_period)

    T_media, T_sigma = exp2.resultado_promedio("Cronómetro")
    import math
    L = 0.500   # m — longitud del péndulo
    g_exp = 4 * math.pi**2 * L / T_media**2
    lab_mec.registrar_experimento(exp2)

    print("\n--- Experimento de péndulo ---")
    exp2.reporte()
    print(f"\n  T promedio: ({T_media:.4f} ± {T_sigma:.4f}) s")
    print(f"  g experimental: {g_exp:.3f} m/s²  (real: 9.806)")

    # borrar el laboratorio no destruye los instrumentos ni los experimentos
    print("\n--- Los instrumentos sobreviven al laboratorio ---")
    del lab_mec
    print(f"  Cronómetro: {cronometro}")   # sigue vivo
    print(f"  Experimento pendulo: {exp2}")  # también
