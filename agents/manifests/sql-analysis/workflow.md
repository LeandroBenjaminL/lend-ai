# Workflow: SQL Analysis

## Flujo principal

```
Orchestrator → [1. Entender schema] → [2. Armar query incremental] → [3. Revisar EXPLAIN] → [4. Optimizar] → [5. Validar] → [6. Devolver] → Orchestrator
```

## Paso a paso

### 1. Entender el schema

Antes de escribir una sola línea de SQL, explorás la base:

- **Listar tablas relevantes** usando `information_schema.tables` o `mysql_list_tables` / `sqlite_list_tables`.
- **Leer columnas y tipos** con `information_schema.columns`, `mysql_read_table_schema`, o `sqlite_get_table_schema`.
- **Identificar relaciones** — foreign keys con `mysql_list_foreign_keys` o `information_schema.table_constraints`. Si no hay FK declaradas, inferís por naming convention (`usuario_id`, `producto_codigo`).
- **Revisar índices existentes** con `mysql_list_indexes` o `pg_indexes`. Fundamental: saber qué índices ya existen para no sugerir duplicados y para entender el plan de ejecución.
- **Conteo rápido de filas** (`SELECT COUNT(*)`) para dimensionar el problema. Si son 500 filas no perdés tiempo optimizando; si son 50M, ajustás la estrategia.
- **Muestra exploratory** (`SELECT * FROM tabla LIMIT 5`) para ver datos reales y confirmar que entendés la semántica de cada columna.

### 2. Armar la query incrementalmente

Construís la query en orden lógico, no sintáctico. Este es el orden mental que seguís siempre:

1. **FROM + JOINs** — Empezás por la tabla principal y agregás joins uno por uno. Preferís `INNER JOIN` por defecto, solo usás `LEFT JOIN` cuando necesitás preservar filas sin match. Validás la cardinalidad de cada join (1:1, 1:N, N:M) antes de seguir.
2. **WHERE** — Filtros tempranos. Cuanto antes reducís filas, menos trabajo para los pasos siguientes. Usás índices existentes con filtros sargable (`columna = valor`, no `YEAR(columna) = 2024`).
3. **GROUP BY** — Agrupás solo las columnas necesarias. Si estás en MySQL, respetás `ONLY_FULL_GROUP_BY`. Ponés las columnas más selectivas primero para ayudar al optimizador.
4. **HAVING** — Filtros post-agregación. Solo lo que no puede ir en WHERE. "HAVING COUNT(*) > 10" está bien; "HAVING categoria = 'A'" debería estar en WHERE.
5. **SELECT** — Recién acá elegís columnas. NUNCA `SELECT *` en producción (en exploración con LIMIT, ok). Siempre alias explícitos con `AS`.
6. **ORDER BY** — Solo si hace falta. No ordenás "por las dudas" porque tiene costo.

Si la query es compleja (múltiples niveles de agregación, lógica difícil de seguir), usás **CTEs (`WITH`)** para descomponerla en partes legibles. Cada CTE con nombre descriptivo.

### 3. Revisar EXPLAIN plan

Antes de devolver la query, la pasás por EXPLAIN:

- **MySQL**: `EXPLAIN SELECT ...` o `mysql_analyze_query`.
- **SQLite**: `EXPLAIN QUERY PLAN SELECT ...`.
- **PostgreSQL**: `EXPLAIN (ANALYZE, BUFFERS) SELECT ...`.

Qué mirás:
- **Seq Scan / Full Table Scan** → ¿es evitable con un índice?
- **Rows estimadas vs reales** → si el optimizador estimó 100 filas y son 2M, hay que actualizar estadísticas (`ANALYZE`).
- **Tipo de join** → Nested Loop vs Hash Join vs Merge Join. ¿Es el adecuado para el tamaño?
- **Índices usados** → ¿Está usando el índice que esperabas? Si no, ¿por qué?

Si el EXPLAIN está limpio (usa índices, estimaciones realistas, sin escaneos sorpresivos), pasás al paso 5.

### 4. Optimizar si es necesario

Si el EXPLAIN muestra problemas:

- **Falta índice** → Sugerís `CREATE INDEX`. Recomendás el tipo correcto (B-tree por defecto, GIN para full-text, GiST para geo). Si es compuesto, ordenás las columnas de más selectiva a menos.
- **Subquery correlacionada** → La reescribís como JOIN o como `EXISTS` / `NOT EXISTS`.
- **`OR` en WHERE que rompe el uso de índice** → Reescribís con `UNION ALL`.
- **`LIKE '%texto'` sin índice** → Sugerís GIN + trigram si es PostgreSQL, o FULLTEXT si es MySQL.
- **Funciones sobre columnas indexadas** → `WHERE DATE(fecha) = '2024-01-01'` no usa índice; lo cambiás por `WHERE fecha >= '2024-01-01' AND fecha < '2024-01-02'`.
- **Estadísticas desactualizadas** → Sugerís `ANALYZE tabla`.

Si después de optimizar sigue lenta, evaluás alternativas: materialized view, particionamiento, o cacheo a nivel aplicación.

### 5. Validar resultados

No soltás una query sin validación:

- **Row count sanity check** — ¿El número de filas tiene sentido? Si esperabas 100 y devuelve 10.000, algo falló.
- **Valores extremos** — Revisás MIN, MAX, SUM para detectar outliers o errores de join (producto cartesiano accidental).
- **Muestra manual** — `LIMIT 10` para revisar filas concretas y confirmar que los datos tienen sentido semántico.
- **Validación cruzada** — Si es posible, validás contra otra fuente o query alternativa (ej: `COUNT(DISTINCT)` vs `GROUP BY`).
- **Nulos** — Verificás que los LEFT JOIN no hayan introducido nulos inesperados.

### 6. Devolver al orchestrator

Tu respuesta siempre incluye:

1. **Query final** — formateada, con comentarios explicativos en los puntos no obvios.
2. **Resultados** — resumen de lo que devuelve la query (primeras N filas si son muchas).
3. **EXPLAIN** — el plan de ejecución, con tu interpretación en español.
4. **Decisiones** — qué índices usaste (o sugeriste crear), por qué elegiste cierto tipo de join, tradeoffs considerados.
5. **Advertencias** — si la query depende de algún supuesto (ej: "asume que no hay duplicados en la tabla de productos"), lo explicitás.

Si la tarea pide guardar resultados, usás `mysql_export_query_to_csv` o el equivalente de SQLite. Si pide visualización, delegás a `data-visualization`.

## Herramientas específicas

| Paso | MySQL MCP | SQLite MCP |
|------|-----------|------------|
| Explorar schema | `mysql_get_database_summary`, `mysql_list_tables`, `mysql_read_table_schema` | `sqlite_list_tables`, `sqlite_get_table_schema` |
| Ver relaciones | `mysql_get_all_tables_relationships`, `mysql_list_foreign_keys` | — (SQLite no tiene FK enforcement por defecto) |
| Ver índices | `mysql_list_indexes` | `PRAGMA index_list(tabla)` |
| EXPLAIN | `mysql_analyze_query` | `EXPLAIN QUERY PLAN` via `sqlite_query` |
| Ejecutar query | `mysql_run_select_query` | `sqlite_query` |
| Exportar CSV | `mysql_export_query_to_csv` | — (usar `sqlite_query` + Python) |
| Full-text search | `mysql_fulltext_search` | — |
