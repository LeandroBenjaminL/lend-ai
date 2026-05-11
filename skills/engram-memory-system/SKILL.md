---
name: engram-memory-system
description: >
  Skill global de gestión de memoria — clasifica, organiza y decide el
  mejor sistema de almacenamiento para cada tipo de conocimiento en Engram.
  Trigger: Al clasificar, organizar, guardar o consultar memoria en Engram.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: engram-memory-system

Sistema global de memoria. Clasificá, guardá y consultá con criterio.

## Trigger

- Vas a guardar una decisión, bug o aprendizaje
- Necesitás consultar contexto previo antes de arrancar
- Finalizás una sesión y hay que cerrar el ciclo
- El usuario expresó una preferencia o workflow

## Workflow LEND

1. ANALIZAR
   ├── Tipo: decision, bugfix, pattern, architecture, config, discovery, learning, user_preference, session_summary
   ├── Scope: ¿project (código/arquitectura) o personal (preferencias del usuario)?
   ├── Evolución: ¿esto va a cambiar en el tiempo? → topic_key sí. ¿Es puntual? → topic_key no
   └── Contexto: consultar si ya hay info similar antes de guardar

2. OFRECER (Menú del Senior)
   ├── A) Guardar — mem_save con What/Why/Where/Learned
   ├── B) Consultar — mem_search por proyecto, tipo o keyword
   └── C) Resumen de sesión — mem_session_summary al finalizar

3. ELEGIR → confirmación

4. HACER
   ├── Formato: **What**, **Why**, **Where**, **Learned**
   ├── Tipo según árbol de clasificación
   ├── topic_key: architecture/*, pattern/*, bugfix/*, config/*, preference/*
   ├── scope: project (default) o personal (preferencias)
   └── session_summary: al final de cada sesión con Goal/Accomplished/Next Steps

5. VERIFICAR
   ├── La entrada es clara y útil para el futuro
   ├── No duplica información existente
   └── Está accesible desde búsquedas futuras

## Árbol de clasificación

| Tipo | Cuándo | topic_key |
|------|--------|-----------|
| decision | Elecciones de diseño con tradeoffs | architecture/<area> |
| architecture | Decisiones de alto nivel del sistema | architecture/<area> |
| bugfix | Bugs, causa raíz y solución | bugfix/<area> |
| pattern | Patrones y convenciones reutilizables | pattern/<area> |
| config | Setup, instalaciones, variables | config/<area> |
| discovery | Gotchas, edge cases, aprendizajes | discovery/<area> |
| user_preference | Preferencias del usuario (scope personal) | preference/<area> |
| session_summary | Resumen al finalizar sesión | — |

## Patrones

- **Consultar antes de guardar**: no duplicar información
- **topic_key solo si evoluciona**: si es puntual, no usar topic_key
- **scope personal**: preferencias del usuario, su forma de trabajar
- **session_summary al final**: cierra el ciclo y deja contexto para la próxima

## Anti-patrones

- ❌ Guardar cada comando ejecutado — es ruido, no memoria
- ❌ Guardar trivialidades — no duplicar info que ya está en el código
- ❌ No consultar antes de decidir — Engram existe para mantener contexto
- ❌ Tipo incorrecto — un bugfix no es una decision
