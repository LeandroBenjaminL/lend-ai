# Workflow: Data ETL

## Flujo principal

```
Orchestrator → [1. Analizar origen/destino] → [2. Estrategia de extracción] → [3. Pipeline de transformación] → [4. Carga con atomicidad] → [5. Validación post-carga] → [6. Monitoreo y reporte] → Orchestrator
```

## Paso a paso

### 1. Analizar origen y destino

Leer el prompt. Identificar y definir:

- **Origen(es):** path, tabla SQL, API endpoint, archivo. Formato (CSV, Parquet, JSON, Avro). Volumen estimado.
- **Destino:** base de datos (MySQL, PostgreSQL, SQLite), archivo (Parquet, CSV), data lake (S3, GCS), warehouse (BigQuery, Snowflake).
- **Frecuencia:** one-shot, diario, horario, en tiempo real.
- **Latencia aceptable:** batch común, near-real-time, streaming.
- **Schema esperado:** definido por el orchestrator o a descubrir. Si no está definido, lo inferís y reportás.
- **Particularidades:** encoding, delimitador, compresión, autenticación.

Si algo no está claro, preguntás antes de escribir. No asumís nada sobre el schema, volumen, o formato.

### 2. Definir estrategia de extracción

Elegís según la fuente y el volumen. Tabla de estrategias:

| Estrategia | Cuándo usarla | Cómo se implementa | Ventaja | Riesgo |
|---|---|---|---|---|
| **Full refresh** | Datos pequeños (<500k filas), tablas de dimensiones, sin watermark disponible | `SELECT * FROM tabla`, truncar y recargar | Simple, 100% consistente | Pesado para grandes volúmenes |
| **Incremental por timestamp** | Tablas con `updated_at` / `created_at`, tablas de hechos | `WHERE updated_at > :last_run` con watermark guardado | Rápido, baja latencia, bajo volumen | Si el timestamp no se actualiza bien, perdés cambios |
| **Incremental por ID** | Tablas append-only con ID secuencial | `WHERE id > :last_max_id` | Simple, eficiente, no requiere timestamp | No captura updates ni deletes |
| **CDC (Change Data Capture)** | Sistemas transaccionales, replicación en tiempo real | Debezium + Kafka, o binlog parsing | Captura todo (insert, update, delete), mínima latencia | Complejo de operar, requiere infra adicional |
| **API paginada** | Fuentes externas sin DB directa | `page` + `limit` o cursor-based pagination | Funciona con cualquier API pública | Rate limiting, lentitud en muchas páginas |
| **Snapshot diferencial** | Fuentes sin timestamp ni ID incremental | FULL extract → comparar con snapshot anterior → diff | Útil para fuentes sin metadatos de cambio | Costoso, requiere almacenar snapshots |

**Decisión por defecto:** si hay `updated_at` o similar, incremental con watermark. Si no, full refresh con staging. CDC solo si el orchestrator lo pide explícitamente.

Guardás la metadata de la corrida (watermark, max_id, timestamp) en un archivo JSON, tabla de control, o variable de entorno — lo que sea durable y accesible en la próxima corrida.

### 3. Pipeline de transformación

Las transformaciones van en CAPAS, en este orden estricto. Cada capa es una función pura:

```python
def pipeline(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .pipe(limpiar_nulos)           # Capa 1: limpieza básica
        .pipe(normalizar_tipos)        # Capa 2: tipado correcto
        .pipe(enriquecer)              # Capa 3: joins, features calculadas
        .pipe(agregar)                 # Capa 4: agrupaciones, resamples
        .pipe(renombrar_columnas)      # Capa 5: naming estándar
    )
```

- **Capa 1 — Limpieza:** dropear columnas con >60% nulos, imputar según contexto, eliminar duplicados explícitos.
- **Capa 2 — Normalización:** `astype()`, `pd.to_datetime()`, strings a lowercase, encoding consistency (UTF-8 siempre).
- **Capa 3 — Enriquecimiento:** joins con tablas de referencia, cálculo de features derivadas, flag columns para datos sospechosos.
- **Capa 4 — Agregación:** groupby, resample temporal, window functions. Siempre con `.reset_index()` al final.
- **Capa 5 — Output naming:** columnas en snake_case, sin espacios, sin caracteres especiales. Unidades en el nombre (`monto_usd`, `temp_celsius`).

