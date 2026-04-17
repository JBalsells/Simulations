# Patrones de Diseño — Referencia de Clase

Ejemplos implementados en Python con contexto de simulaciones de fisica.

---

## 1. Principios SOLID

Base teorica antes de ver patrones. SOLID es un conjunto de 5 principios que buscan que el software sea facil de entender, mantener y extender.

| Letra | Principio | Idea central |
|---|---|---|
| **S** | Single Responsibility | Una clase, una sola responsabilidad |
| **O** | Open/Closed | Abierta para extender, cerrada para modificar |
| **L** | Liskov Substitution | Una subclase debe poder reemplazar a su padre sin romper nada |
| **I** | Interface Segregation | Interfaces pequeñas y especificas, no una gigante |
| **D** | Dependency Inversion | Depender de abstracciones, no de clases concretas |

### Detalle de cada principio

**S — Single Responsibility**
Una clase `Factura` no deberia calcular totales, guardar en base de datos, generar PDF y enviar correo al mismo tiempo. Mejor: una clase por responsabilidad.

**O — Open/Closed**
En vez de editar una clase llena de `if` cada vez que aparece un nuevo tipo de descuento, se crean nuevas clases que extienden el comportamiento.

**L — Liskov Substitution**
Si `Ave` tiene metodo `volar()`, entonces `Pinguino` no encaja bien como subclase si no puede volar. La subclase debe comportarse de forma compatible con su padre.

**I — Interface Segregation**
En vez de una interfaz gigante `Trabajador` con `programar()`, `cocinar()`, `conducir()`, es mejor separar segun necesidad real.

**D — Dependency Inversion**
`Notificador` no deberia depender de `CorreoGmail` directamente, sino de una abstraccion `ServicioDeCorreo`. Asi se puede cambiar Gmail por otro sin romper todo.

---

## 2. Que es un patron de diseño

> Un patron de diseño no te da el programa terminado, sino una manera inteligente de organizar clases y objetos para resolver un problema repetitivo.

### No son codigo copiado

Un patron no depende de un lenguaje especifico ni tiene una unica implementacion correcta. Se adapta al contexto. Lo que se mantiene no es el codigo, sino la idea estructural.

> Un algoritmo se ejecuta. Un patron se diseña.

### Problemas que resuelven

- Demasiado acoplamiento entre clases
- Clases muy grandes que hacen demasiadas cosas
- Codigo dificil de extender sin romper otras partes
- Creacion de objetos desordenada o dependiente de detalles concretos
- Exceso de `if/else` para manejar variantes de logica

### Diferencia entre algoritmo, patron y arquitectura

Estos tres conceptos operan en **capas distintas** del software. De la mas concreta a la mas abstracta:

```
+-----------------------------------------------+
|              ARQUITECTURA                      |  <- Nivel de sistema
|  Como se divide y comunica el sistema entero   |
|  MVC, microservicios, cliente-servidor         |
+-----------------------------------------------+
|           PATRONES DE DISEÑO                   |  <- Nivel de clases / modulos
|  Como se organizan clases y responsabilidades  |
|  Singleton, Observer, Strategy...              |
+-----------------------------------------------+
|              ALGORITMOS                        |  <- Nivel de funcion / metodo
|  Pasos concretos para resolver un calculo      |
|  Ordenar, buscar, integrar numericamente...    |
+-----------------------------------------------+
```

| Concepto | Capa | Se enfoca en | Ejemplo |
|---|---|---|---|
| **Algoritmo** | Funcion / metodo | Pasos para resolver un problema especifico | Ordenar una lista, metodo de Euler |
| **Patron** | Clase / modulo | Como organizar clases y responsabilidades | Como crear objetos, como notificar cambios |
| **Arquitectura** | Sistema completo | Estructura global y comunicacion entre partes | MVC, microservicios, cliente-servidor |

> En una tienda en linea: la **arquitectura** define si el sistema sera monolitico o por microservicios; el **patron** define como organizar la creacion de metodos de pago; el **algoritmo** define como ordenar productos por precio.

