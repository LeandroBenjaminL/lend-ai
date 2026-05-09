# Workflow: Python Environment

## Flujo principal

```
Orchestrator → [1. Elegir gestor] → [2. Crear entorno] → [3. Instalar dependencias] → [4. Congelar versiones] → [5. Verificar reproducibilidad] → [6. Documentar setup] → Orchestrator
```

## Paso a paso

### 1. Elegir gestor de entornos

Evaluar el proyecto y recomendar la herramienta correcta:

| Escenario | Herramienta | Motivo |
|---|---|---|
| Script simple, app web, pocas dependencias | **venv + pip** | Liviano, viene con Python, sin overhead |
| Data science, ML, paquetes con C (numpy, scipy, lightgbm) | **conda** | Maneja dependencias binarias que pip sufre para compilar |
| Librería/paquete que se va a publicar | **poetry** | Lockfile, build system integrado, publish a PyPI |
| Proyecto legacy con `setup.py` o `setup.cfg` | **venv + pip** en modo editable | Respetar el build system existente |

Preguntar si no está claro: ¿Qué stack usan? ¿Tiene dependencias binarias (numpy, scipy, tensorflow)? ¿Se va a distribuir como paquete?

### 2. Crear entorno

- **venv**: `python -m venv .venv` en la raíz del proyecto.
- **conda**: `conda create -n <nombre> python=<version>` con la versión exacta de Python que necesita el proyecto.
- **poetry**: `poetry init` si es proyecto nuevo, o `poetry install` si ya tiene `pyproject.toml`.

Nombre del entorno:
- Para `venv`: siempre `.venv/`.
- Para `conda`: nombre descriptivo del proyecto, sin espacios, en minúsculas con guiones: `mi-proyecto`, `churn-predictor`.
- Siempre agregar `.venv/` al `.gitignore` si no está.

Verificar creación: `python --version` y `which python` apuntan al entorno.

### 3. Instalar dependencias

- **Si existe `requirements.txt`**: `pip install -r requirements.txt`.
- **Si existe `environment.yml`**: `conda env update -f environment.yml`.
- **Si existe `pyproject.toml`**: `poetry install`.
- **Si no existe nada**: instalar una por una a pedido del usuario, siempre con versión mínima (`pandas>=2.0.0`).

Regla de oro: nunca `pip install <paquete>` a pelo sin versión ni entorno activo. Siempre preguntar: "¿ya activaste el entorno?"

### 4. Congelar versiones exactas

- **venv/pip**: `pip freeze > requirements.txt`.
- **conda**: `conda env export --no-builds > environment.yml` (sin builds para ser cross-platform).
- **poetry**: `poetry lock` (ya genera `poetry.lock` automático al instalar).

El archivo de lock DEBE quedar en el repo. Sin lockfile, no hay build determinístico.

### 5. Verificar que el entorno sea reproducible

- Revisar que `requirements.txt` tenga versiones exactas (`==`), no solo mínimas (`>=`).
- Para conda, verificar que `environment.yml` no tenga dependencias del sistema operativo que rompan cross-platform.
- Si es posible: recrear el entorno desde cero con los archivos generados para confirmar que funciona.
- Revisar `.gitignore`: `.venv/`, `.env`, `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`.

### 6. Documentar setup en README

Agregar (o actualizar) una sección de Setup en el README del proyecto con:

```markdown
## Setup

1. Crear entorno virtual:
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows

2. Instalar dependencias:
   pip install -r requirements.txt

3. Configurar variables de entorno:
   cp .env.example .env
   # Editar .env con tus credenciales
```

Para conda, mostrar el equivalente con `conda env create -f environment.yml`. Para poetry, con `poetry install`.

Si el proyecto usa `.env`, siempre mencionar `cp .env.example .env` — nunca documentar credenciales reales.
