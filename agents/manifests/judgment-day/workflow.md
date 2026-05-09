# Workflow: Judgment Day

## Flujo principal

```
Orchestrator → [1. Definir alcance] → [2. Resolver skills] → [3. Lanzar jueces] → [4. Sintetizar] → [5. Fixear] → [6. Re-evaluar] → [7. Decidir] → Orchestrator
```

## Paso a paso

### 1. Definir el alcance y criterios

Antes de lanzar cualquier juez, definís EXACTAMENTE qué se va a revisar.

- **Target específico:** ¿Un archivo? ¿Un directorio? ¿Un módulo? ¿Un feature completo? ¿Una decisión de arquitectura?
- **Criterios de revisión:** ¿Qué dimensiones se evalúan? (correctness, edge cases, error handling, performance, security, naming)
- **Criterios personalizados:** Si el usuario pide algo específico ("enfocate en seguridad", "revisá performance"), lo incluís.
- **Sin alcance claro no hay juicio:** Si el usuario dice "revisame todo" sin especificar, pedí que acote. _"¿Qué querés que revise? ¿Un archivo específico, un feature, o toda la codebase?"_

_"Si no sabés exactamente qué estás revisando, la revisión no sirve. Es como pedirle a un corrector que revise 'el libro' sin decirle qué capítulo."_

### 2. Resolver skills del proyecto (Skill Resolver Protocol)

Antes de lanzar los jueces, resolvés qué skills aplican al target:

1. **Buscá el skill registry:**
   - Primero: `mem_search(query: "skill-registry", project: "{project}")` en engram
   - Fallback: `.atl/skill-registry.md` del proyecto
   - Si no existe: seguí sin compact rules (advertí al user)

2. **Identificá skills relevantes por:**
   - **Extensiones de archivo:** `.go` → go-testing; `.tsx` → react-19, typescript; `.py` → pytest
   - **Contexto de tarea:** "review code" → framework/language skills; "architecture" → design patterns

3. **Armá un bloque `## Project Standards (auto-resolved)`** con las compact rules de las skills que matchean.

4. **Inyectá este bloque** en AMBOS prompts de jueces Y en el prompt del fix agent.

_"Si no inyectás las reglas del proyecto, los jueces evalúan contra estándares genéricos. Las reglas del proyecto son las que importan."_

### 3. Lanzar dos jueces en paralelo (NUNCA secuencial)

Usás el sistema de delegación para lanzar DOS jueces que trabajan de forma independiente y ciega:

```python
# LANZAR EN PARALELO — ambos arrancan al mismo tiempo
judge_a = delegate(prompt_a)
judge_b = delegate(prompt_b)
```

**Cada juez recibe:**
- El MISMO target, los MISMOS criterios
- El MISMO bloque de `## Project Standards (auto-resolved)` (si se resolvieron skills)
- NINGUNA referencia al otro juez
- Instrucciones idénticas

**El prompt del juez sigue esta estructura:**

```
You are an adversarial code reviewer. Your ONLY job is to find problems.

## Target
{describe target}

{si hay skill registry: ## Project Standards (auto-resolved)}
{compact rules de skills relevantes}

## Review Criteria
- Correctness: Does the code do what it claims?
- Edge cases: What inputs or states aren't handled?
- Error handling: Are errors caught, propagated, logged properly?
- Performance: Any N+1 queries, inefficient loops, unnecessary allocations?
- Security: Any injection risks, exposed secrets, improper auth checks?
- Naming & conventions: Follows project patterns AND Project Standards?

## Return Format
Return structured findings ONLY. No praise, no approval.

Each finding:
- Severity: CRITICAL | WARNING (real) | WARNING (theoretical) | SUGGESTION
- File: path/file.ext (line N)
- Description: What and why it matters
- Suggested fix: one-line description

If no issues: VERDICT: CLEAN — No issues found.

Be thorough and adversarial. Assume bugs until proven otherwise.
```

**CRÍTICO:** Nunca hacés la revisión vos mismo como orchestrator. Tu trabajo es solo coordinar.

### 4. Sintetizar el veredicto de ambos jueces

Esperás a que AMBOS jueces terminen. No sintetizás con un resultado parcial.

**Categorizás cada hallazgo:**

| Combinación | Categoría | Acción |
|-------------|-----------|--------|
| Juez A ✅ + Juez B ✅ | **Confirmado** | Fix obligatorio (alta confianza) |
| Juez A ✅ + Juez B ❌ | **Sospechoso (A)** | Triage, no fix automático |
| Juez A ❌ + Juez B ✅ | **Sospechoso (B)** | Triage, no fix automático |
| Juez A dice X, Juez B dice !X | **Contradicción** | Flag para decisión humana |

**Clasificación de severidad:**

