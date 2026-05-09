---
name: skill-registry
description: >
  Crea o actualiza el registro de skills del proyecto: escanea skills,
  escribe .atl/skill-registry.md y guarda en engram. Trigger: "update skills",
  "skill registry", "actualizar skills", o después de instalar/remover skills.
license: MIT
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T2-fast
---

# Skill: skill-registry

Generar el catálogo de skills con reglas compactas que los delegadores
inyectan directamente en prompts de sub-agentes.

## Trigger

- Instalaste o removiste skills.
- Seteaste un proyecto nuevo.
- El usuario pidió actualizar el registro.
- `sdd-init` lo llama automáticamente.

## Por qué existe

Los sub-agentes no deberían leer SKILL.md enteros en cada delegación. Sería
caro y lento. El registry se construye UNA VEZ (caro) y se lee barato en cada
delegación. Los sub-agentes reciben solo las **compact rules** (5-15 líneas
por skill) pre-resueltas en su prompt de lanzamiento.

## Workflow

### 1. Escaneá skills de usuario

Buscá `*/SKILL.md` en todos estos directorios (los que existan):

```
~/.claude/skills/        # Claude Code
~/.config/opencode/skills/  # OpenCode
~/.gemini/skills/        # Gemini CLI
~/.cursor/skills/        # Cursor
~/.copilot/skills/       # VS Code Copilot
{project-root}/.claude/skills/
{project-root}/skills/
```

**SKIP**: `sdd-*`, `_shared`, `skill-registry`.

**Deduplicá**: si mismo nombre en varios lados, priorizá project-level.

### 2. Generá compact rules (5-15 líneas por skill)

De cada SKILL.md extraé SOLO:
- Reglas accionables ("hacé X", "nunca Y", "preferí Z sobre W")
- Patrones clave con ejemplos de una línea
- Breaking changes que causarían bugs si se ignoran

**NO incluyas**: propósito, motivación, cuándo-usar, ejemplos completos,
pasos de instalación. Solo lo que el sub-agente necesita para APLICAR la skill.

```markdown
### react-19
- No useMemo/useCallback — React Compiler maneja memoización
- use() para promises/context, reemplaza useEffect en data fetching
- Server Components por defecto; 'use client' solo para interactividad
```

### 3. Escaneá convenciones del proyecto

Buscá: `AGENTS.md`, `CLAUDE.md` (project-level), `.cursorrules`, `GEMINI.md`.
Si encontrás un archivo índice (como `AGENTS.md`), leélo y extraé TODAS las
rutas que referencia. Incluí el índice Y las rutas en la tabla.

### 4. Escribí el registry

```
.atl/skill-registry.md
```

```markdown
# Skill Registry
**Delegator use only.** Sub-agents NO leen esto. Reciben compact rules inyectadas.

## User Skills
| Trigger | Skill | Path |

## Compact Rules
### {skill-name}
- Rule 1
- Rule 2

## Project Conventions
| File | Path | Notes |
```

### 5. Persistí también en engram

```python
mem_save(title="skill-registry", topic_key="skill-registry",
         type="config", project="{project}", capture_prompt=False,
         content="{registry markdown}")
```

## Patrones

- **Siempre escribí `.atl/skill-registry.md`** — es el source of truth, no depende de engram.
- **Compact rules concisas**: el valor está en la precisión, no en la cantidad.
- **Deduplicación**: project-level gana contra user-level.
- **Agregá `.atl/` al `.gitignore`** si existe y no está ya.

## Anti-patrones

- Poner propósito o motivación en compact rules — el sub-agente no necesita saber por qué,
  necesita saber qué hacer.
- Escanear solo un directorio — cada tool usa una ruta distinta.
- Saltarse el paso de engram — la memoria cross-session es clave para que el agente
  no pierda el registry entre sesiones.
- Compact rules de 30 líneas — si una skill necesita tanto, está mal diseñada.
