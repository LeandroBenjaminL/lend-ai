# Patrones: Data Explorer

## Perfil rápido de un DataFrame

```python
def quick_profile(df):
    print(f"Shape: {df.shape}")
    print(f"Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nDuplicados: {df.duplicated().sum()}")
    print(f"\n=== Nulos ===")
    nulls = df.isnull().sum()
    print(nulls[nulls > 0] if any(nulls > 0) else "Sin nulos")
    print(f"\n=== Tipos ===")
    print(df.dtypes.value_counts())
```

## Detectar outliers (IQR)

```python
def detect_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    return len(outliers), lower, upper
```

## Cardinality check

```python
def cardinality_check(df, threshold=50):
    for col in df.select_dtypes(include='object').columns:
        uniques = df[col].nunique()
        if uniques > threshold:
            print(f"⚠️  {col}: {uniques} valores únicos (alta cardinalidad)")
```
