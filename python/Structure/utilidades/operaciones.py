class Operaciones:

    @staticmethod
    def sumar_lista(lista: list) -> int:
        """Suma todos los elementos de una lista."""
        total = 0
        for num in lista:
            total += num
        return total

    @staticmethod
    def sumar_pares(lista: list) -> int:
        """Suma solo los elementos pares de una lista."""
        total = 0
        for num in lista:
            if num % 2 == 0:
                total += num
        return total
