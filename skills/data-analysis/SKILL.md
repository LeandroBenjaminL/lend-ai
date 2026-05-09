---
name: data-analysis
description: >
  Análisis y manipulación de datos con Pandas y NumPy.
  Trigger: Cuando necesitás analizar datasets, manipular DataFrames, o hacer cálculos numéricos con Python.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.1"
  model_tier: T3-balanced
---

# Skill: data-analysis

Análisis y manipulación de datos tabulares con Pandas y NumPy. Es la skill base de todo el ecosistema — casi todo arranca acá.

## Trigger

Cargá esta skill cuando:
- Necesitás cargar, explorar y manipular datos tabulares (CSV, Excel, Parquet, SQL)
- Vas a hacer transformaciones: merges, groupby, pivot tables, reshapes
- Querés hacer análisis exploratorio (EDA) completo
- Trabajás con arrays numéricos y necesitás operaciones vectorizadas

## Por qué Pandas (y cuándo NO)

Pandas es el estándar de facto porque su API es declarativa y expresiva: decís *qué* querés hacer, no *cómo*. Pero no es siempre la mejor herramienta:

| Situación | Alternativa | Por qué |
|-----------|-------------|---------|
| Dataset > 10GB | **Polars** o **DuckDB** | Pandas carga todo en memoria. Polars es lazy y paraleliza. |
| Operaciones SQL-like | **DuckDB** | Hacés SQL directamente sobre CSV/Parquet sin cargar. |
| Datos muy anidados (JSON) | **Pandas json_normalize** o **Polars** | Pandas sufre con anidamiento profundo. |
| Machine Learning | **Pandas + numpy** + sklearn | Sigue siendo el estándar para pre-procesamiento. |

## Workflow de análisis

```python
import pandas as pd
import numpy as np

def explorar_dataset(df):
    print(f"Shape: {df.shape}")
    print(f"\nTipos:\n{df.dtypes}")
    print(f"\nNulos:\n{df.isnull().sum()}")
    print(f"\nStats:\n{df.describe(include='all')}")
    print(f"\nDuplicados: {df.duplicated().sum()}")
    print(f"\nHead:\n{df.head()}")
```

**Por qué siempre explorar primero**: anticipás problemas de tipos, nulos y outliers antes de meterte en el análisis serio. Te ahorra debugging a los gritos a las 2am.

## Transformaciones clave

| Operación | Código | Nota |
|-----------|--------|------|
| Groupby + agg | `df.groupby('cat').agg({'val': ['mean', 'sum', 'count']})` | Usá `NamedAgg` si querés nombres lindos |
| Pivot table | `df.pivot_table(index='cat', columns='fecha', values='val', aggfunc='sum')` | Ideal para heatmaps |
| Merge | `pd.merge(df1, df2, on='key', how='left')` | Siempre verificá cardinalidad después |
| Filter | `df.query('edad > 30 & salario < 50000')` | Más legible que el boolean indexing |
| Apply | `df['col'].apply(lambda x: x**2)` | Preferí operaciones vectorizadas cuando puedas |
| Astype | `df['col'] = df['col'].astype('float32')` | Clave para ahorrar memoria en datasets grandes |

## Optimización de memoria

```python
for col in df.select_dtypes('object').columns:
    df[col] = df[col].astype('category')

for col in df.select_dtypes('int64').columns:
    df[col] = df[col].astype('int32')
```

**Por qué**: los tipos default de pandas son conservadores (int64, float64). Bajar a int32/float32 reduce memoria ~50% sin pérdida de precisión para la mayoría de los casos.

## Ejemplo completo

```python
df = pd.read_csv('ventas.csv', parse_dates=['fecha'])

resumen = df.groupby([df['fecha'].dt.to_period('M'), 'producto']).agg({
    'cantidad': 'sum',
    'precio_unitario': 'mean',
    'total': 'sum'
}).round(2)

top = df.groupby('producto')['total'].sum().nlargest(10)
corr = df.select_dtypes(include=[np.number]).corr()
```

## Anti-patrones

- ❌ **Iterar con for loops en vez de vectorizar**: `for i in range(len(df))` cuando podés hacer `df['col'] * 2`
- ❌ **No verificar merge cardinalidad**: un merge 1:N cuando esperabas 1:1 te duplica filas sin aviso
- ❌ **Usar `inplace=True`**: silencia errores y no encadena bien. Preferí `df = df.assign(...)`
- ❌ **Cargar todo con tipos default**: si tenés 50 columnas object, estás desperdiciando memoria al pedo
- ❌ **Chained indexing**: `df[df['a'] > 0]['b']` puede crear copias o views. Usá `.loc[df['a'] > 0, 'b']`

## Tools relevantes

- `pandas` / `numpy` — core
- `polars` — alternativa moderna para big data
- `duckdb` — SQL engine embebido, ideal para querys ad-hoc sobre archivos
- `pandera` — validación de DataFrames con esquemas
- `pandas-profiling` / `ydata-profiling` — profiling automático
