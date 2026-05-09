# Workflow: Skill Creator

## Flujo principal

```
Orchestrator → [1. Diagnosticar necesidad] → [2. Diseñar skill] → [3. Escribir SKILL.md] → [4. Agregar assets/references] → [5. Verificar completitud] → [6. Registrar] → Orchestrator
```

## Paso a paso

### 1. Diagnosticar si realmente se necesita una skill

Antes de escribir UNA línea, evaluás si la skill es necesaria.

**Preguntas de diagnóstico:**

- **¿Es un patrón recurrente?** Si el equipo se encuentra con esto una vez al año, no es una skill. Si es semanalmente, sí.
- **¿Ya está documentado?** Si existe documentación clara, referenciála en vez de crear una skill nueva.
- **¿Es conocimiento tácito?** Las skills son mejores para capturar conocimiento que el equipo sabe pero no está escrito.
- **¿La IA se beneficiaría?** Si sin la skill la IA comete errores consistentes, es una skill necesaria.
- **¿Es un one-off?** Si es para una tarea única, no crees una skill.

**Cuándo NO crear una skill:**
- Ya existe documentación completa (creá una referencia)
- El patrón es trivial o auto-explicativo
- Es una tarea de una sola vez
- Es un concepto demasiado específico de un proyecto que cambia semanalmente

_"Una skill no es un wiki. Si la IA puede resolverlo sin ayuda, no necesita una skill. Si el equipo nunca tuvo este problema, no necesita una skill para prevenirlo."_

### 2. Diseñar la skill: estructura, trigger y contenido crítico

Con la necesidad confirmada, diseñás la skill antes de escribir.

**Definir el trigger (lo más importante):**
El trigger define CUÁNDO la IA carga la skill. Debe ser preciso.

- Buen trigger: "Cuando escribís tests en Go, usás teatest, o agregás cobertura de tests"
- Mal trigger: "Testing" (demasiado vago, no especifica lenguaje ni contexto)
- Buen trigger: "Cuando creás un issue, reportás un bug, o solicitás una feature en GitHub"
- Mal trigger: "Issues" (no especifica plataforma ni acción)

**Estructura de directorios:**

```
skills/{skill-name}/
├── SKILL.md              # Requerido — archivo principal
├── assets/               # Opcional — templates, schemas, ejemplos
│   ├── template.py
│   └── schema.json
└── references/           # Opcional — links a documentación local
    └── docs.md
```

**Decisión assets/ vs references/:**
- ¿Code templates? → `assets/`
- ¿JSON schemas? → `assets/`
- ¿Example configs? → `assets/`
- ¿Link a docs existentes? → `references/`
- ¿Link a guías externas? → `references/` (con path local)

### 3. Escribir el SKILL.md

El SKILL.md sigue el template estándar:

```markdown
---
name: {skill-name}
description: >
  {Descripción one-line de lo que hace la skill}.
  Trigger: {Cuándo cargar esta skill}.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
  model_tier: {T2-fast | T3-balanced | T4-reasoning}
  allowed-tools: {tools if needed}
---

## When to Use

- {bullet 1: cuándo usar esta skill}
- {bullet 2}
- {bullet 3}

## Critical Patterns

{Las reglas más importantes — tablas de decisión, constraints, patrones clave}
{La IA DEBE saber esto para no cometer errores}

## Code Examples

{Ejemplos mínimos y enfocados}
{Cada ejemplo resuelve UN problema específico}

## Commands

```bash
{comandos comunes que la IA necesita ejecutar}
```

## Resources

- **Templates**: See [assets/](assets/) for {desc}
- **Documentation**: See [references/](references/) for {desc}
```

**Frontmatter fields:**

| Field | Requerido | Descripción |
|-------|-----------|-------------|
| `name` | Sí | Identifier (lowercase, hyphens) |
| `description` | Sí | What + Trigger en un solo bloque |
| `license` | Sí | Siempre `Apache-2.0` |
| `metadata.author` | Sí | `gentleman-programming` |
| `metadata.version` | Sí | Semantic version |
| `metadata.model_tier` | Recomendado | T2-fast, T3-balanced, T4-reasoning |

**Reglas de contenido:**

| Hacer | NO hacer |
|-------|----------|
| Empezar con los patrones más críticos | Agregar sección Keywords (el agente busca en frontmatter, no en body) |
| Usar tablas para árboles de decisión | Duplicar contenido de docs existentes (referenciar) |
| Mantener ejemplos mínimos y enfocados | Incluir explicaciones largas |
| Incluir Commands section | Agregar troubleshooting sections |
| Cada línea debe ser accionable | Hacer re-referencia a web URLs (usar paths locales) |

**Model tier selection:**

| Tier |Uso | Ejemplos |
|------|-----|----------|
| T2-fast | Skills simples, workflows cortos, triggers frecuentes | comment-writer, branch-pr, issue-creation |
| T3-balanced | Skills con patrones y ejemplos de código | cognitive-doc-design, go-testing, skill-creator |
| T4-reasoning | Skills complejas con múltiples pasos y decisiones | judgment-day |

### 4. Agregar assets y references (si aplica)

**Assets:** Archivos que la IA necesita leer o usar como template.

```
skills/{skill-name}/assets/
├── template.py        # Template de código
├── schema.json        # Schema de validación
└── config.example.yaml  # Config de ejemplo
```

**References:** Links a documentación existente dentro del proyecto.

```markdown
# References

- **API Docs**: See [docs/api/developer-guide.mdx](../../docs/api/developer-guide.mdx)
- **Architecture**: See [docs/architecture/overview.md](../../docs/architecture/overview.md)
```

**Regla:** Siempre paths LOCALES, no URLs. Si la documentación está en una URL, descargala o referenciá localmente.

### 5. Verificar completitud

Checklist pre-registro:

- [ ] La skill no existe ya en `skills/`
- [ ] El patrón es recurrente (no one-off)
- [ ] El nombre sigue las convenciones (`{tecnología}`, `{proyecto}-{componente}`, `{acción}-{target}`)
- [ ] El frontmatter está completo (name, description con trigger, license, author, version)
- [ ] Los Critical Patterns son claros y accionables
- [ ] Los code examples son mínimos (resuelven UN problema)
- [ ] Commands section existe con comandos copiables
- [ ] assets/ o references/ existen si hacen falta
- [ ] Estructura de directorios correcta

### 6. Registrar la skill en AGENTS.md

Después de crear la skill, la registrás en `AGENTS.md` (o el archivo de índice de skills del proyecto):

```markdown
| `{skill-name}` | {Descripción} | [SKILL.md](skills/{skill-name}/SKILL.md) |
```

Además, si el proyecto tiene un sistema de skill registry (`.atl/skill-registry.md`), corrés `skill-registry` para que lo actualice.

### Output final

Tu entregable al orchestrator es:

1. **Estructura de directorios** creada
2. **SKILL.md** completo con frontmatter, patrones, ejemplos y comandos
3. **Assets/references** si aplican
4. **Registro actualizado** en AGENTS.md y skill registry

_"Una skill no es documentación. Es una instrucción just-in-time. Si la IA tiene que leer 100 líneas para encontrar lo que necesita, la skill está mal diseñada."_
