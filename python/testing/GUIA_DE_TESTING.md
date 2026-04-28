# Guía Completa de Testing en Software

## ¿Qué es un test?

Un test (o prueba) es código que verifica que otro código funciona correctamente. En lugar de probar manualmente una aplicación cada vez que haces un cambio, escribes tests automatizados que se pueden ejecutar en cualquier momento para confirmar que todo sigue funcionando como se espera.

---

## ¿Por qué escribir tests?

- **Detectan errores temprano** — es mucho más barato encontrar un bug antes de que llegue a producción.
- **Dan confianza para refactorizar** — puedes reorganizar o mejorar código sin miedo a romper algo sin darte cuenta.
- **Documentan el comportamiento esperado** — un test bien escrito describe exactamente qué debe hacer una función.
- **Facilitan la colaboración** — cuando alguien nuevo llega al proyecto, los tests le explican cómo se supone que funciona todo.
- **Reducen la deuda técnica** — el código con tests es más fácil de mantener a largo plazo.

---

## La Pirámide de Testing

La pirámide de testing es un modelo que describe cuántos tests de cada tipo deberías tener:

```
        /\
       /  \
      / E2E\        ← Pocos (lentos, costosos)
     /------\
    /Integr. \      ← Algunos
   /----------\
  / Unit Tests \    ← Muchos (rápidos, baratos)
 /--------------\
```

La base es grande porque los unit tests son rápidos, fáciles de escribir y muy específicos. Conforme subes, los tests son más complejos y lentos.

---

## Tipos de Tests

### 1. Unit Tests (Tests Unitarios)

Son el tipo más fundamental. Prueban una **sola unidad de código** en completo aislamiento: una función, un método, o una clase.

**Características:**
- Muy rápidos (milisegundos)
- No dependen de bases de datos, red, ni otros sistemas
- Si fallan, sabes exactamente dónde está el problema
- Son el tipo más abundante en un proyecto bien testeado

**Cuándo usarlos:**
- Para probar lógica de negocio
- Para probar algoritmos
- Para probar transformaciones de datos
- Para probar validaciones

**Ejemplo conceptual:**
```python
# Función a testear
def sumar(a, b):
    return a + b

# Test unitario
def test_sumar_dos_positivos():
    resultado = sumar(3, 4)
    assert resultado == 7
```

---

### 2. Integration Tests (Tests de Integración)

Prueban cómo **múltiples componentes trabajan juntos**. Por ejemplo, probar que tu código se comunica bien con una base de datos o con una API externa.

**Características:**
- Más lentos que los unit tests
- Requieren infraestructura real (BD, servicios, etc.)
- Detectan problemas de comunicación entre componentes
- Más difíciles de configurar

**Cuándo usarlos:**
- Para probar que el acceso a base de datos funciona
- Para probar la integración con APIs externas
- Para probar la comunicación entre módulos del sistema

**Ejemplo conceptual:**
```python
def test_guardar_usuario_en_bd():
    db = ConexionBaseDeDatos()
    usuario = Usuario(nombre="Ana", email="ana@ejemplo.com")
    db.guardar(usuario)
    
    usuario_guardado = db.buscar(email="ana@ejemplo.com")
    assert usuario_guardado.nombre == "Ana"
```

---

### 3. End-to-End Tests / E2E (Tests de Extremo a Extremo)

Prueban el **flujo completo de la aplicación** tal como lo usaría un usuario real: desde la interfaz hasta la base de datos y de vuelta.

**Características:**
- Los más lentos de todos
- Simulan interacciones reales de usuario
- Dan la mayor confianza de que el sistema funciona
- Son frágiles (se rompen con cambios de UI)
- Herramientas comunes: Selenium, Playwright, Cypress

**Cuándo usarlos:**
- Para los flujos más críticos del negocio (login, checkout, registro)
- Para smoke tests antes de un deploy
- Para validar que las partes del sistema se integran correctamente

---

### 4. Functional Tests (Tests Funcionales)

