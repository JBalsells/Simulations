import matplotlib.pyplot as plt


class Graficas:

    def __init__(self, valores_n: list, tiempos: list, memorias: list):
        self.valores_n = valores_n
        self.tiempos = tiempos
        self.memorias = memorias

    def graficar(self) -> None:
        """Muestra gráficas de n vs tiempo vs memoria."""
        etiquetas = [str(n) for n in self.valores_n]

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Fibonacci: rendimiento por número de términos")

        axes[0].plot(etiquetas, self.tiempos, marker="o", color="steelblue")
        axes[0].set_title("Tiempo de ejecución")
        axes[0].set_xlabel("n (términos)")
        axes[0].set_ylabel("Tiempo (s)")
        axes[0].grid(True)

        axes[1].plot(etiquetas, self.memorias, marker="o", color="darkorange")
        axes[1].set_title("Memoria de respuesta")
        axes[1].set_xlabel("n (términos)")
        axes[1].set_ylabel("Bytes")
        axes[1].grid(True)

        plt.tight_layout()
        plt.show()
