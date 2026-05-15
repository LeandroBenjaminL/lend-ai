---
name: engram-memory-system
description: "Skill global de gestión de memoria — clasifica, organiza y decide el mejor sistema de almacenamiento para cada tipo de conocimiento en Engram."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Sistema de Memoria Engram

Cargá esta skill cuando estés por guardar o consultar memoria en Engram.

## ⚠️ REGLA DE ORO

**Guardá SIN PREGUNTAR.** No le preguntes al usuario "¿guardo esto?". Guardalo. Siempre.

Si no estás seguro del proyecto, pensalo 2 segundos. Si aún así no sabés, preguntá. Pero no preguntes "¿lo guardo?", preguntá "¿en qué proyecto?".

## Jerarquía de topic_key (carpetas virtuales)

```
topic_key = <area>/<subarea>
```

| Carpeta | Para qué | Ejemplo |
|---------|----------|---------|
| `architecture/infra` | Servidores, redes, Tailscale, VPNs | `architecture/infra` |
| `architecture/data` | Pipelines, ETL, DB schema | `architecture/data` |
| `architecture/frontend` | Componentes, estado, routing | `architecture/frontend` |
| `architecture/system` | Ecosistema, agentes, skills, SDD | `architecture/system` |
| `architecture/database` | SQL, esquemas, migraciones | `architecture/database` |
| `bugfix/python` | Errores en código Python | `bugfix/python` |
| `bugfix/infra` | Errores de infraestructura | `bugfix/infra` |
| `bugfix/config` | Errores de configuración | `bugfix/config` |
| `bugfix/tool` | Errores de herramientas/MCPs | `bugfix/tool` |
| `pattern/python` | Patrones de Python | `pattern/python` |
| `pattern/git` | Patrones de git y PRs | `pattern/git` |
| `pattern/workflow` | Patrones de flujo de trabajo | `pattern/workflow` |
| `pattern/architecture` | Patrones arquitectónicos | `pattern/architecture` |
| `discovery/tool` | Descubrimientos sobre herramientas | `discovery/tool` |
| `discovery/workflow` | Descubrimientos sobre procesos | `discovery/workflow` |
| `discovery/ecosystem` | Descubrimientos sobre el ecosistema | `discovery/ecosystem` |
| `config/mcp` | Configuraciones de MCPs | `config/mcp` |
| `config/environment` | Variables de entorno, setup | `config/environment` |
| `config/tool` | Configuraciones de herramientas | `config/tool` |
| `config/system` | Config del ecosistema | `config/system` |
| `decision/architecture` | Decisiones arquitectónicas | `decision/architecture` |
| `decision/tool` | Decisiones sobre herramientas | `decision/tool` |
| `decision/workflow` | Decisiones sobre flujo | `decision/workflow` |
| `learning/language` | Aprendizaje de lenguajes | `learning/language` |
| `learning/tool` | Aprendizaje de herramientas | `learning/tool` |
| `learning/domain` | Aprendizaje de dominios | `learning/domain` |
| `preference/workflow` | Cómo le gusta trabajar al usuario | `preference/workflow` |
| `preference/tech-stack` | Tecnologías que prefiere | `preference/tech-stack` |
| `preference/communication` | Cómo le gusta que le hablen | `preference/communication` |
| `preference/general` | Otras preferencias | `preference/general` |

## Guardado automático (sin preguntar)

| Cuándo | type | topic_key | scope |
|--------|------|-----------|-------|
| Cambiaste configuración | `config` | `config/<area>` | project |
| Encontraste y fixeaste un bug | `bugfix` | `bugfix/<area>` | project |
| Tomaste una decisión con tradeoffs | `decision` | `decision/<area>` | project |
| Descubriste algo no obvio | `discovery` | `discovery/<area>` | project |
| Identificaste un patrón reusable | `pattern` | `pattern/<area>` | project |
| Aprendiste algo del usuario | `user_preference` | `preference/<area>` | **personal** |
| Definiste arquitectura | `architecture` | `architecture/<area>` | project |
| Terminaste una sesión | `session_summary` | — | project |
| Aprendizaje general | `learning` | `learning/<area>` | project |

## Perfil del usuario (crece solo)

Cuando descubras algo nuevo del usuario (cómo trabaja, qué prefiere, qué no le gusta):
1. Guardalo como `user_preference` con scope `personal`
2. Usá topic_key `preference/<area>` (ej: `preference/communication`, `preference/tech-stack`)
3. Si ya existe una entrada con ese topic_key, se actualiza sola (upsert)
4. **No preguntes** — guardalo y seguí

## Formato del contenido

```
**What**: [qué pasó, una línea]
**Why**: [por qué, qué problema resolvía]
**Where**: [archivos/componentes afectados, o la fuente del aprendizaje]
**Learned**: [gotchas, edge cases, decisiones no obvias — omitir si no aplica]
```

## Árbol de tipos

```
¿Qué tipo de información es?
│
├── architecture → decisiones de alto nivel sobre estructura
│   → topic_key: architecture/<area>
│   → scope: project
│
├── bugfix → bugs con causa raíz y solución
│   → topic_key: bugfix/<area>
│   → scope: project
│
├── pattern → patrones reutilizables, convenciones
│   → topic_key: pattern/<area>
│   → scope: project
│
├── config → configuraciones, setup, instalaciones
│   → topic_key: config/<area>
│   → scope: project
│
├── discovery → gotchas, edge cases, aprendizajes no obvios
│   → topic_key: discovery/<area>
│   → scope: project
│
├── decision → elecciones con tradeoffs documentados
│   → topic_key: decision/<area>
│   → scope: project
│
├── learning → aprendizajes generales
│   → topic_key: learning/<area>
│   → scope: project
│
├── user_preference → todo sobre el usuario
│   → topic_key: preference/<area>
│   → scope: personal (SIEMPRE)
│
└── session_summary → resumen al finalizar sesión
    → usar mem_session_summary, NO mem_save
    → scope: project
```

## Reglas de scope

| Scope | Cuándo usarlo |
|-------|--------------|
| `project` | Código, arquitectura, bugs, config, skills del proyecto actual |
| `personal` | TODO lo que sea del usuario: preferencias, forma de trabajar, gustos |

## Cuándo NO guardar

- ❌ Cada comando que ejecutaste (no es un log)
- ❌ Trivialidades (instalaciones de paquetes obvias)
- ❌ Info que ya está en el código (para eso está el repo)
- ❌ Lo mismo dos veces (usá topic_key para upsert)

## Cuándo consultar (antes de actuar)

- ✅ Al empezar sesión: `mem_context` o `mem_search`
- ✅ Antes de decisiones importantes: `mem_search "tema"`
- ✅ Cuando un error parece conocido: `mem_search type:bugfix`
- ✅ Cuando no recordás una preferencia: `mem_search scope:personal`
- ✅ Antes de crear algo nuevo: ver si ya hay patrones similares
