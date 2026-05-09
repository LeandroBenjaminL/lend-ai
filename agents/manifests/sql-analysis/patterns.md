# Patterns: SQL Cheat Sheet

## JOINs

| Tipo | Sintaxis | Cuándo usarlo |
|------|----------|---------------|
| INNER JOIN | `FROM a INNER JOIN b ON a.id = b.a_id` | Solo filas con match en ambas tablas. Es tu default. |
| LEFT JOIN | `FROM a LEFT JOIN b ON a.id = b.a_id` | Todas las filas de `a`, nulos donde `b` no tiene match. |
| RIGHT JOIN | `FROM a RIGHT JOIN b ON a.id = b.a_id` | Lo mismo pero al revés. Mejor reescribir como LEFT JOIN para claridad. |
| FULL OUTER JOIN | `FROM a FULL JOIN b ON a.id = b.a_id` | Todas las filas de ambas, con nulos donde no hay match. Para reconciliación. |
| CROSS JOIN | `FROM a CROSS JOIN b` | Producto cartesiano. Solo con tablas chicas y a propósito. |
| SELF JOIN | `FROM empleados e INNER JOIN empleados m ON e.manager_id = m.id` | Una tabla que se referencia a sí misma (jerarquías). |
| LATERAL JOIN | `FROM a LEFT JOIN LATERAL (SELECT ... LIMIT 1) b ON true` | Subquery que puede referenciar columnas de `a`. PostgreSQL. |

### Anti-patrones de JOIN

```sql
-- ❌ Mal: subquery correlacionada como JOIN
SELECT * FROM a WHERE a.id IN (SELECT a_id FROM b WHERE status = 'activo')

-- ✅ Bien: INNER JOIN
SELECT a.* FROM a INNER JOIN b ON a.id = b.a_id WHERE b.status = 'activo'

-- ❌ Mal: JOIN con OR (rompe índices, genera nested loops)
SELECT * FROM a JOIN b ON a.id = b.a_id OR a.codigo = b.codigo

-- ✅ Bien: UNION de JOINs individuales
SELECT * FROM a JOIN b ON a.id = b.a_id
UNION
SELECT * FROM a JOIN b ON a.codigo = b.codigo
```

---

## Window Functions

| Función | Sintaxis | Qué hace |
|---------|----------|----------|
| ROW_NUMBER | `ROW_NUMBER() OVER (PARTITION BY depto ORDER BY salario DESC)` | Numera filas 1, 2, 3... sin gaps. |
| RANK | `RANK() OVER (PARTITION BY depto ORDER BY salario DESC)` | Ranking con gaps (1, 1, 3 si hay empate). |
| DENSE_RANK | `DENSE_RANK() OVER (...)` | Ranking sin gaps (1, 1, 2 si hay empate). |
| LAG | `LAG(ventas, 1, 0) OVER (ORDER BY fecha)` | Valor de la fila anterior. Útil para delta y crecimiento. |
| LEAD | `LEAD(ventas, 1) OVER (ORDER BY fecha)` | Valor de la fila siguiente. Para forecasting. |
| SUM OVER | `SUM(monto) OVER (PARTITION BY cliente ORDER BY fecha)` | Running total (acumulado). |
| AVG OVER | `AVG(ventas) OVER (PARTITION BY producto ORDER BY fecha ROWS 6 PRECEDING)` | Media móvil de 7 días. |
| FIRST_VALUE | `FIRST_VALUE(precio) OVER (PARTITION BY producto ORDER BY fecha)` | Primer valor de la partición. |
| NTILE | `NTILE(4) OVER (ORDER BY salario)` | Divide en N buckets (cuartiles, deciles, etc.). |

### Window Frame

```sql
-- Los defaults implícitos (sin ROWS/RANGE):
-- RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- Media móvil de 3 filas (la actual + 2 anteriores):
AVG(valor) OVER (ORDER BY fecha ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- Todas las filas de la partición (para % del total):
SUM(valor) OVER (PARTITION BY categoria)  -- sin ORDER BY → toda la partición
```

---

## CTEs (Common Table Expressions)

