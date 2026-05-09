# Workflow: ETL Pipelines

## Flujo principal

```
Orchestrator → [1. Analizar] → [2. Decidir estrategia] → [3. Extraer] → [4. Transformar] → [5. Cargar] → [6. Validar] → [7. Reportar] → Orchestrator
```

## Paso a paso

### 1. Analizar fuentes y destinos
Leer el prompt. Identificar: fuentes (CSV, Parquet, SQL, API REST), destino (DB, archivo, data lake), frecuencia (una vez, diario, hourly), volumen estimado. Si el volumen no está claro, lo preguntás.

### 2. Decidir estrategia
- **ETL vs ELT**: Si el destino es un data warehouse con poder de cómputo (BigQuery, Snowflake) → ELT. Si es PostgreSQL/SQLite/Parquet local → ETL clásico.
- **Batch vs streaming**: Por defecto, batch. Solo considerás streaming si el requisito de latencia es <1 minuto o hay eventos en tiempo real.
- **Incremental vs full**: Si hay columna `updated_at` o watermark, usás incremental. Si no, full refresh controlado.

### 3. Extraer con validación de schema
- Archivos locales: `pandas.read_csv`/`read_parquet` con `dtype` explícito.
- SQL: `pd.read_sql` con chunks si >100k filas. Usar `database-connections`.
- APIs: `api-integration` con paginación y rate-limiting.
- **Validación inmediata**: `df.shape`, tipos de columnas. Si el schema no coincide con lo esperado, ALERTÁS y no continuás.

### 4. Transformar en capas
Orden estricto: **(a) Limpiar** (nulos, duplicados, tipos) → **(b) Enriquecer** (joins, features calculadas) → **(c) Agregar** (groupby, resample, window functions).
Cada capa es una función pura: recibe DataFrame, devuelve DataFrame. Sin side effects.

### 5. Cargar con atomicidad
- **Staging obligatorio**: cargar a tabla temporal o archivo `.tmp`, verificar row count, recién después renombrar/swap.
- `if_exists='replace'` solo si tenés backup o staging previo. Para DBs relacionales: `BEGIN; TRUNCATE staging; INSERT; COMMIT;`.
- Chunked loading si >1M filas: `chunksize=50000` con `method='multi'`.

### 6. Validar post-carga
- Row count origen vs destino.
- Muestreo aleatorio: 10 filas del destino vs fuente.
- Si se configuraron constraints (no nulos, rangos, unicidad), verificarlos contra el destino.
- Si algo falla, logueás WARNING o ERROR según severidad.

### 7. Logging, monitoreo y reporte
- Logging estructurado desde el segundo 0: timestamps, duración de cada etapa, row counts.
- Si es pipeline recurrente, dejás hook para monitoreo (archivo de estado, callback, o métrica).
- Devolvés al orchestrator: resultado (éxito/fallo), estadísticas, ruta del output.
