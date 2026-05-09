---
name: data-profiling
description: >
  Análisis automático de calidad y perfil de datasets con ydata-profiling, sweetviz y pandas nativo.
  Trigger: Cuando recibís un dataset nuevo y necesitás entenderlo rápido, o cuando querés un reporte de calidad de datos.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.1"
  model_tier: T2-fast
---

# Skill: data-profiling

Generación automática de perfiles y reportes de calidad de datos. Para entender un dataset en segundos sin escribir cien líneas de EDA.

## Trigger

Cargá esta skill cuando:
- Recibís un dataset nuevo y querés entenderlo de un vistazo
- Necesitás generar reportes de calidad de datos automáticos
- Querés detectar correlaciones, outliers y distribuciones sin código manual
- Necesitás comparar dos datasets (antes/después de limpieza, train vs test)

## Por qué profilear

El profiling automático no reemplaza el EDA, lo acelera. En lugar de escribir 20 celdas de Jupyter para ver distribuciones, nulos y correlaciones, generás un reporte en 2 líneas y te concentrás en lo que realmente importa: entender los problemas de fondo.

## 1. Perfil rápido sin librerías externas

```python
import pandas as pd
import numpy as np

def perfil_rapido(df: pd.DataFrame) -> dict:
    numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()

    print(f"Shape: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"Numéricas ({len(numericas)}): {numericas}")
    print(f"Categóricas ({len(categoricas)}): {categoricas}")

    nulos = df.isnull().sum()
    if nulos.any():
        print(f"Nulos:")
        print(nulos[nulos > 0].sort_values(ascending=False)
              .to_frame('nulos')
              .assign(pct=lambda x: (x['nulos']/len(df)*100).round(1)))

    dups = df.duplicated().sum()
    print(f"Duplicados: {dups:,} ({dups/len(df)*100:.1f}%)")

perfil_rapido(df)
```

## 2. ydata-profiling — reporte HTML completo

```python
from ydata_profiling import ProfileReport

# Completo (ideal para datasets < 100k filas)
profile = ProfileReport(df, title="Análisis de Dataset", explorative=True)
profile.to_file("reporte_profiling.html")

# Minimal (para datasets grandes)
profile = ProfileReport(df, minimal=True)
profile.to_file("reporte_minimal.html")
```

**Por qué minimal para datasets grandes**: el profiling completo calcula correlaciones, pairwise y distribuciones detalladas. En datasets > 100k filas puede tardar minutos. Minimal salta los cálculos pesados.

## 3. sweetviz — comparar datasets

```python
import sweetviz as sv

reporte = sv.compare([df_train, "Train"], [df_test, "Test"])
reporte.show_html("comparacion.html")

reporte = sv.compare_intra(df, df["genero"] == "M", ["Hombre", "Mujer"])
reporte.show_html("segmentos.html")
```

## 4. Detección de problemas

```python
def detectar_problemas(df):
    problemas = []
    for col in df.columns:
        pct_nulo = df[col].isnull().mean()
        if pct_nulo > 0.5:
            problemas.append(f"{col}: {pct_nulo:.0%} nulos — considerar eliminar")
    for col in df.select_dtypes(include=[np.number]).columns:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = ((df[col] < q1 - 3*iqr) | (df[col] > q3 + 3*iqr)).sum()
        if outliers > 0:
            problemas.append(f"{col}: {outliers} outliers extremos")
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) > 0.9:
            problemas.append(f"{col}: alta cardinalidad ({df[col].nunique()} únicos) — ¿es un ID?")
    return problemas
```

## Anti-patrones

- ❌ **Usar profiling completo en datasets > 500k filas**: se cuelga. Usá `minimal=True` o sampleá.
- ❌ **Confiar ciegamente en el profiling**: detecta correlaciones, no causalidad. La interpretación la ponés vos.
- ❌ **No revisar los datos que el profiling marca como "OK"**: el profiling no sabe si tus datos son correctos, solo si son consistentes.
- ❌ **Compartir reportes de profiling con datos sensibles**: los reportes HTML incluyen valores extremos y distribuciones enteras.

## Alternativas

- **ydata-profiling**: el estándar actual. Reemplazó a `pandas-profiling`. Reportes muy completos.
- **sweetviz**: mejor para comparar dos datasets (train/test, antes/después). Visualmente más lindo.
- **D-Tale**: interfaz web interactiva para explorar datos sin código.
- **Great Expectations**: para equipos que necesitan validación en pipelines de producción.

## Tools relevantes

- `ydata-profiling` — profiling completo con reportes HTML
- `sweetviz` — comparación de datasets
- `missingno` — visualización de patrones de nulos
- `D-Tale` — exploración interactiva web
- `great_expectations` — validación en pipelines CI/CD
