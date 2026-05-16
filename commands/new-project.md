---
description: Scaffold completo para empezar un proyecto de datos desde cero
agent: data-analyst
subtask: true
---

Creá la estructura completa de un proyecto de datos nuevo.

FLUJO:
1. Preguntá el nombre del proyecto
2. Preguntá: fuente de datos, tipo de análisis, herramientas
3. Scaffold:
   ```
   {nombre}/
   ├── data/
   │   ├── raw/          # Datos originales (read-only)
   │   └── processed/    # Datos limpios
   ├── notebooks/        # Exploración y análisis
   ├── src/              # Código reutilizable
   │   ├── etl.py
   │   ├── features.py
   │   └── viz.py
   ├── tests/
   ├── reports/
   ├── requirements.txt
   ├── .env
   ├── .gitignore
   └── README.md
   ```
4. Inicializá git
5. Creá entorno virtual con python-environment skill
6. Instalá dependencias base
7. Mostrá resumen

SKILLS A CARGAR:
- python-environment
- git-data

REGLAS:
- Preguntá antes de crear archivos
- No sobrescribas directorios existentes
- Explicá para qué sirve cada carpeta/archivo

## Uso

`/new-project lending-model`

`/new-project customer-churn --source postgres --type classification`

## Ejemplo

Input: `/new-project churn-predictor`

Output:
```
🚀 Proyecto creado: churn-predictor/

churn-predictor/
├── data/raw/          # Lectura de DB -> raw
├── data/processed/    # Datos limpios
├── notebooks/         # EDA + modelado
├── src/
│   ├── etl.py         # Extracción desde DB
│   ├── features.py    # Feature engineering
│   └── viz.py         # Visualizaciones
├── tests/
├── reports/
├── .env               # Variables de entorno
├── .gitignore
└── README.md

✅ git init
✅ Entorno virtual creado
✅ pandas, scikit-learn, matplotlib instalados
```
