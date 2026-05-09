---
name: branch-pr
description: >
  Flujo de creación de PRs siguiendo el sistema issue-first.
  Trigger: Cuando creás un PR, preparás cambios para review, o abrís una branch.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.1"
  model_tier: T2-fast
---

# Skill: branch-pr

Crear PRs que el revisor pueda entender sin llamadas de emergencia.

## Trigger

Cargá esta skill cuando:
- Terminaste de implementar y vas a abrir un PR.
- Te pidieron que mandes los cambios a review.
- Querés crear una branch con el nombre correcto.

## Por qué existe

Un PR bien hecho se revisa en minutos. Uno mal hecho arranca una cadena de
"qué quisiste decir acá" que nadie tiene tiempo de responder. La consistencia
libera carga cognitiva: si todos los PRs tienen la misma estructura, el revisor
no pierde energía buscando la información clave.

## Workflow

```
1. Verificá que el issue linked tenga status:approved
2. Creá la branch con formato type/descripcion
3. Implementá con commits convencionales
4. Ejecutá shellcheck en scripts modificados
5. Abrí el PR con el template
6. Agregá exactamente UNA label type:*
7. Esperá que pasen los checks automáticos
```

### Branches

Formato: `^(feat|fix|chore|docs|refactor|perf|test|build|ci|revert)\/[a-z0-9._-]+$`

| Tipo | Ejemplo |
|------|---------|
| Feature | `feat/user-login` |
| Bug fix | `fix/zsh-glob-error` |
| Chore | `chore/update-ci-actions` |
| Docs | `docs/installation-guide` |

### PR Body (usá el template)

El template está en `.github/PULL_REQUEST_TEMPLATE.md`. No te saltees secciones.

Lo mínimo que necesita:

```markdown
Closes #<issue>

<Tipo: uno de bug/feature/docs/refactor/chore/breaking-change>

## Summary
1-3 bullets de qué hace este PR.

## Changes
| Archivo | Cambio |

## Test Plan
- [ ] Scripts pasan shellcheck
- [ ] Probé manualmente la funcionalidad afectada
```

## Ejemplos

### Buen PR

```
feat(scripts): agregar flag --agent a setup.sh for Codex support

Closes #42

Type: feature

## Summary
- Agrega flag --agent a setup.sh
- Skills se linkean a .codex/ cuando corresponde
- Tests cubren los 3 agentes soportados

## Changes
| scripts/setup.sh | Flag --agent + switch case |
| scripts/test_setup.sh | Tests para cada agente |

## Test Plan
- [x] shellcheck scripts/*.sh
- [x] ./setup.sh --agent codex → skills en .codex/
- [x] ./setup.sh sin flag → defaults a claude
```

## Patrones

- **Un issue por PR**: si no hay issue, no hay PR. No existe PR sin issue linked.
- **Una label type:** exactamente una. Si sobra o falta, el CI falla.
- **Commits convencionales**: `feat(scope):`, `fix(scope):`, etc.
- **Shellcheck siempre**: si tocaste scripts, corré shellcheck antes de pushear.
- **Mensaje de commit explica el resultado**, no el listado de archivos.

## Anti-patrones

- Mandar un PR sin linked issue → el CI lo rechaza directo.
- Poner más de una label `type:*` → el CI lo rechaza.
- PRs de 800 líneas que mezclan refactor + feature + docs → partilos (ver `chained-pr`).
- Body vacío tipo "closes #1" nada más → el revisor tiene que adivinar qué cambió.
- Escribir el resumen del PR en inglés cuando el proyecto habla español → rompe consistencia.
