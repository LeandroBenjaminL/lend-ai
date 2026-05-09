# Workflow: Git Data

## Flujo principal

```
Orchestrator → [1. Configurar .gitignore] → [2. Estructurar repo] → [3. Estrategia de datos grandes] → [4. Commitear limpio] → [5. CI/CD si necesario] → Orchestrator
```

## Paso a paso

### 1. Configurar .gitignore para data science

Este paso es primero y no negociable. Antes de que exista un solo commit, el `.gitignore` tiene que estar listo.

**Qué SIEMPRE va ignorado:**

```
# Datos — Git es para código, no para datos
data/raw/
data/processed/
*.csv
*.parquet
*.xlsx
*.db
*.sqlite
*.feather

# Modelos entrenados — van en git-lfs o DVC, nunca directo
models/
*.pkl
*.joblib
*.h5
*.onnx

# Entornos y cachés
.env
.venv/
env/
__pycache__/
*.pyc
.ipynb_checkpoints/
.mypy_cache/
.pytest_cache/

# Notebooks con outputs
*.ipynb  # si usás nbstripout, lo manejás con hooks. Si no, ignorá los .ipynb

# Reportes generados
reports/figures/
*.html

# Datos de IDE
.vscode/
.idea/
```

**Qué SÍ se versiona (excepciones):**

```gitignore
# Excepciones — sí versionar
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/samples/*.csv
!data/samples/*.parquet
```

**Verificación obligatoria después de crear el .gitignore:**

```bash
# Verificar que archivos grandes no van a colarse
find . -size +10M -not -path "./.git/*" -not -path "./.venv/*"
# Confirmar que el .gitignore reconoce los archivos correctos
git check-ignore -v data/raw/ventas.csv
```

### 2. Estructurar el repo correctamente

La estructura no es decorativa — es un contrato con el equipo. Todo el mundo sabe dónde van las cosas.

```
proyecto-data/
├── data/
│   ├── raw/              # Datos originales — NUNCA se tocan, NUNCA se commitean
│   ├── processed/        # Datos limpios/transformados
│   └── samples/          # Muestras chicas para tests (sí se commitean)
├── notebooks/            # Exploración y prototipado
│   ├── 01-exploracion.ipynb
│   └── 02-modelado.ipynb
├── src/                  # Código reutilizable (módulos Python)
│   ├── data/             # Carga y preprocesamiento
│   ├── features/         # Feature engineering
│   ├── models/           # Entrenamiento y predicción
│   └── visualization/    # Visualizaciones reutilizables
├── models/               # Modelos entrenados (versionados con DVC/git-lfs)
├── reports/              # Reportes generados (HTML, PDF, Markdown)
│   └── figures/          # Gráficos exportados
├── tests/                # Tests unitarios y de integración
├── config/               # Archivos de configuración (YAML, JSON, TOML)
├── requirements.txt      # Dependencias congeladas
├── environment.yml       # Si usás conda
├── .gitignore
├── .gitattributes        # Configuración de git-lfs
├── .dvc/                 # Configuración de DVC (si aplica)
├── dvc.yaml              # Pipeline de DVC (si aplica)
├── README.md
├── Makefile              # Comandos comunes (opcional pero recomendado)
└── pyproject.toml        # Configuración del proyecto
```

**Decisiones clave al estructurar:**
- `data/raw/` y `data/processed/` tienen `.gitkeep` para que los directorios existan en el repo sin los datos.
- `data/samples/` es para datasets de prueba chicos (<1 MB) que sí se commitean. Ideal para tests y CI.
- `notebooks/` va separado de `src/` para marcar la diferencia entre exploración y código de producción.
- Si el proyecto es puramente notebooks y no va a producción, `src/` puede ser opcional.

### 3. Decidir estrategia para datos grandes

No hay una sola respuesta correcta. La decisión depende del tamaño, frecuencia de cambio, y contexto del proyecto.

**Árbol de decisión:**

```
¿El archivo de datos pesa más de 100 MB?
├── NO  → Commitealo normalmente (pero ojo con samples, mejor usar data/samples/)
└── SÍ  → ¿Necesitás versionado semántico de datos (trackear qué dataset usó cada experimento)?
          ├── NO  → git-lfs
          │        - git lfs track "*.csv" "*.parquet" "*.pkl"
          │        - git add .gitattributes
          │        - git commit -m "chore: configurar git-lfs"
          │        - Ideal para datasets <1 GB que cambian poco
          │        - Límite: storage depende del plan de GitHub/GitLab
          │
          └── SÍ  → DVC (Data Version Control)
                   - dvc init
                   - dvc add data/raw/dataset.csv
                   - git add data/raw/.gitignore data/raw/dataset.csv.dvc
                   - dvc remote add -d myremote s3://bucket/dvc-store
                   - dvc push
                   - Ideal para pipelines de ML con experimentos
                   - Los archivos .dvc son chicos, se commitean. Los datos van al remote.
```

