# Patterns: Git Data Cheat Sheet

## .gitignore para Data Science

```gitignore
# === Datos (NUNCA versionar) ===
data/raw/
data/processed/
*.csv
*.parquet
*.xlsx
*.db
*.sqlite
*.feather

# === Modelos (van en git-lfs o DVC) ===
models/
*.pkl
*.joblib
*.h5
*.onnx

# === Entornos y cachés ===
.env
.venv/
env/
__pycache__/
*.pyc
.ipynb_checkpoints/
.mypy_cache/
.pytest_cache/
.dvc/cache/

# === Notebooks (si no usás nbstripout) ===
# *.ipynb

# === Reportes ===
reports/figures/
*.html

# === IDE ===
.vscode/
.idea/

# === Excepciones — sí versionar ===
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/samples/*.csv
!data/samples/*.parquet
```

## Git LFS para archivos grandes

```bash
# Instalar (una vez por máquina)
git lfs install

# Trackear por extensión
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.pkl"
git lfs track "*.joblib"
git lfs track "*.h5"
git lfs track "*.onnx"

# Trackear por carpeta
git lfs track "models/**"
git lfs track "data/processed/**"

# Commitear la config
git add .gitattributes
git commit -m "chore(lfs): configurar git-lfs para archivos de datos y modelos"

# Ver qué está trackeado
git lfs track

# Migrar archivos existentes a LFS
git lfs migrate import --include="*.csv,*.pkl" --everything
```

## DVC — Data Version Control

```bash
# Inicializar
dvc init
git add .dvc/
git commit -m "chore(dvc): inicializar DVC"

# Versionar un dataset
dvc add data/raw/ventas.csv
# Genera data/raw/ventas.csv.dvc (chico, se commitea)
# Agrega data/raw/ al .gitignore automáticamente

git add data/raw/ventas.csv.dvc data/raw/.gitignore
git commit -m "data(raw): agregar dataset de ventas Q1 2024"

# Configurar remote storage
dvc remote add -d myremote s3://mi-bucket/dvc
dvc remote add -d myremote gs://mi-bucket/dvc       # Google Cloud
dvc remote add -d myremote azure://mi-container/dvc  # Azure

git add .dvc/config
git commit -m "chore(dvc): configurar remote S3"

# Push de datos al remote
dvc push

# Pull cuando clonás el repo
git clone <repo-url>
dvc pull

# Pipeline DVC (reproducible)
dvc stage add -n prepare \
  -d src/data/prepare.py -d data/raw/ventas.csv \
  -o data/processed/ventas_clean.csv \
  python src/data/prepare.py

dvc repro  # ejecuta el pipeline completo
```

## Limpiar notebooks

```bash
# Hook automático (recomendado)
pip install nbstripout
nbstripout --install          # hook para TODO el repo
nbstripout --install --path notebooks/  # solo carpeta notebooks

# Manual (un archivo)
nbstripout notebook.ipynb

# Manual con nbconvert
jupyter nbconvert --ClearOutputPreprocessor.enabled=True \
  --to notebook notebook.ipynb

# Verificar que está limpio (útil en CI)
nbstripout --check notebooks/*.ipynb

# Para un solo notebook sin modificar el original
nbstripout --dry-run notebook.ipynb
```

## Conventional commits para data

```bash
# feat: nuevo análisis, feature, funcionalidad
git commit -m "feat(eda): análisis exploratorio del dataset de ventas"
git commit -m "feat(model): entrenar LightGBM con lag features"
git commit -m "feat(viz): agregar gráfico de correlaciones"

# fix: corrección de bug o error en datos
git commit -m "fix(cleaning): filtro de outliers usaba >= en lugar de >"
git commit -m "fix(pipeline): resolver duplicados en join de facturación"

# data: solo para samples o metadata (NUNCA el dataset completo)
git commit -m "data(samples): agregar muestra de 100 filas para tests"
git commit -m "data(metadata): actualizar referencias S3 en config"

# chore: configuración, herramientas, dependencias
git commit -m "chore(deps): actualizar pandas a 2.2.0"
git commit -m "chore(gitignore): ignorar *.feather y *.parquet"
git commit -m "chore(lfs): trackear modelos con git-lfs"

# docs: documentación
git commit -m "docs(readme): documentar estructura del repo"
git commit -m "docs(contributing): guía de conventional commits"

# refactor: mejora de código sin cambiar comportamiento
git commit -m "refactor(etl): extraer lógica de limpieza a módulo"
```

## Branching para experimentos

```bash
# Rama principal (producción/estable)
main

# Desarrollo
develop

# Features y experimentos
git checkout -b feat/eda-ventas
git checkout -b feat/model-lightgbm
git checkout -b feat/dashboard-tendencias

# Fixes
git checkout -b fix/cleaning-nulls
git checkout -b fix/pipeline-memory-leak

# Experimentos descartables (nunca mergean)
git checkout -b exp/prophet-vs-arima
git checkout -b exp/features- NLP

# Convención: exp/ son ramas de exploración que pueden morir
# feat/ son ramas que van a mergearse a develop/main
```

## Comandos de diagnóstico

```bash
# ¿Hay archivos grandes que no deberían commitearse?
find . -size +10M -not -path "./.git/*" -not -path "./.dvc/*"

# ¿Qué archivos de datos están en staging por error?
git diff --cached --name-only -- 'data/*' '*.csv' '*.parquet'
git reset HEAD data/  # deshacer si hay algo

# ¿El .gitignore está funcionando?
git check-ignore -v data/raw/ventas.csv

# ¿Cuánto pesa el repo? (para diagnosticar hinchazón)
git count-objects -vH

# Historial de cambios en notebooks (limpio gracias a nbstripout)
git log --oneline -- notebooks/

# ¿Qué ramas experimentales tengo sin mergear?
git branch --no-merged main

# Últimos commits con scope de datos
git log --oneline --grep="data\|model\|eda\|viz" -20
```

## Anti-patrones (lo que NUNCA hacés)

| ❌ Anti-patrón | ✅ Corrección |
|---|---|
| `git add .` sin revisar qué hay | `git status` primero, después `git add` quirúrgico |
| Commitear `data/raw/dataset.csv` (500 MB) | `.gitignore` + DVC o git-lfs |
| Notebook con 10,000 líneas de diff por outputs | `nbstripout --install` antes del primer commit |
| Commit "update" o "fix" sin contexto | Conventional commits: `feat(scope): descripción` |
| `models/modelo_final.pkl` commiteado | Git LFS: `git lfs track "*.pkl"` |
| Mezclar datos, código y notebooks en un solo commit masivo | Commits atómicos por scope |
| Rama `exp/modelo-raro` mergeada a main sin revisión | Las ramas `exp/` nunca mergean, solo informan |
| `.env` con credenciales commiteado | `.gitignore` + `.env.example` como template |
