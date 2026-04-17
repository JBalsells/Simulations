# Factory Method — Patron Creacional

## Que problema resuelve

En una simulacion, necesitas crear distintos tipos de particulas: electrones, protones, neutrones. Cada una tiene su propia masa y carga. Sin Factory, el codigo de la simulacion tendria que conocer y construir cada clase concreta directamente:

```python
# Sin factory: el cliente sabe demasiado
if tipo == "electron":
    p = Electron()
elif tipo == "proton":
    p = Proton()
# ... y cada vez que agregues una particula, modificas este bloque
```

**Factory Method centraliza esa logica** en un solo lugar. El cliente solo pide `"electron"` y recibe el objeto listo.

---

## Cuando usarlo

- Cuando el tipo de objeto a crear se decide en tiempo de ejecucion
- Cuando quieres agregar nuevos tipos sin modificar el codigo existente
- Para centralizar y encapsular la logica de construccion de objetos

---

## Diagrama de funcionamiento

```
Simulacion (cliente)
       |
       | ParticulaFactory.crear("proton")
       v
  ParticulaFactory
       |
       | busca en el catalogo: "proton" -> Proton
       v
    Proton()          <- construye el objeto con masa y carga correctas
       |
       v
  Particula lista para usar
```

---

## El codigo, linea por linea

```python
# Clase base: define que operaciones tienen TODAS las particulas
class Particula:
    def __init__(self, nombre, masa_kg, carga_C):
        self.nombre  = nombre
        self.masa_kg = masa_kg
        self.carga_C = carga_C

# Cada particula concreta solo define sus propios valores
class Electron(Particula):
    def __init__(self):
        super().__init__("Electron", masa_kg=9.109e-31, carga_C=-1.602e-19)

# La fabrica: un diccionario mapea nombre -> clase
class ParticulaFactory:
    _catalogo = {
        "electron": Electron,
        "proton":   Proton,
        "neutron":  Neutron,
    }

    @staticmethod
    def crear(tipo: str) -> Particula:
        clase = ParticulaFactory._catalogo.get(tipo.lower())
        return clase()    # Instancia la clase y la devuelve
```

---

## Salida del programa

```
Particulas creadas por la fabrica:
  Electron   | masa = 9.109e-31 kg | carga = -
  Proton     | masa = 1.673e-27 kg | carga = +
  Neutron    | masa = 1.675e-27 kg | carga = neutra
```

---

## Agregar una nueva particula (sin tocar la simulacion)

```python
class Muon(Particula):
    def __init__(self):
        super().__init__("Muon", masa_kg=1.883e-28, carga_C=-1.602e-19)

# Solo agrega una linea en el catalogo:
ParticulaFactory._catalogo["muon"] = Muon
```

La simulacion no cambia. Solo la fabrica se actualiza.

---

## Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| Agregar nuevos tipos no rompe el codigo existente | Mas clases en el proyecto |
| El cliente no depende de clases concretas | Puede ser excesivo si solo hay 1 o 2 tipos |
| Logica de construccion en un solo lugar | |

---

## Analogia del mundo real

Es como un acelerador de particulas: tu le dices al acelerador "quiero un haz de protones" y el se encarga de configurarlo todo correctamente. Tu no tienes que saber los detalles de como se acelera cada tipo de particula.