**Cuándo usar storage externo sin DVC:**
- Datasets >10 GB que ya están en S3/GCS con versionado propio.
- Solución: guardar referencias (URLs, paths) en un archivo de configuración versionado (ej: `config/datasets.yaml`).
- Ejemplo: `datasets: { ventas_2024: "s3://mi-bucket/datasets/ventas/2024/v3.parquet" }`

**Comandos de verificación:**

```bash
# Antes de commitear, chequear que no hay archivos grandes
find . -size +10M -not -path "./.git/*" -not -path "./.dvc/*"
# Si encontrás algo >10M, este paso falla. Volvé a decidir estrategia.
```

### 4. Commitear código y notebooks limpios

El commit es el momento de la verdad. Acá se define si el repo es mantenible o un basurero.

**Pre-commit: limpieza obligatoria de notebooks.**

```bash
# Instalar nbstripout (una sola vez por repo)
pip install nbstripout
nbstripout --install  # configura el hook de pre-commit automáticamente

# O limpiar manualmente si no querés el hook
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to notebook notebook.ipynb
```

**Conventional commits con scope de datos:**

```
# Formato: tipo(scope): descripción

# Features (nuevo análisis, funcionalidad)
feat(eda): análisis exploratorio del dataset de ventas Q1
feat(model): entrenar LightGBM con features de fecha
feat(viz): agregar dashboard de tendencias mensuales

# Fixes (correcciones)
fix(cleaning): corregir imputación de nulos en columna precio
fix(pipeline): resolver race condition en ETL de facturación
fix(notebook): eliminar outputs commiteados por error

# Datos (solo samples o metadata)
data(samples): agregar muestra de 100 filas para tests
data(metadata): actualizar referencias de datasets en config

# Chore (configuración, herramientas)
chore(gitignore): agregar *.parquet y *.feather
chore(lfs): configurar git-lfs para modelos entrenados
chore(dvc): inicializar DVC y configurar remote S3

# Docs
docs(readme): documentar estructura del repo y flujo de datos
```

**Qué NUNCA commitear (checklist mental antes de cada `git add`):**
- [ ] ¿Hay archivos >1 MB que no sean código? → No commitees, evaluá git-lfs/DVC.
- [ ] ¿Las notebooks tienen outputs, imágenes, o metadata de ejecución? → Corré nbstripout primero.
- [ ] ¿Hay archivos de entorno (.env, .venv/)? → Ya deberían estar en .gitignore.
- [ ] ¿Commiteaste `data/raw/` o `data/processed/`? → `git reset HEAD data/` urgente.
- [ ] ¿El mensaje de commit explica el "por qué" y no solo el "qué"? → Si no, reescribilo.

### 5. Configurar CI/CD si necesario

No todo proyecto de datos necesita CI/CD, pero si el código va a producción o hay equipo, es invaluable.

**Qué validar en CI (GitHub Actions / GitLab CI):**

```yaml
# .github/workflows/data-ci.yml (ejemplo conceptual)
name: Data Project CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint Python
        run: |
          pip install ruff
          ruff check src/ tests/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/ -v

  check-large-files:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Reject large files
        run: |
          FILES=$(find . -size +5M -not -path "./.git/*" -not -path "./.dvc/*")
          if [ -n "$FILES" ]; then
            echo "ERROR: Archivos grandes detectados:"
            echo "$FILES"
            echo "Usá git-lfs o DVC para archivos >5MB."
            exit 1
          fi

  nb-clean:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check notebook cleanliness
        run: |
          pip install nbstripout
          nbstripout --check notebooks/*.ipynb
```

**Cuándo SÍ configurar CI/CD:**
- Hay más de una persona tocando el código.
- El código de `src/` se usa en producción o pipelines automáticos.
- Querés evitar que alguien commitee un dataset de 200 MB por accidente (el job `check-large-files` es tu firewall).
- Las notebooks necesitan control de calidad automatizado.

**Cuándo NO es necesario:**
- Proyecto exploratorio de una sola persona.
- Análisis ad-hoc que no va a mantenerse en el tiempo.
- Prototipo rápido donde la velocidad importa más que la rigurosidad.

En esos casos, alcanza con un buen `.gitignore` y disciplina manual.
