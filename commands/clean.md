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
