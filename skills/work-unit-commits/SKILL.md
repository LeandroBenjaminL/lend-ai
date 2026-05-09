---
name: work-unit-commits
description: >
  ⚠️ DEPRECADA — Reemplazada por commits-real.
  Estructura los commits como unidades de trabajo entregables en vez de
  lotes por tipo de archivo. Trigger: cuando implementás un cambio,
  preparás commits, dividís PRs.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T2-fast
---

# Skill: work-unit-commits

> **⚠️ DEPRECADA**: Esta skill fue reemplazada por
> [`commits-real`](../commits-real/SKILL.md). Todas las reglas de commits,
> voz y documentación están unificadas ahí.
>
> **No cargues esta skill. Cargá `commits-real` en su lugar.**

## Por qué fue reemplazada

El concepto de "work unit commits" era correcto, pero estaba aislado de las
reglas de voz y documentación. `commits-real` integra todo: la misma filosofía
de unidades de trabajo entregables, pero con la voz, el formato y las reglas
de documentación en un solo lugar. No tiene sentido tener tres skills que
hablan de lo mismo.

## Lo que esta skill enseñaba (ahora en commits-real)

| Concepto | Ahora en commits-real |
|----------|----------------------|
| Commit por unidad de trabajo | Sección 2 (Commits) |
| Tests y docs con el código | Sección 2 (Commits): checklist |
| Mensaje explica resultado, no archivos | Sección 2 (Commits): formato |
| PR-ready cada commit | Sección 2 (Commits): split examples |
| SDD workload guard | Sección 5 (Project Rules) |

## Referencia rápida (por si llegás acá por error)

La regla de oro: cada commit es una unidad de trabajo entregable.

```
✅ feat(auth): agregar validación de token JWT
   └── Incluye: modelo + lógica + tests

❌ add models   ← no cuenta una historia
❌ add services
```

Checklist antes de commitear:
- [ ] Un solo propósito claro
- [ ] El repo funciona aplicando solo este commit
- [ ] Tests y docs incluidos si cambia algo relevante
- [ ] Rollback no rompe cosas no relacionadas

Pero todo esto está mejor explicado y con ejemplos en `commits-real`.
