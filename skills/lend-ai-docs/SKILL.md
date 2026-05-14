---
name: lend-ai-docs
description: >
  Documentación senior — multi-archivo, Google-style docstrings, ADR,
  y documentación técnica en inglés.
  Trigger: Al escribir documentación, generar docstrings, o estructurar la documentación de un proyecto.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: lend-ai-docs

Documentación senior. Código sin docs es deuda técnica.

## Trigger

- Terminaste una función y necesitás su docstring
- Vas a crear o actualizar un README, ARCHITECTURE, o CHANGELOG
- Necesitás documentar una decisión de arquitectura (ADR)
- El proyecto no tiene documentación y hay que arrancarla

## Workflow LEND

1. ANALIZAR
   ├── Tipo: docstring (API pública), README (proyecto), ADR (decisión), guía (cómo usar)
   ├── Audiencia: ¿desarrollador, usuario, operador?
   ├── Estado: ¿docs desde cero o actualizar existentes?
   └── Lenguaje: inglés técnico US para código y commits

2. OFRECER (Menú del Senior)
   ├── A) Docstrings — Google-style para funciones y clases públicas
   ├── B) README + ARCHITECTURE — visión general del proyecto + estructura
   └── C) ADR — documentar decisión con contexto, opciones y resultado

3. ELEGIR → confirmación

4. HACER
   ├── Google-style: Args, Returns, Raises, Examples (cuando aplica)
   ├── README: qué hace, cómo instalar, cómo usar, configuración
   ├── ARCHITECTURE: estructura, agentes, skills, decisiones técnicas
   ├── ADR: título, contexto, opciones, decisión, consecuencias
   └── Inglés técnico US, claro y directo

5. VERIFICAR
    ├── La documentación es útil sin leer el código
    ├── Los ejemplos funcionan (ejecutables)
    └── No hay información desactualizada

## Cognitive Load Patterns (diseñar docs que reduzcan carga mental)

| Patrón | Regla |
|--------|-------|
| **Lead with answer** | Empezá con el outcome, no con el viaje. El lector necesita saber YA qué resuelve esto. |
| **Progressive disclosure** | Mostrá lo esencial primero. Detalles y edge cases después, colapsados o linkeados. |
| **Chunking** | Agrupá en secciones de 3-5 ítems. Nadie procesa una pared de texto. |
| **Signposting** | Cada sección anticipa qué vas a encontrar. "Esto cubre: instalación, configuración, primeros pasos." |
| **Recognition over recall** | No hagas que el lector recuerde info de 3 secciones atrás. Repetí o linkeá. |
| **Review empathy** | Diseñá para el que revisa tu PR: qué leer primero, qué está out of scope, cómo llegaste acá. |

## Default doc shape

```
# Outcome Title (lo que se logra, no lo que se hace)

## Quick path (2-3 pasos para el 80% de los casos)

## Details table (para el 20% que necesita más)

| Qué | Cómo | Cuándo |
|-----|------|--------|
| ... | ...  | ...    |

## Checklist (accionable, con checkboxes)

- [ ] Step 1
- [ ] Step 2

## Next step (una sola acción clara)
```

## PR review doc guidelines

- **What to review first**: los archivos de alto impacto, con justificación
- **What's out of scope**: lo que NO está en este PR (no hagas adivinar al reviewer)
- **Chain context**: si esto es parte de una cadena de PRs, linkealos
- **Test plan**: qué se testeó manualmente y qué automáticamente
