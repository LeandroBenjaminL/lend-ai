# Skill: sdd-init

## Qué es

Inicializa SDD en un proyecto: detecta stack, testing capabilities, convenciones, y configura el backend de persistencia.

**El principio**: sin init bien hecho, todas las fases siguientes operan a ciegas. Es la base del ciclo SDD.

## Trigger

El orquestador te llama al arrancar SDD en un proyecto nuevo, o cuando alguien dice "sdd init" / "iniciar sdd".

## Modos de persistencia

| Modo | Qué hace | Para qué |
|------|----------|----------|
| `engram` | Persiste artifacts en Engram (memoria persistente) | Solo dev, fast iteration. Sin `openspec/` dir |
| `openspec` | Crea `openspec/` con archivos en disco | Equipos, git-friendly, audit trail completo |
| `hybrid` | Ambos: Engram + openspec | Lo mejor de ambos mundos |
| `none` | Solo detecta contexto, no persiste nada | Sesiones efímeras, exploración |

## Workflow

### 1. Detectá el proyecto
```
Stack: package.json, go.mod, pyproject.toml, Cargo.toml, etc.
Convenciones: linters, test frameworks, CI, formatters
Arquitectura: patrones en uso (MVC, hexagonal, etc.)
```

### 2. Detectá testing capabilities (OBLIGATORIO)
```
Test Runner: {vitest/jest/pytest/go test/cargo test} o NOT FOUND
Test Layers: Unit, Integration, E2E → {AVAILABLE/NOT INSTALLED}
Coverage: {command} o NOT AVAILABLE
Quality: linter, type checker, formatter
```

### 3. Resolvé Strict TDD Mode
```
1. System prompt / agent config → "strict-tdd-mode" marker
2. openspec/config.yaml → strict_tdd field
3. Default: true SI hay test runner, false si no
NO preguntes al usuario interactivamente.
```

### 4. Inicializá backend (openspec mode)
```
openspec/
├── config.yaml   ← project config + testing capabilities
├── specs/        ← fuente de verdad (vacío inicialmente)
└── changes/
    └── archive/  ← cambios completados
```

### 5. Generá config.yaml
```yaml
schema: spec-driven
context: |
  Stack: {detected}
  Testing: {detected framework}
  Strict TDD: {true/false}
rules:
  proposal: [Include rollback plan, Identify affected modules]
  specs: [Use Given/When/Then, Use RFC 2119]
  design: [Include sequence diagrams, Document rationale]
  tasks: [Group by phase, Hierarchical numbering]
  apply: [Follow existing patterns, Load relevant skills]
  verify: [Run tests, Compare against every scenario]
  archive: [Warn before destructive merges]
```

### 6. Persistí testing capabilities (OBLIGATORIO)
Como observation separada: `sdd/{project}/testing-capabilities`. Esto evita redes cubrir en cada sdd-apply/verify.

### 7. Construí skill registry
Escribí `.atl/skill-registry.md` + Engram si está disponible.

### 8. Devolvé summary estructurado

```markdown
## SDD Initialized
**Project**: {name}
**Stack**: {detected}
**Persistence**: {mode}
**Strict TDD**: {enabled/disabled/unavailable}

### Testing Capabilities
| Capability | Status |
|------------|--------|
| Test Runner | {tool} ✅ / ❌ |
| Unit/Integration/E2E | ✅ / ❌ |
| Coverage | ✅ / ❌ |
| Linter | {tool} ✅ / ❌ |

### Next Steps
Ready for /sdd-explore <topic> or /sdd-new <change-name>.
```

## Ejemplos

1. **Init en proyecto Node/Express**: package.json → vitest + supertest. Testing: unit ✅, integration ✅. Strict TDD: true. Modo openspec.

2. **Init en proyecto Go**: go.mod → go test built-in. Coverage: go test -cover. Strict TDD: true. Modo engram (solo dev).

3. **Init en proyecto Python sin tests**: pyproject.toml, no pytest. Strict TDD: false. Modo none (exploración efímera).

## Reglas

- **NUNCA** crees placeholder spec files — los specs los crea sdd-spec
- **SIEMPRE** detectá testing capabilities — no es opcional
- Siempre persistí testing capabilities como observation separada
- Si Strict TDD se pide pero no hay test runner → false + explicá por qué
- Mode engram: no crees `openspec/` directory
- Config.yaml: máx 10 líneas de context

## Anti-patrones

- ❌ **No detectar testing**: Las fases apply/verify necesitan saber con qué testear
- ❌ **Config enormes**: El context tiene que ser conciso (≤10 líneas)
- ❌ **Preguntar al usuario**: El mode y strict_tdd se resuelven de config, no interactivamente — no hay con quién hablar
- ❌ **Saltear skill registry**: Skills no cargadas = apply sin contexto
