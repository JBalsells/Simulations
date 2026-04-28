# Guía de Configuración y Serialización de Datos

## ¿Qué es la serialización de datos?

**Serializar** significa convertir una estructura de datos en memoria (un objeto, diccionario, lista) a un formato que se pueda guardar en disco o transmitir por red. **Deserializar** es el proceso inverso: leer ese formato y reconstruir la estructura en memoria.

```
[Objeto en memoria]  →  serializar  →  [Texto/Bytes en archivo o red]
[Texto en archivo]   →  deserializar →  [Objeto en memoria]
```

Los formatos más usados para esto son **JSON, YAML, XML, TOML e INI**.

---

## ¿Por qué separar la configuración del código?

Mezclar valores de configuración dentro del código fuente es un antipatrón conocido como **hardcoding**. Los problemas que genera:

- Tienes que recompilar o editar código para cambiar un parámetro.
- Las credenciales (contraseñas, API keys) quedan expuestas en el repositorio.
- No puedes usar el mismo código en distintos entornos (dev, staging, prod) sin modificarlo.

La solución es externalizar la configuración:

```
# ❌ Hardcoded
DB_HOST = "192.168.1.10"
DB_PORT = 5432
API_KEY = "sk-abc123"

# ✅ Desde archivo de configuración
config = cargar_config("config.yaml")
DB_HOST = config["database"]["host"]
```

---

## Formatos de Configuración y Serialización

### JSON — JavaScript Object Notation

El formato más universal. Nació en el mundo JavaScript pero hoy se usa en absolutamente todo: APIs REST, archivos de configuración, bases de datos NoSQL.

**Sintaxis:**
```json
{
  "nombre": "mi-app",
  "version": "1.0.0",
  "debug": false,
  "puerto": 8080,
  "base_de_datos": {
    "host": "localhost",
    "puerto": 5432,
    "nombre": "produccion_db"
  },
  "servicios_permitidos": ["auth", "pagos", "notificaciones"],
  "limites": {
    "max_conexiones": 100,
    "timeout_segundos": 30.5
  }
}
```

**Tipos de datos soportados:**
| Tipo | Ejemplo |
|------|---------|
| String | `"hola mundo"` |
| Number | `42`, `3.14` |
| Boolean | `true`, `false` |
| Null | `null` |
| Array | `[1, 2, 3]` |
| Object | `{"clave": "valor"}` |

**Limitaciones:**
- No soporta comentarios (gran queja de la comunidad)
- Verbose para configuraciones muy anidadas
- Las comas finales en listas/objetos son inválidas

**En Python:**
```python
import json

# Leer
with open("config.json") as f:
    config = json.load(f)

# Escribir
with open("output.json", "w") as f:
    json.dump(datos, f, indent=2)

# Desde/hacia string
texto = json.dumps({"clave": "valor"})
datos = json.loads(texto)
```

---

### YAML — YAML Ain't Markup Language

Diseñado para ser lo más legible posible por humanos. Es el estándar de facto para configuración de herramientas DevOps (Docker, Kubernetes, GitHub Actions, Ansible).

**Sintaxis:**
```yaml
# Los comentarios sí son válidos en YAML
nombre: mi-app
version: "1.0.0"
debug: false
puerto: 8080

base_de_datos:
  host: localhost
  puerto: 5432
  nombre: produccion_db
  credenciales:
    usuario: admin
    password: secreto  # ⚠️ nunca hardcodear passwords reales

servicios_permitidos:
  - auth
  - pagos
  - notificaciones

limites:
  max_conexiones: 100
  timeout_segundos: 30.5

# Texto multilínea
descripcion: |
  Esta es una descripción larga
  que ocupa múltiples líneas
  y se preservan los saltos.

# Texto en una línea (colapsa saltos)
resumen: >
  Este texto largo
  se convierte en una sola línea.
```

**Tipos de datos soportados:**
| Tipo | Ejemplo |
|------|---------|
| String | `"hola"` o `hola` (sin comillas) |
| Integer | `42` |
| Float | `3.14` |
| Boolean | `true`/`false` o `yes`/`no` |
| Null | `null` o `~` |
| Lista | `- item` (indentada) o `[a, b, c]` |
| Mapa | `clave: valor` |
| Multilínea | `\|` (literal) o `>` (folded) |