Una forma simple de recordarlo:
- El **algoritmo** dice *que pasos seguir*
- El **patron** dice *como organizar el codigo*
- La **arquitectura** dice *como dividir el sistema*

---

## 3. Antipatrones

Un antipatron es lo opuesto a un patron de diseño: es una **solucion comun que parece razonable pero que en la practica genera mas problemas** de los que resuelve.

> Si un patron es una buena practica documentada, un antipatron es una mala practica documentada.

Son utiles conocerlos porque aparecen con frecuencia en codigo real, especialmente cuando el software crece sin planificacion.

### Antipatrones comunes

| Antipatron | Descripcion | Señal de alerta |
|---|---|---|
| **God Object** | Una clase que lo sabe y lo hace todo | Una clase con cientos de metodos y atributos |
| **Spaghetti Code** | Codigo sin estructura, dificil de seguir | Funciones enormes con muchos `if` anidados |
| **Magic Numbers** | Numeros literales sin nombre ni explicacion en el codigo | `if velocidad > 340:` sin saber por que 340 |
| **Copy-Paste Programming** | Resolver problemas copiando bloques en vez de abstraer | El mismo bloque de logica aparece en 5 lugares |
| **Premature Optimization** | Optimizar antes de saber si hay un problema real de rendimiento | Codigo ilegible para "hacerlo rapido" sin haberlo medido |
| **Golden Hammer** | Usar siempre la misma herramienta sin importar el problema | "Usamos Singleton para todo" |
| **Lava Flow** | Codigo muerto que nadie se atreve a borrar "por si acaso" | Funciones o clases comentadas que llevan meses sin usarse |
| **Boat Anchor** | Componente que se mantiene en el proyecto aunque ya no se usa | Libreria o modulo importado que no cumple ninguna funcion actual |
| **Dead Code** | Codigo que existe pero nunca se ejecuta | Variables, funciones o ramas `if` que ninguna ruta alcanza |
| **Hard Coding** | Valores de configuracion escritos directamente en el codigo fuente | URLs, contrasenas o rutas de archivo dentro del codigo |
| **Shotgun Surgery** | Un cambio pequeño obliga a modificar muchas clases distintas | "Para cambiar el formato de fecha toque 12 archivos" |
| **Feature Envy** | Un metodo usa mas datos de otra clase que de la propia | Un metodo accede constantemente a atributos de un objeto ajeno |
| **Poltergeist** | Clase que solo existe para llamar metodos de otra clase y desaparece | Clase intermediaria sin logica propia que solo delega todo |
| **Yo-Yo Problem** | Jerarquia de herencia tan profunda que hay que saltar entre muchos niveles para entender el flujo | Clases que heredan de clases que heredan de clases... |
| **Big Ball of Mud** | Sistema sin arquitectura definida donde todo depende de todo | No hay separacion de capas, modulos ni responsabilidades claras |
| **Reinventing the Wheel** | Implementar desde cero algo que ya existe y funciona bien en librerias estandar | Escribir un parser JSON o un ordenador propio sin razon |

### Diferencia clave

```
Patron      = solucion probada a un problema frecuente   ✓
Antipatron  = solucion intuitiva que crea deuda tecnica  ✗
```

La deuda tecnica es el costo acumulado de malas decisiones de diseño: codigo que funciona hoy pero que se vuelve cada vez mas dificil de mantener, corregir o extender.

---

## 4. Categorias de patrones

Los 23 patrones clasicos del libro *Design Patterns* (Gang of Four, 1994). Los marcados con ✅ estan implementados en este repositorio.

### Creacionales — *Como se crean los objetos*

Objetivo: hacer flexible y desacoplada la creacion de instancias.

Preguntas clave: ¿quien debe crear este objeto? ¿como evitar depender de clases concretas? ¿cuantas instancias deben existir?

