# Workflow: File Formats

## Flujo principal

```
Orchestrator → [1. Detectar] → [2. Leer] → [3. Validar carga] → [4. Convertir (opcional)] → [5. Guardar] → Orchestrator
```

## Paso a paso

### 1. Detectar formato y encoding

Antes de leer, inspeccionar el archivo:

- **Extensión**: primer indicio, pero no confiés ciegamente.
- **Encoding**: leer primeros bytes para detectar BOM (UTF-8, UTF-16, UTF-32). Si no hay BOM, usar `chardet` sobre las primeras 10k líneas. Encoding LATIN1 es común en datos de Argentina y España.
- **Separador en CSV**: `csv.Sniffer` sobre primeras 5 líneas, o heurística: si hay más `;` que `,`, es punto y coma. Si hay tabs, es TSV.
- **Decimal**: si los números usan `,` como decimal (formato europeo/latino), seteá `decimal=','` y `thousands='.'`.
- **Compresión**: si el archivo termina en `.gz`, `.bz2`, `.xz`, `.zip`, usar `compression='infer'` o el parámetro explícito.

Output de este paso: `(formato, encoding, sep, decimal, compression, nrows_estimadas)`.

### 2. Leer con los parámetros correctos

Según el formato detectado:

| Formato | Función | Parámetros clave |
|---------|---------|-----------------|
| CSV/TSV | `pd.read_csv()` | `sep`, `encoding`, `parse_dates`, `dtype`, `na_values`, `decimal`, `thousands` |
| Excel | `pd.read_excel()` | `sheet_name`, `header`, `dtype`, `na_values` |
| Parquet | `pd.read_parquet()` | `columns` (solo las necesarias), `engine='pyarrow'` |
| JSON | `pd.read_json()` | `orient`, `lines=True` para JSONL, `encoding` |
| Feather | `pd.read_feather()` | `columns` |
| HDF5 | `pd.read_hdf()` | `key`, `columns` |

**Reglas de oro al leer**:
- Siempre `dtype` explícito para IDs y códigos (evitar que `00123` se vuelva `123`).
- `parse_dates` para toda columna que sea fecha.
- Para archivos grandes (>1 GB), usar `chunksize` con iteración o `columns` para leer solo lo necesario.
- `low_memory=False` en CSVs para evitar warnings de tipos mixtos.
- Mostrar siempre: shape, tiempo de carga, memoria usada (`df.memory_usage(deep=True).sum() / 1e6`).

### 3. Validar que los datos se leyeron bien

Checklist post-carga:

- `df.shape` coincide con lo esperado (si sabés cuántas filas debería tener).
- `df.isnull().sum()` — ¿nulos inesperados? Posible encoding mal interpretado o separador incorrecto.
- `df.dtypes` — ¿tipos correctos? Si un int64 se leyó como object, revisar `na_values` y espacios.
- `df.head(3)` y `df.tail(3)` — ojeo visual.
- Si hay columnas con nombres raros (espacios, caracteres especiales), limpiar con `df.columns = df.columns.str.strip()`.

Si algo falla, volver al paso 1 con la info nueva.

### 4. Convertir a otro formato (si es necesario)

Razones para convertir:
- **Origen CSV → Destino Parquet**: para guardar datos procesados (10x más chico, 5x más rápido de leer).
- **Origen Excel → Destino CSV**: para alimentar pipelines o bases de datos.
- **Origen JSON anidado → CSV/Parquet**: normalizar con `pd.json_normalize()` antes de guardar.
- **Origen Parquet → CSV**: solo si el destino es un stakeholder no técnico.

Al convertir:
- Preservar tipos (`category`, `datetime64`, integers pequeños).
- Si el destino es CSV para Excel de Windows, usar `encoding='utf-8-sig'` (BOM).
- Si el destino es Parquet, usar `compression='snappy'` (balance velocidad/tamaño) o `'zstd'` (máxima compresión).

### 5. Guardar optimizando según destino

| Formato | Función | Parámetros clave |
|---------|---------|-----------------|
| CSV | `df.to_csv()` | `index=False`, `encoding='utf-8-sig'`, `sep=','`, `decimal='.'` |
| Excel | `df.to_excel()` | `index=False`, `sheet_name`, `engine='openpyxl'` |
| Parquet | `df.to_parquet()` | `compression='snappy'`, `engine='pyarrow'`, `index=False` |
| JSON | `df.to_json()` | `orient='records'`, `lines=True`, `force_ascii=False` |
| Feather | `df.to_feather()` | simple, sin params extra |

**Reglas de oro al guardar**:
- `index=False` siempre, salvo que el índice tenga información semántica.
- Comprimir CSVs grandes: `df.to_csv('archivo.csv.gz', compression='gzip')`.
- Para Excel con múltiples hojas: usar `pd.ExcelWriter` con contexto `with`.
- Mostrar siempre: tamaño del archivo resultante, tiempo de escritura, factor de compresión si aplica.
