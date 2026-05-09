# Patterns: Judgment Day

> _La revisión de código más efectiva no es la que hace la persona más inteligente. Es la que hacen dos personas que no se hablan entre sí._

## Tabla de síntesis de veredicto

| Hallazgo en Juez A | Hallazgo en Juez B | Categoría | Acción |
|--------------------|--------------------|-----------|--------|
| ✅ Encontrado | ✅ Encontrado | **Confirmado** | Fix obligatorio (alta confianza) |
| ✅ Encontrado | ❌ No encontrado | **Sospechoso (A only)** | Triage, no fix automático |
| ❌ No encontrado | ✅ Encontrado | **Sospechoso (B only)** | Triage, no fix automático |
| ✅ Dice X | ✅ Dice !X | **Contradicción** | Flag para decisión humana |
| ❌ No encontrado | ❌ No encontrado | **Clean** | Todo bien |

## Tabla de clasificación de severidad

| Severidad | Definición | Ejemplo | Acción |
|-----------|------------|---------|--------|
| **CRITICAL** | Causa bug, data loss, security hole en producción | Nil pointer dereference, SQL injection, data corruption | Fix inmediato + re-judge |
| **WARNING (real)** | Causa problema en escenario realista | Silent error on disk full, poor error handling, race condition | Fix + re-judge si también hay CRITICALs |
| **WARNING (theoretical)** | Requiere condiciones extremas o input malicioso | Path traversal con manifest malicioso, race en <1ms | Reportar como INFO, NO fix |
| **SUGGESTION** | Mejora opcional | Naming, estilo, optimización menor | Fix inline si trivial, NO re-judge |

## Tabla de determinación "real vs theoretical"

| Pregunta | Real | Theoretical |
|----------|------|-------------|
| ¿Un usuario normal usando la herramienta como fue diseñada puede triggerearlo? | ✅ Sí → **Real** | ❌ No → **Theoretical** |
| ¿Requiere un manifest malicioso o input deliberadamente corrupto? | ❌ No | ✅ Sí → **Theoretical** |
| ¿Requiere condiciones de carrera en <1ms que no ocurren en práctica? | ❌ No | ✅ Sí → **Theoretical** |
| ¿Requiere que el usuario haga click en dos lugares en menos de 100ms? | ❌ No | ✅ Sí → **Theoretical** |
| ¿Requiere un path de archivo con caracteres que el SO no permite? | ❌ No | ✅ Sí → **Theoretical** |
| ¿Ocurre con datos de entrada normales (strings, números, fechas)? | ✅ Sí → **Real** | ❌ No |

## Tabla de convergencia (cuándo aprobar)

| Round | Hallazgos | Acción |
|-------|-----------|--------|
| **Round 1** | 0 issues de ningún tipo | ✅ **APPROVED** (sin fixes) |
| **Round 1** | CRITICALs o WARNINGs (real) confirmados | Presentar al user, preguntar si fixear |
| **Round 1** | Solo SUGGESTIONs o WARNINGs (theoretical) | ✅ **APPROVED** (reportar como INFO) |
| **Round 2** (post-fix) | 0 CRITICALs + 0 confirmed WARNINGs | ✅ **APPROVED** |
| **Round 2** | CRITICALs confirmados | Fix Agent + Round 3 |
| **Round 3** (2 fixes) | CRITICALs confirmados | Preguntar al user si seguir iterando |
| **User dice no** | Issues restantes | ⚠️ **ESCALATED** |

## Tabla de estructura del prompt de Judge

| Sección | Contenido | Requerido |
|---------|-----------|-----------|
| Role | "You are an adversarial code reviewer. Your ONLY job is to find problems." | ✅ Siempre |
| Target | Descripción específica de qué revisar | ✅ Siempre |
| Project Standards | Compact rules del skill registry | ✅ Si existe registry |
| Review Criteria | Correctness, Edge cases, Error handling, Performance, Security, Naming | ✅ Siempre |
| Return Format | Structured findings: Severity, File, Description, Suggested fix | ✅ Siempre |
| WARNING classification rule | "Can a normal user trigger this?" → real vs theoretical | ✅ Siempre |
| Skill Resolution note | `**Skill Resolution**: {injected\|fallback\|none}` | ✅ Siempre |

