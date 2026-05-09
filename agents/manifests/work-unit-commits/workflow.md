# Workflow: Work Unit Commits

## Flujo principal

```
Orchestrator → [1. Analizar cambio] → [2. Identificar work units] → [3. Verificar atómica] → [4. Estructurar commits] → [5. Escribir messages] → [6. Verificar coherencia] → Orchestrator
```

## Paso a paso

### 1. Analizar el cambio total

Antes de tocar `git add`, entendés el alcance completo del cambio.

- **¿Qué archivos se modificaron?** Revisás `git diff --stat` para tener la vista completa.
- **¿Qué comportamientos cambiaron?** No archivos — comportamientos. "Agregué validación de token", "Corregí el parsing de fechas", "Actualicé docs de API". Cada comportamiento es un candidato a work unit.
- **¿Qué dependencias hay entre cambios?** ¿El cambio B necesita que el cambio A esté primero? ¿O son independientes?
- **¿Hay cambios mezclados?** ¿Un archivo toca dos cosas distintas? Eso es una señal de alerta.

_"Si mirás `git diff` y ves 3 cambios no relacionados en el mismo diff, ya tenés un problema. Cada diff debería contar UNA historia."_

### 2. Identificar las work units

Una work unit es un comportamiento entregable, atómico y verificable. Se define por:

- **Un propósito claro:** "Agregar validación de token JWT al middleware"
- **Un scope acotado:** toca N archivos que juntos implementan esa validación
- **Verificación incluida:** tests, docs, o verificación manual de ESA unidad
- **Rollback razonable:** revertir este commit no afecta otros cambios

**Ejemplos de work units bien identificadas:**

| Proyecto | Work unit | Archivos típicos |
|----------|-----------|------------------|
| Auth | Agregar modelo de token con validación | `auth/model.go`, `auth/model_test.go` |
| Auth | Wirear validación en login flow | `auth/middleware.go`, `auth/handler.go`, `auth/handler_test.go` |
| API | Endpoint GET /users con paginación | `api/users.go`, `api/users_test.go`, `docs/api.md` |
| Fix | Corregir parsing de fechas UTC | `utils/time.go`, `utils/time_test.go` |
| Docs | Actualizar README con ejemplos de API | `README.md` |

**Anti-patrones de work units:**

| Mal | Por qué |
|-----|---------|
| "Modelos y servicios" | Mezcla domain model con lógica de negocio |
| "Tests" | Tests sin el código que testean no son una unidad |
| "Refactor y feature" | Refactor y feature nueva son dos cambios distintos |
| "Fix de bugs varios" | Cada bug es una work unit separada |
| "WIP" | No es un comportamiento entregable |

### 3. Verificar atomicidad de cada unidad

Cada work unit tiene que pasar el **test de atomicidad**. La unidad es atómica si:

- [ ] **Tiene un solo propósito:** el commit message se puede escribir en una línea tipo "feat(auth): add token validation"
- [ ] **Es autocontenido:** el repo funciona igual si solo aplicás este commit
- [ ] **No mezcla concerns:** no toca lógica de negocio Y formateo Y refactor Y docs en el mismo commit
- [ ] **Es reversible sin pérdida:** revertir este commit no deshace cambios de otra unidad
- [ ] **Incluye su verificación:** tests o docs que validan esta unidad están EN ESTE commit, no en otro
- [ ] **No es un checkpoint:** no es "lo que tenía a las 5pm". Es una unidad completa de trabajo.

**Prueba práctica:** Si alguien te pregunta "¿qué hace este commit?" y la respuesta tiene la palabra "y" (ej: "agrega validación Y corrige el formateo Y actualiza docs"), NO es atómico. Partilo.

### 4. Estructurar la secuencia de commits

Con las work units identificadas, definís el orden:

- **Dependencias primero:** Si B depende de A, A va primero.
- **Foundation antes que features:** Primero modelos y tipos, después lógica de negocio, después integración, después docs.
- **Independientes en paralelo:** Si A y B no dependen entre sí, el orden no importa.
- **Fix antes que feature:** Un bug fix va antes que una feature nueva.

**Estructura típica para un feature mediano:**

```
Commit 1: feat(auth): add token validation domain model and tests
  → auth/model.go, auth/model_test.go

Commit 2: feat(auth): wire token validation into login flow
  → auth/middleware.go, auth/handler.go, auth/handler_test.go

Commit 3: feat(api): add user list endpoint with pagination
  → api/users.go, api/users_test.go

Commit 4: docs(api): document user endpoints with examples
  → docs/api.md, README.md
```

**Para un fix:**

```
Commit 1: fix(parser): correct UTC timezone parsing
  → utils/time.go, utils/time_test.go
```

**Para chained PRs:** Si el total supera ~400 líneas, cada commit o grupo de commits afines pasa a ser un PR separado en el chain. No esperás a tener todo para hacer PR — PRdeás cada work unit independiente.

### 5. Escribir commit messages semánticos

Cada commit message sigue **Conventional Commits** con estructura precisa.

**Formato:**

```
<tipo>(<scope>): <descripción en imperativo>

<opcional: cuerpo explicando POR QUÉ, no QUÉ>

<opcional: footer con breaking changes o issues>
```

**Reglas:**
- `tipo` es obligatorio: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `style`, `ci`, `build`, `revert`
- `scope` es opcional pero recomendado: `auth`, `api`, `parser`, `cli`, etc.
- `descripción` es en imperativo, presente: "add", "fix", "remove", no "added", "fixed", "removed"
- El cuerpo explica el **por qué**, no el qué. El qué ya está en el diff.
- Sin trailers de `Co-Authored-By`.

**Buenos ejemplos:**

```
feat(auth): add JWT token validation middleware

Validates Bearer tokens on protected routes before passing to handlers.
Uses the RSA public key from the environment for verification.

Closes #42
```

```
fix(parser): handle nil input in date parsing

The parser panicked when receiving nil pointers from the HTTP layer.
Added nil check before type assertion.
```

```
refactor(api): extract pagination logic into shared helper

Reduces duplication across 3 endpoints that implement cursor pagination.
No behavior change — extracted and tested separately.
```

**Malos ejemplos:**

```
"varios cambios" — no dice nada
"fix" — no dice qué fix
"actualizaciones" — no dice qué se actualizó
"WIP" — no es un commit, es un checkpoint
"cambios en models y services" — describe archivos, no comportamiento
```

### 6. Verificar coherencia del historial

Antes de pasar la secuencia al orchestrator, revisás el plan de commits como si fueras un reviewer del historial:

- [ ] Cada commit tiene UN propósito claro
- [ ] La descripción en imperativo presente: "add", "fix", "remove"
- [ ] El repo funciona aplicando solo el primer commit (si alguien hace `git checkout` en ese punto, todo anda)
- [ ] Los tests están en el mismo commit que el código que testean
- [ ] Las docs están en el mismo commit que el cambio que documentan
- [ ] No hay commits de "fixup" o "typo" — esos se squash antes del PR
- [ ] No hay "test" commits sin el código correspondiente
- [ ] El historial cuenta una historia progresiva, no una cronología de checkpoints
- [ ] Si es parte de un chained PR, cada PR tiene sus commits claros y su límite de 400 líneas

### Output final

Tu entregable al orchestrator es:

1. **Plan de commits** con la secuencia ordenada, cada uno con su mensaje y archivos incluidos
2. **Agrupación en PRs** si corresponde (commit único, PR único, o chained PRs)
3. **Justificación de splits** que hiciste (por qué esta work unit va separada de esta otra)

_"Un buen historial de git es como un libro de historia: tiene capítulos, cada capítulo cubre un tema, y podés leerlos en orden o saltar al que te interesa. Un mal historial es como un tacho de papeles revueltos."_
