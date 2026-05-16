---
description: Ejecutar una revisión adversarial rápida del análisis actual
agent: data-analyst
subtask: true
---

Ejecutá una mini Judgment Day sobre el análisis en curso.

FLUJO:
1. Tomá el contexto actual (código, resultados, conclusiones)
2. Revisá adversarialmente: errores, sesgos, suposiciones, edge cases
3. Clasificá hallazgos: CRITICAL / WARNING real / WARNING teórico / SUGGESTION
4. Devolvé tabla de hallazgos
5. Preguntá si querés corregir los confirmados

SKILLS A CARGAR: data-verify, cognitive-doc-design

## Uso

`@judgment-day review PR #42`

`@judgment-day review --scope analysis`

## Ejemplo

Input: `@judgment-day review --scope analysis`

Output:
```
🔍 Judgment Day — Revisión Adversarial
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID  | Severidad    | Hallazgo
────┼──────────────┼─────────────────────────────────────────
#1  | 🔴 CRITICAL  | Variable 'ingresos' no está normalizada
     |              | → afecta coeficientes del modelo
#2  | 🟡 WARNING   | Train/test split no es temporal
     |              | → fuga de datos futura
#3  | 💡 SUGGESTION | Agregar validación cruzada

¿Querés corregir los hallazgos críticos? (s/n)
```
