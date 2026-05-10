---
name: shared-git-data
description: >
  Git para proyectos de datos — versionado de notebooks, datasets, y
  pipelines. Estrategias para mantener el repo limpio.
  Trigger: Cuando trabajás con git en proyectos de data science, commitás notebooks, manejás datasets con versionado, o configurás un repo de datos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T1-ultra-fast
---

# Skill: shared-git-data

Git para data science. No es como git para código.

## Trigger

- Arrancás un proyecto de datos y creás el repo
- Vas a commitear un notebook y no querés mandar outputs al pedo
- El dataset debería estar en el repo o no?
- Necesitás versionar pipelines sin versionar datos pesados

## Workflow LEND

```
1. ANALIZAR
   ├── Proyecto: ¿análisis, pipeline, dashboard?
   ├── Datos: ¿cuánto pesan? ¿pueden ir al repo? (< 100MB)
   ├── Notebooks: ¿outputs incluidos o limpios?
   └── Colaboración: ¿sos vos solo o trabajan varios?

2. OFRECER (Menú del Senior)
   ├── A) Git estándar — código + notebooks limpios + datos chicos (< 100MB)
   ├── B) Git + DVC — datos grandes versionados pero no en el repo
   └── C) Git + nbstripout — notebooks sin outputs, limpios para diff

3. ELEGIR → confirmación

4. HACER
   ├── .gitignore: .venv/, __pycache__/, *.pyc, .env, data/raw/
   ├── nbstripout: git config filter.nbstripout.extrakeys 'metadata.kernel'
   ├── DVC: dvc init + dvc add data/raw/dataset.csv + git add data/raw/dataset.csv.dvc
   ├── README.md con instrucciones para reproducir
   ├── requirements.txt congelado
   └── Commits descriptivos: "feat: agrego modelo de churn" no "update"

5. VERIFICAR
   ├── .gitignore cubre lo que no debe estar en el repo
   ├── Los notebooks se pueden diffear (sin outputs)
   └── Un git clone + pip install es suficiente para arrancar
```

## Patrones

- **Código en git, datos fuera**: datasets > 100MB no van al repo. DVC o S3.
- **Notebooks sin outputs**: nbstripout para que los diffs sean legibles.
- **.gitignore estricto**: .venv, __pycache__, .env, data/raw, .ipynb_checkpoints.
- **README que funciona**: cualquiera clona, instala y corre.
- **Commits semánticos**: feat:, fix:, chore:, docs:, refactor:.

## Anti-patrones

- ❌ Committear datasets de 500MB — el repo pesa una tonelada
- ❌ Notebooks con outputs en git — diff ilegible de 10k líneas JSON
- ❌ No tener .gitignore — .venv, __pycache__ y .env terminan en el repo
- ❌ Mensajes de commit vagos — "cambios", "update", "fix"
- ❌ README vacío — nadie sabe cómo arrancar el proyecto