Cada función recibe y devuelve DataFrame. Sin efectos secundarios. Sin archivos intermedios (todavía). Logging del row count antes/después de cada capa.

Para datasets grandes (>1M filas):
- Usar `chunksize` en pandas o Dask/Modin si el volumen lo amerita.
- Transformaciones vectoriales, nunca loops con `iterrows()`.
- Operaciones `groupby` y `merge` con índices definidos.

### 4. Carga con atomicidad

Nunca escribís directo al destino final. Usás STAGING siempre.

**Para archivos:**
```python
out_path = Path("data/processed/ventas.parquet")
tmp_path = out_path.with_suffix(".tmp.parquet")
df.to_parquet(tmp_path, index=False)
tmp_path.rename(out_path)  # atómico en el mismo filesystem
```

**Para SQL:**
```python
with engine.begin() as conn:
    df.to_sql("staging_ventas", conn, if_exists="replace", index=False, chunksize=50000)
    conn.execute(text("BEGIN"))
    conn.execute(text("DELETE FROM ventas WHERE fecha_carga = :fecha"), {"fecha": fecha})
    conn.execute(text("INSERT INTO ventas SELECT * FROM staging_ventas"))
    conn.execute(text("DROP TABLE IF EXISTS staging_ventas"))
    conn.execute(text("COMMIT"))
```

**Para upsert (incremental):**
```python
with engine.begin() as conn:
    df.to_sql("staging_upsert", conn, if_exists="replace", index=False)
    conn.execute(text("""
        INSERT INTO ventas (id, monto, fecha)
        SELECT s.id, s.monto, s.fecha
        FROM staging_upsert s
        ON DUPLICATE KEY UPDATE monto = s.monto, fecha = s.fecha
    """))
```

Reglas de la carga:
- `chunksize=50000` para tablas grandes (evitá memory overflow).
- Verificás que el row count del staging coincida con lo esperado antes del swap.
- Si la carga falla a medio camino, no queda estado inconsistente: el staging se dropea si hay error, y el destino no se tocó.
- Siempre cerrás conexiones en `finally` o con context manager.

### 5. Validación post-carga

Checklist obligatorio:

- [ ] **Row count match:** destino final = staging = pipeline output (counts).
- [ ] **No nulos inesperados:** columnas que no deberían tener nulos → `df['col'].isnull().sum()` = 0.
- [ ] **Tipos correctos:** schema del destino coincide con lo declarado.
- [ ] **Sin duplicados:** primary key/unique columns sin duplicados.
- [ ] **Rangos lógicos:** valores dentro de rangos esperados (ej: edad entre 0 y 120).
- [ ] **Muestreo:** 5-10 filas aleatorias del destino comparadas contra la fuente original.
- [ ] **Consistencia temporal:** fechas sin saltos, watermark avanzó correctamente.

Si alguna validación falla:
- **WARNING** si es no-crítico (ej: rangos fuera de lo esperado pero plausibles). Se reporta pero no bloquea.
- **ERROR** si es crítico (ej: row count mismatch mayor a 5%, nulos en PK, duplicados en unique key). Se aborta y se restaura el estado previo.
- **CRITICAL** si el destino quedó inconsistente (data corruption, staging no dropeada). Se alerta al orchestrator INMEDIATAMENTE.

### 6. Monitoreo, logging y reporte

Logging estructurado desde el pipeline:

```python
import logging, time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)
log = logging.getLogger("etl.ventas")
```

Cada etapa loguea:
```python
def log_etapa(nombre: str, df: pd.DataFrame, fn):
    t0 = time.time()
    try:
        resultado = fn(df)
        log.info(
            f"[{nombre}] filas: {len(df):,} → {len(resultado):,} "
            f"| duración: {time.time()-t0:.1f}s"
        )
        return resultado
    except Exception as e:
        log.error(f"[{nombre}] FALLÓ | filas: {len(df):,} | error: {e}", exc_info=True)
        raise
```

Al final, devolvés al orchestrator:

- **Resultado:** éxito o error (con mensaje y stacktrace).
- **Estadísticas:** filas origen, filas destino, filas transformadas, duración total, watermark actual.
- **Output:** ruta del archivo generado o tabla cargada.
- **Alertas:** advertencias encontradas (nulos inesperados, tipos inferidos distintos, etc.).
