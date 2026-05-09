---
name: python-environment
description: >
  Gestión de entornos Python para data science: conda, venv, pip, dependencias y variables de entorno.
  Trigger: Cuando necesitás crear o gestionar un entorno Python, instalar dependencias, o configurar variables de entorno para un proyecto.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T1-ultra-fast
---

# Skill: python-environment

## Para qué sirve

Gestionar entornos Python para que cada proyecto tenga sus propias dependencias sin romper otros proyectos. Si no usás entornos, eventualmente vas a tener conflictos de versiones que te van a hacer perder horas. Los entornos aíslan las dependencias de cada proyecto.

## Trigger (cuándo cargar esta skill)

- Estás arrancando un proyecto nuevo y necesitás configurar el entorno
- Te llega un proyecto con `environment.yml` o `requirements.txt`
- Necesitás compartir tu entorno con alguien más
- Tenés que configurar API keys y secretos sin hardcodearlos

## Workflow paso a paso

1. **Elegí el gestor**: `conda` para data science/ML, `venv` para proyectos livianos
2. **Creá el entorno**: `conda create -n proyecto python=3.11` o `python -m venv .venv`
3. **Activá el entorno**: siempre verificá que `which python` apunte al entorno correcto
4. **Instalá dependencias**: primero pandas/numpy con conda (optimizado), el resto con pip
5. **Exportá el entorno**: `conda env export > environment.yml` o `pip freeze > requirements.txt`
6. **Configurá variables de entorno**: creá un `.env` y agregalo al `.gitignore`

## Patrones esenciales

### 1. conda vs venv — cuándo usar cada uno

| Aspecto | conda | venv + pip |
|---------|-------|-----------|
| **Mejor para** | Data science, ML, numpy/scipy/pandas | Proyectos web, scripts, apps generales |
| **Gestiona** | Python + binarios C del sistema | Solo paquetes Python |
| **Tamaño** | +500 MB | ~20 MB |
| **Velocidad instalación** | Más lento (resuelve dependencias) | Rápido |
| **Reproducibilidad** | Excelente (resuelve versiones exactas) | Buena (pero a veces inconsistente) |

**¿Por qué conda para data science?** Porque paquetes como numpy, pandas, scikit-learn dependen de bibliotecas C compiladas (BLAS, LAPACK). `pip` a veces las instala mal o faltan optimizaciones. `conda` las resuelve con binarios pre-compilados y optimizados.

### 2. conda — flujo completo para data science

```bash
# Crear entorno con versión exacta de Python
conda create -n mi-proyecto python=3.11

# Activar
conda activate mi-proyecto

# Instalar con conda (preferí esto para data science)
conda install pandas numpy matplotlib seaborn scikit-learn jupyter

# Paquetes que no están en conda → usá pip (dentro del entorno activado)
pip install lightgbm plotly streamlit

# Exportar entorno reproducible
conda env export > environment.yml

# Recrear desde cero
conda env create -f environment.yml

# Limpiar
conda deactivate
conda env remove -n mi-proyecto
```

### 3. venv + pip — alternativa liviana

Ideal para cuando compartís el proyecto y no querés asumir que todos tienen conda.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
pip freeze > requirements.txt  # guardar versiones exactas
deactivate
```

### 4. requirements.txt bien armado

Especificá versiones mínimas con `>=` para que sea compatible, no versiones exactas (a menos que necesites reproducibilidad absoluta).

```txt
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
plotly>=5.15.0
streamlit>=1.25.0
python-dotenv>=1.0.0
sqlalchemy>=2.0.0
pyarrow>=12.0.0
lightgbm>=4.0.0
```

### 5. Variables de entorno — nunca hardcodees credenciales

Las API keys, passwords, y conexiones a DB nunca van en el código. Van en un `.env` que no se sube al repo.

```python
# .env (agregar al .gitignore!)
DB_HOST=localhost
DB_USER=leandro
DB_PASSWORD=pass_segura
API_KEY=sk-xxx

# En Python
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv('DB_HOST')
api_key = os.getenv('API_KEY')
```

## Alternativas

- **conda vs mamba**: `mamba` es un reemplazo directo de conda pero 10x más rápido para resolver dependencias. Instalalo con `conda install mamba -c conda-forge` y usá `mamba` en vez de `conda` para instalar.
- **Poetry / uv**: Herramientas modernas para gestión de dependencias. `uv` es increíblemente rápido (hecho en Rust). Probá `uv venv` y `uv pip install`.
- **Docker en vez de entornos**: Si necesitás reproducibilidad absoluta (misma versión de Python, mismas libs del sistema), Docker es la solución definitiva. El entorno va dentro del container.

## Anti-patrones

- ❌ **Trabajar en el Python base**: Instalar todo con `pip install` sin crear un entorno. Eventualmente dos proyectos van a pedir versiones distintas de la misma lib, y ahí empezaron los problemas.
- ❌ **requirements.txt sin versiones**: `pip freeze` da versiones exactas. Compartí esas, no un `requirements.txt` sin versiones que instala cualquier cosa.
- ❌ **Crear un entorno nuevo para cada mini-script**: Si tenés 20 carpetas con 20 entornos distintos, te vas a quedar sin espacio. Agrupá proyectos similares.
- ❌ **Subir `.env` al repo**: Es la forma más rápida de filtrar credenciales. Si ya lo hiciste, rotá las claves YA.
- ❌ **Olvidarse de activar el entorno**: Correr `pip install` y que se instale en el Python global. Siempre verificá con `which pip` o `pip list | grep paquete`.

## Comandos

```bash
# Diagnóstico rápido
python --version
which python
pip list | grep pandas

# Actualizar pip
python -m pip install --upgrade pip

# Ver qué entorno está activo
conda info --envs  # el activo tiene *
```
