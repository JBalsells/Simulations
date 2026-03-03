"""
Sobrecarga — Ejemplo 3: Carrito de compras
==========================================
Operadores: __add__, __sub__, __mul__, __contains__, __len__, __str__
"""


class Carrito:
    def __init__(self, productos: dict = None):
        self.productos = dict(productos) if productos else {}

    def __str__(self):
        return str(self.productos)

    def __add__(self, otro):
        """c1 + c2 — une dos carritos sumando cantidades."""
        nuevo = dict(self.productos)
        for nombre, cantidad in otro.productos.items():
            nuevo[nombre] = nuevo.get(nombre, 0) + cantidad
        return Carrito(nuevo)

    def __sub__(self, nombre: str):
        """carrito - "leche" — elimina un producto."""
        nuevo = dict(self.productos)
        nuevo.pop(nombre, None)
        return Carrito(nuevo)

    def __mul__(self, factor: int):
        """carrito * 2 — duplica todas las cantidades."""
        return Carrito({k: v * factor for k, v in self.productos.items()})

    def __contains__(self, nombre: str):
        """"leche" in carrito — verifica si existe el producto."""
        return nombre in self.productos

    def __len__(self):
        """len(carrito) — total de ítems."""
        return sum(self.productos.values())


if __name__ == "__main__":
    c1 = Carrito({"leche": 2, "pan": 1})
    c2 = Carrito({"leche": 1, "huevos": 6})

    print(c1 + c2)            # une los dos carritos
    print(c1 - "pan")         # elimina "pan"
    print(c1 * 3)             # triplica cantidades
    print("leche" in c1)      # True
    print("café" in c1)       # False
    print(len(c1))            # 3
