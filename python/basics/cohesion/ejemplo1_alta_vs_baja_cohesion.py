"""
Cohesión — Ejemplo 1: Alta vs. baja cohesión en análisis de datos
==================================================================
Conceptos OOP: cohesión (cuánto "hace una sola cosa" una clase),
               principio de responsabilidad única (SRP), refactoring.

Idea central
------------
Una clase tiene ALTA COHESIÓN cuando todos sus métodos y atributos
se relacionan con UN único propósito bien definido.
Una clase tiene BAJA COHESIÓN cuando mezcla responsabilidades distintas.

Regla práctica: si el nombre de la clase requiere la palabra "y"
o "varios", probablemente tiene baja cohesión.

Mala práctica — clase con baja cohesión:
-----------------------------------------
    class FisicaExperimento:
        medir_temperatura()        ← medición
        guardar_en_archivo()       ← I/O
        calcular_promedio()        ← estadística
        graficar_resultados()      ← visualización
        enviar_reporte_email()     ← comunicación

Buena práctica — clases con alta cohesión:
-------------------------------------------
    class SensorTemperatura        ← sólo mide
    class AnalizadorEstadistico    ← sólo calcula estadísticas
    class Exportador               ← sólo guarda/carga datos

Tareas para el estudiante
-------------------------
1. ¿Qué clase tiene mayor cohesión: `SensorTemperatura` o
   `FisicaExperimentoBajaCohesion`? ¿Por qué?
2. Extrae la clase `Exportador` con métodos guardar_csv() y
   cargar_csv() y conéctala a `AnalizadorEstadistico`.
3. Agrega `SensorPresion` siguiendo el mismo patrón de alta cohesión.
"""

import math
import random


# ===========================================================================
# BAJA COHESIÓN — clase que hace todo (anti-patrón)
# ===========================================================================

class FisicaExperimentoBajaCohesion:
    """⚠ EJEMPLO DE LO QUE NO SE DEBE HACER.

    Esta clase mezcla: adquisición de datos, análisis estadístico,
    detección de anomalías, representación textual y 'exportación'.
    Es difícil de testear, extender y reutilizar.
    """

    def __init__(self):
        self.datos        = []
        self.unidad       = "°C"
        self.archivo_log  = "experimento.txt"
        self.email_destino = "investigador@lab.edu"

    def medir(self, valor_crudo: float, offset: float = 0.5):
        calibrado = valor_crudo - offset
        self.datos.append(calibrado)

    def calcular_promedio(self):
        return sum(self.datos) / len(self.datos) if self.datos else 0

    def calcular_desv(self):
        if len(self.datos) < 2:
            return 0
        m = self.calcular_promedio()
        return math.sqrt(sum((x - m)**2 for x in self.datos) / len(self.datos))

    def detectar_outliers(self, z_umbral=2.0):
        m, s = self.calcular_promedio(), self.calcular_desv()
        return [x for x in self.datos if s > 0 and abs(x - m) / s > z_umbral]

    def guardar_en_archivo(self):
        # Simula guardar (no crea archivo real)
        print(f"  [Baja cohesión] Guardando {len(self.datos)} datos en "
              f"'{self.archivo_log}'")

    def enviar_reporte(self):
        print(f"  [Baja cohesión] Enviando reporte a {self.email_destino}")

    def mostrar_todo(self):
        print(f"  [Baja cohesión] Datos={self.datos[:3]}... "
              f"Promedio={self.calcular_promedio():.2f} "
              f"σ={self.calcular_desv():.2f}")
        self.guardar_en_archivo()
        self.enviar_reporte()


# ===========================================================================
# ALTA COHESIÓN — cada clase tiene UNA responsabilidad
# ===========================================================================

class SensorTemperatura:
    """SÓLO mide y calibra. No analiza, no guarda, no envía."""

    def __init__(self, offset: float = 0.5, ruido: float = 0.2):
        self._offset = offset
        self._ruido  = ruido

    def leer(self, temperatura_real: float) -> float:
        """Simula una lectura con error sistemático y ruido."""
        crudo = temperatura_real + self._offset + random.gauss(0, self._ruido)
        return crudo - self._offset   # calibración

    def __repr__(self):
        return f"SensorTemperatura(offset={self._offset}, σ={self._ruido})"


