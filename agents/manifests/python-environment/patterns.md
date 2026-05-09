# Patterns: Python Environment Cheat Sheet

## venv — creación y activación

```bash
# Crear
python -m venv .venv

# Activar (Linux/Mac)
source .venv/bin/activate

# Activar (Windows)
.venv\Scripts\activate

# Desactivar
deactivate

# Eliminar
rm -rf .venv
```

## conda — flujo completo

```bash
# Crear entorno con Python específico
conda create -n mi-proyecto python=3.11

# Activar
conda activate mi-proyecto

# Instalar paquetes (conda primero, pip después)
conda install pandas numpy matplotlib seaborn scikit-learn jupyter
pip install lightgbm  # solo lo que no está en conda

# Desactivar
conda deactivate

# Listar entornos
conda env list

# Eliminar
conda env remove -n mi-proyecto
```

## conda env — exportar e importar

```bash
# Exportar (sin builds para cross-platform)
conda env export --no-builds > environment.yml

# Exportar solo paquetes instalados explícitamente
conda env export --from-history > environment.yml

# Recrear desde archivo
conda env create -f environment.yml

# Actualizar entorno existente
conda env update -f environment.yml --prune
```

## pip freeze y requirements.txt

```bash
# Congelar versiones exactas
pip freeze > requirements.txt

# Instalar desde requirements
pip install -r requirements.txt

# Instalar sin cache (entornos CI/CD)
pip install -r requirements.txt --no-cache-dir

# Ver paquetes instalados
pip list
pip show pandas  # detalle de un paquete

# Actualizar pip
python -m pip install --upgrade pip
```

## poetry — flujo completo

```bash
# Inicializar proyecto nuevo
poetry init

# Agregar dependencia (registra en pyproject.toml + lockea)
poetry add pandas numpy matplotlib

# Agregar dependencia de desarrollo
poetry add --group dev pytest black ruff

# Instalar todo desde pyproject.toml + poetry.lock
poetry install

# Actualizar lockfile
poetry lock

# Activar shell del entorno
poetry shell

# Ejecutar comando dentro del entorno
poetry run python script.py
```

## Variables de entorno con python-dotenv

```bash
# Instalar
pip install python-dotenv
```

```python
# .env (NUNCA commitear — va al .gitignore)
DB_HOST=localhost
DB_PORT=5432
API_KEY=sk-abc123
DEBUG=true

# En Python
from dotenv import load_dotenv
import os

load_dotenv()  # busca .env en el directorio actual

db_host = os.getenv('DB_HOST', 'localhost')
api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'false').lower() == 'true'
port = int(os.getenv('DB_PORT', '5432'))
```

## .gitignore mínimo para entornos Python

```gitignore
# Entorno virtual
.venv/
venv/
env/

# Variables de entorno (CREDENCIALES)
.env
*.env

# Python cache
__pycache__/
*.pyc
*.pyo

# Jupyter
.ipynb_checkpoints/

# Dependencias compiladas
*.egg-info/
dist/
build/

# OS
.DS_Store
Thumbs.db
```

## .env.example — plantilla sin secretos

```bash
# .env.example — commitear este, NO el .env real
DB_HOST=localhost
DB_PORT=5432
DB_USER=tu_usuario
DB_PASSWORD=cambiar_esto
API_KEY=tu_api_key
DEBUG=false
```

El `README` debe decir `cp .env.example .env` y editar.

## Verificación de entorno

```bash
# ¿Qué Python estoy usando?
which python
python --version

# ¿Está activo el venv/conda?
echo $VIRTUAL_ENV        # venv: muestra path si está activo
echo $CONDA_DEFAULT_ENV   # conda: muestra nombre del entorno

# ¿Qué paquetes y versiones?
pip list --format=freeze
conda list
```

## Resolución de problemas frecuentes

| Problema | Causa probable | Solución |
|---|---|---|
| `pip` instala en el sistema, no en el venv | Entorno no activado | `source .venv/bin/activate` primero |
| `conda` no encuentra el paquete | No está en defaults ni conda-forge | `conda install -c conda-forge <paquete>` |
| Error de compilación C (numpy, scipy) | Faltan build tools del sistema | Usar conda, o instalar build-essential/python-dev |
| `pip freeze` muestra paquetes del sistema | Venv creado con `--system-site-packages` | Recrear sin ese flag |
| `ModuleNotFoundError` en otra máquina | `requirements.txt` no congelado | `pip freeze > requirements.txt` y commitearlo |
| `.env` no se carga | `load_dotenv()` no se llamó, o path incorrecto | `load_dotenv('/ruta/absoluta/.env')` |
