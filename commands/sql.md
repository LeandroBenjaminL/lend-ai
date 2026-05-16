---
description: Ejecutar consultas SQL directo desde el chat — SELECT, JOINs, window functions
agent: data-analyst
subtask: true
---

Ejecutá una consulta SQL sobre el dataset o base de datos indicada.

FLUJO:
1. Identificá la base de datos o archivo (SQLite, CSV, PostgreSQL)
2. Si es archivo, cargalo en SQLite con pandas
3. Ejecutá la consulta
4. Mostrá resultados en tabla
5. Explicá la query paso a paso (enseñanza)

SKILLS A CARGAR: sql-analysis, database-connections

REGLAS:
- Si el usuario no da DB, preguntale primero
- Mostrá el plan de la query antes de ejecutar
- Explicá cada cláusula (SELECT, WHERE, JOIN, etc.)

## Uso

`@data-analyst /sql "SELECT * FROM users WHERE signup > 2024"`

`@data-analyst /sql "SELECT category, AVG(price) FROM products GROUP BY category HAVING AVG(price) > 100"`

## Ejemplo

Input: `@data-analyst /sql "SELECT cliente_id, COUNT(*) as pedidos FROM ventas GROUP BY cliente_id ORDER BY pedidos DESC LIMIT 5"`

Output:
```
🗄️ Query SQL sobre: ventas.csv (cargado en SQLite)

Plan:
  • GROUP BY cliente_id → agrupa por cliente
  • COUNT(*) → cuenta pedidos por cliente
  • ORDER BY pedidos DESC → top compradores
  • LIMIT 5 → solo los primeros 5

Resultados:
  | cliente_id | pedidos |
  |------------|---------|
  | 4521       | 89      |
  | 3308       | 74      |
  | 1123       | 62      |
  | 9982       | 58      |
  | 7654       | 51      |
```
