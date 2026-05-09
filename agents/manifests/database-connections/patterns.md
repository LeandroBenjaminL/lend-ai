# Patterns: Database Connections Cheat Sheet

## Connection Strings

```python
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# === Desde variable de entorno (recomendado) ===
engine = create_engine(os.getenv('DATABASE_URL'))

# === PostgreSQL ===
engine = create_engine('postgresql://user:password@host:5432/database')
engine = create_engine('postgresql+psycopg2://user:password@host:5432/database')  # driver explícito

# === MySQL ===
engine = create_engine('mysql+pymysql://user:password@host:3306/database')

# === SQLite ===
engine = create_engine('sqlite:///datos.db')       # archivo
engine = create_engine('sqlite:///:memory:')        # en memoria (tests)

# === Con parámetros extra ===
engine = create_engine(
    os.getenv('DATABASE_URL'),
    pool_size=10,           # conexiones en el pool
    max_overflow=20,        # extras sobre pool_size
    pool_pre_ping=True,     # ping antes de usar (SIEMPRE en prod)
    pool_recycle=3600,      # reciclar conexiones cada 1h
    echo=False              # True para debuggear queries SQL
)
```

---

## Context Manager (EL patrón que siempre usás)

```python
from sqlalchemy import text

# === Lectura: engine.connect() ===
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM ventas"))
    total = result.scalar()
    print(f"Total: {total}")
# conexión cerrada automáticamente

# === Transacción: engine.begin() ===
with engine.begin() as conn:
    conn.execute(text("UPDATE precios SET valor = valor * 1.1 WHERE categoria = 'A'"))
    conn.execute(text("INSERT INTO log (accion) VALUES ('aumento_precios')"))
# commit automático al salir, rollback si hay excepción

# === Transacción con commit manual ===
with engine.connect() as conn:
    with conn.begin():  # inicia transacción
        conn.execute(text("DELETE FROM staging"))
        # si algo falla, rollback automático
    # conn sigue abierta para más operaciones
```

---

## Pandas ↔ Base de Datos

```python
import pandas as pd

# === LEER ===

# Query simple
df = pd.read_sql('SELECT * FROM ventas LIMIT 1000', engine)

# Query con parámetros (seguro, anti-injection)
df = pd.read_sql(
    "SELECT * FROM ventas WHERE fecha >= %(inicio)s AND categoria = %(cat)s",
    engine,
    params={'inicio': '2024-01-01', 'cat': 'electrónica'}
)

# Chunked reading (tablas grandes, no explota memoria)
chunks = []
for chunk in pd.read_sql('SELECT * FROM tabla_grande', engine, chunksize=10000):
    chunks.append(chunk.procesar())  # procesar chunk a chunk
df = pd.concat(chunks)

# === ESCRIBIR ===

# Crear tabla nueva
df.to_sql('tabla_nueva', engine, if_exists='replace', index=False)

# Agregar filas a tabla existente
df.to_sql('tabla_existente', engine, if_exists='append', index=False)

# Con tipos SQL específicos
from sqlalchemy import types
df.to_sql('ventas', engine, if_exists='replace', index=False, dtype={
    'fecha': types.Date(),
    'monto': types.Float(),
    'categoria': types.String(100)
})

# Insert masivo con method='multi' (más rápido para muchas filas)
df.to_sql('ventas', engine, if_exists='append', index=False, method='multi', chunksize=1000)

# Insert con psycopg2 directo (máxima velocidad para PostgreSQL)
import psycopg2
from psycopg2.extras import execute_values
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
with conn.cursor() as cur:
    execute_values(cur, "INSERT INTO ventas (col1, col2) VALUES %s", df.values.tolist())
conn.commit()
conn.close()
```

---

## Connection Pooling

