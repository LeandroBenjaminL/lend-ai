# Workflow: Database Connections

## Flujo principal

```
Orchestrator → [1. Definir motor] → [2. Crear connection string] → [3. Context manager o pool] → [4. Ejecutar query] → [5. Cerrar conexión] → [6. Manejar errores] → Orchestrator
```

## Paso a paso

### 1. Definir motor y credenciales

Antes de escribir una sola línea de código, definís:

- **Base de datos**: PostgreSQL, MySQL, SQLite, ¿otra?
- **Driver**: `psycopg2` (PostgreSQL), `pymysql` (MySQL), `sqlite3` (SQLite nativo).
- **Credenciales**: **NUNCA hardcodeadas.** Siempre desde variables de entorno o `.env` con `python-dotenv`.

```python
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
```

Regla de oro: si la variable de entorno no existe, el script **falla temprano** con un mensaje claro, no con un `None` que explota 47 líneas después.

### 2. Crear connection string

Según la base de datos:

| Motor | Formato |
|-------|---------|
| PostgreSQL | `postgresql://user:password@host:5432/database` |
| PostgreSQL + psycopg2 | `postgresql+psycopg2://user:password@host:5432/database` |
| MySQL + pymysql | `mysql+pymysql://user:password@host:3306/database` |
| SQLite (archivo) | `sqlite:///ruta/al/archivo.db` |
| SQLite (memoria) | `sqlite:///:memory:` |

Si la URL viene de variable de entorno, la usás directo. Si no, la armás con `os.getenv` para cada parte (host, port, user, password, dbname).

### 3. Usar context manager o pool

**Siempre** usás context manager. Es la única forma de garantizar que la conexión se cierre, incluso si hay excepción.

```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL, pool_size=5, pool_pre_ping=True)

# Lectura simple
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM tabla"))
    total = result.scalar()

# Transacción (commit automático al salir del with)
with engine.begin() as conn:
    conn.execute(text("UPDATE tabla SET col = valor WHERE condicion"))
```

**Parámetros críticos del pool:**
- `pool_size`: conexiones máximas mantenidas abiertas. Default 5, ajustar según carga.
- `pool_pre_ping=True`: hace un ping antes de usar la conexión. Evita errores si el servidor de BD se reinició. **Siempre en producción.**
- `pool_recycle`: tiempo en segundos para reciclar conexiones. Útil si el server de BD tiene `wait_timeout`.
- `max_overflow`: conexiones extra por encima del pool_size. Default 10.

### 4. Ejecutar query o leer tabla

**Leer con Pandas:**

```python
import pandas as pd

# Query simple
df = pd.read_sql('SELECT * FROM ventas LIMIT 1000', engine)

# Query con parámetros (anti SQL injection)
df = pd.read_sql(
    "SELECT * FROM ventas WHERE fecha >= %(inicio)s AND categoria = %(cat)s",
    engine,
    params={'inicio': '2024-01-01', 'cat': 'electrónica'}
)

# Chunks para tablas grandes
for chunk in pd.read_sql('SELECT * FROM tabla_grande', engine, chunksize=10000):
    chunk.to_csv('output.csv', mode='a', header=False)
```

**Escribir con Pandas:**

```python
# Crear tabla nueva
df.to_sql('tabla_nueva', engine, if_exists='replace', index=False)

# Insertar en tabla existente
df.to_sql('tabla_existente', engine, if_exists='append', index=False)

# Con tipos específicos
from sqlalchemy import types
df.to_sql('ventas', engine, if_exists='replace', index=False, dtype={
    'fecha': types.Date(),
    'monto': types.Float(),
    'categoria': types.String(100)
})
```

**Ejecutar SQL directo (sin Pandas):**

```python
from sqlalchemy import text

with engine.connect() as conn:
    # SELECT
    result = conn.execute(text("SELECT id, nombre FROM usuarios WHERE activo = :activo"), {'activo': True})
    rows = result.fetchall()

    # INSERT / UPDATE / DELETE (usar engine.begin() para transacción)
    with engine.begin() as txn:
        txn.execute(text("INSERT INTO log (accion, fecha) VALUES (:accion, NOW())"), {'accion': 'importación'})
```

### 5. Cerrar conexión correctamente

Con context manager (`with`), la conexión se cierra automáticamente. Punto. No necesitás `conn.close()` manual.

```python
# ✅ Bien: context manager — se cierra solo
with engine.connect() as conn:
    df = pd.read_sql('SELECT * FROM tabla', conn)

# ❌ Mal: conexión manual — si hay excepción, queda abierta
conn = engine.connect()
df = pd.read_sql('SELECT * FROM tabla', conn)
conn.close()  # ¿y si la línea de arriba explota?
```

Cuando usás `pd.read_sql()` directo con un engine, Pandas abre y cierra la conexión internamente. Es seguro. Pero si pasás una conexión explícita como segundo argumento, la responsabilidad de cerrarla es tuya.

**Cerrar el engine entero** al terminar el script:

```python
engine.dispose()  # cierra todas las conexiones del pool
```

### 6. Manejar errores de conexión

Siempre con try/except, mensajes claros, y sin trazas crípticas para el usuario final:

```python
from sqlalchemy.exc import OperationalError, TimeoutError

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except OperationalError as e:
    raise ConnectionError(
        f"No se pudo conectar a la base de datos.\n"
        f"Host: {host}\n"
        f"Error original: {e.orig}"
    ) from e
except TimeoutError:
    raise ConnectionError(
        f"Timeout conectando a {host}:{port}. ¿El servidor está corriendo?"
    )
```

**Errores comunes y qué hacer:**
- `OperationalError: could not connect to server` → Host/puerto incorrecto, servidor caído, firewall.
- `TimeoutError` → Servidor no responde, network lento, pool agotado.
- `ProgrammingError: relation does not exist` → Tabla no existe o schema incorrecto.
- `IntegrityError` → Violación de constraint (FK, unique, not null). Revisar datos.
- `pool_pre_ping` detecta conexiones zombie → Se reconecta automáticamente sin que el usuario vea error.

## Herramientas específicas

| Paso | Herramienta |
|------|-------------|
| Explorar schema MySQL | `mysql_get_database_summary`, `mysql_list_tables`, `mysql_read_table_schema` |
| Explorar schema SQLite | `sqlite_list_tables`, `sqlite_get_table_schema` |
| Probar conectividad | `engine.connect()` + `SELECT 1` |
| Leer con Pandas | `pd.read_sql(query, engine, params={...})` |
| Escribir con Pandas | `df.to_sql(name, engine, if_exists='replace', index=False)` |
| Guardar credenciales | Archivo `.env` + `python-dotenv`, nunca en el código |
