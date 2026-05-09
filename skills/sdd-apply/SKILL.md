# Skill: sdd-apply

## Qué es

Implementa tareas del cambio. Escribís código real siguiendo los specs (el QUÉ), el diseño (el CÓMO), y las tasks (el ORDEN).

**El principio**: apply no es "programar libre". Es ejecutar un plan verificado. Cada línea de código responde a un requirement en los specs.

## Trigger

El orquestador te lanza para implementar una o más tareas específicas de un cambio.

## Workflow

### 1. Cargá contexto
Antes de escribir una línea:
1. Leé los specs (qué debe hacer el código)
2. Leé el design (cómo estructurarlo)
3. Leé el código existente en los archivos afectados
4. Revisá las convenciones del proyecto (`config.yaml`)

### 2. Verificá workload decision
Si el forecast dice `400-line budget risk: High`, `Chained PRs: Yes`, o `Decision needed: Yes`, confirmá que el orquestador dio una resolución:
- **auto-chain**: implementá solo tu work unit asignada
- **exception-ok** o `single-pr` con `size:exception`: seguí solo si el prompt lo autoriza explícitamente
- Si no hay resolución → STOP, devolvé `blocked`

### 3. Leé apply progress previo
Si hay batches anteriores de tasks, leé el progress previo (`mem_search` o archivo). NO sobreescribas — mergeá completados anteriores + nuevos.

### 4. Determiná modo TDD
```
Leé testing capabilities:
├── strict_tdd: true + test runner → STRICT TDD MODE
│   Cargá strict-tdd.md, seguí RED→GREEN→REFACTOR
├── strict_tdd: false o sin test runner → STANDARD MODE
└── No hay silencio: si TDD está activo, lo seguís o reportás failure
```

### 5. Implementá (Standard Mode)

```
POR CADA TASK:
├── Leé el spec scenario (acceptance criteria)
├── Leé las design decisions (constraints)
├── Match existing code patterns
├── Escribí el código
├── Marcá [x] en tasks.md
└── Notá cualquier desviación o issue
```

### 6. Marcá tasks completas
```markdown
- [x] 1.1 Crear `middleware.go` con JWT validation
- [ ] 1.2 Agregar routes ← pendiente
```

### 7. Persistí progress
- artifact: `apply-progress`, topic_key: `sdd/{change-name}/apply-progress`
- Mergeá con progress previo (nunca perdás completados anteriores)
- En openspec: actualizá `tasks.md` con [x]
- En engram: `mem_update` con el tasks observation ID

### 8. Devolvé summary

```markdown
## Implementation Progress
**Mode**: {Strict TDD | Standard}

### Completed Tasks
- [x] {task 1.1}
- [x] {task 1.2}

### Files Changed
| File | Action | What |
|------|--------|------|

### Deviations from Design
{si applica: qué se desvió y por qué}

### Remaining Tasks
- [ ] {next task}

### Status
{N}/{total} tasks complete. Ready for {next batch / verify}.
```

## Ejemplos

1. **Apply de rate limiting**: Tasks 1.1-1.3. Creás `middleware/rate-limiter.go`, agregás config, integrás en router. Mode: Standard. Files: 3 changed. Next: verify.

2. **Apply con Strict TDD**: Tasks 2.1-2.2. RED: escribís test que falla para `validateEmail()`. GREEN: implementás la función. REFACTOR: limpiás. Next: verify con TDD checks.

3. **Apply de chained PR slice**: Tasks asignadas son solo las del PR 1 (foundation). Implementás interfaces y config. Scope autónomo. Return: PR boundary clear.

## Reglas

- **Siempre** leé specs antes de implementar — son tu acceptance criteria
- **Siempre** seguí el design — no te mandes por otro approach por tu cuenta
- Match existing code patterns — no introduzcas estilos nuevos sin necesidad
- Si el diseño está mal o incompleto, NOTALO en el return, no lo cambiés silenciosamente
- Si una task está bloqueada, STOP y reportá
- Nunca implementes tasks que no te asignaron
- Si TDD Mode activo: el módulo `strict-tdd.md` OVERRIDE el Step 5 (Standard)
- Workload decision requerida sin resolución → STOP, no escribas código

## Anti-patrones

- ❌ **Codear sin leer specs**: Estás implementando otra cosa
- ❌ **Freelancear otro approach**: "Yo creo que en vez de Redis mejor SQLite" — si no está en el design, no corresponde
- ❌ **No marcar tasks**: El orquestador no sabe qué avanzaste
- ❌ **Sobreescribir progress previo**: Perdés el registro de batches anteriores
- ❌ **Implementar de más**: Hacer features que los specs no piden es deuda técnica
