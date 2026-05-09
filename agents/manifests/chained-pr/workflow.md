# Workflow: Chained PR

## Flujo principal

```
Orchestrator → [1. Evaluar tamaño] → [2. Elegir estrategia] → [3. Planificar slices] → [4. Estructurar cadena] → [5. Documentar mapa] → [6. Crear PRs] → Orchestrator
```

## Paso a paso

### 1. Evaluar el tamaño total del cambio

Antes de crear PRs, calculás el tamaño total del cambio.

- **Sumás líneas cambiadas:** `git diff main...HEAD --stat` o estimación basada en los archivos tocados.
- **Comparás con el budget:** 400 líneas cambiadas (`additions + deletions`). Es el límite de lo que un reviewer puede procesar con atención sostenida (~60 minutos).
- **Clasificás el riesgo:**
  - < 200 líneas → PR único, sin necesidad de split
  - 200-400 líneas → PR único, monitorear tamaño
  - 400-800 líneas → Chained PR recomendado (2 slices)
  - 800+ líneas → Chained PR obligatorio (3+ slices)

_"El reviewer no es una máquina de procesar diffs. Es un humano que tiene 60 minutos para darle atención a tu código. Respetá su tiempo."_

### 2. Elegir la estrategia de encadenamiento

Cuando el cambio supera 400 líneas, **le preguntás al usuario** qué estrategia prefiere. No asumís.

**Las opciones:**

| Estrategia | Mecánica | Mejor para |
|-----------|----------|------------|
| **Stacked PRs to main** | Cada PR mergea a main en orden. El PR 2 apunta al branch del PR 1. Cuando PR1 mergea, PR2 se reubica a main. | Equipos rápidos, startups, slices independientes |
| **Feature Branch Chain** | Todos los PRs apuntan a una branch feature compartida. Solo el tracker PR mergea a main. | Control de rollback, releases coordinados, integración antes de main |
| **size:exception** | Un solo PR con aprobación del maintainer. | Código generado, migraciones, vendor diffs |

**Preguntale al usuario:**

```
Este cambio tiene aproximadamente N líneas, superando el budget de 400.
¿Cómo querés dividirlo?

1. Stacked PRs to main — cada slice mergea independientemente
2. Feature Branch Chain — todos los slices a una branch feature, tracker mergea a main
3. size:exception — mantener un solo PR con aprobación del maintainer
```

**Cacheás la respuesta** para el resto de la sesión. No preguntás de nuevo a menos que el scope cambie.

### 3. Planificar los slices autónomos

Con la estrategia elegida, dividís el cambio en slices. Cada slice es un **chained PR** que debe cumplir:

**Requisitos de autonomía:**
- [ ] CI verde en su propio branch
- [ ] Un solo deliverable outcome claro
- [ ] Rollback razonable sin revertir trabajo no relacionado
- [ ] Verificación incluida (tests, docs, o verificación manual)
- [ ] Reviewable sin leer los otros PRs de la cadena

**Criterios de división:**
- **Por capa arquitectónica:** primero domain model, después lógica de negocio, después integración, después UI
- **Por feature:** feature A completa, después feature B completa
- **Por preocupación:** foundation/setup, después core logic, después tests, después docs
- **Por archivo:** solo si los archivos son verdaderamente independientes

**Ejemplo de división para un feature de 1200 líneas:**

```
Slice 1 (350 líneas): feat(auth): add token validation domain model + tests
  → auth/model.go, auth/model_test.go

Slice 2 (380 líneas): feat(auth): wire validation into login flow + tests
  → auth/middleware.go, auth/handler.go, auth/handler_test.go

Slice 3 (250 líneas): feat(api): add user endpoints with pagination
  → api/users.go, api/users_test.go

Slice 4 (220 líneas): docs: document auth and user API
  → docs/auth.md, docs/api.md, README.md
```

Total: 1200 líneas → 4 PRs de ~300 líneas cada uno. Todos bajo el budget de 400.

### 4. Estructurar la cadena y las dependencias

Dependiendo de la estrategia elegida, estructurás las branches:

**Stacked PRs to main:**

```
main
 └── feat/token-model            # PR 1 → a main
      └── feat/login-flow        # PR 2 → a feat/token-model → después a main
           └── feat/user-api     # PR 3 → a feat/login-flow → después a main
                └── feat/docs    # PR 4 → a feat/user-api → después a main
```

