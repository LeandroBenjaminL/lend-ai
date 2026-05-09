# Skill: sdd-design

## Qué es

Traduce los specs (el QUÉ) en un plan técnico concreto (el CÓMO). Documenta decisiones de arquitectura, data flow, y cambios de archivos.

**El principio**: el diseño captura el razonamiento. No es solo "qué archivos tocar", sino "por qué esta solución y no otra". El próximo dev (o vos en 3 meses) necesita entender las decisiones.

## Trigger

El orquestador te llama después de sdd-spec (o en paralelo si los specs ya están claros) para diseñar la implementación.

## Workflow

### 1. Leé proposal + specs
Entendé qué hay que construir y qué comportamiento se espera.

### 2. Leé el codebase real
Antes de diseñar, leé el código que se va a afectar:
- Entry points y estructura de módulos
- Patrones existentes (cómo se hacen cosas similares)
- Interfaces y dependencias
- Testing infrastructure

### 3. Escribí design.md

```markdown
# Design: {Change Title}

## Technical Approach
{Strategy general. Cómo mapea al approach del proposal?}

## Architecture Decisions
### Decision: {Title}
**Choice**: {lo que elegimos}
**Alternatives**: {lo que descartamos}
**Rationale**: {por qué esto y no lo otro}

## Data Flow
{Diagrama ASCII si aplica}
    Component A ──→ Component B

## File Changes
| File | Action | Description |
|------|--------|-------------|
| `path/to/new.go` | Create | {qué hace} |
| `path/to/existing.ts` | Modify | {qué cambia y por qué} |

## Interfaces / Contracts
{Definiciones de tipos, interfaces, API contracts. Code blocks con el lenguaje del proyecto.}

## Testing Strategy
| Layer | What | How |
|-------|------|-----|

## Migration / Rollout
{Si aplica: feature flags, migraciones, rollout por fases. Si no: "No migration required".}

## Open Questions
- [ ] {preguntas técnicas sin resolver}
```

### 4. Persistí
- artifact: `design`, topic_key: `sdd/{change-name}/design`

### 5. Devolvé summary

```markdown
## Design Created
**Approach**: {one-liner}
**Key Decisions**: {N}
**Files**: {N new, M modified}
**Testing**: {unit/integration/e2e coverage planned}
**Next**: Tasks (sdd-tasks)
```

## Ejemplos

1. **Diseño de rate-limiting**: Middleware pattern (como el auth middleware existente). Decision: en memoria vs Redis → Redis por persistencia. File changes: `middleware/rate-limiter.go` Create, `server/routes.go` Modify.

2. **Diseño de logging estructurado**: Reemplazar console.log por winston (Node). Decision: winston vs pino → pino (más rápido, ya es依存). File changes: `src/lib/logger.ts` Create, migrate calls gradualmente.

3. **Diseño de migración PostgreSQL**: Nuevo adapter + repository pattern. Decision: raw SQL vs ORM → Prisma (el proyecto ya lo usa). Migration: script de hasta con data seed.

## Reglas

- **Siempre** leé el codebase real antes de diseñar — no adivinés
- Cada decisión necesita rationale (el "por qué")
- Usá paths de archivos CONCRETOS, no descripciones abstractas
- Seguí los patrones EXISTENTES del proyecto, aunque no sean los que recomendarías
- Diagramas ASCII simples > diagramas bonitos
- Si tenés open questions que BLOQUEAN el diseño, decilo claro
- Máximo 800 words. Decisiones de arquitectura como tablas (opción | trade-off | decisión). Code snippets solo para patrones no obvios.
- Si encontrás que el codebase usa un patrón distinto al que recomendarías, NOTALO pero SEGUÍ el patrón existente a menos que el cambio lo modifique explícitamente

## Anti-patrones

- ❌ **Diseñar sin leer el código**: Garantizado que vas a proponer algo que no encaja
- ❌ **Decisiones sin rationale**: "Usamos Redis porque sí" no sirve; "Usamos Redis porque necesitamos persistencia y ya está en el stack" sí
- ❌ **Sobreingeniería**: Diseñar para escenarios que los specs no piden
- ❌ **Paths abstractos**: "El archivo de auth" vs "internal/auth/middleware.go" — el segundo es el que sirve
- ❌ **Saltar testing strategy**: Si no decís cómo se testea, después verify no tiene contra qué comparar
