# Patterns: Data ETL Cheat Sheet

## Patrones de extracción

### Full refresh

```python
# Apropiado para: dimensiones pequeñas (<500k), tablas sin watermark
def extract_full(engine, table: str) -> pd.DataFrame:
    log.info(f"Extrayendo FULL de {table}")
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    log.info(f"Extraídas {len(df):,} filas de {table}")
    return df
```

### Incremental por timestamp (el más común)

```python
def cargar_watermark(path: str = "watermark.json") -> str | None:
    try:
        with open(path) as f:
            return json.load(f).get("last_run")
    except FileNotFoundError:
        return None

def guardar_watermark(ts: str, path: str = "watermark.json"):
    with open(path, "w") as f:
        json.dump({"last_run": ts}, f)

def extract_incremental(engine, table: str, ts_col: str) -> pd.DataFrame:
    watermark = cargar_watermark()
    if watermark:
        query = f"SELECT * FROM {table} WHERE {ts_col} > :watermark ORDER BY {ts_col}"
        df = pd.read_sql(query, engine, params={"watermark": watermark})
    else:
        df = pd.read_sql(f"SELECT * FROM {table}", engine)
    nueva_watermark = df[ts_col].max() if not df.empty else watermark
    if nueva_watermark:
        guardar_watermark(str(nueva_watermark))
    return df
```

### Por ID secuencial

```python
def extract_incremental_id(engine, table: str, id_col: str) -> pd.DataFrame:
    max_id = cargar_watermark() or 0
    query = f"SELECT * FROM {table} WHERE {id_col} > :max_id ORDER BY {id_col}"
    df = pd.read_sql(query, engine, params={"max_id": max_id})
    if not df.empty:
        guardar_watermark(str(df[id_col].max()))
    return df
```

### API con paginación y rate limiting

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import time

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
def fetch_page(url: str, params: dict) -> list[dict]:
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    time.sleep(0.5)  # rate limiting preventivo
    return resp.json()

def extract_api_paginated(base_url: str, page_size: int = 1000) -> pd.DataFrame:
    all_data = []
    page = 1
    while True:
        data = fetch_page(base_url, {"page": page, "limit": page_size})
        if not data:
            break
        all_data.extend(data)
        log.info(f"API page {page}: {len(data)} registros")
        page += 1
    return pd.DataFrame(all_data)
```

## Patrones de carga

### Carga atómica a archivo Parquet

```python
from pathlib import Path

def save_parquet_atomic(df: pd.DataFrame, path: str) -> str:
    out = Path(path)
    tmp = out.with_suffix(".tmp.parquet")
    df.to_parquet(tmp, index=False)
    if out.exists():
        out.unlink()
    tmp.rename(out)
    log.info(f"Guardado atómico: {path} ({len(df):,} filas)")
    return str(out)
```

### Carga atómica a SQL (staging → swap)

```python
def load_sql_atomic(df: pd.DataFrame, engine, table: str, pk_cols: list[str] | None = None):
    staging = f"staging_{table}"
    with engine.begin() as conn:
        df.to_sql(staging, conn, if_exists="replace", index=False, chunksize=50000)
        count = conn.execute(text(f"SELECT COUNT(*) FROM {staging}")).scalar()
        if count != len(df):
            raise RuntimeError(f"Row count mismatch: staging={count}, df={len(df)}")
        conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
        conn.execute(text(f"ALTER TABLE {staging} RENAME TO {table}"))
    log.info(f"Carga atómica: {table} ({count:,} filas)")
```

### Upsert en MySQL

```sql
INSERT INTO target (id, monto, fecha)
SELECT s.id, s.monto, s.fecha
FROM staging s
ON DUPLICATE KEY UPDATE monto = s.monto, fecha = s.fecha;
```

### UPSERT en PostgreSQL

```sql
INSERT INTO target (id, monto, fecha)
SELECT id, monto, fecha FROM staging
ON CONFLICT (id) DO UPDATE SET monto = EXCLUDED.monto, fecha = EXCLUDED.fecha;
```

### Carga chunked para datasets grandes

```python
def load_chunked(df: pd.DataFrame, engine, table: str, chunksize: int = 50000):
    with engine.begin() as conn:
        for i in range(0, len(df), chunksize):
            chunk = df.iloc[i:i + chunksize]
            chunk.to_sql(table, conn, if_exists="append", index=False)
            log.info(f"Chunk {i}-{i+len(chunk)}: {len(chunk)} filas cargadas")