class AnalizadorEstadistico:
    """SÓLO realiza cálculos estadísticos sobre una colección de datos."""

    def __init__(self, datos: list[float]):
        if not datos:
            raise ValueError("La lista de datos no puede estar vacía.")
        self._datos = list(datos)

    @property
    def n(self) -> int:
        return len(self._datos)

    def media(self) -> float:
        return sum(self._datos) / self.n

    def desv_estandar(self) -> float:
        m = self.media()
        return math.sqrt(sum((x - m)**2 for x in self._datos) / self.n)

    def error_estandar(self) -> float:
        """σ / √n — incertidumbre de la media."""
        return self.desv_estandar() / math.sqrt(self.n)

    def mediana(self) -> float:
        s = sorted(self._datos)
        mid = self.n // 2
        return s[mid] if self.n % 2 else (s[mid - 1] + s[mid]) / 2

    def outliers(self, z_umbral: float = 2.0) -> list[float]:
        m, s = self.media(), self.desv_estandar()
        return [x for x in self._datos if s > 0 and abs(x - m) / s > z_umbral]

    def intervalo_confianza_95(self) -> tuple[float, float]:
        """Media ± 1.96·σ/√n — intervalo de confianza 95 %."""
        delta = 1.96 * self.error_estandar()
        m = self.media()
        return m - delta, m + delta

    def __repr__(self):
        return f"AnalizadorEstadistico(n={self.n}, media={self.media():.3f})"


class ReportadorTexto:
    """SÓLO formatea y muestra resultados. No calcula ni mide."""

    def __init__(self, titulo: str, unidad: str):
        self.titulo = titulo
        self.unidad = unidad

    def mostrar_resumen(self, analizador: AnalizadorEstadistico) -> None:
        ic_min, ic_max = analizador.intervalo_confianza_95()
        print(f"\n  === {self.titulo} ===")
        print(f"  N muestras  : {analizador.n}")
        print(f"  Media       : ({analizador.media():.4f} ± "
              f"{analizador.error_estandar():.4f}) {self.unidad}")
        print(f"  σ           : {analizador.desv_estandar():.4f} {self.unidad}")
        print(f"  Mediana     : {analizador.mediana():.4f} {self.unidad}")
        print(f"  IC 95%      : [{ic_min:.4f}, {ic_max:.4f}] {self.unidad}")
        outliers = analizador.outliers()
        if outliers:
            print(f"  Outliers    : {outliers}")
        else:
            print(f"  Outliers    : ninguno")


# ===========================================================================
# Programa principal
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("COHESIÓN — alta vs. baja")
    print("=" * 60)

    T_REAL = 23.5   # °C — temperatura "verdadera"
    N      = 20     # número de mediciones

    # --- Baja cohesión ---
    print("\n[BAJA COHESIÓN]")
    exp_malo = FisicaExperimentoBajaCohesion()
    for _ in range(N):
        exp_malo.medir(T_REAL + random.gauss(0, 0.2))
    exp_malo.mostrar_todo()

    # --- Alta cohesión ---
    print("\n[ALTA COHESIÓN]")
    sensor    = SensorTemperatura(offset=0.5, ruido=0.2)
    mediciones = [sensor.leer(T_REAL) for _ in range(N)]

    analiz    = AnalizadorEstadistico(mediciones)
    reporte   = ReportadorTexto("Temperatura del horno", "°C")
    reporte.mostrar_resumen(analiz)

    # Reutilización: el mismo analizador sirve para otros datos
    print("\n  [Reutilizando AnalizadorEstadistico con datos de presión]")
    presiones = [101_325 + random.gauss(0, 50) for _ in range(15)]
    analiz_p  = AnalizadorEstadistico(presiones)
    rep_p     = ReportadorTexto("Presión atmosférica", "Pa")
    rep_p.mostrar_resumen(analiz_p)
