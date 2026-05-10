---
name: engram-memory-system
description: "Skill global de gestión de memoria — clasifica, organiza y decide el mejor sistema de almacenamiento para cada tipo de conocimiento en Engram."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: engram-memory-system

Cargá esta skill cuando estés por guardar o consultar memoria en Engram. Es la skill global que orquesta el sistema de memoria del ecosistema.

## Árbol de clasificación

Antes de guardar, clasificá la memoria usando este árbol:

```
¿Qué tipo de información es?
│
├── decision
│   Elecciones de diseño con tradeoffs documentados
│   → Ej: "Elegimos Zustand sobre Redux porque..."
│   → topic_key: architecture/<area>
│   → scope: project
│
├── architecture
│   Decisiones de alto nivel sobre estructura del sistema
│   → Ej: "Microservicios con API Gateway en lugar de monolito"
│   → topic_key: architecture/<area>
│   → scope: project
│
├── bugfix
│   Bugs encontrados, su causa raíz y cómo se solucionaron
│   → Ej: "FTS5 crashea con caracteres especiales"
│   → topic_key: bugfix/<area>
│   → scope: project
│
├── pattern
│   Patrones reutilizables, convenciones, templates
│   → Ej: "Convención de commits conventional commits"
│   → topic_key: pattern/<area>
│   → scope: project
│
├── config
│   Configuraciones, setup, instalaciones, variables de entorno
│   → Ej: "MCP de Docker necesita PYTHONPATH=x"
│   → topic_key: config/<area>
│   → scope: project
│
├── discovery
│   Gotchas, edge cases, aprendizajes no obvios
│   → Ej: "El paquete X ya no existe en npm, se migró a Y"
│   → topic_key: discovery/<area>
│   → scope: project
│
├── learning
│   Aprendizajes generales sin una categoría específica
│   → Ej: "Cómo funciona el sistema de tiers en model-router"
│   → topic_key: learning/<area>
│   → scope: project
│
├── user_preference
│   Preferencias del usuario, su forma de trabajar, gustos
│   → Ej: "Al usuario no le gustan los emojis en outputs"
│   → topic_key: preference/<area>
│   → scope: personal
│
├── session_summary
│   Resumen completo al finalizar una sesión
│   → Usá mem_session_summary, no mem_save
│   → scope: project
│
└── manual
    Cualquier cosa que no encaje arriba
    → topic_key: auto-generado
    → scope: project
```

## Reglas de scope

| Scope | Cuándo usarlo |
|-------|--------------|
| `project` | Todo lo que sea específico de este proyecto: código, arquitectura, bugs, config, skills |
| `personal` | Preferencias del usuario, forma de trabajar, atajos, gustos personales |

## Reglas de topic_key

Usá topic_key cuando la información evoluciona (se actualiza en el tiempo):

| Situación | topic_key |
|-----------|-----------|
| Decisión de arquitectura que puede cambiar | `architecture/<area>` |
| Bug recurrente en un área | `bugfix/<area>` |
| Patrón que refinamos | `pattern/<area>` |
| Preferencia del usuario | `preference/<area>` |
| Config global | `config/<area>` |
| Un descubrimiento puntual (no evoluciona) | No usar topic_key |

## Cuándo guardar

- ✅ Después de cada decisión significativa (con alternativas documentadas)
- ✅ Al encontrar y corregir un bug (incluir causa raíz)
- ✅ Al finalizar una sesión (usar mem_session_summary)
- ✅ Cuando descubrís algo no obvio (gotcha, edge case)
- ✅ Cuando el usuario expresa una preferencia clara
- ⛔ NO guardar cada comando que ejecutaste
- ⛔ NO guardar trivialidades (instalaciones de paquetes obvias)
- ⛔ NO duplicar info que ya está en el código (para eso está el repo)

## Cuándo consultar

- ✅ Al empezar una sesión → `mem_context` o `mem_search` por proyecto
- ✅ Antes de decisiones de arquitectura → `mem_search "tema"`
- ✅ Cuando un error parece familiar → `mem_search type:bugfix`
- ✅ Cuando no recordás una preferencia del usuario → `mem_search scope:personal`
- ✅ Antes de crear una skill nueva → ver si ya hay patrones similares

## Formato del contenido

Toda entrada usa esta estructura:

```
**What**: [qué se hizo, en una línea]
**Why**: [por qué, qué problema resolvía]
**Where**: [archivos/rutas afectadas]
**Learned**: [gotchas, edge cases, decisiones no obvias — omitir si no aplica]
```

## Flujo completo: antes de guardar

```
1. CLASIFICAR → usar el árbol de clasificación
2. ELEGIR scope → project o personal
3. DECIDIR topic_key → solo si evoluciona
4. REDACTAR → What, Why, Where, Learned
5. GUARDAR → mem_save (o mem_session_summary si es fin de sesión)
```
