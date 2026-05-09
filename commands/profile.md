---
description: Reporte de calidad y perfil del dataset — nulos, outliers, cardinalidad, alertas
agent: data-analyst
subtask: true
---

Generá un perfil de calidad completo del dataset.

FLUJO:
1. Cargá el dataset
2. Detectá problemas: nulos >30%, alta cardinalidad, outliers extremos, columnas constantes
3. Generá reporte de calidad con `data-profiling` skill
4. Devolvé tabla de alertas priorizadas (🔴 crítico, 🟡 warning, 🟢 ok)

SKILLS A CARGAR:
- data-profiling
- data-validation

REGLAS:
- No modifiques archivos
- Si ydata-profiling no está instalado, usá pandas nativo
- Priorizá los problemas más graves primero
