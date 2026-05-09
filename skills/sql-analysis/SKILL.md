---
name: sql-analysis
description: >
  Consultas SQL para análisis de datos con joins, window functions y agregaciones.
  Trigger: Cuando necesitás consultar bases de datos, hacer análisis en SQL, joins, subqueries, o window functions.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.1"
  model_tier: T3-balanced
---

# Skill: sql-analysis

Consultas SQL para análisis de datos. Mover el cómputo a la base de datos ahorra transferencia de datos y memoria local.

## Trigger

Cargá esta skill cuando:
- Tenés datos en una base SQL y necesitás extraerlos para análisis
- Hacés agregaciones complejas (GROUP BY, HAVING, ventanas)
- Combinás múltiples tablas con JOINs
- Querés preparar datos directamente desde la DB en lugar de pandas

## Por qué SQL en vez de pandas

Si los datos están en la base, SQL suele ser más eficiente: la base puede filtrar, agregar y JOINear antes de mandarte los datos. Con pandas tendrías que traer todo a memoria y hacer el mismo trabajo localmente. Para datasets > 1M filas, la diferencia es abismal.

## 1. Exploración rápida

```sql
-- Schema y tablas disponibles
SELECT table_name, table_type FROM information_schema.tables
WHERE table_schema = 'public';

-- Primeros registros — siempre limitá
SELECT * FROM tabla LIMIT 100;

-- Conteos y nulos
SELECT
  COUNT(*) as total,
  COUNT(columna) as no_nulos,
  COUNT(DISTINCT columna) as unicos
FROM tabla;
```

**Por qué siempre LIMIT**: traerte 10M filas por accidente congela tu cliente y la base. Hacé siempre SELECT con LIMIT hasta que estés seguro de la query.

## 2. Joins analíticos

```sql
SELECT
    a.categoria,
    COUNT(DISTINCT a.usuario_id) as usuarios,
    ROUND(AVG(b.monto), 2) as ticket_promedio,
    SUM(b.monto) as ingresos_totales
FROM usuarios a
INNER JOIN transacciones b ON a.usuario_id = b.usuario_id
WHERE b.fecha >= '2024-01-01'
GROUP BY a.categoria
HAVING COUNT(DISTINCT a.usuario_id) > 10
ORDER BY ingresos_totales DESC;
```

**Tip**: después de cualquier JOIN, verificá cardinalidad. Un JOIN 1:N cuando esperabas 1:1 te duplica filas sin aviso. Hacé `SELECT COUNT(*), COUNT(DISTINCT pk)` antes y después.

## 3. Window Functions

```sql
SELECT
    fecha,
    producto,
    ventas,
    SUM(ventas) OVER (PARTITION BY producto ORDER BY fecha) as acumulado,
    LAG(ventas) OVER (PARTITION BY producto ORDER BY fecha) as venta_anterior,
    ROUND(
        (ventas - LAG(ventas) OVER (PARTITION BY producto ORDER BY fecha))
        / NULLIF(LAG(ventas) OVER (PARTITION BY producto ORDER BY fecha), 0) * 100,
        2
    ) as crecimiento_pct
FROM ventas_diarias;
```

**Por qué window functions**: permiten calcular acumulados, diferencias y rankings sin agrupar las filas. Cada fila conserva su identidad mientras ves el contexto del grupo.

## Ejemplo desde Python

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost:5432/mydb')

df = pd.read_sql("""
    SELECT categoria, EXTRACT(MONTH FROM fecha) as mes,
           COUNT(*) as transacciones,
           SUM(monto) as ingresos
    FROM transacciones
    GROUP BY categoria, EXTRACT(MONTH FROM fecha)
    ORDER BY categoria, mes
""", engine)
```

## Anti-patrones

- ❌ **SELECT *** en producción**: trae columnas que no necesitás, gasta memoria y ancho de banda. Siempre especificá columnas.
- ❌ **JOIN sin índices**: si las columnas del JOIN no están indexadas, la base hace full table scan y se cuelga.
- ❌ **No filtrar antes de JOIN**: `WHERE` después del JOIN filtra después de combinar. Si podés filtrar antes, usá subqueries o CTEs.
- ❌ **Hacer JOINs en Python**: si los datos están en la misma DB, hace el JOIN en SQL. Es más rápido y transferís menos datos.
- ❌ **Olvidar NULLIF en divisiones**: dividir por cero mata la query. Usá `NULLIF(denominador, 0)`.

## Alternativas

- **DuckDB**: SQL engine embebido que corre directo sobre CSV/Parquet sin servidor. Ideal para análisis ad-hoc.
- **SQLite**: para datasets chicos (< 1GB), embebido, cero configuración.
- **Polars**: API de DataFrame con lazy evaluation, más rápido que pandas con sintaxis similar a SQL.

## Tools relevantes

- `sqlalchemy` — conexión a DBs desde Python
- `duckdb` — SQL embebido sobre archivos
- `psycopg2` / `mysql-connector` — drivers específicos
- `sqlite3` — base embebida sin setup
- `polars` — alternativa a pandas con sintaxis SQL-like