```python
# === Pool básico ===
engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # conexiones mantenidas abiertas
    max_overflow=10,    # extras temporales bajo pico de carga
    pool_pre_ping=True, # testea conexión antes de usarla
    pool_recycle=1800   # recicla cada 30 min (evita timeout del server)
)

# === Pool en aplicaciones web (Flask/FastAPI) ===
# Crear el engine UNA vez a nivel módulo, reusarlo en todos los requests
# NUNCA crear un engine por request

# === Ver estado del pool ===
print(engine.pool.status())  # "Pool size: 5  Connections in pool: 2 ..."

# === Cerrar todo el pool al terminar ===
engine.dispose()  # cierra todas las conexiones, libera recursos
```

---

## psycopg2 (PostgreSQL directo, sin SQLAlchemy)

```python
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

# Conexión
conn = psycopg2.connect(
    host=os.getenv('PGHOST'),
    dbname=os.getenv('PGDATABASE'),
    user=os.getenv('PGUSER'),
    password=os.getenv('PGPASSWORD')
)

try:
    # Cursor como diccionario
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # SELECT con parámetros
        cur.execute("SELECT * FROM ventas WHERE categoria = %s", ('electrónica',))
        rows = cur.fetchall()

    # Insert masivo (más rápido que to_sql para PostgreSQL)
    with conn.cursor() as cur:
        execute_values(cur, "INSERT INTO ventas (col1, col2) VALUES %s", df.values.tolist())

    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
```

---

## SQLite nativo (sqlite3)

```python
import sqlite3

# Conexión con context manager
with sqlite3.connect('datos.db') as conn:
    # Crear tabla
    conn.execute('CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY, monto REAL)')

    # Insertar
    conn.execute('INSERT INTO ventas (monto) VALUES (?)', (150.0,))
    conn.commit()

    # Leer con Pandas
    df = pd.read_sql('SELECT * FROM ventas', conn)

# Conexión en memoria para tests
with sqlite3.connect(':memory:') as conn:
    df.to_sql('ventas', conn, index=False)
    result = pd.read_sql('SELECT COUNT(*) as n FROM ventas', conn)
```

---

## Manejo de Errores

```python
from sqlalchemy.exc import (
    OperationalError,   # conexión caída, host no encontrado
    TimeoutError,        # timeout de conexión
    ProgrammingError,    # error de sintaxis SQL, tabla no existe
    IntegrityError,      # violación de constraint
    InternalError        # errores internos del motor
)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except OperationalError as e:
    raise ConnectionError(f"No se pudo conectar. Error: {e.orig}") from e
except TimeoutError:
    raise ConnectionError("Timeout. ¿El servidor responde?")
except ProgrammingError as e:
    raise ValueError(f"Error en la query SQL: {e}") from e
except IntegrityError as e:
    raise ValueError(f"Violación de integridad (FK, unique, etc): {e.orig}") from e
```

---

## Reglas de Oro

| # | Regla | Por qué |
|---|-------|---------|
| 1 | **Credenciales en `.env`, nunca hardcodeadas** | Si commiteás una password, ya es pública para siempre. |
| 2 | **Siempre context manager** (`with engine.connect()`) | Un exception handler no te salva de una connection leak. El `with` sí. |
| 3 | **`pool_pre_ping=True` en producción** | Sin esto, el pool te da conexiones zombie después de un reinicio del server. |
| 4 | **Nunca `SELECT *` en producción** | Explicitás columnas, evitás sorpresas cuando la tabla cambia. |
| 5 | **Parámetros, nunca string interpolation** | `params={'x': valor}` previene SQL injection. `f"WHERE x = {valor}"` no. |
| 6 | **`chunksize` para tablas grandes** | `pd.read_sql(chunksize=10000)` no explota la memoria. |
| 7 | **Un engine por aplicación, no por query** | Crear engines es caro. Uno solo, lo reusás. |
| 8 | **`engine.dispose()` al terminar** | Cerras el pool y liberás conexiones. Buen ciudadano. |
| 9 | **Mensajes de error en español claro** | "Connection refused" no le dice nada al usuario. "No se pudo conectar a la base en host X" sí. |
| 10 | **Probar conexión con `SELECT 1`** | Antes de mandar una query de 200 líneas, verificás que la conexión anda. |
