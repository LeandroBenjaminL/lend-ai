---
name: data-cleaning
description: >
  Limpieza y preparación de datos con Pandas.
  Trigger: Cuando necesitás limpiar datos, manejar nulos, duplicados, outliers, o preparar datasets para análisis.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.1"
  model_tier: T1-ultra-fast
---

# Skill: data-cleaning

Limpieza y preparación de datos. Es el paso que más tiempo lleva en cualquier proyecto de datos — y el que más errores evita si se hace bien.

## Trigger

Cargá esta skill cuando:
- Recibís un dataset nuevo y necesitás revisar nulos, tipos, duplicados
- Hay valores inconsistentes, formatos mezclados o datos sucios
- Necesitás normalizar, estandarizar o transformar columnas
- Estás por modelar o visualizar y querés datos confiables

## Por qué limpiar primero

Un modelo entrenado con datos sucios da resultados estúpidos con alta confianza. La limpieza no es un paso opcional — es lo que separa un análisis confiable de una pérdida de tiempo. El 80% del tiempo de un data project se va en limpieza, y está bien.

## Pipeline de limpieza estándar

```python
def limpiar_dataset(df):
    reporte = {}
    # 1. Duplicados — siempre primero
    dups = df.duplicated().sum()
    if dups:
        df = df.drop_duplicates()
    reporte['duplicados'] = dups

    # 2. Nulos por columna
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    reporte['nulos_por_columna'] = nulos.to_dict()

    # 3. Tipos de datos — verificá que sean los esperados
    reporte['tipos'] = {c: str(d) for c, d in df.dtypes.items()}

    # 4. Stats rápidas
    reporte['forma'] = df.shape

    return df, reporte
```

**Por qué duplicados primero**: si eliminás duplicados después de imputar nulos, podés estar imputando filas que después vas a borrar — trabajo al pedo.

## Estrategias para nulos — por qué cada una

| Tipo de columna | Estrategia | Por qué |
|----------------|-----------|---------|
| Numérica sin outliers | Media | Preserva la media de la distribución |
| Numérica con outliers | Mediana | La mediana es robusta a outliers, la media no |
| Categórica | Moda o "Desconocido" | La moda mantiene la distribución. "Desconocido" es honesto. |
| Serie temporal | Forward fill (`ffill()`) | El valor anterior suele ser la mejor estimación |
| Muchos nulos (>50%) | Eliminar columna | Imputar el 50%+ de una columna es inventar datos |

## Detección de outliers con IQR

```python
def detectar_outliers(df, columna):
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    return df[(df[columna] < limite_inferior) | (df[columna] > limite_superior)]
```

**Por qué IQR y no Z-score**: IQR no asume normalidad. Z-score funciona mal con distribuciones asimétricas o datasets chicos. IQR es más robusto.

## Ejemplo

```python
df = pd.read_csv('datos_raw.csv')

df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
df['categoria'] = df['categoria'].str.strip().str.lower()
df = df.drop_duplicates(subset=['id'])
df['precio'].fillna(df['precio'].median(), inplace=True)
```

## Comandos rápidos

```python
df.info()
df.isnull().sum()
df.describe(include='all')
df.duplicated().sum()
```

## Anti-patrones

- ❌ **Imputar todo con la media**: si tenés outliers, la media está sesgada. Usá mediana.
- ❌ **Borrar filas con nulos sin pensar**: si los nulos no son aleatorios, estás introduciendo sesgo.
- ❌ **No revisar tipos después de cargar**: `read_csv` a veces se equivoca con tipos. Siempre verificá con `dtypes`.
- ❌ **Usar `inplace=True` en pipelines**: hace el código más difícil de debuggear y testear.
- ❌ **Asumir que no hay duplicados**: siempre verificá. Una join mal hecha upstream puede duplicarte filas sin aviso.

## Alternativas

- **Pandas** es el estándar para limpieza en Python.
- **Polars** tiene mejor performance en limpieza de datasets grandes (>5GB).
- **Pydantic** + **Pandera** para validar esquemas en vez de limpiar a mano.
- **Great Expectations** para pipelines de producción con expectativas declarativas.

## Tools relevantes

- `pandas` — core de limpieza
- `pandera` — esquemas y validación de DataFrames
- `pyjanitor` — extensiones de limpieza con nombres estilo R (limpiar, renombrar, etc.)
- `regex-data` (skill hermana) — para limpieza de texto complejo
