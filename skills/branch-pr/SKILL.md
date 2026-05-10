---
name: branch-pr
description: >
  Creación de PRs con issue-first — branch naming, commits, descripción
  y review. PRs chicos, enfocados y revisables.
  Trigger: Cuando creás un PR, preparás cambios para review, o abrís una branch.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: branch-pr

PRs que se pueden revisar en 5 minutos, no en 5 horas.

## Trigger

- Vas a crear una nueva branch para trabajar
- Terminaste los cambios y abrís un PR
- Te pidieron review de un PR
- Un PR está muy grande y hay que partirlo

## Workflow LEND

1. ANALIZAR
   ├── Issue: ¿hay issue asociado? ¿qué resuelve?
   ├── Scope: ¿cuántos archivos? ¿cuántas líneas? (>400 → chained-pr)
   └── Branch: ¿sobre qué branch base? (main, develop, feature)

2. OFRECER (Menú del Senior)
   ├── A) Branch + PR simple — branch directa + PR con template mínimo
   ├── B) PR con descripción — contexto, cambios, testing, screenshots
   └── C) PR estructurado — issue link, descripción, checklist, breaking changes

3. ELEGIR → confirmación

4. HACER
   ├── Branch name: `tipo/issue-numero-descripcion` (feat/123-login, fix/456-crash)
   ├── Commits: conventional commits, atómicos
   ├── PR description: qué, por qué, cómo, testing, screenshots
   ├── Template: contexto, cambios, evidencia, checklist de review
   ├── PR chico: < 400 líneas. Si es más grande → chained-pr
   └── Labels: feat, fix, chore, breaking, needs-review

5. VERIFICAR
   ├── El PR tiene descripción clara
   ├── Los tests pasan en CI
   └── No hay conflictos con la branch base
