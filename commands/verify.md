---
description: Verificar que los resultados del análisis sean correctos y respondan la pregunta
agent: data-analyst
subtask: true
---

Revisemos los resultados antes de darlos por buenos.

FLUJO:
1. Tomá la pregunta original y los resultados
2. Revisá: ¿responde la pregunta? ¿los datos soportan la conclusión?
3. Verificá supuestos estadísticos
4. Buscá sesgos o errores lógicos
5. Devolvé: ✅ verificado / ⚠️ dudas / ❌ rechazado

SKILLS A CARGAR: data-verify

## Uso

`@data-analyst /verify analysis.ipynb`

`@data-analyst /verify --scope resultados`

## Ejemplo

Input: `@data-analyst /verify churn-analysis.ipynb`

Output:
```
🔎 Verificación — churn-analysis.ipynb

✅ Verificado: los resultados responden la pregunta original
  • ¿Qué impulsa el churn? → Conclusión respaldada por datos

✅ Supuestos estadísticos ok
  • Normalidad de residuos: ✅
  • Homocedasticidad: ✅
  • Multicolinealidad: ✅ (VIF < 5)

⚠️ Dudas:
  • Muestra desbalanceada (85/15) — considerar SMOTE
  • Correlación ≠ causalidad — advertir en conclusiones

Estado final: ✅ Verificado con observaciones
```
