---
name: etl-pipelines
description: >
  Patrones ETL/ELT para pipelines de datos: extracción, transformación y carga con Pandas y Python.
  Trigger: Cuando necesitás construir un pipeline de datos, procesar archivos en batch, automatizar transformaciones, o diseñar el flujo de datos de un proyecto.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: etl-pipelines

## Para qué sirve

Diseñar y automatizar pipelines ETL/ELT (Extraer → Transformar → Cargar) con Python. El objetivo es que los datos fluyan de forma confiable desde origen a destino, con logging, manejo de errores, y capacidad de re-ejecución.

## Trigger (cuándo cargar esta skill)

- Vas a construir un pipeline batch que corre periódicamente
- Tenés que extraer datos de múltiples fuentes, transformarlos, y llevarlos a un destino
- Necesitás procesar archivos en lote con consistencia y logging
- Querés automatizar un flujo que hoy hacés a mano con scripts sueltos

## Workflow paso a paso

1. **Identificá orígenes y destino**: ¿de dónde vienen los datos? (CSV, API, DB, S3) ¿adónde van? (Parquet, DB, Data Warehouse)
2. **Diseñá la E**: Extracción idempotente — si se corta a la mitad, que se pueda re-ejecutar sin duplicar. Usá `logging` para saber cuánto se extrajo.
3. **Diseñá la T**: Cada transformación en función separada y testeable. No mezcles limpieza con feature engineering en la misma función.
4. **Diseñá la L**: Carga siempre en modo append o replace. Si es append, asegurate de tener un control de duplicados.
5. **Agregá manejo de errores**: No dejes que un error en un archivo rompa todo el lote.
6. **Programá la ejecución**: `schedule` para local, cron para servidor, o Prefect/Airflow para orquestación seria.

## Patrones esenciales

### 1. Pipeline modular con logging

Separar cada etapa en su función. El logging es tu tablero de control: cuando falla, sabés en qué paso sin leer código.

```python
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s — %(levelname)s — %(message)s')
log = logging.getLogger(__name__)

def extraer(ruta: str) -> pd.DataFrame:
    log.info(f"Extrayendo datos de {ruta}")
    return pd.read_csv(ruta, encoding='utf-8')

def transformar(df: pd.DataFrame) -> pd.DataFrame:
    log.info("Transformando datos...")
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
    return df.dropna(subset=['id', 'fecha']).drop_duplicates(subset='id')

def cargar(df: pd.DataFrame, destino: str) -> None:
    df.to_parquet(destino, index=False)
    log.info(f"Cargados {len(df):,} registros")

def pipeline(origen: str, destino: str) -> None:
    inicio = datetime.now()
    cargar(transformar(extraer(origen)), destino)
    log.info(f"Pipeline completado en {(datetime.now()-inicio).seconds}s")
```

### 2. Chunking para datasets grandes

Si el archivo no entra en memoria, no lo fuerces. Pandas te deja leer por chunks y procesar de a tandas. Esto evita OOM (Out of Memory) kills.

```python
def procesar_grande(ruta: str, destino: str, chunk_size: int = 50_000):
    log.info(f"Procesando {ruta} en chunks de {chunk_size:,}")
    resultados = []
    for i, chunk in enumerate(pd.read_csv(ruta, chunksize=chunk_size)):
        log.info(f"  Chunk {i+1}...")
        chunk = transformar(chunk)
        resultados.append(chunk)
    df_final = pd.concat(resultados, ignore_index=True)
    df_final.to_parquet(destino, index=False)
    log.info(f"Total: {len(df_final):,} registros")
```

### 3. Pipeline con reporte de resultados

Devolver un objeto estructurado permite que el orquestador sepa si el pipeline funcionó.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ResultadoPipeline:
    exitoso: bool; registros: int; errores: list; duracion: float

def pipeline_robusto(origen: str, destino: str) -> ResultadoPipeline:
    errores = []; inicio = datetime.now()
    try:
        df = extraer(origen)
    except FileNotFoundError:
        return ResultadoPipeline(False, 0, [f"No encontrado: {origen}"], 0)
    try:
        df = transformar(df)
    except Exception as e:
        errores.append(f"Error en transformación: {e}")
    try:
        cargar(df, destino)
    except Exception as e:
        return ResultadoPipeline(False, 0, [f"Error en carga: {e}"], 0)
    return ResultadoPipeline(True, len(df), errores, (datetime.now()-inicio).total_seconds())
```

### 4. Programación con schedule (para scripts locales)

```python
import schedule, time

schedule.every().day.at("06:00").do(lambda: pipeline_robusto('raw.csv', 'proc.parquet'))
schedule.every().monday.at("08:00").do(lambda: pipeline_robusto('raw2.csv', 'proc2.parquet'))

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Alternativas

- **Prefect / Dagster**: Orquestación profesional con UI, retry automático, y dependencias entre tareas. Usalas cuando tengas +5 pipelines o necesites monitoreo serio.
- **Airflow**: El estándar corporativo. Más pesado de configurar, pero si tu equipo ya lo usa, no inventes la rueda.
- **pandas vs polars**: Si tu pipeline procesa millones de filas, considerá [Polars](https://www.pola.rs) que es más rápido y usa menos memoria. Misma API mental, otro motor.
- **SQL puro (ELT)**: Si los datos ya están en una DB, hacé las transformaciones en SQL con `dbt`. Más rápido y más fácil de auditar.

## Anti-patrones

- ❌ **Pipeline monolítico**: Una sola función de 200 líneas que extrae, limpia, transforma y carga. Imposible de testear, imposible de debuggear.
- ❌ **No loggear**: Si no hay logs, cuando falla no sabés en qué paso. Es como manejar con los ojos cerrados.
- ❌ **Datos en memoria sin chunking**: Cargar 10 GB en un DataFrame con 8 GB de RAM. Eventualmente va a explotar.
- ❌ **Ignorar tipos de dato**: Dejar que pandas infiera todo automáticamente y después sorprenderte cuando `id` se convierte en float.
- ❌ **No hacer copia en transformación**: Usar `df.dropna(inplace=True)` modifica el original y puede causar side effects. Usá `df = df.copy()` al entrar a transformar.

## Comandos

```bash
pip install schedule prefect  # o solo schedule para local

# Correr pipeline
python pipeline.py

# Log a archivo
python pipeline.py 2>&1 | tee logs/pipeline_$(date +%Y%m%d).log
```
