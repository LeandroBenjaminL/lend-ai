# Workflow: Branch PR

## Flujo principal

```
Orchestrator → [1. Verificar issue] → [2. Crear branch] → [3. Implementar] → [4. Validar pre-PR] → [5. Abrir PR] → [6. Etiquetar] → [7. Verificar checks] → Orchestrator
```

## Paso a paso

### 1. Verificar que el issue está aprobado

Antes de crear CUALQUIER cosa, verificás que el issue exista y tenga `status:approved`.

- **Buscás el issue:** Revisás que el issue referenciado esté abierto, no sea un duplicado, y esté en scope del proyecto.
- **Verificás status:** El issue DEBE tener la label `status:approved`. Si no la tiene, no podés crear el PR. Punto.
- **Sin issue no hay PR:** Si no hay un issue linkeado, no creás el PR. Decíselo al orchestrator y pedí que primero abra un issue con `issue-creation`.

_"Cada línea de código sin un issue aprobado es una deuda técnica que no sabés si el equipo necesita. Si no hay issue aprobado, no hay PR."_

### 2. Crear la branch con el naming correcto

La branch se crea desde `main` (o la rama base que corresponda) con el formato exacto:

```
<tipo>/<descripción>
```

El tipo coincide con el tipo de cambio:

| Tipo | Cuándo |
|------|--------|
| `feat/` | Nueva feature |
| `fix/` | Bug fix |
| `chore/` | Mantenimiento, tooling, CI |
| `docs/` | Documentación |
| `refactor/` | Refactor sin cambio de comportamiento |
| `perf/` | Mejora de performance |
| `test/` | Tests nuevos o mejorados |
| `style/` | Formateo, estilo |
| `build/` | Cambios en build system |
| `ci/` | Cambios en CI |
| `revert/` | Revertir un cambio anterior |

**Reglas del nombre:**

- Solo minúsculas, números, guiones y puntos: `[a-z0-9._-]`
- Sin espacios, sin underscores, sin mayúsculas
- Descriptivo pero conciso: `feat/user-login`, `fix/zsh-glob-error`, `chore/update-ci-actions`
- NO: `mi-branch`, `testing`, `asd123`, `FIX/BUG`, `feature/login`

```bash
git checkout -b feat/user-login main
```

### 3. Implementar con conventional commits

Todos los commits en la branch deben seguir **Conventional Commits**:

```
<tipo>(<scope>): <descripción en imperativo>
```

**Tipos permitidos:** `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`

**Reglas:**
- Commits atómicos (una unidad de trabajo por commit)
- Descripción en imperativo presente: "add validation", no "added validation"
- Scope opcional pero recomendado: `feat(auth): add token validation`
- `!` para breaking changes: `feat!: redesign auth system`
- Sin trailers de `Co-Authored-By`

**Ejemplos:**

```
feat(scripts): add Codex support to setup.sh
fix(skills): correct topic key format
docs(readme): update configuration guide
refactor(skills): extract shared persistence logic
```

### 4. Validar antes del push (pre-flight checks)

Antes de pushear y abrir el PR, corrés las validaciones automáticas:

```bash
# Shellcheck en scripts modificados
shellcheck scripts/*.sh

# Verificar que los tests pasan
go test ./...   # o npm test, pytest, etc.
```

**Checklist pre-push:**

- [ ] Todos los commits siguen Conventional Commits
- [ ] El branch name sigue el formato `<tipo>/<descripción>`
- [ ] Los scripts modificados pasan `shellcheck`
- [ ] Los tests pasan localmente
- [ ] No hay `Co-Authored-By` trailers en los commits
- [ ] El issue referenciado tiene `status:approved`

### 5. Abrir el PR con el template completo

Creás el PR usando `gh` y el template de PR del repo:

```bash
git push -u origin feat/user-login
gh pr create --title "feat(scope): description" --body "Closes #N" --body-file body.md
```

**El body del PR DEBE contener obligatoriamente:**

```markdown
### 1. Linked Issue (REQUIRED)
Closes #42

### 2. PR Type (REQUIRED)
- [ ] Bug fix
- [x] New feature
- [ ] Documentation only
- [ ] Code refactoring
- [x] Maintenance/tooling
- [ ] Breaking change

### 3. Summary
- Feature X implementada
- Tests agregados para casos A, B, C
- Documentación actualizada

### 4. Changes
| File | Change |
|------|--------|
| `auth/login.go` | Added login handler |
| `auth/login_test.go` | Added test cases |

### 5. Test Plan
- [x] Scripts run without errors: `shellcheck scripts/*.sh`
- [x] Tests pass: `go test ./...`
- [x] Skills load correctly in target agent

### 6. Contributor Checklist
- [x] Linked an approved issue
- [x] Added exactly one `type:*` label
- [x] Ran shellcheck on modified scripts
- [x] Skills tested in at least one agent
- [x] Docs updated if behavior changed
- [x] Conventional commit format
- [x] No `Co-Authored-By` trailers
```

**Reglas del body:**
- `Closes #N`, `Fixes #N`, o `Resolves #N` (case insensitive) — obligatorio.
- El issue linkeado DEBE tener `status:approved`.
- El tipo de PR debe coincidir con el tipo de commit principal.

### 6. Agregar la label de tipo

Agregás EXACTAMENTE UNA label `type:*` al PR:

| Tipo de cambio | Label |
|----------------|-------|
| Bug fix | `type:bug` |
| New feature | `type:feature` |
| Documentation | `type:docs` |
| Refactoring | `type:refactor` |
| Maintenance | `type:chore` |
| Breaking change | `type:breaking-change` |

```bash
gh pr edit <number> --add-label "type:feature"
```

Una sola label. No más, no menos. El sistema de CI lo verifica.

### 7. Verificar que los checks pasen

Después de abrir el PR, verificás que los checks automáticos se disparen:

| Check | Qué verifica | Qué hace si falla |
|-------|-------------|-------------------|
| Check Issue Reference | El body contiene `Closes/Fixes/Resolves #N` | Agregar el reference |
| Check Issue Has status:approved | El issue linkeado tiene `status:approved` | Pedir approval al maintainer |
| Check PR Has type:* Label | El PR tiene exactamente una label `type:*` | Agregar la label correcta |
| Shellcheck | Los scripts .sh pasan shellcheck | Corregir errores de shellcheck |

Si algún check falla, corregís y pusheás de nuevo (los checks se re-ejecutan automáticamente).

### Output final

Tu entregable al orchestrator es:

1. **PR creado** con URL (`gh pr view` para obtener la URL)
2. **Resumen de checks** (pasaron todos / alguno falló)
3. **Labels asignadas** (cuáles se agregaron)

_"Un PR bien armado es un regalo para el reviewer. Tiene todo lo que necesita saber, en el orden que lo necesita, sin tener que buscar nada."_
