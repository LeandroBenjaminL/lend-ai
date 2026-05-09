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
