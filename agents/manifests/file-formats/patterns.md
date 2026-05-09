# Patterns: Formatos de Datos — Cheat Sheet

## Cuándo usar cada formato

| Formato | Usar para | No usar para |
|---------|-----------|-------------|
| **CSV** | Intercambio con terceros, datos <100 MB, git-friendly | Datasets grandes, datos con tipos complejos |
| **Parquet** | Almacenamiento intermedio, ML, datos >100 MB, pipelines | Compartir con no técnicos, edición manual |
| **Excel** | Reportes finales, stakeholders no técnicos, dashboards manuales | Datasets >1M filas, pipelines, automatización |
| **JSON** | APIs REST, datos anidados, configuraciones, NoSQL | Datos tabulares grandes, análisis |
| **JSONL** | Logs, streaming, datos semi-estructurados línea a línea | Datos con relaciones entre registros |
| **Feather** | Intercambio rápido Python↔R, caché temporal | Archivo a largo plazo, compatibilidad cross-version |
| **HDF5** | Datasets científicos, arrays multidimensionales | Intercambio simple, compatibilidad cross-language |

## CSV — Lectura robusta

```python
import pandas as pd
import chardet
import csv

# 1. Detectar encoding
with open('datos.csv', 'rb') as f:
    raw = f.read(100_000)
    encoding = chardet.detect(raw)['encoding']  # ej: 'Latin-1'

# 2. Detectar separador
with open('datos.csv', 'r', encoding=encoding) as f:
    sample = ''.join(f.readline() for _ in range(5))
    dialect = csv.Sniffer().sniff(sample)
    sep = dialect.delimiter  # ',' o ';' o '\t'

# 3. Leer con todo configurado
df = pd.read_csv(
    'datos.csv',
    sep=sep,
    encoding=encoding,
    parse_dates=['fecha', 'created_at'],
    dtype={'id_cliente': str, 'codigo_postal': str, 'categoria': 'category'},
    na_values=['', 'N/A', 'null', 'NULL', '-', '#N/D'],
    decimal=',',
    thousands='.',
    low_memory=False,
)

# 4. CSV comprimido — directo
df = pd.read_csv('datos.csv.gz')                  # auto-detecta .gz
df = pd.read_csv('datos.csv.bz2', compression='bz2')
df = pd.read_csv('datos.zip', compression='zip')  # solo un archivo dentro
```

## CSV — Escritura correcta

```python
# Básico (siempre index=False)
df.to_csv('output.csv', index=False)

# Para Excel en Windows (BOM para que detecte UTF-8)
df.to_csv('output.csv', index=False, encoding='utf-8-sig')

# Con compresión
df.to_csv('output.csv.gz', index=False, compression='gzip')

# Formato europeo (coma decimal, punto y coma separador)
df.to_csv('output.csv', index=False, sep=';', decimal=',')
```

## Excel — Lectura y escritura

```python
# Leer hoja específica
df = pd.read_excel('reporte.xlsx', sheet_name='Ventas', header=0)

# Leer todas las hojas → dict de DataFrames
hojas = pd.read_excel('reporte.xlsx', sheet_name=None)

# Leer rango específico
df = pd.read_excel('reporte.xlsx', sheet_name='Ventas', usecols='A:G', nrows=5000)

# Escribir múltiples hojas
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df_ventas.to_excel(writer, sheet_name='Ventas', index=False)
    df_costos.to_excel(writer, sheet_name='Costos', index=False)
    df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
```

## Parquet — El caballo de batalla

```python
# Guardar (siempre con compresión)
df.to_parquet('datos.parquet', engine='pyarrow', compression='snappy')
df.to_parquet('datos.parquet', engine='pyarrow', compression='zstd')    # más chico
df.to_parquet('datos.parquet', engine='pyarrow', compression='gzip')    # máximo

# Leer — solo las columnas necesarias (pushdown)
df = pd.read_parquet('datos.parquet', columns=['fecha', 'monto', 'categoria'])

# Particionado por columna (para datasets enormes)
df.to_parquet('data/', partition_cols=['anio', 'mes'])
df = pd.read_parquet('data/', filters=[('anio', '=', 2024)])  # lee solo un año
```

## JSON / JSONL

