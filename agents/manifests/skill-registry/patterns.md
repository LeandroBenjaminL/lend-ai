# Patterns: Skill Registry

> _El registro de skills no es un inventario. Es un sistema de navegación. Cada skill tiene su trigger, sus reglas compactas, y su path._

## Tabla de decisión: qué skills incluir en el registro

| Skill | Incluir? | Razón |
|-------|----------|-------|
| `go-testing` | ✅ Incluir | Skill de coding, necesaria para code review |
| `cognitive-doc-design` | ✅ Incluir | Skill de workflow, necesaria para documentación |
| `sdd-init` | ❌ SKIP | SDD workflow skill (sdd-*) |
| `sdd-design` | ❌ SKIP | SDD workflow skill (sdd-*) |
| `_shared` | ❌ SKIP | Referencia interna, no es skill invocable |
| `skill-registry` | ❌ SKIP | Es esta misma skill |
| `branch-pr` | ✅ Incluir | Skill de workflow |
| `data-analysis` | ✅ Incluir | Skill de dominio de datos |

## Tabla de escaneo: dónde buscar skills

| Prioridad | Ubicación | Nivel | Cómo escanear |
|-----------|-----------|-------|---------------|
| 1 | `{project-root}/skills/` | Project | Glob `*/SKILL.md` |
| 2 | `{project-root}/.claude/skills/` | Project | Glob `*/SKILL.md` |
| 3 | `~/.claude/skills/` | User | Glob `*/SKILL.md` |
| 4 | `~/.config/opencode/skills/` | User | Glob `*/SKILL.md` |
| 5 | `~/.gemini/skills/` | User | Glob `*/SKILL.md` |
| 6 | `~/.cursor/skills/` | User | Glob `*/SKILL.md` |
| 7 | `~/.copilot/skills/` | User | Glob `*/SKILL.md` |

## Tabla de deduplicación

| Escenario | Resolución |
|-----------|------------|
| Misma skill en user-level y project-level | ✅ Gana project-level (más específico al proyecto) |
| Misma skill en dos user-levels | ✅ Gana la primera encontrada (orden de prioridad) |
| Misma skill en dos project-levels | ✅ Gana la que está en `skills/` (específica de skills) |
| Skills con mismo nombre pero distinto propósito | ⚠️ Investigar si es la misma skill renombrada o son distintas |

## Tabla de qué incluir en compact rules vs qué dejar fuera

| Incluir en compact rules ✅ | Dejar fuera ❌ |
|----------------------------|----------------|
| Reglas accionables: "usar table-driven tests" | Propósito o motivación |
| Constraints: "nunca usar t.Fatal en loop" | "When to use" (el delegador ya decidió) |
| Patrones clave con ejemplos de 1 línea | Ejemplos completos de código |
| Gotchas: "los golden files van en testdata/" | Pasos de instalación |
| Preferencias: "preferir interface sobre mock" | Historia de la tecnología |
| Breaking changes: "Go 1.22 cambia loop variables" | Tutoriales extensos |

## Tabla de archivos de convenciones del proyecto

| Archivo | Qué contiene | Prioridad |
|---------|-------------|-----------|
| `AGENTS.md` o `agents.md` | Índice de skills y agentes del proyecto | Alta — puede referenciar otros archivos |
| `CLAUDE.md` | Instrucciones específicas para Claude | Alta |
| `.cursorrules` | Reglas para Cursor | Media |
| `GEMINI.md` | Instrucciones para Gemini | Media |
| `copilot-instructions.md` | Instrucciones para Copilot | Media |

## Anti-patrones del skill registry

| Anti-patrón | Problema | Solución |
|-------------|----------|----------|
| **Compact rules muy largas** | 30+ líneas por skill, el sub-agente no procesa todas | Mantener 5-15 líneas. Destilar a lo esencial. |
| **Compact rules muy cortas** | 1-2 líneas que no dan suficiente guía | Agregar reglas accionables y gotchas |
| **No escanear todos los directorios** | Skills perdidas que nadie sabe que existen | Escanear TODOS los directorios de skills |
| **No deduplicar** | Misma skill aparece dos veces con reglas distintas | Project-level > user-level. Primera encontrada > segunda. |
| **SDD skills incluidas** | `sdd-init`, `sdd-design`, etc. en el registro de coding skills | SKIP todas las `sdd-*` |
| **Saltar el archivo** | Solo guardar a engram, no escribir `.atl/skill-registry.md` | SIEMPRE escribir el archivo. Engram es bonus. |
| **Compact rules con motivación** | "Esta skill sirve para cuando necesitás..." en vez de reglas | Solo reglas. La motivación no la necesita el sub-agente. |
| **No actualizar después de cambios** | Registry desactualizado, skills nuevas no aparecen | Correr después de instalar/remover skills |
| **Referencias web en compact rules** | URLs que pueden morir | Paths locales a archivos del proyecto |

## Checklist de generación de compact rules

Por cada skill encontrada:

- [ ] **Leí el SKILL.md** (hasta 200 líneas; si es más largo, leo frontmatter + Critical Patterns)
- [ ] **Extraje name** del frontmatter
- [ ] **Extraje trigger** de `description` (después de "Trigger:")
- [ ] **Generé compact rules** de 5-15 líneas con SOLO reglas accionables
- [ ] **No incluí** propósito, motivación, when-to-use, ejemplos largos
- [ ] **Incluí gotchas** que causarían bugs si se ignoran
- [ ] **Incluí preferencias** importantes del equipo
- [ ] **Cada línea es accionable** — el sub-agente sabe qué hacer

## Checklist de escritura del registro

- [ ] `.atl/` directory existe
- [ ] `.atl/skill-registry.md` escrito con User Skills table + Compact Rules + Project Conventions
- [ ] Engram persist (si `mem_save` está disponible), con `capture_prompt: false`
- [ ] `.gitignore` tiene `.atl/` (si no estaba)
- [ ] Skills `sdd-*`, `_shared`, y `skill-registry` están excluidas
- [ ] Skills duplicadas están resueltas (project-level gana)
- [ ] Los triggers en la tabla son claros y específicos
- [ ] Las compact rules son concisas y accionables

## Principios fundamentales

1. **El archivo siempre se escribe.** Engram es bonus, no reemplazo. `.atl/skill-registry.md` es la fuente de verdad.
2. **Compact rules es lo único que importa.** El sub-agente no lee el SKILL.md completo — recibe las compact rules pre-resueltas.
3. **5-15 líneas por skill.** Nada más. Si no podés resumir una skill en 15 líneas, la skill está mal diseñada.
4. **Solo reglas accionables.** "Usar table-driven tests", no "los table-driven tests son una buena práctica porque..."
5. **El registro se actualiza con cada cambio de skills.** No es estático. Correlo después de instalar/remover.

> _El registro no es para humanos. Es para que cualquier agente que lance sub-agentes pueda resolver en 0.2 segundos qué skills aplican y qué reglas seguir. Si el registro está incompleto, los sub-agentes van a cometer errores que ya fueron resueltos._
