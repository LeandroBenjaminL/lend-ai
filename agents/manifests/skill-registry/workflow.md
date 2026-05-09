# Workflow: Skill Registry

## Flujo principal

```
Orchestrator → [1. Escanear skills] → [2. Extraer compact rules] → [3. Escanear convenciones] → [4. Construir registro] → [5. Escribir archivo] → [6. Persistir a engram] → [7. Devolver resumen] → Orchestrator
```

## Paso a paso

### 1. Escanear todas las skills disponibles

Barrés TODOS los directorios donde pueden existir skills. No asumís que están en un solo lugar.

**User-level skills (globales):**
```
~/.claude/skills/
~/.config/opencode/skills/
~/.gemini/skills/
~/.cursor/skills/
~/.copilot/skills/
```

**Project-level skills (workspace):**
```
{project-root}/.claude/skills/
{project-root}/.gemini/skills/
{project-root}/.agent/skills/
{project-root}/skills/              <- ruta genérica
```

**Qué escaneás:**
- Glob por `*/SKILL.md` en cada directorio
- Leés el frontmatter de cada SKILL.md para extraer `name` y `description`
- Anotás el path completo de cada skill encontrada

**Qué SKIPEÁS:**
- `sdd-*` — son skills internas del workflow SDD, no son coding/task skills
- `_shared` — son referencias compartidas, no skills invocables
- `skill-registry` — es esta misma skill, no te escaneés a vos mismo

**Deduplicación:**
- Si la misma skill existe en user-level y project-level → project-level gana (más específico)
- Si está en dos user-levels → la primera encontrada
- Misma skill → mismo nombre → mismo propósito → merge a la más específica

_"Si no lo escaneaste, no existe para el registry. Si existe pero no lo encontraste, es igual a que no exista."_

### 2. Extraer compact rules (la parte más importante)

Para cada skill encontrada, generás un bloque de **compact rules** de 5-15 líneas.

**Qué incluir en compact rules:**
- Reglas accionables ("do X", "never Y", "prefer Z over W")
- Constraints importantes
- Patrones clave con ejemplos de una línea
- Breaking changes o gotchas que causarían bugs si se ignoran

**Qué NO incluir:**
- Propósito o motivación
- "When to use" sections
- Ejemplos de código completos
- Pasos de instalación
- Nada que el sub-agente no necesite APLICAR

**Formato por skill:**

```markdown
### {skill-name}
- Regla accionable 1
- Regla accionable 2
- Patrón clave: ejemplo breve
- Gotcha: X causa Y si no se maneja
```

**Ejemplo de compact rules para una skill de Go testing:**

```markdown
### go-testing
- Usar table-driven tests para funciones puras
- Bubbletea: testear state transitions con Model.Update(), renders con golden files
- teatest para flujos completos de TUI
- Golden files en testdata/, flag -update para regenerar
- Mockear con interfaces de 1-2 métodos, no frameworks
- t.TempDir() para archivos temporales
- t.Parallel() para tests independientes
- testing.Short() para skip integración en CI rápido
```

_"Las compact rules son lo único que el sub-agente recibe. Si no son precisas y accionables, el sub-agente va a cometer errores."_

### 3. Escanear convenciones del proyecto

Buscás archivos de convenciones en la raíz del proyecto:

- `agents.md` o `AGENTS.md`
- `CLAUDE.md` (solo project-level, no `~/.claude/CLAUDE.md`)
- `.cursorrules`
- `GEMINI.md`
- `copilot-instructions.md`
- Cualquier otro archivo de instrucciones del proyecto

**Si se encuentra un archivo índice (ej: `AGENTS.md`):**
- Leé su contenido completo
- Extraé TODAS las rutas de archivos referenciadas
- Incluí el archivo índice + todas las rutas referenciadas en el registro

**Si se encuentra un archivo de convenciones standalone (ej: `CLAUDE.md`):**
- Registralo directamente con su path

### 4. Construir el registro markdown

Armás el documento completo con esta estructura:

```markdown
# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| {trigger text} | {skill name} | {full path} |

## Compact Rules

### {skill-name-1}
- Rule 1
- Rule 2

### {skill-name-2}
- Rule 1
- Rule 2

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| {file} | {path} | {description} |
```

**Reglas del formato:**
- La tabla de User Skills tiene Trigger, Skill, Path
- Los Compact Rules están agrupados por skill con headers H3
- Project Conventions lista todos los archivos de convenciones encontrados
- Si no hay skills ni convenciones, igual escribís un registro vacío (para que los delegadores no pierdan tiempo buscando)

### 5. Escribir el archivo .atl/skill-registry.md

**Siempre escribís el archivo**, independientemente de si engram está disponible o no.

```bash
mkdir -p .atl/
# Escribís el contenido del registro en .atl/skill-registry.md
```

El archivo `.atl/skill-registry.md` es la fuente de verdad principal. Está disponible para cualquiera que tenga acceso al filesystem del proyecto.

**Si `.gitignore` existe y `.atl` no está listado:**
Agregás `.atl/` al gitignore. No querés versionar el registro (es generado, no manual).

### 6. Persistir a engram (si está disponible)

Si el sistema `mem_save` está disponible, guardás el registro también a engram:

```
mem_save(
  title: "skill-registry",
  topic_key: "skill-registry",
  type: "config",
  project: "{project}",
  capture_prompt: false,
  content: "{full registry markdown}"
)
```

`capture_prompt: false` porque es un artifact automatizado, no un save humano.

`topic_key: "skill-registry"` asegura que la próxima vez que corras esto, se actualice el mismo registro en vez de crear uno nuevo.

**Dos fuentes, cero pérdida:**
- Filesystem → siempre disponible
- Engram → disponible entre sesiones
- Si engram falla, el archivo está. Si el archivo se pierde, engram lo recupera.

### 7. Devolver resumen al orchestrator

```markdown
## Skill Registry Updated

**Project**: {project name}
**Location**: .atl/skill-registry.md
**Engram**: {saved / not available}

### User Skills Found
| Skill | Trigger |
|-------|---------|
| {name} | {trigger} |

### Project Conventions Found
| File | Path |
|------|------|
| {file} | {path} |

### Next Steps
The orchestrator reads this registry once per session and passes pre-resolved skill paths to sub-agents.
To update after installing/removing skills, run this skill again.
```

### Output final

Tu entregable al orchestrator es:

1. **`.atl/skill-registry.md`** actualizado con todas las skills y compact rules
2. **Engram persist** (si disponible)
3. **Resumen** con skills encontradas, convenciones, y ubicación

_"El registro de skills no es un inventario. Es un mapa de navegación para que cualquier sub-agente sepa exactamente qué reglas aplicar. Si el mapa está incompleto, el sub-agente va a cometer errores que ya fueron resueltos."_