Prueban que el sistema cumple con los **requisitos funcionales** desde la perspectiva del usuario, sin importar cómo está implementado internamente. Son similares a los E2E pero no necesariamente involucran la UI.

**Características:**
- Se basan en especificaciones o historias de usuario
- Caja negra: no se preocupan por el código interno
- Validan comportamiento, no implementación

---

### 5. Regression Tests (Tests de Regresión)

Son tests que se escriben específicamente para verificar que un **bug ya corregido no vuelva a aparecer**. Cada vez que corriges un bug, escribes un test que lo reproduce y lo agregas a la suite.

**Características:**
- Previenen que errores pasados reaparezcan
- Documenta el historial de bugs del proyecto
- Se acumulan con el tiempo

**Flujo de trabajo:**
1. Encuentras un bug
2. Escribes un test que reproduce el bug (falla)
3. Corriges el bug (el test pasa)
4. El test queda en el proyecto para siempre

---

### 6. Smoke Tests

Son un subconjunto muy básico de tests que verifican que las **funcionalidades más críticas del sistema funcionan** después de un deploy o cambio importante. Son el "¿está encendido?" del software.

**Características:**
- Muy rápidos y superficiales
- Se corren primero antes de tests más profundos
- Si fallan, no vale la pena correr el resto

---

### 7. Performance Tests (Tests de Rendimiento)

Verifican que el sistema funciona correctamente bajo **carga o en condiciones de estrés**.

**Subtipos:**
- **Load testing**: ¿soporta la carga esperada de usuarios?
- **Stress testing**: ¿cómo se comporta cuando se supera el límite?
- **Soak testing**: ¿se degrada con el tiempo bajo uso sostenido?

**Herramientas comunes:** JMeter, k6, Locust

---

### 8. Security Tests (Tests de Seguridad)

Verifican que el sistema **no tiene vulnerabilidades** conocidas.

**Subtipos:**
- **SAST (Static Application Security Testing)**: analiza el código fuente
- **DAST (Dynamic Application Security Testing)**: ataca la aplicación en ejecución
- **Penetration testing**: simulación de ataques reales

---

### 9. Acceptance Tests (Tests de Aceptación)

También llamados UAT (User Acceptance Testing). Los realiza el **cliente o usuario final** para confirmar que el sistema cumple sus expectativas antes de aceptarlo oficialmente.

**BDD (Behavior Driven Development)** usa acceptance tests escritos en lenguaje natural:

```gherkin
Dado que el usuario está en la página de login
Cuando ingresa credenciales válidas
Entonces debe ser redirigido al dashboard
```

---

### 10. Contract Tests (Tests de Contrato)

En arquitecturas de microservicios, verifican que **dos servicios que se comunican entre sí** cumplen con el contrato de la API (los endpoints, parámetros y respuestas esperadas).

**Herramienta popular:** Pact

---

## Conceptos Clave en Testing

### Assertions (Afirmaciones)

Una assertion verifica que una condición es verdadera. Si no lo es, el test falla.

```python
assert resultado == 42          # Python nativo
assert resultado is not None
assert "error" not in mensaje
```

### Mocks, Stubs y Fakes

Cuando un unit test necesita interactuar con algo externo (BD, API, sistema de archivos), usamos "dobles de prueba":

- **Mock**: objeto que verifica que fue llamado correctamente
- **Stub**: reemplaza una dependencia y retorna datos predefinidos
- **Fake**: implementación simplificada pero funcional (ej: base de datos en memoria)

```python
from unittest.mock import MagicMock

# En lugar de llamar a una API real, usamos un mock
api = MagicMock()
api.obtener_precio.return_value = 100.0

resultado = calcular_total(cantidad=3, api=api)
assert resultado == 300.0
api.obtener_precio.assert_called_once()
```

### Fixtures

Son datos o estado de prueba que se configuran antes de ejecutar los tests y se limpian después.

