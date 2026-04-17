"""
*args y **kwargs
================
Permiten que una funcion acepte cualquier cantidad de argumentos,
sin tener que definir cuantos recibe de antemano.

    *args   -> argumentos posicionales  -> llegan como tupla
    **kwargs -> argumentos con nombre   -> llegan como diccionario
"""


# --- *args: argumentos posicionales sin limite ---

def suma_total(*args):
    print(f"args recibidos: {args}")
    return sum(args)


# --- **kwargs: argumentos con nombre sin limite ---

def describir_particula(**kwargs):
    print(f"kwargs recibidos: {kwargs}")
    for propiedad, valor in kwargs.items():
        print(f"  {propiedad}: {valor}")


resultado = suma_total(3,4,5,67,34)
print(f"Resultado: {resultado}\n")

describir_particula(nombre="Electron", masa=9.109e-31, carga=-1)

describir_particula(nombre="Proton", masa=1.673e-27, carga=+1, estable=True)
