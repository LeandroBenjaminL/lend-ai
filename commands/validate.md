---
description: Validar calidad y schema de un dataset — tipos, rangos, nulos, reglas
agent: data-analyst
subtask: true
---

Validá un dataset contra reglas de calidad definidas.

FLUJO:
1. Cargá el dataset
2. Mostrá schema actual
3. Preguntá reglas de validación o usá defaults
4. Ejecutá validaciones: tipos, nulos permitidos, rangos, valores únicos
5. Mostrá resultados: ✅ pasó / ❌ falló / ⚠️ warning
6. Explicá qué significa cada validación

SKILLS A CARGAR: data-validation, data-profiling

REGLAS:
- Usá Pandera si está instalado, sino pandas nativo
- No modifiques el dataset — solo validá
- Devolvé un reporte claro de pasa/no pasa

## Uso

`@data-analyst /validate dataset.csv --schema schema.json`

`@data-analyst /validate ventas.csv --no-nulls "precio,email" --range "precio:0-10000"`

## Ejemplo

Input: `@data-analyst /validate clientes.csv --schema schema.json`

Output:
```
✅ Validación — clientes.csv vs schema.json

Regla              │ Estado  │ Detalle
───────────────────┼─────────┼──────────────────────────
Tipos correctos    │ ✅      │ 8/8 columnas ok
Nulos permitidos   │ ❌      │ email tiene 5 nulos (max 0)
Rango precio       │ ✅      │ 0-9,999 (dentro de 0-10,000)
Valores únicos OK  │ ✅      │ cliente_id sin duplicados

Resumen: ❌ 1 fallo — corregí nulos en email
```
