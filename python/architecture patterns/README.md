# Patrones de Arquitectura — Referencia de Clase

Guia de referencia sobre los principales patrones de arquitectura de software.

---

## 1. Que es un patron de arquitectura

Un patron de arquitectura es una **solucion general y reutilizable a un problema recurrente en el diseño estructural de un sistema de software**. Opera a un nivel mas alto que los patrones de diseño: no organiza clases u objetos, sino modulos, capas, servicios y la forma en que se comunican entre si.

> Si un patron de diseño te dice como organizar clases, un patron de arquitectura te dice como organizar el sistema completo.

### Que problema resuelven

A medida que un sistema crece, aparecen problemas como:

- Dificultad para escalar partes del sistema de forma independiente
- Cambios en la base de datos que rompen la logica de negocio
- Interfaces de usuario acopladas a la logica interna
- Sistemas donde todo depende de todo y nadie sabe que impacto tiene un cambio
- Equipos que no pueden trabajar en paralelo porque los modulos estan entrelazados

Los patrones de arquitectura proponen estructuras probadas para evitar estos problemas desde el inicio del diseño.

---

## 2. Diferencia entre arquitectura, patron de diseño y algoritmo

```
+-----------------------------------------------+
|          PATRONES DE ARQUITECTURA              |  <- Nivel de sistema
|  Como se divide y comunica el sistema entero   |
|  MVC, Microservicios, Hexagonal, Event-Driven  |
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

| Nivel | Pregunta que responde | Ejemplo |
|---|---|---|
| **Algoritmo** | Como resuelvo este calculo paso a paso? | Metodo de Euler para integracion numerica |
| **Patron de diseño** | Como organizo estas clases? | Observer para notificar cambios de estado |
| **Patron de arquitectura** | Como divido y conecto el sistema? | MVC para separar datos, logica y vista |

---

## 3. Categorias de patrones de arquitectura

### Patrones de capas — *Como se estructura internamente el sistema*

Se enfocan en dividir el sistema en capas o zonas con responsabilidades claras, donde cada capa solo puede comunicarse con las adyacentes.

Preguntas clave: ¿donde vive la logica de negocio? ¿como se separa la interfaz de los datos? ¿como evitar que un cambio en la base de datos rompa la logica?

| Patron | Descripcion | Cuando usarlo |
|---|---|---|
| **Layered Architecture** | Divide el sistema en capas horizontales: presentacion, logica de negocio y datos. Cada capa solo depende de la que esta debajo | Aplicaciones con estructura clara y equipos separados por responsabilidad |
| **MVC** (Model-View-Controller) | Separa datos (Model), interfaz (View) y logica de control (Controller). El Controller conecta Model y View | Aplicaciones web y de escritorio con interfaces de usuario |
| **MVP** (Model-View-Presenter) | Variante de MVC donde el Presenter maneja toda la logica de presentacion y la View es completamente pasiva | Interfaces donde se quiere mayor testabilidad de la logica visual |
| **MVVM** (Model-View-ViewModel) | La View se enlaza directamente al ViewModel mediante binding. El ViewModel expone el estado de la UI | Frameworks modernos: Vue, Angular, WPF, SwiftUI |
| **Hexagonal** (Ports & Adapters) | El nucleo de la aplicacion no depende de nada externo. Todo lo externo (BD, APIs, UI) se conecta a traves de puertos y adaptadores | Cuando se quiere que la logica de negocio sea completamente independiente de la infraestructura |
| **Clean Architecture** | Capas concentricas donde las dependencias apuntan siempre hacia adentro. El nucleo no conoce nada externo | Sistemas donde la logica de negocio debe sobrevivir cambios de framework, BD o interfaz |
| **Onion Architecture** | Similar a Clean Architecture. El dominio esta en el centro y las capas externas dependen de las internas, nunca al reves | Aplicaciones orientadas al dominio con mucha logica de negocio |

---

### Patrones de sistemas distribuidos — *Como se comunican servicios independientes*

Se enfocan en sistemas donde distintas partes corren de forma separada y necesitan coordinarse.

Preguntas clave: ¿como se comunican los servicios? ¿como se mantiene la consistencia entre partes? ¿como manejar fallos parciales?

| Patron | Descripcion | Cuando usarlo |
|---|---|---|
| **Microservicios** | El sistema se divide en servicios pequeños, independientes y desplegables por separado, cada uno con su propia base de datos | Sistemas grandes que necesitan escalar partes de forma independiente |
| **Event-Driven** | Los componentes se comunican publicando y consumiendo eventos asincronos. Nadie llama a nadie directamente | Sistemas donde las partes deben estar desacopladas y reaccionar a cambios en tiempo real |
| **CQRS** (Command Query Responsibility Segregation) | Separa las operaciones de escritura (Commands) de las de lectura (Queries) en modelos distintos | Sistemas con mucha diferencia entre la carga de lectura y escritura |
| **Event Sourcing** | El estado del sistema no se guarda directamente: se reconstruye reproduciendo el historial de eventos | Sistemas donde el historial de cambios es tan importante como el estado actual |
| **Saga** | Maneja transacciones distribuidas entre microservicios mediante una secuencia de pasos locales y eventos compensatorios | Flujos de negocio que abarcan multiples servicios y pueden necesitar deshacerse parcialmente |
| **Broker** | Un intermediario central (message broker) coordina la comunicacion entre componentes sin que se conozcan entre si | Sistemas donde muchos productores y consumidores de datos necesitan desacoplarse |

---

### Otros patrones reconocidos

| Patron | Descripcion | Cuando usarlo |
|---|---|---|
| **Pipe and Filter** | Los datos pasan por una cadena de transformaciones secuenciales. Cada filtro recibe una entrada y produce una salida | Procesamiento de datos, compiladores, pipelines ETL |
| **Space-Based** | Distribuye tanto el procesamiento como el almacenamiento en nodos para evitar cuellos de botella centrales | Sistemas con altisima concurrencia y necesidad de escalar horizontalmente |
| **Service-Oriented (SOA)** | El sistema se compone de servicios reutilizables que se comunican mediante un protocolo estandar | Integracion de sistemas empresariales heterogeneos |
| **Serverless** | La logica se divide en funciones pequeñas que se ejecutan bajo demanda en infraestructura gestionada por terceros | Cargas de trabajo variables donde no se quiere administrar servidores |

---

## 4. Comparativa rapida de los mas usados

| Patron | Complejidad | Escalabilidad | Ideal para |
|---|---|---|---|
| Layered | Baja | Media | Aplicaciones clasicas, equipos pequeños |
| MVC / MVP / MVVM | Baja-Media | Media | Apps con interfaz de usuario |
| Hexagonal / Clean | Media | Alta | Sistemas con logica de negocio compleja |
| Microservicios | Alta | Muy alta | Sistemas grandes con equipos independientes |
| Event-Driven | Media-Alta | Alta | Sistemas reactivos y en tiempo real |
| CQRS + Event Sourcing | Alta | Alta | Sistemas con historial y alta carga de lecturas |

---

## 5. Antipatrones de arquitectura

Al igual que en diseño, existen malas practicas documentadas a nivel arquitectonico.

| Antipatron | Descripcion | Señal de alerta |
|---|---|---|
| **Big Ball of Mud** | Sistema sin arquitectura definida donde todo depende de todo | No hay separacion de capas ni modulos con responsabilidades claras |
| **Monolith First (mal aplicado)** | Monolito que crece sin control y nunca se refactoriza | Un solo proyecto con miles de clases sin estructura interna |
| **Distributed Monolith** | Sistema que parece de microservicios pero todos los servicios deben desplegarse juntos | Cambiar un servicio obliga a redesplegar todos los demas |
| **Shared Database Antipattern** | Multiples servicios o modulos acceden y modifican la misma base de datos directamente | Un cambio de esquema en la BD rompe varios servicios a la vez |
| **God Service** | Un servicio en microservicios que termina haciendo demasiadas cosas | Un servicio con cientos de endpoints que conoce todos los demas dominios |
| **Chatty Services** | Microservicios que se llaman entre si constantemente para completar una operacion simple | Una sola accion del usuario genera decenas de llamadas entre servicios |
| **Hardcoded Topology** | La arquitectura asume una infraestructura fija y no puede adaptarse a cambios | URLs, IPs o nombres de servicios escritos directamente en el codigo |

---

## 6. Relacion con SOLID y patrones de diseño

Los patrones de arquitectura no reemplazan a SOLID ni a los patrones de diseño. Se complementan:

```
SOLID
  └── guia el diseño de clases individuales

Patrones de diseño
  └── guian la organizacion de clases y modulos

Patrones de arquitectura
  └── guian la estructura global del sistema
```

Un sistema bien construido aplica los tres niveles:
- Sus **clases** siguen SOLID
- Sus **modulos** usan patrones de diseño donde corresponde
- Su **estructura global** sigue un patron de arquitectura apropiado al problema

> No existe un patron de arquitectura universalmente correcto. La eleccion depende del tamaño del equipo, la escala esperada del sistema y la complejidad del dominio.
