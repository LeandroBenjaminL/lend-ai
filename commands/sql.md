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
