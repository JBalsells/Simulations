"""
Sobrecarga — Ejemplo 4: Texto con estilo
=========================================
Operadores: __add__, __mul__, __contains__, __len__, __str__
"""


class Texto:
    def __init__(self, contenido: str, estilo: str = "normal"):
        self.contenido = contenido
        self.estilo = estilo

    def __str__(self):
        if self.estilo == "mayusculas":
            return self.contenido.upper()
        if self.estilo == "titulo":
            return self.contenido.title()
        return self.contenido

    def __add__(self, otro):
        """t1 + t2 — concatena dos textos."""
        return Texto(self.contenido + " " + otro.contenido, self.estilo)

    def __mul__(self, veces: int):
        """texto * 3 — repite el texto."""
        return Texto(" ".join([self.contenido] * veces), self.estilo)

    def __contains__(self, palabra: str):
        """"hola" in texto — busca una palabra."""
        return palabra.lower() in self.contenido.lower()

    def __len__(self):
        """len(texto) — número de palabras."""
        return len(self.contenido.split())


if __name__ == "__main__":
    t1 = Texto("hola mundo", estilo="mayusculas")
    t2 = Texto("buenas tardes")

    print(t1)                  # HOLA MUNDO
    print(t1 + t2)             # HOLA MUNDO BUENAS TARDES
    print(t2 * 3)              # buenas tardes buenas tardes buenas tardes
    print("mundo" in t1)       # True
    print("adios" in t1)       # False
    print(len(t1))             # 2