```python
import pytest

@pytest.fixture
def lista_de_numeros():
    return [5, 3, 8, 1, 9, 2, 7, 4, 6]

def test_ordenamiento(lista_de_numeros):
    resultado = ordenar(lista_de_numeros)
    assert resultado == [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Setup y Teardown

Código que se ejecuta **antes y después** de cada test (o de toda la suite) para preparar y limpiar el entorno.

```python
class TestMiClase:
    def setup_method(self):
        # Se ejecuta antes de cada test
        self.db = crear_base_de_datos_temporal()

    def teardown_method(self):
        # Se ejecuta después de cada test
        self.db.eliminar()
```

### Coverage (Cobertura)

Mide qué **porcentaje del código fuente es ejecutado** por los tests. Un 80-90% es generalmente considerado bueno.

```bash
# Correr tests con reporte de coverage en Python
pytest --cov=mi_modulo --cov-report=html
```

> ⚠️ 100% de coverage no garantiza que los tests sean buenos. Es posible cubrir código sin probar casos importantes.

---

## TDD — Test Driven Development

Una metodología de desarrollo donde primero escribes los tests, y luego el código que los hace pasar.

**El ciclo Red-Green-Refactor:**

1. 🔴 **Red**: Escribe un test que falla (el código aún no existe)
2. 🟢 **Green**: Escribe el código mínimo para que el test pase
3. 🔵 **Refactor**: Mejora el código sin cambiar su comportamiento

**Beneficios del TDD:**
- Te obliga a pensar en el diseño antes de codificar
- Garantiza que todo el código tiene tests
- Produce código más modular y desacoplado

---

## BDD — Behaviour Driven Development

Extensión del TDD donde los tests se escriben en **lenguaje natural** entendible por el negocio.

```gherkin
Feature: Ordenamiento de listas
  Scenario: Ordenar lista de enteros
    Given una lista desordenada [3, 1, 2]
    When se aplica el algoritmo de ordenamiento
    Then el resultado debe ser [1, 2, 3]
```

**Herramientas:** Behave (Python), Cucumber (Java/Ruby)

---

## Buenas Prácticas

1. **Un test = una cosa** — cada test debe verificar una sola condición.
2. **Tests independientes** — los tests no deben depender del orden de ejecución.
3. **Nombres descriptivos** — `test_ordenar_lista_vacia_retorna_lista_vacia` es mejor que `test1`.
4. **Arrange-Act-Assert (AAA)** — estructura clara: preparar datos → ejecutar código → verificar resultado.
5. **Tests rápidos** — los tests lentos se dejan de correr. Mantén los unit tests en milisegundos.
6. **No testear implementación, testear comportamiento** — si cambias cómo funciona internamente pero el resultado es el mismo, el test no debería fallar.
7. **Tests deterministas** — un test siempre debe dar el mismo resultado bajo las mismas condiciones.

---

## Herramientas de Testing en Python

| Herramienta | Tipo | Descripción |
|---|---|---|
| `unittest` | Unit/Integration | Módulo estándar de Python, sin instalación extra |
| `pytest` | Unit/Integration | El más popular, muy flexible y con plugins |
| `mock` / `unittest.mock` | Mocking | Para crear mocks y stubs |
| `pytest-cov` | Coverage | Reporte de cobertura de código |
| `hypothesis` | Property-based | Genera casos de prueba automáticamente |
| `tox` | Automatización | Corre tests en múltiples versiones de Python |
| `Selenium` / `Playwright` | E2E | Automatización de browser para E2E |
| `locust` | Performance | Load testing en Python |

---

## Cómo correr los tests

```bash
# Correr todos los tests
pytest

# Correr un archivo específico
pytest tests.py

# Correr un test específico
pytest tests.py::test_bubble_sort_lista_normal

# Con salida detallada
pytest -v

# Con reporte de coverage
pytest --cov=. -v

# Parar al primer fallo
pytest -x
```

---

## Estructura recomendada de un proyecto

```
mi_proyecto/
├── src/
│   └── algoritmos.py       ← código fuente
├── tests/
│   ├── unit/
│   │   └── test_algoritmos.py
│   ├── integration/
│   │   └── test_db.py
│   └── e2e/
│       └── test_flujos.py
├── pytest.ini
└── requirements.txt
```