**Reglas críticas:**
- La **indentación con espacios** (no tabs) define la jerarquía.
- Un espacio de más o de menos rompe el archivo.
- Las cadenas con caracteres especiales (`:`, `#`, etc.) deben ir entre comillas.

**En Python:**
```python
import yaml  # pip install pyyaml

# Leer
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Escribir
with open("output.yaml", "w") as f:
    yaml.dump(datos, f, default_flow_style=False, allow_unicode=True)
```

> Siempre usar `yaml.safe_load()` en lugar de `yaml.load()` para evitar vulnerabilidades de ejecución de código arbitrario.

---

### XML — eXtensible Markup Language

El formato más antiguo y verbose de todos. Fue el estándar dominante antes de JSON. Hoy sigue siendo muy usado en sistemas empresariales, configuraciones Java (Maven, Spring), SOAP APIs, y documentos de Office.

**Sintaxis:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<aplicacion>
  <nombre>mi-app</nombre>
  <version>1.0.0</version>
  <debug>false</debug>
  <puerto>8080</puerto>

  <base_de_datos>
    <host>localhost</host>
    <puerto>5432</puerto>
    <nombre>produccion_db</nombre>
  </base_de_datos>

  <servicios_permitidos>
    <servicio>auth</servicio>
    <servicio>pagos</servicio>
    <servicio>notificaciones</servicio>
  </servicios_permitidos>

  <!-- Atributos también son válidos -->
  <limites max_conexiones="100" timeout_segundos="30.5" />
</aplicacion>
```

**Características únicas de XML:**
- **Esquemas (XSD)**: puedes validar que el XML cumple una estructura específica.
- **Namespaces**: evitan conflictos entre etiquetas de distintas fuentes.
- **XPath**: lenguaje de consulta para navegar el documento.
- **XSLT**: transformar XML en otros formatos (HTML, CSV, etc.).

**En Python:**
```python
import xml.etree.ElementTree as ET

# Leer
tree = ET.parse("config.xml")
root = tree.getroot()
host = root.find("base_de_datos/host").text

# Con lxml (más potente)
from lxml import etree
tree = etree.parse("config.xml")
hosts = tree.xpath("//base_de_datos/host/text()")
```

---

### TOML — Tom's Obvious Minimal Language

Creado por Tom Preston-Werner (cofundador de GitHub). Diseñado para ser más simple que YAML y más legible que JSON. Es el formato oficial de configuración de **Rust (Cargo.toml)** y Python (pyproject.toml).

**Sintaxis:**
```toml
# Comentarios válidos como en YAML
nombre = "mi-app"
version = "1.0.0"
debug = false
puerto = 8080

[base_de_datos]
host = "localhost"
puerto = 5432
nombre = "produccion_db"

[limites]
max_conexiones = 100
timeout_segundos = 30.5

[[servicios]]  # lista de objetos
nombre = "auth"
activo = true

[[servicios]]
nombre = "pagos"
activo = true
```

**En Python (3.11+):**
```python
import tomllib  # módulo estándar desde Python 3.11

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
```

---

### INI / CFG

El formato más simple y antiguo. Usado por Python (`configparser`), Windows, y muchas herramientas legacy.

```ini
[aplicacion]
nombre = mi-app
version = 1.0.0
debug = false

[base_de_datos]
host = localhost
puerto = 5432
nombre = produccion_db

[limites]
max_conexiones = 100
```

**En Python:**
```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
host = config["base_de_datos"]["host"]
```

---

## Comparativa de Formatos

| Característica | JSON | YAML | XML | TOML | INI |
|---|---|---|---|---|---|
| Comentarios | ❌ | ✅ | ✅ | ✅ | ✅ |
| Legibilidad humana | Media | Alta | Baja | Alta | Alta |
| Anidamiento | ✅ | ✅ | ✅ | Limitado | ❌ |
| Tipado | Básico | Básico | Ninguno | Básico | Todo string |
| Esquemas/Validación | JSON Schema | JSON Schema | XSD | ❌ | ❌ |
| Verbosidad | Media | Baja | Muy alta | Baja | Muy baja |
| Uso principal | APIs, configs | DevOps, configs | Empresarial | Rust/Python | Legacy |
| Módulo Python | `json` (stdlib) | `pyyaml` (pip) | `xml` (stdlib) | `tomllib` (3.11+) | `configparser` (stdlib) |

---

## Variables de Entorno

Para configuración sensible (passwords, API keys), las variables de entorno son la práctica estándar. Nunca se guardan en el repositorio.

```python
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # carga desde archivo .env (solo para desarrollo)

DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
API_KEY = os.getenv("API_KEY", "valor_por_defecto")
```

Archivo `.env` (agregar al `.gitignore`):
```
DATABASE_PASSWORD=mi_password_secreto
API_KEY=sk-abc123xyz
```

---

## Infrastructure as Code (IaC)

Infrastructure as Code es la práctica de **definir y gestionar infraestructura** (servidores, redes, bases de datos, contenedores) usando archivos de configuración en lugar de hacerlo manualmente.

**Beneficios:**
- La infraestructura es reproducible y versionada en git
- Se puede desplegar el mismo entorno en cualquier lugar
- Los cambios son auditables (quién cambió qué y cuándo)
- Elimina el "en mi máquina funciona"

---

### Docker Compose (YAML)

Define y orquesta múltiples contenedores Docker para un entorno local o de staging.

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql://postgres:password@db:5432/mydb
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

```bash
# Levantar todo el stack
docker compose up -d

# Ver logs
docker compose logs -f web

# Apagar
docker compose down
```

---

### Kubernetes (YAML)

Define cómo se despliegan aplicaciones en un cluster de Kubernetes.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-api
  labels:
    app: mi-api
spec:
  replicas: 3                    # 3 instancias corriendo
  selector:
    matchLabels:
      app: mi-api
  template:
    metadata:
      labels:
        app: mi-api
    spec:
      containers:
        - name: mi-api
          image: mi-usuario/mi-api:v1.2.0
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:    # la password viene de un Secret, no hardcodeada
                  name: db-secret
                  key: url
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:         # Kubernetes reinicia el contenedor si falla
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: mi-api-service
spec:
  selector:
    app: mi-api
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

---

### GitHub Actions (YAML)

Define pipelines de CI/CD que se ejecutan automáticamente en cada push o pull request.

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpassword
        options: >-
          --health-cmd pg_isready
          --health-interval 10s

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Instalar dependencias
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Correr tests
        run: pytest --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:testpassword@localhost/testdb

      - name: Publicar cobertura
        uses: codecov/codecov-action@v3

  deploy:
    needs: test              # solo se ejecuta si los tests pasan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy a producción
        run: echo "Aquí iría el comando de deploy"
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}   # secreto guardado en GitHub
```

---

### Terraform (HCL)

Terraform usa su propio formato HCL (muy similar a YAML/JSON) para definir infraestructura en la nube.

```hcl
# main.tf — crear una instancia EC2 en AWS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "servidor_web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_type

  tags = {
    Name        = "servidor-web-prod"
    Environment = "production"
  }
}

variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.micro"
}
```

```bash
terraform init      # descargar providers
terraform plan      # previsualizar cambios
terraform apply     # aplicar cambios
terraform destroy   # eliminar todo
```

---

### Ansible (YAML)

Automatiza la configuración de servidores remotos.

```yaml
# playbook.yml
---
- name: Configurar servidor web
  hosts: servidores_web
  become: true              # ejecutar como sudo

  vars:
    app_port: 8000
    app_dir: /opt/mi-app

  tasks:
    - name: Instalar Python y pip
      apt:
        name:
          - python3
          - python3-pip
        state: present
        update_cache: true

    - name: Copiar código de la aplicación
      copy:
        src: ./src/
        dest: "{{ app_dir }}"
        owner: www-data

    - name: Instalar dependencias Python
      pip:
        requirements: "{{ app_dir }}/requirements.txt"

    - name: Iniciar servicio
      systemd:
        name: mi-app
        state: started
        enabled: true
```

---

## Buenas Prácticas

1. **Nunca hardcodear secrets** — passwords, API keys, tokens siempre en variables de entorno o gestores de secretos (Vault, AWS Secrets Manager).
2. **Versionar la configuración en git** — pero nunca los secretos.
3. **Un archivo de configuración por entorno** — `config.dev.yaml`, `config.prod.yaml`.
4. **Validar la configuración al inicio** — si falta una clave requerida, fallar rápido con un mensaje claro.
5. **Documentar las claves de configuración** — especialmente las no obvias.
6. **Usar `.gitignore`** para `.env`, `*.local.yaml`, archivos con credenciales.
7. **Proveer valores por defecto** para configuraciones opcionales.

```
# .gitignore
.env
.env.local
config.local.yaml
secrets/
```
