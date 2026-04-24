"""
API de Inventario — configurada desde config.json

Demuestra cómo cargar y usar configuración JSON en Python.
No requiere dependencias externas (json es stdlib).
"""

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ── Carga y validación de configuración ──────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "config.json"


def cargar_config(ruta: Path) -> dict:
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {ruta}")
    with open(ruta) as f:
        config = json.load(f)
    _validar_config(config)
    return config


def _validar_config(config: dict) -> None:
    claves_requeridas = ["api", "autenticacion", "base_de_datos", "inventario"]
    faltantes = [c for c in claves_requeridas if c not in config]
    if faltantes:
        raise ValueError(f"Configuración incompleta. Claves faltantes: {faltantes}")

    impuesto = config["inventario"]["impuesto_porcentaje"]
    if not (0 <= impuesto <= 100):
        raise ValueError(f"impuesto_porcentaje debe estar entre 0 y 100, recibido: {impuesto}")


# ── Modelos ───────────────────────────────────────────────────────────────────

@dataclass
class Producto:
    id: int
    nombre: str
    categoria: str
    precio: float
    stock: int


@dataclass
class ResultadoPaginado:
    items: list
    total: int
    pagina: int
    items_por_pagina: int
    total_paginas: int


@dataclass
class RespuestaProducto:
    id: int
    nombre: str
    categoria: str
    precio_con_impuesto: float
    stock: int
    alerta_stock_bajo: bool


# ── Lógica de la API ──────────────────────────────────────────────────────────

