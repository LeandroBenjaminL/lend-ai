# Patterns: Work Unit Commits

> _El historial de git no es un backup. Es un relato. Si alguien hace `git log` en 6 meses, tiene que entender QUÉ pasó, POR QUÉ, y en QUÉ ORDEN._

## Tabla de decisión: ¿esto es una work unit?

| Pregunta | Sí ✅ | No ❌ |
|----------|------|------|
| ¿Tiene un propósito único y claro? | `feat(auth): add token validation` | `varios cambios` |
| ¿El repo funciona aplicando solo este commit? | El código compila y los tests pasan | El repo está roto sin el próximo commit |
| ¿Incluye su propia verificación? | Tests o docs en el mismo commit | Tests en otro commit |
| ¿Se puede revertir sin perder otros cambios? | `git revert` sin conflictos | Revertir deshace trabajo no relacionado |
| ¿El commit message explica el POR QUÉ? | "Agrega validación porque el middleware actual no checkea tokens expirados" | "fix auth" |
| ¿Tiene menos de 400 líneas cambiadas? | ~200 líneas, review rápido | 800+ líneas, reviewer sufre |

## Tabla de split: mal vs bien

| Situación | Split MALO (por tipo de archivo) | Split BUENO (por work unit) |
|-----------|--------------------------------|----------------------------|
| Feature de auth | Commit 1: `auth/model.go`, `auth/middleware.go` | Commit 1: `auth/model.go` + `auth/model_test.go` (domain model) |
| | Commit 2: `auth/handler.go` | Commit 2: `auth/middleware.go` + `auth/handler.go` + tests (flow) |
| | Commit 3: `auth/*_test.go` (todos los tests) | Commit 3: docs (si aplica) |
| Bug fix + refactor | Commit 1: `fix: corregir parser` (incluye refactor) | Commit 1: `fix(parser): handle nil input` |
| | | Commit 2: `refactor(parser): extract date validation` |
| Docs + feature | Commit 1: `docs: update README` | Commit 1: `feat: add user API` + `api.go` + `api_test.go` |
| | Commit 2: `feat: add user API` (los docs ya no reflejan el API nuevo) | Commit 2: `docs: document user API` |
| Feature grande | Un commit de 1200 líneas | 3-4 chained PRs de ~300 líneas cada uno |

## Tabla de errores comunes en commit messages

| Error | Ejemplo | Por qué está mal | Cómo fixear |
|-------|---------|------------------|-------------|
| **Vago** | `fix` | No dice qué fix | `fix(parser): handle nil input in date parsing` |
| **Checkpoint** | `WIP` | No es una unidad de trabajo | Partir en commits atómicos o squash |
| **Descripción de archivos** | `Cambios en models y services` | Describe archivos, no comportamiento | `feat(auth): add user profile model and service` |
| **Pasado** | `Added validation` | Debe ser imperativo presente | `add validation` |
| **Muy largo** | `feat: add user login with token validation, update middleware, fix tests, and update docs` | Mezcla múltiples unidades | Partir en 2-3 commits |
| **Sin scope** | `fix: handle error` | No dice qué área | `fix(auth): handle token expiry error` |
| **Sin por qué** | `refactor: extract function` | Dice qué, no por qué | `refactor: extract date parser for reuse in billing module` |
| **Ticket number solo** | `Fix PROJ-123` | El issue dice qué, el commit debe decir por qué | `fix: handle nil input (PROJ-123)` |
| **Co-Authored-By** | `feat: add feature\n\nCo-Authored-By: AI <ai@example.com>` | Prohibido por reglas del proyecto | Eliminar trailer |

## Tipos de commit y sus significados

| Tipo | Significado | Ejemplo | Release impact |
|------|-------------|---------|----------------|
| `feat` | Nueva feature para el usuario | `feat(auth): add OAuth2 login` | Minor version bump |
| `fix` | Bug fix | `fix(parser): handle nil input` | Patch version bump |
| `docs` | Cambios en documentación | `docs(readme): add examples` | No release |
| `refactor` | Refactor sin cambio de comportamiento | `refactor(auth): extract validation` | No release |
| `perf` | Mejora de performance | `perf(db): add index on user_id` | Patch version bump |
| `test` | Tests nuevos o mejorados | `test(auth): add token tests` | No release |
| `chore` | Mantenimiento, tooling, CI | `chore(ci): add shellcheck` | No release |
| `style` | Formateo, linting | `style: format with gofmt` | No release |
| `build` | Build system o dependencias | `build: upgrade to Go 1.22` | No release |
| `ci` | Cambios en CI | `ci: add branch validation` | No release |
| `revert` | Revertir un commit anterior | `revert: undo broken setup change` | Patch version bump |

## Anti-patrones de estructura de commits

| Anti-patrón | Cómo se ve | Problema | Solución |
|-------------|------------|----------|----------|
| **The dump** | 1 commit con todo el feature (model + service + handler + tests + docs) | Imposible de revisar, imposible de revertir parcialmente | Partir en work units atómicas |
| **The scavenger hunt** | Tests en un commit separado del código que testean | Reviewer tiene que saltar entre commits para entender | Tests van con el código que verifican |
| **The time capsule** | Commits cada 30 minutos: `WIP`, `more work`, `try something` | El historial es un diario personal, no un relato | Squash antes de PR, mantener solo unidades completas |
| **The kitchen sink** | Un commit de refactor + fix + feature todo mezclado | Si hay bug, no sabés qué parte del commit lo causó | Cada tipo de cambio va separado |
| **The nested dependency** | Commit 2 necesita a Commit 1 pero Commit 1 no anda solo | El reviewer no puede revisar en orden lógico | Cada commit debe ser autocontenido |
| **The cleanup** | Commit final `fixup`, `typo`, `oops` | Ruido en el historial | Squashear con el commit que corrige |
| **The giant message** | Commit message de 20 líneas que debería ser 3 commits | Un commit está haciendo demasiadas cosas | Partir en commits más chicos |

## Checklist de verificación pre-PR

Antes de abrir el PR, revisás el plan de commits:

- [ ] Cada commit tiene UN solo propósito (no mezcla feat + fix + refactor)
- [ ] El commit message sigue Conventional Commits: `tipo(scope): descripción`
- [ ] El commit message explica el POR QUÉ (no el qué — el qué está en el diff)
- [ ] Los tests están en el mismo commit que el código que verifican
- [ ] Las docs están en el mismo commit que el cambio que documentan
- [ ] El repo funciona aplicando solo el primer commit (si alguien checkoutea ahí, todo anda)
- [ ] No hay commits de `WIP`, `fixup`, `typo`, o `test` sin código
- [ ] El total de líneas cambiadas no supera ~400 por PR (si supera, parte en chained PRs)
- [ ] No hay trailers `Co-Authored-By` en ningún commit
- [ ] El historial cuenta una historia progresiva, no una cronología

## Principios fundamentales

1. **Un commit no es un backup.** Es una comunicación con tu futuro yo y con tu equipo.
2. **Si no podés escribir el commit message en una línea, el commit no es atómico.**
3. **Los tests sin el código que verifican no existen.** Y el código sin tests es no verificable.
4. **El tamaño importa.** 400 líneas no es un límite arbitrario — es lo que un revisor procesa con atención.
5. **El historial de git se lee más veces de las que se escribe.** Invertí tiempo en que sea legible.

> _Si alguien llega a tu repo dentro de 6 meses y el `git log` es un borrón de "varios cambios" y "WIP", le estás fallando a tu equipo. Cada commit es una carta al reviewer del futuro._
