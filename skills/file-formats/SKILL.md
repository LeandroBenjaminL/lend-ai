---
name: file-formats
description: >
  Lectura y escritura de formatos de datos: CSV, Excel, Parquet, JSON, HDF5, archivos comprimidos y más.
  Trigger: Cuando necesitás leer o guardar datos en distintos formatos, convertir entre formatos, o elegir el formato correcto para tu caso.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T1-ultra-fast
---

# Skill: file-formats

## Para qué sirve

Leer y escribir datos en distintos formatos según el contexto. Cada formato existe por una razón: CSV para intercambio, Parquet para rendimiento, Excel para reportes, JSON para APIs. Saber cuál usar en cada caso te ahorra dolores de cabeza (y GB de RAM).

## Trigger (cuándo cargar esta skill)

- Necesitás elegir qué formato usar para guardar datos procesados
- Te llegan archivos en un formato que no conocés
- Tenés que convertir entre formatos (ej: CSV → Parquet)
- Querés leer múltiples archivos de un directorio como un solo dataset

## Workflow paso a paso

1. **Identificá el propósito**: ¿es para archivar? → Parquet. ¿Para compartir con no-técnicos? → Excel. ¿Para una API? → JSON.
2. **Pensá en el tamaño**: +1 GB → Parquet con compresión. -100 MB → CSV o JSON va bien.
3. **Preservá los tipos**: CSV no guarda tipos de dato. Parquet sí. Si después de leer CSV tenés que andar casteando, usaste el formato incorrecto.
4. **Comprimí si es necesario**: `.gz` o `.zip` reducen drásticamente el tamaño.
5. **Verificá la codificación**: UTF-8 para todo, pero Excel prefiere UTF-8-BOM. `utf-8-sig` es tu amigo.

## Tabla de formatos: cuándo usar cada uno

| Formato | Ideal para... | Ventaja clave | Cuidado con... |
|---------|--------------|---------------|----------------|
| **CSV** | Intercambio universal, datos chicos | Lo abre cualquiera | No preserva tipos, lento, no soporta anidados |
| **Parquet** | Datos procesados, archivo, análisis | 10x más rápido que CSV, compresión nativa, preserva tipos | No legible en editor de texto |
| **Excel** | Reportes para usuarios no técnicos | Familiar, múltiples hojas, formateo visual | Límite 1M filas, lento, no para datos |
| **JSON** | APIs, datos anidados (logs, eventos) | Reflecta estructuras jerárquicas | Ineficiente para tablas planas grandes |
| **Feather** | Intercambio rápido Python ↔ R | Velocidad de lectura/escritura bestial | No sirve para archivar (poca compresión) |
| **HDF5** | Datos enormes (imágenes, señales) | Soporta arrays multidimensionales | Complejo de usar, curva de aprendizaje |

## Patrones esenciales

### 1. CSV con parámetros correctos

El CSV parece fácil, pero es donde más errores aparecen. Codificaciones, separadores, decimales — cada archivo viene con su propia config.

```python
import pandas as pd

# Lectura defensiva
df = pd.read_csv(
    'datos.csv',
    sep=',',
    encoding='utf-8',
    parse_dates=['fecha'],
    dtype={'id': str, 'codigo': str},     # IDs como string, no int
    na_values=['', 'N/A', 'null', '-'],
    thousands='.',
    decimal=','                             # archivos con coma decimal
)

# Escritura compatible con Excel
df.to_csv('output.csv', index=False, encoding='utf-8-sig')
```

**¿Por qué `dtype={'id': str}`?** Porque si un ID es `'00123'`, pandas lo lee como `123` y perdés el cero. Decirle el tipo de entrada evita estas transformaciones silenciosas.

### 2. Excel — múltiples hojas

```python
# Leer todas las hojas
hojas = pd.read_excel('reporte.xlsx', sheet_name=None)  # dict: {hoja: DataFrame}

# Escribir múltiples hojas
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df_ventas.to_excel(writer, sheet_name='Ventas', index=False)
    df_costos.to_excel(writer, sheet_name='Costos', index=False)
```

### 3. Parquet — el rey del almacenamiento analítico

Parquet es columnar: guarda los datos por columna en vez de por fila. Eso significa que leer solo 3 columnas de un archivo de 100 columnas es rapidísimo porque no lee el resto.

```python
# Guardar con compresión snappy (balance velocidad/tamaño)
df.to_parquet('datos.parquet', engine='pyarrow', compression='snappy')

# Leer solo las columnas que necesitás
df = pd.read_parquet('datos.parquet', columns=['fecha', 'monto', 'categoria'])
```

### 4. Archivos comprimidos — sin descomprimir a mano

Pandas lee `.gz` y `.zip` directamente. Si tenés que descomprimir primero, estás al pedo.

```python
df = pd.read_csv('datos.csv.gz', compression='gzip')
df = pd.read_csv('datos.csv.zip')   # auto-detecta

# Archivo adentro de un zip
import zipfile
with zipfile.ZipFile('datos.zip') as z:
    with z.open('ventas.csv') as f:
        df = pd.read_csv(f)
```

### 5. Múltiples archivos → un solo DataFrame

```python
from pathlib import Path

archivos = Path('data/raw').glob('*.csv')
df = pd.concat([pd.read_csv(f) for f in archivos], ignore_index=True)

# Con nombre de archivo como columna (útil para trackear origen)
dfs = []
for f in Path('data/raw').glob('*.csv'):
    temp = pd.read_csv(f)
    temp['archivo_origen'] = f.stem
    dfs.append(temp)
df = pd.concat(dfs, ignore_index=True)
```

## Alternativas

- **Pandas vs Polars**: Polars lee los mismos formatos pero suele ser 2-10x más rápido. Probá `pl.read_csv()`, `pl.read_parquet()`.
- **Delta Lake**: Si trabajás en equipo y necesitás versionado de datos, Delta Lake (formato sobre Parquet) te da transacciones ACID y time travel.
- **CSV vs DuckDB**: Para análisis pesados sobre CSV, usá DuckDB en vez de pandas. `duckdb.sql("SELECT * FROM 'datos.csv'")` es mucho más rápido que `pd.read_csv`.

## Anti-patrones

- ❌ **Usar Excel como base de datos**: Excel no es una DB. No le metas 500K filas. Se va a colgar, y vos también esperando.
- ❌ **CSV sin especificar tipos**: Dejar que pandas infiera `dtype` lleva a sorpresas: códigos postales que pierden ceros, fechas que no se parsean, montos que se convierten mal.
- ❌ **No comprimir archivos grandes**: Un CSV de 5 GB comprimido puede pasar a 300 MB. No comprimir es despilfarrar espacio y ancho de banda.
- ❌ **Parquet con gzip en vez de snappy**: La compresión gzip es lenta para leer y escribir. Snappy da buen ratio con mucha más velocidad.

## Comandos

```bash
# Comparar tamaño de formatos
python3 -c "
import pandas as pd, os
df = pd.read_csv('datos.csv')
df.to_parquet('datos.parquet')
print(f'CSV: {os.path.getsize(\"datos.csv\")/1e6:.1f} MB')
print(f'Parquet: {os.path.getsize(\"datos.parquet\")/1e6:.1f} MB')
"
```