class APIInventario:
    def __init__(self, config: dict):
        self.cfg_api = config["api"]
        self.cfg_auth = config["autenticacion"]
        self.cfg_db = config["base_de_datos"]
        self.cfg_cache = config["cache"]
        self.cfg_inv = config["inventario"]
        self.cfg_archivos = config["archivos"]
        self.logger = logging.getLogger("inventario.api")

        self._intentos_fallidos: dict[str, int] = {}
        self._productos_db = self._seed_productos()

    def _seed_productos(self) -> list[Producto]:
        return [
            Producto(1, "Laptop Lenovo X1", "electronica", 8500.00, 15),
            Producto(2, "Camiseta Polo", "ropa", 120.00, 3),
            Producto(3, "Arroz 5 libras", "alimentos", 22.50, 200),
            Producto(4, "Silla de oficina", "hogar", 950.00, 8),
            Producto(5, "Pesa 10kg", "deportes", 180.00, 25),
            Producto(6, "Mouse inalámbrico", "electronica", 220.00, 7),
            Producto(7, "Jean slim fit", "ropa", 245.00, 2),
        ]

    # ── Autenticación ─────────────────────────────────────────────────────────

    def autenticar(self, usuario: str, password: str) -> Optional[str]:
        intentos = self._intentos_fallidos.get(usuario, 0)
        max_intentos = self.cfg_auth["intentos_maximos"]

        if intentos >= max_intentos:
            self.logger.warning(
                f"Usuario '{usuario}' bloqueado tras {max_intentos} intentos fallidos. "
                f"Desbloqueo en {self.cfg_auth['bloqueo_minutos']} minutos."
            )
            return None

        if password == "password123":
            self._intentos_fallidos[usuario] = 0
            token = f"jwt.{usuario}.{self.cfg_auth['algoritmo']}.exp{self.cfg_auth['expiracion_minutos']}m"
            self.logger.info(f"Login exitoso para '{usuario}'")
            return token
        else:
            self._intentos_fallidos[usuario] = intentos + 1
            restantes = max_intentos - self._intentos_fallidos[usuario]
            self.logger.warning(
                f"Password incorrecto para '{usuario}'. Intentos restantes: {restantes}"
            )
            return None

    # ── Productos ─────────────────────────────────────────────────────────────

    def _aplicar_impuesto(self, precio: float) -> float:
        factor = 1 + (self.cfg_inv["impuesto_porcentaje"] / 100)
        return round(precio * factor, 2)

    def _a_respuesta(self, producto: Producto) -> RespuestaProducto:
        return RespuestaProducto(
            id=producto.id,
            nombre=producto.nombre,
            categoria=producto.categoria,
            precio_con_impuesto=self._aplicar_impuesto(producto.precio),
            stock=producto.stock,
            alerta_stock_bajo=producto.stock <= self.cfg_inv["stock_minimo_alerta"],
        )

    def listar_productos(
        self,
        pagina: int = 1,
        categoria: Optional[str] = None,
    ) -> ResultadoPaginado:
        items_por_pagina = self.cfg_inv["paginacion"]["items_por_pagina"]
        max_items = self.cfg_inv["paginacion"]["max_items"]

        if categoria and categoria not in self.cfg_inv["categorias"]:
            raise ValueError(
                f"Categoría '{categoria}' inválida. "
                f"Opciones: {self.cfg_inv['categorias']}"
            )

        productos = self._productos_db
        if categoria:
            productos = [p for p in productos if p.categoria == categoria]

        total = min(len(productos), max_items)
        inicio = (pagina - 1) * items_por_pagina
        fin = inicio + items_por_pagina
        pagina_actual = [self._a_respuesta(p) for p in productos[inicio:fin]]

        return ResultadoPaginado(
            items=pagina_actual,
            total=total,
            pagina=pagina,
            items_por_pagina=items_por_pagina,
            total_paginas=max(1, -(-total // items_por_pagina)),  # ceil division
        )

    def obtener_producto(self, producto_id: int) -> Optional[RespuestaProducto]:
        for producto in self._productos_db:
            if producto.id == producto_id:
                return self._a_respuesta(producto)
        return None

    def validar_archivo(self, nombre_archivo: str, tamano_bytes: int) -> bool:
        extension = nombre_archivo.rsplit(".", 1)[-1].lower() if "." in nombre_archivo else ""
        max_bytes = self.cfg_archivos["max_tamano_mb"] * 1024 * 1024

        if extension not in self.cfg_archivos["tipos_permitidos"]:
            self.logger.warning(
                f"Tipo de archivo '{extension}' no permitido. "
                f"Permitidos: {self.cfg_archivos['tipos_permitidos']}"
            )
            return False

        if tamano_bytes > max_bytes:
            self.logger.warning(
                f"Archivo de {tamano_bytes / 1024 / 1024:.1f} MB supera el límite "
                f"de {self.cfg_archivos['max_tamano_mb']} MB"
            )
            return False

        return True

    def info(self) -> dict:
        return {
            "nombre": self.cfg_api["nombre"],
            "version": self.cfg_api["version"],
            "base_url": self.cfg_api["base_url"],
            "cors_origins": self.cfg_api["cors_origins"],
            "cache_ttl": f"{self.cfg_cache['ttl_segundos']}s",
            "db": f"{self.cfg_db['host']}:{self.cfg_db['puerto']}/{self.cfg_db['nombre']}",
        }


# ── Punto de entrada ──────────────────────────────────────────────────────────

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    config = cargar_config(CONFIG_PATH)
    api = APIInventario(config)

    print("=" * 55)
    print(f"  {config['api']['nombre']} — v{config['api']['version']}")
    print("=" * 55)
    print(f"  Endpoint base : {config['api']['base_url']}")
    print(f"  Puerto        : {config['api']['puerto']}")
    print(f"  Impuesto      : {config['inventario']['impuesto_porcentaje']}%")
    print(f"  Cache (Redis) : {config['cache']['host']}:{config['cache']['puerto']}")
    print()

    # -- Autenticación --------------------------------------------------------
    print("── Autenticación ────────────────────────────────")
    token = api.autenticar("jorge", "password123")
    print(f"  Token obtenido : {token}")

    api.autenticar("atacante", "mal_password")
    api.autenticar("atacante", "mal_password")
    api.autenticar("atacante", "mal_password")
    api.autenticar("atacante", "mal_password")
    api.autenticar("atacante", "mal_password")  # bloqueado en este intento
    print()

    # -- Listar todos los productos -------------------------------------------
    print("── GET /api/v3/productos ────────────────────────")
    resultado = api.listar_productos(pagina=1)
    print(f"  Total: {resultado.total} | Página {resultado.pagina}/{resultado.total_paginas}")
    for p in resultado.items:
        alerta = " ⚠ STOCK BAJO" if p.alerta_stock_bajo else ""
        print(
            f"  [{p.id}] {p.nombre:<25} "
            f"Q{p.precio_con_impuesto:>8.2f}  "
            f"stock: {p.stock}{alerta}"
        )
    print()

    # -- Filtrar por categoría ------------------------------------------------
    print("── GET /api/v3/productos?categoria=electronica ──")
    resultado_cat = api.listar_productos(categoria="electronica")
    for p in resultado_cat.items:
        print(f"  [{p.id}] {p.nombre} — Q{p.precio_con_impuesto}")
    print()

    # -- Producto individual --------------------------------------------------
    print("── GET /api/v3/productos/2 ──────────────────────")
    producto = api.obtener_producto(2)
    if producto:
        print(f"  {json.dumps(producto.__dict__, indent=4, ensure_ascii=False)}")
    print()

    # -- Validación de archivos -----------------------------------------------
    print("── Validación de uploads ────────────────────────")
    casos = [
        ("foto_producto.jpg", 2 * 1024 * 1024),   # 2 MB — válido
        ("catalogo.pdf", 6 * 1024 * 1024),         # 6 MB — demasiado grande
        ("script.exe", 100 * 1024),                # tipo no permitido
    ]
    for nombre, tamano in casos:
        valido = api.validar_archivo(nombre, tamano)
        estado = "OK" if valido else "RECHAZADO"
        print(f"  {nombre:<25} {tamano / 1024 / 1024:.1f} MB → {estado}")

    # -- Categoría inválida ---------------------------------------------------
    print()
    try:
        api.listar_productos(categoria="videojuegos")
    except ValueError as e:
        print(f"  Error esperado: {e}")


if __name__ == "__main__":
    main()
