# Patterns: Cheat Sheet de Data Profiling

## 1. ydata-profiling — Reporte HTML completo

```python
from ydata_profiling import ProfileReport

# Reporte completo (default)
profile = ProfileReport(df, title="Mi Dataset", explorative=True)
profile.to_file("reporte.html")

# Versión mínima para datasets grandes (>100k filas)
profile = ProfileReport(df, minimal=True)
profile.to_file("reporte_minimal.html")

# En Jupyter Notebook
profile.to_notebook_iframe()

# Configuración común
profile = ProfileReport(
    df,
    title="Análisis",
    explorative=True,        # modo exploratorio (más stats)
    correlations={"auto": {"calculate": True}},  # correlaciones
    missing_diagrams={"bar": True},              # gráfico de nulos
    interactions={"continuous": True},           # interacciones entre numéricas
)
```

---

## 2. sweetviz — Comparar datasets

```python
import sweetviz as sv

# Dataset único
reporte = sv.analyze(df)
reporte.show_html("reporte.html")

# Comparar train vs test
reporte = sv.compare([df_train, "Train"], [df_test, "Test"])
reporte.show_html("comparacion.html")

# Comparar segmentos (ej: hombres vs mujeres)
reporte = sv.compare_intra(df, df["genero"] == "M", ["Hombre", "Mujer"])
reporte.show_html("segmentos.html")

# Comparar dos datasets con feature target
reporte = sv.compare([df_train, "Train"], [df_test, "Test"], target_feat="precio")
reporte.show_html("comparacion_target.html")
```

---

## 3. Pandas nativo — Exploración rápida

```python
import pandas as pd
import numpy as np

# === Estructura ===
df.shape                          # (filas, columnas)
df.dtypes                         # tipos de cada columna
df.memory_usage(deep=True).sum()  # memoria en bytes

# === Vistazo ===
df.head(10)
df.tail(5)
df.sample(5)                      # filas aleatorias

# === Stats ===
df.describe()                     # solo numéricas
df.describe(include='object')     # solo categóricas
df.describe(include='all')        # todas

# === Nulos ===
df.isnull().sum()                 # nulos por columna
df.isnull().mean() * 100          # % nulos por columna
df.isnull().sum(axis=1)           # nulos por fila
nulos = df.isnull().sum()
nulos[nulos > 0].sort_values(ascending=False)  # solo columnas con nulos

# === Duplicados ===
df.duplicated().sum()             # total duplicados
df[df.duplicated(keep=False)]     # ver filas duplicadas

# === Cardinalidad ===
df.nunique()                      # valores únicos por columna
df.nunique() / len(df) * 100      # % de unicidad
# ⚠️  Si >90% en una categórica → posible ID

# === Valores frecuentes ===
df['columna'].value_counts().head(10)          # top 10
df['columna'].value_counts(normalize=True)     # proporciones
df['columna'].value_counts(dropna=False)       # incluyendo NaN

# === Correlaciones ===
df.corr()                                      # matriz Pearson
df.corr(method='spearman')                     # Spearman (no lineal)
df.corr()['target'].sort_values(ascending=False)  # corr vs target

# === Detectar columnas constantes ===
constantes = [col for col in df.columns if df[col].nunique() == 1]
# ⚠️  Columnas con un solo valor = cero información
```

---

## 4. Detección de columnas con alta cardinalidad

```python
def detectar_alta_cardinalidad(df, umbral=0.9):
    """Columnas categóricas con más del 90% de valores únicos"""
    problemas = []
    for col in df.select_dtypes(include=['object', 'category']).columns:
        ratio = df[col].nunique() / len(df)
        if ratio > umbral:
            problemas.append({
                'columna': col,
                'unicos': df[col].nunique(),
                'pct_unico': round(ratio * 100, 1),
                'tipo': df[col].dtype,
                'sugerencia': '¿Es un ID o clave? Considerar dropear o tratar como índice'
            })
    return sorted(problemas, key=lambda x: x['pct_unico'], reverse=True)

for p in detectar_alta_cardinalidad(df):
    print(f"🔑 {p['columna']}: {p['pct_unico']}% único ({p['unicos']} valores) — {p['sugerencia']}")
```

---

## 5. Detección de columnas potencialmente categóricas mal tipeadas

```python
def detectar_categoricas_mal_tipeadas(df, max_unicos=20):
    """Columnas numéricas con pocos valores únicos que deberían ser categóricas"""
    sospechosas = []
    for col in df.select_dtypes(include=[np.number]).columns:
        unicos = df[col].nunique()
        if unicos <= max_unicos:
            valores = df[col].dropna().unique()
            # ¿Los valores parecen códigos/enums y no valores continuos?
            es_entero = all(v == int(v) for v in valores if not np.isnan(v))
            sospechosas.append({
                'columna': col,
                'unicos': unicos,
                'valores': sorted(valores[:10]),
                'enteros': es_entero,
                'sugerencia': 'Convertir a category' if unicos <= 10 else 'Revisar si es ordinal'
            })
    return sospechosas

for s in detectar_categoricas_mal_tipeadas(df):
    print(f"🔄 {s['columna']}: {s['unicos']} valores — {s['sugerencia']}")
    print(f"   Ejemplos: {s['valores']}")
```

---

## 6. Outliers con IQR

```python
def detectar_outliers(df, factor=3.0):
    """Outliers extremos (3× IQR por defecto)"""
    outliers = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        mask = (df[col] < lower) | (df[col] > upper)
        n = mask.sum()
        if n > 0:
            outliers[col] = {
                'count': n,
                'pct': round(n / len(df) * 100, 1),
                'lower_bound': round(lower, 2),
                'upper_bound': round(upper, 2),
                'min_outlier': df.loc[mask, col].min(),
                'max_outlier': df.loc[mask, col].max(),
            }
    return outliers

for col, stats in detectar_outliers(df).items():
    print(f"📍 {col}: {stats['count']} outliers ({stats['pct']}%) — rango [{stats['min_outlier']}, {stats['max_outlier']}]")
```

---

## 7. Resumen rápido — one-liner de perfil

```python
def perfil_express(df):
    """Resumen ejecutivo de un dataset en 5 líneas"""
    print(f"📐 {df.shape[0]:,} filas × {df.shape[1]} columnas | 💾 {df.memory_usage(deep=True).sum()/1024**2:.1f} MB")
    nulos = df.isnull().sum()
    print(f"⚠️  Nulos: {nulos.sum():,} totales en {sum(nulos > 0)} columnas ({nulos.mean():.1%} global)")
    print(f"🔁 Duplicados: {df.duplicated().sum():,} ({df.duplicated().mean():.1%})")
    print(f"🔢 Numéricas: {len(df.select_dtypes(include=[np.number]).columns)} | 📝 Categóricas: {len(df.select_dtypes(include=['object']).columns)}")
    constantes = sum(df.nunique() == 1)
    if constantes:
        print(f"🪦  {constantes} columna(s) constante(s) — cero información")

perfil_express(df)
```

---

## 8. Instalación

```bash
pip install ydata-profiling sweetviz pandas numpy
```
