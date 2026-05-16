---
description: Verificar que todo el ecosistema funcione correctamente
agent: data-analyst
subtask: true
---

Ejecutá un chequeo completo del ecosistema.

FLUJO:
1. Verificá que el JSON de config sea válido
2. Verificá que existan todos los SKILL.md referenciados
3. Verificá que los sub-agentes tengan tools correctas
4. Verificá que los MCPs estén configurados
5. Verificá que `data-validation` esté en la tabla de delegación de `data-analyst`
6. Verificá que los 6 sub-agentes tengan tools consistentes
7. Reportá cualquier problema

SKILLS A CARGAR: data-validation, cognitive-doc-design

REGLAS:
- No modifiques nada — solo reportá
- Mostrá ✅ pasa / ❌ falla / ⚠️ warning
- Si todo está bien, decilo con confianza

## Uso

`/health`

`/health --verbose`

## Ejemplo

Input: `/health`

Output:
```
🏥 Health Check — LEND.AI Ecosystem
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Config JSON válido
✅ Skills cargadas (42/42)
✅ Sub-agentes con tools correctas
✅ MCPs configurados (4/4)
⚠️ data-validation no está en tabla de delegación
✅ 6 sub-agentes con tools consistentes

Estado general: ✅ OK (1 warning)
```
