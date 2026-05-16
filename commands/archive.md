---
description: Documentar, versionar y cerrar un proyecto de análisis completo
agent: data-analyst
subtask: true
---

Cerremos el proyecto como se debe.

FLUJO:
1. Resumí: pregunta, datos, enfoque, resultado, limitaciones
2. Verificá que esté todo commiteado
3. Documentá hallazgos y aprendizajes
4. Guardá resumen en Engram
5. Devolvé certificado de cierre

SKILLS A CARGAR: data-archive, git-data

## Uso

`@data-analyst /archive lending-model`

`@data-analyst /archive customer-churn-analysis`

## Ejemplo

Input: `@data-analyst /archive churn-analysis-2024`

Output:
```
📦 Certificado de Cierre — churn-analysis-2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Datos commiteados (3 commits)
✅ Resumen guardado en Engram
✅ Notebooks finalizados
✅ Reporte generado: reports/churn-report.md

Resumen: Se analizaron 50K clientes. El churn se explica
principalmente por baja frecuencia de uso y tickets de soporte
no resueltos. Recomendación: implementar programa de retención.
```