## Anti-patrones de Judgment Day

| Anti-patrón | Problema | Cómo evitarlo |
|-------------|----------|---------------|
| **Orquestrador revisa código** | Pierde objetividad, se convierte en juez | TU trabajo es coordinar, no juzgar. Delegá a los judges. |
| **Jueces secuenciales** | Judge B puede contaminarse con el resultado de Judge A | Lanzar AMBOS en paralelo con `delegate()`. |
| **Sin skill registry** | Jueces evalúan contra estándares genéricos | Ejecutar `skill-registry` antes de JD, o advertir al user. |
| **Fix sin re-judge** | Se fixea pero no se verifica que el fix no haya introducido bugs | Siempre re-lanzar judges después del fix. |
| **Iteraciones infinitas** | Cada fix introduce artifacts que generan más rounds | Máximo 2 iteraciones, después preguntar al user. |
| **Aprobación con WARNINGs reales** | Issues no críticos pero reales quedan sin fixear | Fixear WARNINGs reales inline, sin re-judge. |
| **No documentar rounds** | No queda registro de qué se encontró y qué se fixeó | Tabla de veredicto + Fixes Applied en cada round. |
| **Partial verdict** | Sintetizar antes de que ambos jueces terminen | Esperar a que AMBOS delegates retornen. |
| **Juez = Fixer** | Usar un juez para fixear lo que el otro juez encontró | Fix Agent es una delegación separada, no un juez. |

## Estructura de veredicto final

**APPROVED:**
```markdown
## Judgment Day — {target}

### Round 2 — Re-judgment
- Judge A: PASS ✅ — No issues found
- Judge B: PASS ✅ — No issues found

### JUDGMENT: APPROVED ✅
Both judges pass clean. Target is cleared for merge.
```

**ESCALATED:**
```markdown
## Judgment Day — {target}

### JUDGMENT: ESCALATED ⚠️
User chose to stop after 2 fix iterations.

### Remaining Issues
| Finding | Both judges | Severity |
|---------|-------------|----------|
| {desc} | ✅ | CRITICAL |

### History
- Round 1: N issues → Fix 1 applied
- Round 2: M issues remain → Fix 2 applied
- Round 3: Remaining → Escalated

### Recommend
Human review of remaining issues before re-running JD.
```

## Checklist pre-lanzamiento

- [ ] **Target específico:** sé qué archivos/feature voy a revisar (no "todo")
- [ ] **Skill registry consultado:** busqué en engram y `.atl/skill-registry.md`
- [ ] **Compact rules inyectadas:** ambos jueces reciben Project Standards
- [ ] **Criterios definidos:** al menos correctness, edge cases, error handling
- [ ] **User consulted on scope:** si el target no está claro, pregunté primero
- [ ] **Custom criteria included:** si el user pidió algo específico, está en el prompt

## Checklist post-lanzamiento (synthesis)

- [ ] **Ambos jueces terminaron:** no sinteticé con un resultado parcial
- [ ] **Tabla de veredicto:** cada hallazgo categorizado (Confirmado/Sospechoso/Contradicción)
- [ ] **Severidad clasificada:** cada hallazgo tiene CRITICAL/WARNING/SUGGESTION
- [ ] **Real vs Theoretical:** los WARNINGs están clasificados correctamente
- [ ] **User consulted:** pregunté antes de fixear (Round 1) y antes de seguir (después de Round 2)

## Principios fundamentales

1. **El orquestrador NUNCA revisa código.** Su trabajo es coordinar, no juzgar.
2. **Dos jueces ciegos > un experto con sesgo.** La independencia es la clave del protocolo.
3. **Aprobado ≠ sin issues.** Aprobado = sin CRITICALs ni WARNINGs reales. Theoretical warnings pueden quedar.
4. **El usuario decide cuándo parar.** Después de 2 iteraciones, preguntá si quiere seguir.
5. **Sin registro de skills, los jueces son menos efectivos.** Corré skill-registry primero.

> _El ego del revisor único es el peor enemigo de la calidad. Dos personas que no se hablan entre sí, con criterios claros, y un coordinador que no toca el código — esa es la fórmula para una revisión que realmente encuentra bugs._
