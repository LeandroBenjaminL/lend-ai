---
name: database-connections
description: >
  Conexiones a bases de datos con SQLAlchemy, psycopg2 y otros conectores. Integración con Pandas.
  Trigger: Cuando necesitás conectarte a una base de datos (PostgreSQL, MySQL, SQLite, etc.), ejecutar queries, o leer/escribir tablas con Pandas.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: database-connections

## Para qué sirve

Conectar Python con bases de datos relacionales para leer datos como DataFrames y escribir resultados. SQLAlchemy es el estándar porque abstrae las diferencias entre motores (PostgreSQL, MySQL, SQLite) y se integra perfecto con Pandas.

## Trigger (cuándo cargar esta skill)

- Necesitás leer una tabla de la DB y trabajar con Pandas
- Querés escribir resultados de un análisis directo a una tabla
- Tenés que ejecutar queries con parámetros (sin riesgo de SQL injection)
- Estás configurando la conexión a una DB por primera vez

## Workflow paso a paso

1. **Elegí el conector correcto**: PostgreSQL → `psycopg2-binary`, MySQL → `pymysql`, SQLite → viene con Python
2. **Armá el connection string**: `motor://user:pass@host:puerto/db`
3. **Nunca hardcodees credenciales**: usá variables de entorno o `.env`
4. **Probá la conexión** con un `SELECT 1` antes de mandar queries pesadas
5. **Usá context managers** (`with engine.connect()`) para no dejar conexiones colgadas
6. **Parametrizá siempre** los queries — nunca concatenes strings

## Patrones esenciales

### 1. Connection strings y motores

Cada DB tiene su propio dialecto. SQLAlchemy unifica todo bajo una misma API, pero necesitás el conector correcto instalado.

```python
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
engine = create_engine('postgresql://user:password@host:5432/database')
# MySQL
engine = create_engine('mysql+pymysql://user:password@host:3306/database')
# SQLite (archivo local o en memoria)
engine = create_engine('sqlite:///datos.db')
engine = create_engine('sqlite:///:memory:')  # ideal para tests

# Desde variable de entorno (recomendado)
engine = create_engine(os.getenv('DATABASE_URL'))
```

### 2. Leer datos → DataFrame

`pd.read_sql` acepta una query o un nombre de tabla. Usá parámetros con `params=` para evitar SQL injection — esto es obligatorio si los valores vienen del usuario o de un archivo.

```python
import pandas as pd

# Query simple
df = pd.read_sql('SELECT * FROM ventas LIMIT 1000', engine)

# Con parámetros (seguro contra SQL injection)
query = """SELECT * FROM ventas WHERE fecha >= %(inicio)s AND categoria = %(cat)s"""
df = pd.read_sql(query, engine, params={'inicio': '2024-01-01', 'cat': 'electrónica'})

# Tabla entera (más simple si querés todo)
df = pd.read_sql_table('ventas', engine, schema='public')
```

**¿Por qué parametrizar?** Si concatenás `f"WHERE fecha = '{valor}'"` y `valor` viene de un archivo que dice `'2024-01-01' OR 1=1`, tu query se convierte en un desastre. Los parámetros escapan automáticamente.

### 3. Chunking para tablas grandes

Cuando la tabla tiene millones de filas, `pd.read_sql` sin chunks te va a explotar la RAM. Usá `chunksize` para iterar de a tandas.

```python
chunks = []
for chunk in pd.read_sql('SELECT * FROM tabla_grande', engine, chunksize=10000):
    chunk = procesar(chunk)
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)
```

### 4. Escribir DataFrame → base de datos

```python
# Crear tabla nueva (reemplaza si existe)
df.to_sql('tabla_nueva', engine, if_exists='replace', index=False)

# Agregar filas a tabla existente
df.to_sql('ventas', engine, if_exists='append', index=False)

# Con tipos explícitos (SQLAlchemy types)
from sqlalchemy import types
df.to_sql('ventas', engine, if_exists='replace', dtype={
    'fecha': types.Date(),
    'monto': types.Float(),
    'categoria': types.String(100)
})
```

`if_exists='replace'` hace un DROP TABLE + CREATE. Cuidado si la tabla tiene datos que no querés perder — usá `append` o una tabla temporal.

### 5. Conexión segura con context manager

El `with` cierra la conexión automáticamente, incluso si hay un error. Sin esto, las conexiones se acumulan y eventualmente la DB te rechaza.

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM ventas"))
    total = result.scalar()

# Transacción con commit automático al salir del with
with engine.begin() as conn:
    conn.execute(text("UPDATE precios SET valor = valor * 1.1 WHERE categoria = 'A'"))
```

## Alternativas

- **psycopg2 vs asyncpg**: `psycopg2-binary` es el estándar, pero `asyncpg` es 2-3x más rápido para PostgreSQL porque es asincrónico. Usalo si tenés muchas queries concurrentes.
- **SQLAlchemy vs duckdb**: Para análisis exploratorio, [DuckDB](https://duckdb.org) es mucho más rápido y puede leer directamente de Parquet/CSV sin carga. No es una DB tradicional, es una DB embebida para análisis.
- **Pandas vs polars**: `polars` también tiene `read_database` y suele ser más rápido con datasets grandes.

## Anti-patrones

- ❌ **Credenciales en el código**: `engine = create_engine('postgresql://user:pass@host/db')` duramente en el script. Usá `.env` o variables de entorno siempre.
- ❌ **No cerrar conexiones**: Llamar a `pd.read_sql` sin context manager y dejar conexiones abiertas. Eventualmente te quedás sin conexiones disponibles.
- ❌ **SQL injection por concatenar strings**: `f"SELECT * FROM users WHERE name = '{input}'"` es la forma más rápida de que te hackeen. Usá `params=` siempre.
- ❌ **Cargar tablas enteras sin necesidad**: `pd.read_sql('SELECT * FROM tabla_grande')` cuando solo necesitás 3 columnas. Siempre especificá columnas y filtros.

## Comandos

```bash
pip install sqlalchemy psycopg2-binary pymysql python-dotenv

# Probar conexión rápido
python -c "
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://user:pass@localhost/db')
with engine.connect() as conn:
    print(conn.execute(text('SELECT 1')).scalar())
"
```