```sql
-- CTE simple: legibilidad
WITH ventas_mes AS (
    SELECT producto_id, SUM(monto) as total
    FROM ventas WHERE fecha >= '2024-01-01'
    GROUP BY producto_id
)
SELECT p.nombre, vm.total
FROM productos p
JOIN ventas_mes vm ON p.id = vm.producto_id
WHERE vm.total > 10000;

-- CTE recursiva: jerarquías
WITH RECURSIVE jerarquia AS (
    SELECT id, nombre, manager_id, 1 as nivel
    FROM empleados WHERE manager_id IS NULL  -- raíz
    UNION ALL
    SELECT e.id, e.nombre, e.manager_id, j.nivel + 1
    FROM empleados e
    JOIN jerarquia j ON e.manager_id = j.id
)
SELECT * FROM jerarquia ORDER BY nivel, nombre;
```

---

## Subqueries

| Tipo | Sintaxis | Performance |
|------|----------|-------------|
| Escalar | `SELECT (SELECT MAX(fecha) FROM ventas)` | Bien si devuelve 1 fila. |
| IN | `WHERE id IN (SELECT id FROM tabla WHERE ...)` | Mejor reescribir como JOIN o EXISTS. |
| EXISTS | `WHERE EXISTS (SELECT 1 FROM b WHERE b.a_id = a.id)` | Excelente para correlacionadas. Mejor que IN. |
| NOT EXISTS | `WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.a_id = a.id)` | Para anti-join. Índice en la FK es clave. |
| Correlacionada en SELECT | `SELECT a.*, (SELECT COUNT(*) FROM b WHERE b.a_id = a.id)` | Costosa si hay muchas filas. Mejor LEFT JOIN + GROUP BY. |

---

## GROUP BY + HAVING

```sql
SELECT
    categoria,
    EXTRACT(YEAR FROM fecha) as anio,     -- PostgreSQL
    -- YEAR(fecha) as anio,               -- MySQL
    COUNT(*) as transacciones,
    SUM(monto) as ingresos,
    ROUND(AVG(monto), 2) as ticket_promedio
FROM ventas
WHERE fecha >= '2024-01-01'              -- filtro pre-agregación
GROUP BY categoria, EXTRACT(YEAR FROM fecha)
HAVING COUNT(*) > 50                      -- filtro post-agregación
   AND SUM(monto) > 100000
ORDER BY ingresos DESC;
```

---

## CASE WHEN

```sql
SELECT
    nombre,
    salario,
    CASE
        WHEN salario < 50000 THEN 'bajo'
        WHEN salario < 100000 THEN 'medio'
        WHEN salario < 200000 THEN 'alto'
        ELSE 'ejecutivo'
    END as categoria_salarial,
    -- CASE en agregación
    COUNT(CASE WHEN status = 'activo' THEN 1 END) as activos,
    COUNT(CASE WHEN status = 'inactivo' THEN 1 END) as inactivos
FROM empleados
GROUP BY nombre, salario;  -- o mejor GROUP BY categoria_salarial sin nombre
```

---

## COALESCE y CAST

```sql
-- COALESCE: primer valor no nulo
SELECT COALESCE(telefono, email, 'sin contacto') as contacto FROM usuarios;

-- CAST: convertir tipos
SELECT CAST(fecha_str AS DATE) FROM staging;
SELECT fecha_str::DATE FROM staging;  -- PostgreSQL shorthand
SELECT CAST(precio AS DECIMAL(10,2)) FROM productos;
```

---

## Funciones de Fecha

| Operación | PostgreSQL | MySQL | SQLite |
|-----------|-----------|-------|--------|
| Año actual | `EXTRACT(YEAR FROM fecha)` | `YEAR(fecha)` | `strftime('%Y', fecha)` |
| Mes | `EXTRACT(MONTH FROM fecha)` | `MONTH(fecha)` | `strftime('%m', fecha)` |
| Diferencia en días | `fecha2 - fecha1` | `DATEDIFF(fecha2, fecha1)` | `julianday(fecha2) - julianday(fecha1)` |
| Sumar días | `fecha + INTERVAL '7 days'` | `DATE_ADD(fecha, INTERVAL 7 DAY)` | `date(fecha, '+7 days')` |
| Truncar a mes | `DATE_TRUNC('month', fecha)` | `DATE_FORMAT(fecha, '%Y-%m-01')` | `strftime('%Y-%m-01', fecha)` |
| Último día del mes | `fecha + INTERVAL '1 month' - INTERVAL '1 day'` | `LAST_DAY(fecha)` | — |
| Ahora | `NOW()` | `NOW()` | `datetime('now')` |