```python
# JSON estándar
df = pd.read_json('datos.json', orient='records', encoding='utf-8')

# JSONL (una línea por registro) — mucho más eficiente
df = pd.read_json('datos.jsonl', lines=True)

# JSON con datos anidados — normalizar
import json
with open('api_response.json') as f:
    data = json.load(f)
df = pd.json_normalize(data, record_path='items', meta=['total', 'page'])

# Guardar como JSONL (mejor que JSON para datos tabulares)
df.to_json('output.jsonl', orient='records', lines=True, force_ascii=False)
```

## Archivos comprimidos

```python
import zipfile
from pathlib import Path

# Leer archivo dentro de un ZIP
with zipfile.ZipFile('datos.zip') as z:
    print(z.namelist())  # ver qué hay adentro
    with z.open('ventas.csv') as f:
        df = pd.read_csv(f)

# Múltiples CSVs en un ZIP
with zipfile.ZipFile('datos.zip') as z:
    dfs = {name: pd.read_csv(z.open(name)) for name in z.namelist() if name.endswith('.csv')}

# Crear ZIP con CSVs
with zipfile.ZipFile('export.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('ventas.csv', df_ventas.to_csv(index=False))
    z.writestr('costos.csv', df_costos.to_csv(index=False))
```

## Archivos grandes — chunked reading

```python
# Leer por chunks (no explota la memoria)
chunks = []
for chunk in pd.read_csv('gigante.csv', chunksize=100_000):
    # Procesar cada chunk
    chunk['nueva_col'] = chunk['monto'] * 1.21
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)

# Leer solo columnas necesarias (CSV)
df = pd.read_csv('gigante.csv', usecols=['fecha', 'monto', 'categoria'])

# Leer solo N filas para explorar
df = pd.read_csv('gigante.csv', nrows=10_000)
```

## Múltiples archivos de un directorio

```python
from pathlib import Path

# Todos los CSV de una carpeta
archivos = list(Path('data/raw').glob('**/*.csv'))
df = pd.concat([pd.read_csv(f) for f in archivos], ignore_index=True)

# Con tracking de archivo origen
dfs = []
for f in archivos:
    temp = pd.read_csv(f)
    temp['archivo_origen'] = f.stem
    temp['ruta'] = str(f)
    dfs.append(temp)
df = pd.concat(dfs, ignore_index=True)

# Patrón para DataFrames grandes (usar lista + concat, NUNCA append en loop)
# ❌ MAL: df = df.append(chunk)  — deprecado, O(n²)
# ✅ BIEN: lista.append(chunk) → pd.concat(lista)
```

## Encoding — detección y troubleshooting

```python
import chardet

# Detectar encoding de un archivo
with open('misterioso.csv', 'rb') as f:
    result = chardet.detect(f.read(200_000))
    print(f"Encoding: {result['encoding']} (confianza: {result['confidence']:.0%})")

# Encodings comunes por región
# LATIN1 (ISO-8859-1): común en Argentina, España, Europa Occidental
# CP1252: Windows en inglés/español
# UTF-8: estándar moderno
# UTF-8-BOM: UTF-8 con marca de orden de bytes (común en Excel)
# UTF-16: algunas apps legacy de Windows

# Si falla la lectura, intentar en orden:
encodings_to_try = ['utf-8', 'latin1', 'cp1252', 'utf-16', 'iso-8859-1']
for enc in encodings_to_try:
    try:
        df = pd.read_csv('archivo.csv', encoding=enc, nrows=5)
        print(f"✓ {enc} funciona")
        break
    except (UnicodeDecodeError, UnicodeError):
        print(f"✗ {enc} falló")
```

## Conversión entre formatos — one-liners

```python
# CSV → Parquet
pd.read_csv('datos.csv').to_parquet('datos.parquet')

# Excel → CSV
pd.read_excel('reporte.xlsx', sheet_name='Hoja1').to_csv('reporte.csv', index=False)

# JSONL → Parquet
pd.read_json('datos.jsonl', lines=True).to_parquet('datos.parquet')

# Parquet → CSV (solo si es necesario)
pd.read_parquet('datos.parquet').to_csv('datos.csv', index=False)

# Comparar tamaños post-conversión
import os
for fmt, path in [('CSV', 'd.csv'), ('Parquet', 'd.parquet'), ('JSONL', 'd.jsonl')]:
    size_mb = os.path.getsize(path) / 1e6
    print(f"{fmt:>8}: {size_mb:.1f} MB")
```