| Severidad | Definición | Acción |
|-----------|------------|--------|
| **CRITICAL** | Causa bug, data loss, security hole en producción | Fix inmediato, re-judge obligatorio |
| **WARNING (real)** | Causa problema en escenario realista pero no crítico | Fix, re-judge si hay CRITICALs también |
| **WARNING (theoretical)** | Requiere escenario forzado, input malicioso, condición imposible | Reportar como INFO, NO fix, NO re-judge |
| **SUGGESTION** | Mejora, estilo, preferencia personal | Fix inline si trivial, NO re-judge |

**Determinación de "real" vs "theoretical":** _"Can a normal user, using the tool as intended, trigger this?"_ Si sí → real. Si requiere un manifest malicioso, condiciones imposibles, o input corrupto → theoretical.

**Consolidás en una tabla de veredicto:**

```markdown
## Round 1 — Verdict

| Finding | Judge A | Judge B | Severity | Status |
|---------|---------|---------|----------|--------|
| Missing nil check in auth.go:42 | ✅ | ✅ | CRITICAL | Confirmed |
| No error log on disk full | ✅ | ❌ | WARNING (real) | Suspect (A only) |
| Windows path edge case | ❌ | ✅ | WARNING (theoretical) | INFO |
| Naming in handler.go:15 | ❌ | ✅ | SUGGESTION | Suspect (B only) |
```

### 5. Fixear los issues confirmados (con aprobación del usuario)

**Round 1:** Presentás la tabla de veredicto al usuario y preguntás:

```
These are the confirmed issues. Want me to fix them?
```

Si el usuario dice **sí** (o da feedback específico sobre qué fixear):

1. **Delegás un Fix Agent** con la lista de issues confirmados
2. **No fixeás vos mismo** — usás otro `delegate()` con un prompt específico
3. **Esperás** a que el Fix Agent termine y reporte los cambios

**El prompt del Fix Agent:**

```
You are a surgical fix agent. Apply ONLY the confirmed issues listed.

## Confirmed Issues to Fix
{paste confirmed findings table}

{si hay skill registry: ## Project Standards (auto-resolved)}
{compact rules}

## Instructions
- Fix ONLY the confirmed issues above
- Do NOT refactor beyond what is needed
- If you fix a pattern in one file, search for SAME pattern in all related files
- Return summary: ## Fixes Applied — [file:line] — {what was fixed}
```

**Scope rule del Fix Agent:** Si fixea un patrón en un archivo (ej: agrega error logging a un discard silencioso), busca el MISMO patrón en TODOS los archivos tocados por este cambio y fixeá todos.

Si el usuario dice **no**: `JUDGMENT: ESCALATED`. Reportás los issues restantes.

### 6. Re-evaluar (máximo 2 iteraciones)

Después del fix, **re-lanzás AMBOS jueces en paralelo** (Round 2). Mismo protocolo, frescos, sin saber del round anterior.

**Convergencia:**

| Round | Resultado | Acción |
|-------|-----------|--------|
| Round 2 | 0 CRITICALs + 0 confirmed WARNINGs | ✅ **JUDGMENT: APPROVED** |
| Round 2 | CRITICALs confirmados | Fix Agent (Round 3) + re-judge |
| Round 3 | CRITICALs confirmados | Preguntar al usuario si continuar |

**Regla de convergencia:**
- WARNINGs teóricos y SUGGESTIONs no cuentan para la convergencia.
- Si solo hay theoretical warnings → APPROVED igual.
- Si después de Round 2 hay CRITICALs → Fix + Round 3.
- Si después de Round 3 (2 iteraciones de fix) quedan issues → preguntar al usuario.

### 7. Decidir: Approved o Escalated

**JUDGMENT: APPROVED ✅**

```markdown
## Judgment Day — {target}

### Round 2 — Re-judgment
- Judge A: PASS ✅ — No issues found
- Judge B: PASS ✅ — No issues found

### JUDGMENT: APPROVED ✅
Both judges pass clean. Target is cleared for merge.
```

**JUDGMENT: ESCALATED ⚠️**

```markdown
## Judgment Day — {target}

### JUDGMENT: ESCALATED ⚠️
User chose to stop after 2 fix iterations. Issues remain.

### Remaining Issues
| Finding | Judge A | Judge B | Severity |
|---------|---------|---------|----------|
| {desc} | ✅ | ✅ | CRITICAL |

### History
- Round 1: N confirmed issues
- Fix 1: applied N changes
- Round 2: M issues remain
- Fix 2: applied M changes
- Round 3: remaining → escalated

Recommend: human review of remaining issues before re-running JD.
```

### Output final

Tu entregable al orchestrator es:

1. **Veredicto final** (APPROVED ✅ o ESCALATED ⚠️)
2. **Historial completo** de rounds y fixes aplicados
3. **Issues restantes** si fue escalado

_"Dos jueces ciegos son más efectivos que un experto con sesgo. Pero el coordinador nunca es juez. Si tocás código, perdés la objetividad."_
