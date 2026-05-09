---
name: git-data
description: >
  Git y GitHub para proyectos de datos: .gitignore, manejo de archivos grandes, flujo de trabajo con notebooks y datasets.
  Trigger: Cuando trabajás con git en proyectos de data science, commitás notebooks, manejás datasets con versionado, o configurás un repo de datos.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T1-ultra-fast
---

# Skill: git-data

## Para qué sirve

Usar git en proyectos de datos sin volverse loco. Los proyectos de data science tienen necesidades especiales: notebooks que cambian todo el tiempo, datasets que no deberías versionar, modelos binarios, y archivos enormes. Esta skill te da el setup correcto para que git te ayude, no te estorbe.

## Trigger (cuándo cargar esta skill)

- Estás creando un repo nuevo de data science y querés la estructura correcta
- Te pasó que un notebook commitado tiene 20 MB de outputs basura
- Necesitás versionar datasets pero son demasiado grandes para git normal
- Querés establecer una convención de commits para tu equipo de datos

## Workflow paso a paso

1. **Creá el `.gitignore` primero** — antes del primer commit, no después. Así evitas subir basura accidentalmente.
2. **Estructurá el repo**: separá datos crudos, procesados, notebooks, src, modelos.
3. **Configurá `nbstripout`** para que los notebooks se commiteen sin outputs.
4. **Decidí qué hacer con los datos**: ¿Git LFS para datasets chicos? ¿DVC para grandes? ¿Nada y solo código?
5. **Primer commit**: solo estructura, `.gitignore`, y `README.md`.
6. **Usá commits semánticos**: que el mensaje diga QUÉ cambió y POR QUÉ.

## Patrones esenciales

### 1. .gitignore para data science

Lo más importante: los datos crudos no se versionan. Ocupan mucho, cambian poco, y si son pesados rompen el repo. Solo se versiona código, config, y muestras pequeñas.

```gitignore
# Datos — nunca versionar datos crudos grandes
data/raw/
data/processed/
*.csv
*.parquet
*.xlsx
*.db
*.sqlite

# Modelos entrenados — binarios pesados
models/
*.pkl
*.joblib
*.h5

# Entornos y archivos sensibles
.env
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/

# Reportes generados (se regeneran al ejecutar)
reports/figures/
*.html

# Excepciones — sí versionar muestras y estructuras
!data/raw/.gitkeep
!data/processed/.gitkeep
!data/samples/*.csv
```

### 2. nbstripout — limpiar notebooks automáticamente

Los notebooks guardan outputs (gráficos, tablas) como JSON. Un `df.head()` de 10 MB queda en el historial para siempre. `nbstripout` los limpia en cada commit automáticamente.

```bash
pip install nbstripout
nbstripout --install  # git filter automático

# O manual
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to notebook nb.ipynb --inplace
```

**¿Por qué automático?** Si lo configurás como git filter, nunca te olvidás. Si lo hacés a mano, un descuido y tenés 50 MB de outputs en el repo para siempre.

### 3. Estructura de repo de datos

```
proyecto-data/
├── data/
│   ├── raw/          # datos originales — nunca tocar
│   ├── processed/    # datos limpios y transformados
│   └── samples/      # muestras chicas para tests y desarrollo
├── notebooks/        # exploración, análisis, experimentos
├── src/              # código reutilizable (funciones, clases)
├── models/           # modelos entrenados (o .gitkeep)
├── reports/          # reportes y figuras generadas
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

### 4. Git LFS para archivos grandes

Si necesitás versionar datasets o modelos (por ej, para reproducibilidad), Git LFS reemplaza el contenido del archivo con un puntero y guarda el binario en un storage externo.

```bash
git lfs install
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.pkl"
git lfs track "*.h5"

# Commitear .gitattributes (define qué trackea LFS)
git add .gitattributes
git commit -m "chore: configurar git lfs para archivos de datos"
```

### 5. Commits semánticos

El mensaje cuenta una historia. Usá prefijos para entender el tipo de cambio sin leer el diff.

```bash
git commit -m "feat(eda): análisis exploratorio de ventas"
git commit -m "fix(cleaning): corregir imputación de nulos en precio"
git commit -m "data(raw): agregar dataset Q1 2024"
git commit -m "model(lgbm): entrenar con features nuevas"
git commit -m "viz(dashboard): gráfico de tendencias mensuales"
```

## Alternativas

- **Git LFS vs DVC**: DVC ([Data Version Control](https://dvc.org)) está diseñado específicamente para ML/data. Te deja versionar datasets, modelos, y métricas, y los almacena en S3/GDrive/SSH. Es más flexible que Git LFS para proyectos de datos grandes.
- **nbstripout vs jupyter Lab + git**: Si usás Jupyter Lab, hay extensiones para limpiar outputs antes de guardar. Pero `nbstripout` es más confiable porque es automático.
- **git flow vs trunk-based**: En proyectos de datos chicos (1-3 personas), trunk-based development con branches por feature alcanza. git flow es overkill.

## Anti-patrones

- ❌ **Commitear notebooks con outputs**: Ocupan espacio, ensucian el diff, y si contienen datos sensibles los exponés para siempre. Siempre usá `nbstripout`.
- ❌ **Commitear datasets grandes sin LFS**: Un CSV de 200 MB en el historial de git hace que clonar el repo sea eterno. Usá LFS, DVC, o no los versiones.
- ❌ **.gitignore hecho después del primer commit**: Si ya commiteaste archivos grandes, sacarlos del historial requiere `git filter-branch` o `bfg-repo-cleaner`. Hacé el `.gitignore` antes del primer commit.
- ❌ **Mensajes de commit genéricos**: "cambios" o "update" no le sirven a nadie. En 3 meses no sabés qué cambió sin leer el diff entero.
- ❌ **Versionar `.env` o credenciales**: Una vez que subís una API key a GitHub, asumila comprometida. Rotala ya.

## Comandos

```bash
# Ver archivos grandes que no deberías subir
find . -size +10M -not -path "./.git/*"

# Verificar qué va a ignorar .gitignore
git check-ignore -v data/raw/ventas.csv

# Ver solo cambios en notebooks
git log --oneline -- notebooks/

# Sacar archivos del staging
git reset HEAD data/
```
