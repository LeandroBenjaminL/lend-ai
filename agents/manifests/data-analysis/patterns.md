# Patterns: Pandas & NumPy Cheat Sheet

## Carga eficiente

```python
df = pd.read_csv('datos.csv', parse_dates=['fecha'], dtype={'id': 'int32', 'cat': 'category'})
df = pd.read_parquet('datos.parquet')  # 10x más rápido que CSV
```

## Exploración rápida

```python
df.shape         # filas × columnas
df.dtypes        # tipos por columna
df.isnull().sum()  # nulos por columna
df.describe(include='all')  # stats numéricos + categóricos
df.memory_usage(deep=True).sum() / 1e6  # memoria en MB
```

## Operaciones clave

| Patrón | Código |
|---|---|
| GroupBy + agg | `df.groupby('cat').agg({'val': ['mean','sum','count']})` |
| Pivot table | `df.pivot_table(index='region', columns='anio', values='ventas', aggfunc='sum')` |
| Merge | `pd.merge(a, b, on='key', how='left')` |
| Join index | `a.join(b, on='key')` |
| Filter | `df.query('edad > 30 and salario < 50000')` |
| Apply | `df['col'].apply(fn)` — último recurso, preferir vectorizado |
| Melt | `df.melt(id_vars=['id'], var_name='mes', value_name='valor')` |
| Crosstab | `pd.crosstab(df['cat1'], df['cat2'], normalize='index')` |

## Series temporales

```python
df.set_index('fecha').resample('M')['ventas'].sum()
df['fecha'].dt.year  # extraer componentes
df['fecha'].diff()    # lag
df.rolling(7)['val'].mean()  # ventana móvil
```

## Performance y memoria

```python
# Reducir tipos (dataset grande)
for col in df.select_dtypes('object'):
    df[col] = df[col].astype('category')  # si cardinalidad < 50%
for col in df.select_dtypes('int64'):
    df[col] = df[col].astype('int32')
for col in df.select_dtypes('float64'):
    df[col] = df[col].astype('float32')

# Evitar loops — siempre vectorizar
arr = df['val'].to_numpy()
np.where(arr > 100, 'alto', 'bajo')  # condicional vectorizado
np.select([arr < 10, arr < 50], ['bajo', 'medio'], default='alto')
```

## NumPy rápido

```python
np.percentile(arr, [25, 50, 75])  # cuartiles
np.digitize(arr, bins)             # bucketear
np.clip(arr, 0, 100)               # truncar outliers
```
