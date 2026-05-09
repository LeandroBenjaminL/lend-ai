---
name: issue-creation
description: >
  Flujo de creación de issues en GitHub siguiendo el sistema issue-first.
  Trigger: Cuando creás un issue, reportás un bug, o solicitás una feature.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T2-fast
---

# Skill: issue-creation

Crear issues que se puedan entender, triagear y eventualmente convertir en PRs.

## Trigger

- Encontraste un bug o querés una feature nueva.
- Necesitás reportar algo que después va a tener un PR linked.
- Sos maintainer y estás triageando issues.

## Por qué existe

El issue es la semilla de todo cambio. Si está mal definido, el PR que viene
después arrastra esa vaguedad. Issue-first significa: primero entendemos el
problema, después escribimos código. Sin un issue aprobado, no hay PR.

## Workflow

```
1. Buscá si ya existe un issue similar (evitá duplicados)
2. Elegí el template correcto: Bug Report o Feature Request
3. Completá todos los campos obligatorios
4. Checkeá los pre-flight checks
5. Enviá → se auto-etiqueta con status:needs-review
6. Esperá que un maintainer agregue status:approved
7. Recién ahí abrí un PR linked a este issue
```

## Templates

### Bug Report (`.github/ISSUE_TEMPLATE/bug_report.yml`)

Auto-labels: `bug`, `status:needs-review`

| Campo | Por qué importa |
|-------|----------------|
| Bug Description | Sin descripción clara, nadie sabe si es real |
| Steps to Reproduce | Si no se puede reproducir, no se puede fixear |
| Expected vs Actual | La diferencia es el bug |
| OS / Agent / Shell | El mismo bug se comporta distinto en cada entorno |

### Feature Request (`.github/ISSUE_TEMPLATE/feature_request.yml`)

Auto-labels: `enhancement`, `status:needs-review`

| Campo | Por qué importa |
|-------|----------------|
| Problem Description | El dolor que resuelve, no la solución que imaginás |
| Proposed Solution | Cómo debería funcionar desde el usuario |
| Affected Area | Dónde impacta: scripts, skills, docs, CI |

## Label System

| Label | Quién la pone | Significado |
|-------|--------------|-------------|
| `status:needs-review` | Automático | Llegó nuevo, hay que triagearlo |
| `status:approved` | Maintainer | Listo para implementar. Ya podés abrir PR |
| `priority:high` | Maintainer | Urgente, tapando algo |
| `priority:medium` | Maintainer | Importante, no urgente |
| `priority:low` | Maintainer | Nice to have |

## Ejemplos

### Bug report bien hecho

```bash
gh issue create --template "bug_report.yml" \
  --title "fix(scripts): setup.sh falla en zsh con glob error" \
  --body "Steps: 1. Correr setup.sh en zsh. 2. Error: 'no matches found: skills/*'.
Expected: manejar glob sin matching gracefulmente."
```

### Feature request bien hecho

```bash
gh issue create --template "feature_request.yml" \
  --title "feat(scripts): agregar soporte Codex a setup.sh" \
  --body "Problema: setup.sh solo configura Claude y OpenCode.
Solución: flag --agent codex que linkee skills a .codex/"
```

## Patrones

- **Dudás si es bug o feature?** Si rompe algo que andaba → bug. Si agrega algo
  nuevo → feature. Si es una pregunta → Discussion, no issue.
- **Buscá duplicados antes de crear**: `gh issue list --search "keyword"`.
- **Sin `status:approved` no hay PR**: es la regla de oro. Si abrís un PR sin
  el issue aprobado, el CI lo rechaza.
- **Los templates existen por algo**: blank issues están deshabilitados. Usalos.

## Anti-patrones

- Poner "no funciona" sin steps to reproduce → nadie puede investigar.
- Pedir features sin explicar el problema que resuelven → soluciones en busca de problema.
- Crear issues para preguntas → para eso están Discussions.
- Abrir PR sin esperar `status:approved` → lo va a rechazar el CI.
- Título vago tipo "error" o "mejora" → no se encuentra después en búsquedas.
