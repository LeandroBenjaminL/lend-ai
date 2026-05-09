# Patterns: Pull Requests

> _Un PR no es código. Es una solicitud de confianza. Hacela fácil de aprobar._

## Tabla de decisión: validaciones pre-PR

| Check | Comando | Falla si... |
|-------|---------|-------------|
| Issue aprobado | `gh issue view <N>` | El issue no existe o no tiene `status:approved` |
| Branch naming | `git branch --show-current` | No matchea `^(feat\|fix\|chore\|...)\/[a-z0-9._-]+$` |
| Conventional commits | `git log --oneline` | Algún commit no sigue `tipo(scope): desc` |
| Shellcheck | `shellcheck scripts/*.sh` | Algún script tiene errores |
| PR body format | `gh pr view <N> --json body` | Falta `Closes #N`, PR type, checklist incompleto |
| Labels | `gh pr view <N> --json labels` | No tiene exactamente 1 label `type:*` |
| Tests | `go test ./...` (o similar) | Algún test falla |

## Tabla de correspondencia tipo de commit → label de PR

| Commit type | PR label | Tipo de cambio |
|-------------|----------|----------------|
| `feat` | `type:feature` | Nueva funcionalidad |
| `fix` | `type:bug` | Corrección de bug |
| `docs` | `type:docs` | Documentación |
| `refactor` | `type:refactor` | Refactor sin cambio de comportamiento |
| `chore` | `type:chore` | Mantenimiento, tooling |
| `style` | `type:chore` | Formateo, estilo |
| `perf` | `type:feature` | Mejora de performance |
| `test` | `type:chore` | Tests |
| `build` | `type:chore` | Build system |
| `ci` | `type:chore` | CI/CD |
| `revert` | `type:bug` | Revertir cambio |
| `feat!` / `fix!` | `type:breaking-change` | Breaking change |

## Tabla de branch naming

```
<tipo>/<descripción>
```

| Elemento | Regla | Buen ejemplo | Mal ejemplo |
|----------|-------|--------------|-------------|
| `tipo` | `feat`, `fix`, `chore`, `docs`, `refactor`, `perf`, `test`, `style`, `build`, `ci`, `revert` | `feat/user-login` | `feature/login` (no existe `feature`) |
| Separador | `/` | `fix/zsh-glob-error` | `fix-zsh-glob-error` (usa `/` ) |
| `descripción` | minúsculas, `a-z0-9._-` | `chore/update-ci-actions` | `chore/Actualizar_CI` (mayúsculas + underscore) |

## Tabla de partes obligatorias del body del PR

| Sección | Contenido | Validación |
|---------|-----------|------------|
| **Linked Issue** | `Closes #N` o `Fixes #N` o `Resolves #N` | CI checkea que exista el issue y tenga `status:approved` |
| **PR Type** | Checkbox exactamente UNO de 6 opciones | CI checkea que la label coincida |
| **Summary** | 1-3 bullet points del cambio | No hay validación automática |
| **Changes** | `\| File \| Change \|` | Opcional pero recomendado |
| **Test Plan** | Checkboxes de verificación | No hay validación automática |
| **Contributor Checklist** | TODOS los checkboxes marcados | CI checkea algunos items |

## Anti-patrones de PRs

| Anti-patrón | Cómo se ve | Problema | Solución |
|-------------|------------|----------|----------|
| **PR sin issue** | PR sin `Closes #N` | No se sabe qué problema resuelve. CI lo rechaza. | Siempre linkear un issue aprobado |
| **PR monolítico** | 2000+ líneas cambiadas | Nadie lo va a revisar bien | Partir en chained PRs |
| **Branch name random** | `asd123`, `my-branch`, `testing` | No se sabe qué contiene | Seguir `tipo/descripción` |
| **Labels faltantes** | PR sin `type:*` label | CI lo rechaza | Agregar exactamente 1 label |
| **PR body vacío** | Solo el título, sin description | El reviewer no sabe qué revisar | Usar el template completo |
| **Commits sucios** | `WIP`, `fixup`, `typo`, `test` en el historial | Historial imposible de leer | Squash antes del PR |
| **Co-Authored-By** | Trailers de AI en commits | Prohibido por reglas del proyecto | Eliminar antes del push |
| **PR a main directo** | PR apuntando a `main` sin pasar por develop/feature branch | Bypass del flujo de review | Seguir el flujo del proyecto |

## Checklist pre-creación de PR

- [ ] El issue linkeado existe y tiene `status:approved`
- [ ] La branch sigue el formato `<tipo>/<descripción>`
- [ ] Todos los commits siguen Conventional Commits
- [ ] Los scripts modificados pasan `shellcheck`
- [ ] Los tests pasan localmente
- [ ] No hay `Co-Authored-By` trailers
- [ ] El body del PR incluye: Linked Issue, PR Type, Summary, Changes, Test Plan, Contributor Checklist
- [ ] Los checkboxes del Contributor Checklist están todos marcados
- [ ] El total de líneas cambiadas es revisable (< 400 líneas, o justificado con chained PRs)
- [ ] Se agregó exactamente 1 label `type:*` al PR

## Principios fundamentales

1. **Sin issue aprobado no hay PR.** No es burocracia — es coordinación.
2. **El branch name es la primera impresión.** Si está mal, el reviewer ya desconfía.
3. **El body del PR no es opcional.** Es el contrato entre autor y reviewer.
4. **Una label, una branch, un propósito.** Cada PR hace una cosa.
5. **Si el CI lo puede checkear, no le pidas a un humano que lo revise.**

> _Un PR bien armado es un regalo para el reviewer. Tiene todo lo que necesita saber, en el orden que lo necesita, sin tener que buscar nada. El reviewer entra, lee, entiende, y decide._
