# Patterns: ETL Pipelines Cheat Sheet

## Extract — fuentes más comunes

```python
# CSV con schema explícito
df = pd.read_csv('datos.csv', dtype={'id': 'int32', 'cat': 'category'},
                 parse_dates=['fecha'], encoding='utf-8')

# Parquet (rápido, preserva tipos)
df = pd.read_parquet('datos.parquet')

# SQL con chunks (datasets grandes)
for chunk in pd.read_sql("SELECT * FROM ventas", conn, chunksize=50000):
    process(chunk)

# API con paginación
all_data = []
page = 1
while True:
    resp = requests.get(f"{url}?page={page}&limit=1000")
    data = resp.json()
    if not data: break
    all_data.extend(data)
    page += 1
```

## Transform — pipeline de funciones puras

```python
def pipeline(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .pipe(limpiar_nulos)
        .pipe(normalizar_fechas)
        .pipe(enriquecer_con_join, otras_tablas)
        .pipe(agregar_diario)
    )

def limpiar_nulos(df): return df.dropna(subset=['id', 'fecha'])
def normalizar_fechas(df): return df.assign(fecha=pd.to_datetime(df['fecha']))
def enriquecer_con_join(df, lookup): return df.merge(lookup, on='cat_id', how='left')
def agregar_diario(df): return df.groupby('fecha')['monto'].sum().reset_index()
```

## Load — atomicidad con staging

```python
# Carga atómica a archivo: escribir .tmp, luego renombrar
out = Path('data/output.parquet')
tmp = out.with_suffix('.tmp.parquet')
df.to_parquet(tmp, index=False)
tmp.rename(out)                        # atómico en mismo filesystem

# Carga atómica a SQL: staging → swap
with engine.begin() as conn:
    df.to_sql('staging_ventas', conn, if_exists='replace', index=False)
    conn.execute(text("BEGIN"))
    conn.execute(text("DELETE FROM ventas WHERE fecha = :fecha"), {'fecha': run_date})
    conn.execute(text("INSERT INTO ventas SELECT * FROM staging_ventas"))
    conn.execute(text("COMMIT"))
```

## Manejo de errores con reintentos

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
def extraer_con_reintento(ruta: str) -> pd.DataFrame:
    return pd.read_parquet(ruta)
```

## Logging estructurado

```python
import logging, time

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s')
log = logging.getLogger("pipeline")

def etapa(nombre: str, df: pd.DataFrame, fn):
    t0 = time.time()
    result = fn(df)
    log.info(f"[{nombre}] {len(df):,} → {len(result):,} filas | {time.time()-t0:.1f}s")
    return result
```

## Configuración externa (YAML)

```python
# config.yaml
# sources:
#   ventas: {path: data/raw/ventas.csv, encoding: utf-8}
# output: {format: parquet, path: data/processed/}
# dates: {col: fecha, format: "%Y-%m-%d"}

with open('config.yaml') as f:
    cfg = yaml.safe_load(f)

df = pd.read_csv(cfg['sources']['ventas']['path'],
                 encoding=cfg['sources']['ventas']['encoding'])
```

## Decisiones rápidas

| Situación | Decisión |
|---|---|
| <100k filas, 1 fuente | Script simple con pandas + logging |
| >1M filas, múltiples fuentes | DAG con funciones puras, chunks, staging |
| Destino = data warehouse | ELT: extract raw, transform en SQL del warehouse |
| Frecuencia horaria/diaria | Batch con `schedule` o Airflow |
| Latencia <1min requerida | Streaming con Kafka + procesador |
| Columna `updated_at` disponible | Pipeline incremental con watermark |
| Sin watermark, datos <1M | Full refresh diario con staging y swap atómico |