Creación:
```bash
git checkout -b feat/token-model main
# ... commits ...
git push -u origin feat/token-model
gh pr create --base main --title "feat(auth): add token validation" --body "..."

git checkout -b feat/login-flow feat/token-model
# ... commits ...
git push -u origin feat/login-flow
gh pr create --base feat/token-model --title "feat(auth): wire login flow" --body "..."
```

Cuando PR 1 mergea: rebase PR 2 a main, retarget a main.

**Feature Branch Chain:**

```
main
 └── feat/my-feature              # tracker PR → a main (draft, no-merge)
      ├── feat/my-feature-01-core # PR 1 → a feat/my-feature
      ├── feat/my-feature-02-ui   # PR 2 → a feat/my-feature
      └── feat/my-feature-03-docs # PR 3 → a feat/my-feature
```

Creación:
```bash
git checkout -b feat/my-feature main
# Tracker PR (draft)
git push -u origin feat/my-feature
gh pr create --base main --title "feat: my feature" --body "..." --draft

# Child PRs
git checkout -b feat/my-feature-01-core feat/my-feature
gh pr create --base feat/my-feature --title "feat(core): core logic" --body "..."
```

**Regla crítica:** Los child PRs NUNCA apuntan a main. Siempre apuntan a la feature branch. Si apuntan a main, bypassan el tracker.

### 5. Documentar el mapa de la cadena

CADA PR en la cadena debe incluir una sección **Chain Context** en su body:

```markdown
## Chain Context

| Field | Value |
|-------|-------|
| Chain | auth-refactor |
| Tracker PR | #42 |
| Position | 2 of 4 |
| Base | feat/auth |
| Depends on | #41 (token model) |
| Follow-up | #43 (user API) |
| Review budget | 380 / 400 |
| Starts at | feat/login-flow branch |
| Ends with | login flow wired and tested |

### Chain Overview
main
 └── #41 Token model
      └── 📍 #42 This PR (login flow)
           └── #43 User API
                └── #44 Docs
                     └── #42 Tracker

### Chain Status
| PR | Scope | Status |
|----|-------|--------|
| #41 | Token model | ✅ Merged |
| #42 | Login flow | 📍 Review here |
| #43 | User API | ⚪ Pending |
| #44 | Docs | ⚪ Pending |
| #45 | Tracker | 🟡 Draft |

## Scope
- Login handler with JWT validation
- Middleware registration in router
- Error responses for invalid tokens
- Tests for all new handlers

**Excludes:** User API endpoints (next PR), documentation (after PR).

## Autonomy
- [x] CI passes for this branch in isolation
- [x] One deliverable: login with token validation
- [x] Revert without affecting unrelated work
- [x] Tests cover all new code in this PR

## Review Notes
- Review this PR in isolation.
- The token model from PR #41 is a dependency — it's already merged.
- User API in PR #43 is intentionally excluded.
```

**Si la cadena tiene más de 2 PRs,** creás un **tracker PR** (draft, no-merge) que contiene el mapa completo.

### 6. Crear los PRs en orden

Creás los PRs en orden de dependencia:

1. **PR 1 (foundation):** primero, apunta a main (stacked) o a feature branch (chain).
2. **PR 2-N:** cada uno apunta a su base correspondiente.
3. **Tracker PR:** si aplica, draft, con `no-merge`, solo mapa.

```bash
# Verificar tamaño antes de abrir
gh pr view <NUMBER> --json additions,deletions,changedFiles,title,url

# Crear PR apuntando a feature branch
gh pr create --base feat/my-feature \
  --title "feat(core): core logic" \
  --body-file pr-body.md
```

**Después de cada merge/rebase:**
- Stacked: cuando PR anterior mergea, rebaseá el actual a main y retargeteá.
- Chain: mergeá child PRs a feature branch, después mergeá tracker a main.

### Output final

Tu entregable al orchestrator es:

1. **Lista de PRs creados** con URLs, orden y estado
2. **Estrategia elegida** y justificación
3. **Mapa de dependencias** entre PRs
4. **Tracker PR** (si aplica) con el plan completo

_"Una cadena de PRs no es una excusa para mandar código sin terminar. Cada PR individual debe ser un entregable completo y reviewable. Si no funciona solo, no es un slice — es un fragmento."_
