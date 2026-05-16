---
description: Pipeline de limpieza de datos — nulos, duplicados, outliers, tipos, normalización
agent: data-analyst
subtask: true
---

Ejecutá un pipeline completo de limpieza sobre el dataset.

FLUJO:
1. Cargá el dataset
2. Mostrá un plan de limpieza antes de ejecutar
3. Ejecutá paso a paso:
   - Corrección de tipos (fechas, numéricos, categorías)
   - Manejo de nulos (mediana para numéricos, moda para categóricos)
   - Eliminación de duplicados
   - Detección y tratamiento de outliers (clip por percentiles)
   - Normalización de strings (minúsculas, sin espacios extras)
4. Mostrá antes/después de cada paso
5. Devolvé el dataset limpio como CSV o parquet
   Nota: si delegás a data-cleaning, él devuelve resultados inline
   y el agente principal escribe el archivo final.

SKILLS A CARGAR:
- data-cleaning
- regex-data
- data-validation

REGLAS:
- Preguntá antes de eliminar datos (confirmar con el usuario)
- Reportá cuánto se perdió en cada paso
- No sobrescribas archivos originales

## Uso

`@data-analyst /clean dataset.csv --drop-nulls --fill-missing mean`

`@data-analyst /clean clientes.csv --strip-spaces --fix-types --outlier-method clip`

## Ejemplo

Input: `@data-analyst /clean ventas.csv --fill-missing median --drop-duplicates`

Output:
```
📋 Plan de limpieza:
   • 3 columnas numéricas con nulos → mediana
   • 1 columna categórica con nulos → moda
   • Fechas en string → datetime
   • Duplicados → drop

📊 Antes: 1,000 filas | Después: 985 filas
   - Nulos corregidos: 23 valores
   - Duplicados eliminados: 12 filas
   - Outliers tratados (clip p1-p99): 8 valores
   - Tipos corregidos: fecha_venta → datetime,
     precio → float, activo → bool
```