---

## Índices

```sql
-- B-tree (default): búsquedas por igualdad y rango
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_ventas_cliente_fecha ON ventas(cliente_id, fecha);  -- compuesto

-- Único: integridad + búsqueda
CREATE UNIQUE INDEX idx_usuarios_email ON usuarios(email);

-- Parcial: solo las filas activas (PostgreSQL)
CREATE INDEX idx_ventas_activas ON ventas(fecha) WHERE status = 'activo';

-- Full-text (PostgreSQL)
CREATE INDEX idx_documentos_fts ON documentos USING GIN(to_tsvector('spanish', contenido));

-- Full-text (MySQL)
CREATE FULLTEXT INDEX idx_articulos_fts ON articulos(titulo, cuerpo);

-- Trigram para LIKE '%texto%' (PostgreSQL)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_productos_nombre_trgm ON productos USING GIN(nombre gin_trgm_ops);
```

### Reglas de índices compuestos
1. Columna más selectiva primero en WHERE con `=`, después los rangos.
2. `WHERE a = 1 AND b > 10 ORDER BY c` → índice en `(a, b, c)`.
3. Si el WHERE solo tiene `b > 10`, no sirve un índice que empiece con `a`.

---

## EXPLAIN

```sql
-- MySQL
EXPLAIN SELECT ...;
EXPLAIN FORMAT=JSON SELECT ...;  -- más detalle

-- PostgreSQL
EXPLAIN SELECT ...;                    -- plan estimado
EXPLAIN ANALYZE SELECT ...;            -- plan + tiempos reales
EXPLAIN (ANALYZE, BUFFERS) SELECT ...; -- con I/O

-- SQLite
EXPLAIN QUERY PLAN SELECT ...;
```

**Lo que mirás en el EXPLAIN:**
- `type` (MySQL): `ALL` = full table scan (mal), `index` = index scan, `ref`/`eq_ref` = index lookup (bien).
- `rows`: estimación del optimizador. Si difiere mucho de la realidad, `ANALYZE tabla`.
- `Extra: Using filesort` → estás ordenando sin índice. Agregá índice que cubra el ORDER BY.
- `Extra: Using temporary` → estás creando tabla temporal. Revisá GROUP BY / DISTINCT.
- `Seq Scan` (PostgreSQL) en tabla grande sin WHERE → ok si realmente necesitás todas las filas.

---

## Performance Rules (las 10 leyes)

1. **Filtrá temprano.** WHERE antes de JOINs cuando se pueda empujar el filtro.
2. **Índices compuestos bien ordenados.** Columna de `=` primero, luego rangos, luego ORDER BY.
3. **`EXISTS` > `IN`** para subqueries correlacionadas.
4. **CTEs no materializadas (PostgreSQL < 12)** pueden ser performance traps. En versiones viejas, preferí subqueries inline.
5. **`UNION` saca duplicados, `UNION ALL` no.** Usá `UNION ALL` salvo que necesites dedup.
6. **`LIMIT` sin `ORDER BY` es no determinístico.** Siempre ordená si usás LIMIT para paginación.
7. **Funciones sobre columnas en WHERE rompen índices.** `WHERE DATE(fecha) = '2024-01-01'` → `WHERE fecha >= '2024-01-01' AND fecha < '2024-01-02'`.
8. **`SELECT *` solo en exploración.** En producción, siempre columnas explícitas.
9. **`OFFSET` grande es lento.** Para paginación profunda, usá keyset pagination (`WHERE id > ultimo_id ORDER BY id LIMIT N`).
10. **Medí, no adivines.** EXPLAIN antes de crear índices. `EXPLAIN ANALYZE` para ver tiempos reales.
