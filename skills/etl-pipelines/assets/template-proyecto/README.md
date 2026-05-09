# {nombre-del-proyecto}

## Descripción
{Breve descripción del análisis}

## Estructura

```
proyecto/
├── data/
│   ├── raw/          # Datos originales (NO modificar)
│   └── processed/    # Datos limpios y procesados
├── notebooks/        # Jupyter notebooks de análisis
├── src/              # Código reutilizable
│   ├── etl.py        # Pipeline de extracción, transformación, carga
│   ├── features.py   # Feature engineering
│   └── viz.py        # Funciones de visualización
├── reports/          # Reportes generados
├── tests/            # Tests unitarios
├── requirements.txt
├── .env              # Variables de entorno (NO committear)
└── .gitignore
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
```

## Datos
- Fuente: {de dónde vienen los datos}
- Formato: CSV / Parquet / Excel
- Tamaño: {cantidad de registros}