```

## Patrones de transformación

### Pipeline de funciones puras

```python
def pipeline_ventas(raw: pd.DataFrame) -> pd.DataFrame:
    return (raw
        .pipe(_limpiar_nulos)
        .pipe(_normalizar_fechas)
        .pipe(_calcular_monto_neto)
        .pipe(_agregar_diario)
    )

def _limpiar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["id", "fecha", "monto"])

def _normalizar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(fecha=pd.to_datetime(df["fecha"]))

def _calcular_monto_neto(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(monto_neto=df["monto"] - df["descuento"].fillna(0))

def _agregar_diario(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(pd.Grouper(key="fecha", freq="D")).agg(
        total_ventas=("monto_neto", "sum"),
        transacciones=("id", "count"),
        ticket_promedio=("monto_neto", "mean"),
    ).reset_index()
```

### Schema evolution — detección de cambios

```python
def validar_schema(df: pd.DataFrame, schema_esperado: dict[str, str]):
    """schema_esperado: {"col": "int64", "fecha": "datetime64[ns]"}"""
    errores = []
    for col, tipo_esperado in schema_esperado.items():
        if col not in df.columns:
            errores.append(f"Columna faltante: {col}")
            continue
        if str(df[col].dtype) != tipo_esperado:
            errores.append(f"Tipo incorrecto en {col}: esperado {tipo_esperado}, recibido {df[col].dtype}")
    if errores:
        raise SchemaMismatchError("\n".join(errores))
```

### Slowly Changing Dimensions (SCD)

| Tipo | Descripción | Cuándo usarlo |
|---|---|---|
| **SCD Tipo 1** | Sobrescribís el valor anterior. No hay historial. | Atributos que no importa mantener histórico (ej: teléfono actual) |
| **SCD Tipo 2** | Agregás nueva fila con `valid_from`, `valid_to`, `is_current`. | Atributos donde el historial es clave de negocio (ej: categoría de producto, segmento de cliente) |
| **SCD Tipo 3** | Agregás columna de "anterior" al lado de la actual. | Cuando solo importa el valor inmediatamente anterior |

## Anti-patrones (lo que NUNCA hacés)

| Anti-patrón | Qué es | Riesgo | Alternativa |
|---|---|---|---|
| **Hardcodear credenciales** | User/pass/host en el código fuente | Seguridad: exposición en repos, logs, backups | Variables de entorno o secrets manager |
| **No loguear errores** | `except: pass` o solo `print()` | Imposible debuggear sin contexto | `logging.error()` con traceback y métricas |
| **Pipelines sin validación** | Cargar datos sin verificar row counts ni schema | Datos corruptos en prod sin detectar | Validación post-carga automática (paso 5) |
| **Datos sin staging** | Escribir directo al destino final, sobrescribir sin backup | Datos perdidos si el pipeline falla a medio camino | Staging → swap atómico |
| **No tipar columnas** | Dejar que pandas infiera tipos | Sorpresas: un int se vuelve float por un NaN, una fecha se lee como string | `dtype` explícito en `read_csv()`, `astype()` después |
| **`iterrows()` en datasets grandes** | Loop fila por fila en >100k registros | Rendimiento pésimo (10-100x más lento) | Operaciones vectoriales, `apply()` o groupby |
| **Una sola función monolítica** | 500 líneas de transformación en una función | Imposible testear, debuggear, o reusar | Pipeline de funciones puras (una por capa) |
| **Ignorar encoding** | Asumir que los CSVs vienen en UTF-8 | Caracteres rotos, crashes en `read_csv` | `encoding="utf-8"` con fallback a `latin-1` o `cp1252` |
| **Sin reintentos en red** | Una llamada HTTP sin retry | Pipeline frágil ante caídas transitorias | `tenacity` con exponential backoff |
| **Sin watermark guardado** | Calcular el incremental cada vez desde 0 o desde fecha fija | Reprocesa datos viejos o pierde ventana de datos | Guardar watermark en archivo o tabla de control |

## Configuración externa (YAML) — ejemplo

```yaml
# config.yaml
pipeline:
  name: ventas_diarias
  version: 2.1

sources:
  ventas_db:
    type: mysql
    connection_string: "${VENTAS_DB_URL}"      # desde env var
    query: "SELECT * FROM ventas WHERE fecha >= :desde"
    incremental_col: "fecha_actualizacion"
    chunk_size: 50000

  productos:
    type: csv
    path: "data/sources/productos.csv"
    encoding: "utf-8"
    dtype:
      id: int32
      sku: string

targets:
  ventas_diarias:
    type: parquet
    path: "data/processed/ventas/{fecha}.parquet"
    compression: snappy

  ventas_resumen:
    type: sqlite
    table: resumen_ventas
    mode: upsert
    pk: ["fecha"]

logging:
  level: INFO
  file: "logs/pipeline.log"
  format: json

notifications:
  on_error:
    - type: slack
      webhook: "${SLACK_WEBHOOK_URL}"
```

## Manejo de errores con reintentos

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
)
def descargar_con_reintento(url: str) -> bytes:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.content
```

## Decisiones rápidas

| Situación | Decisión |
|---|---|
| <100k filas, 1 fuente, sin watermark | Full refresh con staging. Simple, confiable |
| >1M filas, columna `updated_at` | Incremental con watermark. Guardás en JSON o tabla de control |
| >10M filas, múltiples fuentes | Chunked processing + DAG con funciones puras. Considerar Dask/Polars |
| APIs externas | Paginación + rate limiting + exponential backoff |
| Base de datos transaccional como fuente | CDC si es en vivo, incremental si es batch diario |
| Destino = Parquet local | Staging atómico con `.tmp.parquet` → rename |
| Destino = PostgreSQL | Staging table → `BEGIN; TRUNCATE; INSERT; COMMIT;` o `ON CONFLICT DO UPDATE` |
| Necesitás historial de cambios | SCD Type 2 con `valid_from`, `valid_to`, `is_current` |
| Carga recurrente diaria | Pipeline configurable por fecha: `python run.py --date 2024-01-01` |

## Logging boilerplate

```python
import logging
import sys

def setup_logger(name: str, level: str = "INFO", log_file: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler (opcional)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
```

## Checklist pre-entrega

Antes de dar un pipeline por terminado, verificás:

- [ ] **Idempotencia comprobada:** corré el pipeline dos veces con los mismos parámetros → los datos destino son idénticos (sin duplicados).
- [ ] **Logging completo:** cada etapa loguea filas in/out, duración, y errores. Los logs se pueden parsear.
- [ ] **Manejo de errores:** toda llamada externa (API, DB, archivo) tiene try/except o retry decorator.
- [ ] **Config externalizada:** credenciales vía env vars, rutas y parámetros en YAML/TOML.
- [ ] **Staging implementado:** ningún pipeline escribe directo al destino final sin tabla/archivo temporal.
- [ ] **Validación post-carga:** row count match, sin duplicados en PK, tipos correctos.
- [ ] **Pipeline re-ejecutable:** `python run.py --date 2024-01-01` funciona aunque esa fecha ya se haya procesado (upsert o replace controlado).
- [ ] **Watermark guardado:** si es incremental, el watermark persiste y se usa en la próxima corrida.
- [ ] **Documentación inline:** cada función tiene docstring con qué hace, qué recibe y qué devuelve.
- [ ] **Sin hardcodeos:** no hay IPs, passwords, tokens, ni paths absolutos en el código.
