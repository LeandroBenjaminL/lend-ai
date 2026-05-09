# Patterns: Data Cleaning Cheat Sheet

## Diagnóstico (sin tocar)

```python
# Nulos
df.isnull().sum()                          # conteo por columna
(df.isnull().sum() / len(df) * 100).round(2)  # porcentaje
df.isnull().sum(axis=1).value_counts()     # filas con N nulos

# Duplicados
df.duplicated().sum()                      # total de filas duplicadas
df[df.duplicated(keep=False)].sort_index() # ver duplicados completos

# Outliers (IQR)
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['col'] < Q1 - 1.5*IQR) | (df['col'] > Q3 + 1.5*IQR)]
```

## Capa 1 — Nulos

```python
# Dropeo
df.dropna(axis=1, thresh=len(df)*0.4)      # columnas con >60% nulos
df.dropna(subset=['col_critica'])           # filas donde col clave es nula

# Imputación
df['num'].fillna(df['num'].median())        # mediana (robusta a outliers)
df['cat'].fillna(df['cat'].mode()[0])       # moda para categóricas
df.fillna(method='ffill')                   # forward-fill (series temporales)
df['col'].fillna('DESCONOCIDO')             # constante semántica
```

## Capa 2 — Duplicados

```python
df.drop_duplicates()                        # todas las columnas
df.drop_duplicates(subset=['id', 'fecha'])  # clave compuesta
df.drop_duplicates(subset=['id'], keep='last')  # última ocurrencia
```

## Capa 3 — Outliers

```python
# Clip (truncar sin perder filas)
lo, hi = Q1 - 1.5*IQR, Q3 + 1.5*IQR
df['col'] = df['col'].clip(lo, hi)

# Winsorizar con scipy
from scipy.stats.mstats import winsorize
df['col'] = winsorize(df['col'], limits=(0.05, 0.05))

# Eliminar filas outlier
df_clean = df[(df['col'] >= lo) & (df['col'] <= hi)]
```

## Capa 4 — Tipos y formato

```python
# Conversión de tipos
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
df['cat'] = df['cat'].astype('category')
df['id'] = pd.to_numeric(df['id'], errors='coerce')

# Strings
df['nombre'] = df['nombre'].str.strip().str.lower()
df['tel'] = df['tel'].str.replace(r'[\s\-\(\)]', '', regex=True)

# Regex de extracción
df['email'] = df['texto'].str.extract(r'([\w\.-]+@[\w\.-]+)')
df['codigo_postal'] = df['dir'].str.extract(r'\b(\d{4,5})\b')
```
