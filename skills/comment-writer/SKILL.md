---
name: comment-writer
description: >
  ⚠️ DEPRECADA — Reemplazada por commits-real.
  Escribir comentarios humanos, cálidos y directos en español rioplatense
  para PRs, issues, reviews y chats. Trigger: cuando escribís feedback,
  comentarios de review, mensajes en Slack/Discord.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T2-fast
---

# Skill: comment-writer

> **⚠️ DEPRECADA**: Esta skill fue reemplazada por
> [`commits-real`](../commits-real/SKILL.md). Todas las reglas de voz,
> comentarios y documentación están unificadas ahí.
>
> **No cargues esta skill. Cargá `commits-real` en su lugar.**

## Por qué fue reemplazada

Escribir comentarios, commits y documentación con voces distintas no tiene
sentido. Es la misma persona escribiendo. `commits-real` unifica todo con
una sola voz: rioplatense, directa, sin vueltas. Esta skill duplicaba las
reglas de voz que ahora están centralizadas.

## Lo que esta skill enseñaba (ahora en commits-real)

| Regla | Ahora en commits-real |
|-------|----------------------|
| Ser útil rápido | Sección 1 (Tu voz): "Directo al grano" |
| Ser cálido y directo | Sección 1 (Tu voz): español rioplatense |
| Explicar el por qué | Sección 2 (Commits): formato de mensajes |
| Sin em dashes | Sección 1 (Tu voz): sin em dashes |
| Match del lenguaje del thread | Sección 1 (Tu voz): español rioplatense |

## Referencia rápida (por si llegás acá por error)

Si necesitás escribir un comentario ahora:

```
<Observación o pedido directo>

<Por qué importa, solo si es necesario>

<Próxima acción concreta>
```

Ejemplo:
```markdown
Buenísimo el enfoque. Acá separaría este cambio en otro commit porque
mezcla validación con wiring de UI. Así el rollback es más limpio si
falla la integración.
```

Pero todo esto está mejor explicado en `commits-real`.
