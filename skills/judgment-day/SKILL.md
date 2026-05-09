---
name: judgment-day
description: >
  Protocolo de revisión adversarial: dos sub-agentes jueces ciegos revisan el
  mismo target, sintetiza hallazgos, aplica fixes, y re-evalúa hasta que ambos
  aprueban. Trigger: "judgment day", "doble review", "juzgar", "que lo juzguen".
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.5"
  model_tier: T4-reasoning
---

# Skill: judgment-day

Dos jueces ciegos revisan tu código. Si ambos aprueban, mergeás tranquilo.

## Trigger

- El usuario dice "judgment day", "que lo juzguen", "doble review".
- Implementaste algo crítico (auth, pagos, data-sensitive).
- Necesitás coverage de edge cases que un solo reviewer podría pasar por alto.
- El costo de un bug en prod es mayor que el costo de dos rondas de review.

## Por qué existe

Un solo revisor tiene puntos ciegos. Dos revisores independientes que no se
hablan entre sí encuentran el doble de bugs. Pero hacerlo manual es caro.
Este protocolo automatiza el proceso: lanza dos jueces en paralelo, cruza
resultados, aplica fixes, y re-evalúa hasta que ambos dan el OK.

## Workflow

```
1. Resolvé skills relevantes (buscá skill-registry, inyectá compact rules)
2. Lanzá Juez A y Juez B en paralelo (delegate, async) — mismo target
3. Síntesis: cruzás hallazgos de ambos
   ┌─ Coinciden ambos → CONFIRMADO, fix inmediato
   ├─ Solo Juez A     → SOSPECHOSO (triage)
   ├─ Solo Juez B     → SOSPECHOSO (triage)
   └─ Se contradicen  → bandera roja, decisión manual
4. Si hay CRITICALs o WARNINGs reales confirmados → mostrá tabla al usuario
5. Preguntale: "¿Arreglo los issues confirmados?"
6. Si dice sí → Fix Agent (delegate separado, no uses un juez como fixer)
7. Re-lanzá ambos jueces (Round 2)
8. Si siguen habiendo issues → repetí fix + re-judge (máx 2 iteraciones)
9. Después de 2 iteraciones preguntá: "¿Seguimos o escalamos?"
10. JUDGMENT: APPROVED ✅ o ESCALATED ⚠️
```

## Reglas de severidad

Los jueces clasifican cada hallazgo:

| Severidad | Qué significa | Qué hacer |
|-----------|---------------|-----------|
| CRITICAL | Bug, data loss, security hole | Fix obligatorio, re-judge |
| WARNING (real) | Falla en uso normal del tool | Fix obligatorio |
| WARNING (theoretical) | Requiere input corrupto o edge case rebuscado | Reportar como INFO, NO fixear |
| SUGGESTION | Estilo, naming, preferencia | Fix inline si es trivial, NO re-judge |

**Para clasificar**: preguntate "¿Un usuario normal, usando el tool como
corresponde, puede triggerear esto?" Si sí → real. Si requiere un manifest
malicioso o un race condition de 1ms → theoretical.

## Convergence threshold

- **Round 1**: presentá la tabla al usuario. Preguntá si fixea. Fixeá solo
  después de la confirmación. Re-juzgá completo.
- **Round 2+**: re-juzgá solo si hay CRITICALs confirmados. WARNINGs reales
  se fixean inline sin re-judge. Theoreticals se reportan sin fix.
- **Aprobado**: 0 CRITICALs + 0 WARNINGs reales. Theoreticals y suggestions
  no bloquean.

## Output format

```markdown
## Judgment Day — {target}

| Finding | Juez A | Juez B | Severidad | Estado |
|---------|--------|--------|-----------|--------|
| Missing null check | ✅ | ✅ | CRITICAL | Confirmado |
| Race condition | ✅ | ❌ | WARNING (real) | Sospechoso A |
| Windows edge case | ❌ | ✅ | WARNING (theoretical) | INFO |
```

## Patrones

- **Nunca revises código vos**: orquestás nomás. Los jueces son los que revisan.
- **Jueces en paralelo siempre**: `delegate` async, nunca secuencial.
- **Fix Agent es separado**: nunca uses un juez como fixer. El fixer solo
  aplica los cambios confirmados, sin refactor extra.
- **Misma info a ambos jueces**: incluye compact rules del skill-registry y
  cualquier criterio custom que haya dado el usuario.
- **Self-check**: antes de declarar APPROVED, verificá que cada JD esté en
  estado terminal. Si hubo fixes, que haya pasado por re-judge.

## Anti-patrones

- Declarar APPROVED sin que ambos jueces hayan pasado → no existe aprobación parcial.
- Hacer git push/commit entre fix y re-judge → el re-judge evalúa antes de mergear.
- Un juez sabe del otro → cross-contamination de criterios.
- Ignorar el campo `Skill Resolution` en las respuestas → si el juez reportó
  `fallback-registry`, la cache de skills se perdió; releela.
- Escalar sin preguntarle al usuario → la decisión final es del usuario, no del protocolo.
