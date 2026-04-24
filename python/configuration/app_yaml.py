"""
Sistema de Reportes — configurado desde config.yaml

Demuestra cómo cargar y usar configuración YAML en Python.
Requiere: pip install pyyaml
"""

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import yaml


# ── Carga y validación de configuración ──────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def cargar_config(ruta: Path) -> dict:
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {ruta}")
    with open(ruta) as f:
        config = yaml.safe_load(f)
    _validar_config(config)
    return config


def _validar_config(config: dict) -> None:
    claves_requeridas = ["app", "base_de_datos", "reportes", "logging"]
    faltantes = [c for c in claves_requeridas if c not in config]
    if faltantes:
        raise ValueError(f"Configuración incompleta. Claves faltantes: {faltantes}")


# ── Configuración del logger usando valores del YAML ─────────────────────────

def configurar_logger(cfg_logging: dict) -> logging.Logger:
    nivel = getattr(logging, cfg_logging.get("nivel", "INFO"))
    archivo = cfg_logging.get("archivo", "app.log")

    Path(archivo).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=nivel,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(archivo),
        ],
    )
    return logging.getLogger("reportes")


# ── Modelos ───────────────────────────────────────────────────────────────────

@dataclass
class ConfigReporte:
    directorio_salida: str
    formatos_permitidos: list[str]
    max_filas: int
    incluir_graficas: bool
    colores: dict


@dataclass
class Reporte:
    nombre: str
    datos: list[dict]
    formato: str = "pdf"
    generado_en: datetime = field(default_factory=datetime.now)


# ── Lógica de negocio ─────────────────────────────────────────────────────────

class GeneradorReportes:
    def __init__(self, config: dict):
        self.cfg_app = config["app"]
        self.cfg_db = config["base_de_datos"]
        self.cfg_reportes = ConfigReporte(
            directorio_salida=config["reportes"]["directorio_salida"],
            formatos_permitidos=config["reportes"]["formatos_permitidos"],
            max_filas=config["reportes"]["max_filas_por_reporte"],
            incluir_graficas=config["reportes"]["incluir_graficas"],
            colores=config["reportes"]["paleta_colores"],
        )
        self.cfg_notif = config["notificaciones"]
        self.logger = logging.getLogger("reportes.generador")

    def _validar_formato(self, formato: str) -> None:
        if formato not in self.cfg_reportes.formatos_permitidos:
            raise ValueError(
                f"Formato '{formato}' no permitido. "
                f"Opciones: {self.cfg_reportes.formatos_permitidos}"
            )

    def _validar_tamano(self, datos: list) -> None:
        if len(datos) > self.cfg_reportes.max_filas:
            raise ValueError(
                f"El reporte tiene {len(datos)} filas pero el máximo es "
                f"{self.cfg_reportes.max_filas}"
            )

    def generar(self, reporte: Reporte) -> Path:
        self.logger.info(f"Generando reporte '{reporte.nombre}' en formato {reporte.formato}")

        self._validar_formato(reporte.formato)
        self._validar_tamano(reporte.datos)

        directorio = Path(self.cfg_reportes.directorio_salida)
        directorio.mkdir(parents=True, exist_ok=True)

        timestamp = reporte.generado_en.strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{reporte.nombre}_{timestamp}.{reporte.formato}"
        ruta_salida = directorio / nombre_archivo

        # Simulación de escritura (en un sistema real aquí iría ReportLab, openpyxl, etc.)
        contenido = self._construir_contenido(reporte)
        ruta_salida.write_text(contenido)

        self.logger.info(f"Reporte guardado en: {ruta_salida}")
        self._notificar_si_aplica(reporte.nombre, ruta_salida)
        return ruta_salida

    def _construir_contenido(self, reporte: Reporte) -> str:
        lineas = [
            f"REPORTE: {reporte.nombre}",
            f"Generado: {reporte.generado_en.strftime('%Y-%m-%d %H:%M:%S')}",
            f"App: {self.cfg_app['nombre']} v{self.cfg_app['version']}",
            f"Color primario: {self.cfg_reportes.colores['primario']}",
            f"Incluye gráficas: {self.cfg_reportes.incluir_graficas}",
            "-" * 40,
            f"Total de registros: {len(reporte.datos)}",
            "",
        ]
        for i, fila in enumerate(reporte.datos[:5], 1):
            lineas.append(f"  {i}. {fila}")
        if len(reporte.datos) > 5:
            lineas.append(f"  ... y {len(reporte.datos) - 5} registros más")
        return "\n".join(lineas)

    def _notificar_si_aplica(self, nombre: str, ruta: Path) -> None:
        if self.cfg_notif["email"]["habilitado"]:
            destinatarios = self.cfg_notif["email"]["destinatarios_defecto"]
            self.logger.info(
                f"Notificación enviada a {destinatarios} "
                f"desde {self.cfg_notif['email']['remitente']}"
            )

    def info_conexion_db(self) -> str:
        db = self.cfg_db
        return (
            f"{db['host']}:{db['puerto']}/{db['nombre']} "
            f"(pool: {db['pool']['min_conexiones']}-{db['pool']['max_conexiones']})"
        )


# ── Punto de entrada ──────────────────────────────────────────────────────────

def main():
    config = cargar_config(CONFIG_PATH)
    logger = configurar_logger(config["logging"])

    logger.info(f"Iniciando {config['app']['nombre']} v{config['app']['version']}")
    logger.info(f"Modo debug: {config['app']['debug']}")

    generador = GeneradorReportes(config)
    logger.info(f"Conectando a BD: {generador.info_conexion_db()}")

    ventas = [
        {"producto": "Laptop", "cantidad": 5, "total": 15000.00},
        {"producto": "Mouse", "cantidad": 20, "total": 600.00},
        {"producto": "Monitor", "cantidad": 3, "total": 4500.00},
        {"producto": "Teclado", "cantidad": 12, "total": 1200.00},
        {"producto": "Auriculares", "cantidad": 8, "total": 2400.00},
        {"producto": "Webcam", "cantidad": 6, "total": 1800.00},
    ]

    reporte = Reporte(nombre="ventas_abril", datos=ventas, formato="csv")
    ruta = generador.generar(reporte)
    print(f"\nReporte generado: {ruta}")
    print(f"Contenido:\n{ruta.read_text()}")

    try:
        reporte_invalido = Reporte(nombre="test", datos=ventas, formato="docx")
        generador.generar(reporte_invalido)
    except ValueError as e:
        logger.warning(f"Error esperado: {e}")


if __name__ == "__main__":
    main()