| Patron | Problema que resuelve |
|---|---|
| ✅ [Singleton](creacionales/singleton/) | Garantiza que solo exista una instancia de una clase en todo el programa |
| ✅ [Factory Method](creacionales/factory_method/) | Define una interfaz para crear objetos, pero deja que las subclases decidan que clase instanciar |
| Abstract Factory | Crea familias de objetos relacionados sin depender de sus clases concretas |
| Builder | Construye objetos complejos paso a paso, separando construccion de representacion |
| Prototype | Crea nuevos objetos copiando (clonando) uno existente |

---

### Estructurales — *Como se combinan clases y objetos*

Objetivo: organizar relaciones entre componentes sin volver el sistema rigido.

Preguntas clave: ¿como agregar funcionalidad sin modificar la clase base? ¿como hacer compatibles interfaces distintas? ¿como simplificar el acceso a subsistemas complejos?

| Patron | Problema que resuelve |
|---|---|
| ✅ [Decorator](estructurales/decorator/) | Agrega comportamiento a una funcion u objeto de forma dinamica, envolviendolo en capas |
| ✅ [Adapter](estructurales/adapter/) | Conecta dos interfaces incompatibles actuando como traductor entre ellas |
| Bridge | Separa una abstraccion de su implementacion para que ambas puedan variar independientemente |
| Composite | Trata objetos individuales y colecciones de objetos de la misma manera (estructuras en arbol) |
| Facade | Proporciona una interfaz simplificada a un subsistema complejo |
| Flyweight | Comparte estado entre muchos objetos pequeños para reducir el uso de memoria |
| Proxy | Controla el acceso a un objeto mediante un representante o intermediario |

---

### De comportamiento — *Como interactuan los objetos*

Objetivo: manejar comunicacion, flujo de informacion y distribucion de responsabilidades entre objetos.

Preguntas clave: ¿como cambiar un comportamiento dinamicamente? ¿como notificar cambios a muchos objetos? ¿como encapsular una accion o decision?

| Patron | Problema que resuelve |
|---|---|
| ✅ [Observer](comportamiento/observer/) | Notifica automaticamente a multiples objetos cuando el estado de otro cambia |
| ✅ [Strategy](comportamiento/strategy/) | Encapsula algoritmos intercambiables y permite cambiarlos en tiempo de ejecucion |
| Chain of Responsibility | Pasa una solicitud por una cadena de objetos hasta que uno la maneja |
| Command | Encapsula una accion como objeto, permitiendo deshacer, rehacer o encolar operaciones |
| Iterator | Proporciona una forma de recorrer elementos de una coleccion sin exponer su estructura interna |
| Mediator | Reduce dependencias entre objetos haciendo que se comuniquen a traves de un intermediario |
| Memento | Guarda y restaura el estado previo de un objeto sin violar su encapsulamiento |
| State | Permite que un objeto cambie su comportamiento cuando cambia su estado interno |
| Template Method | Define el esqueleto de un algoritmo en una clase base y deja que las subclases completen los pasos |
| Visitor | Agrega nuevas operaciones a una jerarquia de clases sin modificarlas |
| Interpreter | Define una gramatica para un lenguaje y proporciona un interprete para sus sentencias |

---

## 5. Como leer cada patron

Cada carpeta contiene dos archivos:

```
patron/
  patron.py   <- Codigo Python ejecutable y comentado
  patron.md   <- Explicacion: problema, diagrama, codigo y analogia
```

Orden sugerido:

1. Lee el `.md` — entiende que problema resuelve antes de ver el codigo
2. Corre el `.py` — observa la salida
3. Experimenta — agrega una nueva particula, un nuevo metodo de integracion, un nuevo observador...

---

## 6. Estructura de archivos

```
design patterns/
├── README.md
├── creacionales/
│   ├── singleton/
│   │   ├── singleton.py
│   │   └── singleton.md
│   └── factory_method/
│       ├── factory_method.py
│       └── factory_method.md
├── estructurales/
│   ├── decorator/
│   │   ├── decorator.py
│   │   └── decorator.md
│   └── adapter/
│       ├── adapter.py
│       └── adapter.md
└── comportamiento/
    ├── observer/
    │   ├── observer.py
    │   └── observer.md
    └── strategy/
        ├── strategy.py
        └── strategy.md
```
