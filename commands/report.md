---
description: Generación de reporte automático — HTML, Markdown o Excel con resultados del análisis
agent: data-analyst
subtask: true
---

Generá un reporte automatizado con los resultados del análisis.

FLUJO:
1. Tomá el dataset y los resultados del análisis actual
2. Generá reporte en el formato que el usuario elija:
   - **markdown**: resumen ejecutivo + tablas
   - **excel**: múltiples hojas (datos, resumen, stats)
   - **html**: reporte completo con estilo
3. Incluí siempre:
   - Resumen ejecutivo en español
   - Tabla de métricas principales
   - Alertas de calidad si las hay
   - Recomendaciones

SKILLS A CARGAR:
- reporting
- cognitive-doc-design

REGLAS:
- El formato default es markdown (más liviano)
- Preguntá antes de generar Excel o HTML
- Los archivos guardalos en el dir que te indique el usuario
