# Skill: sdd-tasks

## Qué es

Divide el cambio en tareas concretas, ordenadas por dependencia y agrupadas por fase.

**El principio**: una tarea bien escrita es accionable, verificable, y completable en una sesión. Si una tarea dice "implementar feature", está mal.

## Trigger

El orquestador te llama después de sdd-design para desglosar el cambio en tareas de implementación.

## Workflow

### 1. Leé proposal + specs + design
Identificá todos los archivos a crear/modificar/borrar, el orden de dependencias, y los requerimientos de testing.

### 2. Estimá el workload (Review Workload Forecast)
```
Decision needed before apply: Yes|No
Chained PRs recommended: Yes|No
Chain strategy: stacked-to-main|feature-branch-chain|size-exception|pending
400-line budget risk: Low|Medium|High
```

Si el riesgo es High o probable >400 líneas:
1. Marcá "Chained PRs: Yes"
2. Dividí en work units que puedan ser PRs encadenados
3. Cada unidad: scope autónomo, verification incluida, rollback claro

### 3. Escribí tasks.md

```markdown
# Tasks: {Change Title}

## Review Workload Forecast
{Las 4 líneas de plain-text de arriba}

## Suggested Work Units
| Unit | Goal | PR | Notes |
|------|------|----|-------|
| 1 | {deliverable} | PR 1 | {tests/docs} |
| 2 | {deliverable} | PR 2 | {depends on PR 1} |

## Phase 1: Foundation / Infrastructure
- [ ] 1.1 {archivo} — {qué hacer exactamente}
- [ ] 1.2 {archivo} — {qué hacer}

## Phase 2: Core Implementation
- [ ] 2.1 {acción concreta}
- [ ] 2.2 {acción concreta}

## Phase 3: Testing
- [ ] 3.1 {Test para spec scenario X}
- [ ] 3.2 {Test para spec scenario Y}
```

**Organización típica**:
- Phase 1: Foundation (tipos, interfaces, DB, config)
- Phase 2: Core (lógica principal, business rules)
- Phase 3: Integration/Wiring
- Phase 4: Testing (tests por spec scenario)
- Phase 5: Cleanup (docs, dead code)

### 4. Persistí
- artifact: `tasks`, topic_key: `sdd/{change-name}/tasks`

### 5. Devolvé summary

```markdown
## Tasks Created
| Phase | Tasks | Focus |
|-------|-------|-------|
| Phase 1 | {N} | Infrastructure |
| Phase 2 | {N} | Core |
| Total | {N} | |

### Review Workload Forecast
- 400-line risk: {Low/Medium/High}
- Chained PRs: {Yes/No}
- Decision needed: {Yes/No}

### Next Step
Apply (sdd-apply) o preguntar al usuario por chain strategy.
```

## Ejemplos

1. **Tasks para rate limiting**: Phase 1: `middleware/rate-limiter.go` + config struct. Phase 2: integración en router. Phase 3: tests para cada spec scenario. Workload: Low risk, single PR.

2. **Tasks para migración PostgreSQL**: Phase 1: schema + migrations. Phase 2: adapter + repository. Phase 3: migrar services uno por uno. Phase 4: tests de integración. Workload: High risk, 3 chained PRs.

3. **Tasks pequeñas para hotfix**: Phase 1: fix en `validateEmail()`. Phase 2: test del edge case. Workload: Low, single PR, decision needed: No.

## Reglas

- Toda tarea debe ser: **específica** ("Crear `auth/middleware.go` con JWT"), **accionable** ("Agregar `ValidateToken()`"), **verificable** ("Test: POST /login returns 401 sin token"), **chica** (un archivo o unidad lógica)
- Tasks ordenadas por dependencia — Phase 1 no depende de Phase 2
- Testing tasks referencian scenarios específicos de los specs
- Cada task: completable en UNA sesión
- Numeración jerárquica: 1.1, 1.2, 2.1
- Si TDD activo: RED (escribir test fallido) → GREEN (hacerlo pasar) → REFACTOR
- Máximo 530 words. Cada task: 1-2 líneas. Checklist, no párrafos.
- Siempre incluí Review Workload Forecast con las 4 líneas de plain-text

## Anti-patrones

- ❌ **Tareas vagas**: "Implementar feature" no es una tarea, es un epígrafe
- ❌ **Sin orden de dependencias**: Task 1.1 debería poder hacerse sin la 2.3
- ❌ **Saltarse el workload forecast**: Después llega apply con un PR de 1200 líneas
- ❌ **Tareas monolíticas**: Una task de "todo auth" debería ser 5-6 tareas chicas
- ❌ **Olvidar tests**: Si los specs tienen escenarios, las tasks deben testearlos
