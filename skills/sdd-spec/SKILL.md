# Skill: sdd-spec

## Qué es

Escribe las especificaciones técnicas: requisitos y escenarios en formato Given/When/Then. Describe QUÉ debe hacer el sistema, no CÓMO.

**El principio**: los specs son el contrato verificable. Si podés escribir un test a partir de un escenario, el spec está bien. Si no, es ambiguo.

## Trigger

El orquestador te llama después de sdd-propose para escribir o actualizar los specs del cambio.

## Workflow

### 1. Leé el proposal (obligatorio)
La sección **Capabilities** del proposal es tu contrato primario:
- **New Capabilities** → spec completo nuevo en `specs/{name}/spec.md`
- **Modified Capabilities** → delta spec en `changes/{change-name}/specs/{name}/spec.md`

### 2. Leé specs existentes
Si hay specs previos para los domains afectados, leelos. Tus delta specs describen CAMBIOS sobre ese comportamiento actual.

### 3. Escribí los specs

**Para NEW capabilities** (spec completo):
```markdown
# {Domain} Specification

## Purpose
{Descripción de alto nivel}

## Requirements
### Requirement: {Name}
The system {MUST/SHALL/SHOULD} {behavior}.

#### Scenario: {Name}
- GIVEN {precondition}
- WHEN {action}
- THEN {outcome}
```

**Para MODIFIED capabilities** (delta spec):
```markdown
# Delta for {Domain}

## ADDED Requirements
### Requirement: {Name}
{MUST/SHOULD description}
#### Scenario: {Happy path}
- GIVEN {precondition} - WHEN {action} - THEN {outcome}

## MODIFIED Requirements
### Requirement: {Existing Name}
{Full updated text — COPIA COMPLETA del requirement existente + editado}
(Previously: {one-line summary of change})

## REMOVED Requirements
### Requirement: {Name}
(Reason: {por qué se elimina})
```

### 4. Persistí los specs
- `specs/{domain}/spec.md` para nuevas capabilities
- `changes/{change-name}/specs/{domain}/spec.md` para deltas
- Engram: un solo artifact concatenado con domain headers: `sdd/{change-name}/spec`

### 5. Devolvé summary

```markdown
## Specs Created
**Change**: {name}
| Domain | Type | Requirements | Scenarios |
|--------|------|-------------|-----------|
| {domain} | Delta/New | {N added, M modified} | {total} |

### Next Step
Design (sdd-design) o Tasks (sdd-tasks) si design ya existe.
```

## Ejemplos

1. **Spec nuevo para rate-limiting**: New capability. Requirement: "Rate limit by IP". Scenario happy: 100 requests/min from same IP → 429 on 101st. Scenario edge: different IPs → no limit.

2. **Delta spec para modificar auth**: Modified capability `user-auth`. Requirement "Session expires in 24h" → "Session expires in 1h". MODIFIED: copiás el requirement completo + todos los escenarios, editás el tiempo.

3. **Spec con REMOVED**: Remover feature de "login con SMS". REMOVED Requirements con la razón: "se reemplaza por 2FA app-based".

## Reglas

- **Siempre** Given/When/Then
- **Siempre** RFC 2119: MUST/SHALL/SHOULD/MAY
- **MODIFIED requirements: copiá el bloque COMPLETO** (requirement + todos los escenarios). Si copiás solo lo que cambia, el archive pierde escenarios.
- Cada requirement ≥ 1 scenario (happy path + edge cases idealmente)
- Escenarios TESTEABLES — alguien tiene que poder escribir un test automatizado de cada uno
- **Sin implementation details** — specs describen WHAT, no HOW
- Máximo 650 words. Tablas > narrativa. Escenarios: 3-5 líneas cada uno.
- Si agregás comportamiento sin cambiar existente → usá ADDED, no MODIFIED

## Anti-patrones

- ❌ **Specs sin escenarios**: Son wishful thinking, no contratos verificables
- ❌ **Implementation details en specs**: "Usar JWT con RS256" es diseño, no spec
- ❌ **MODIFIED partial**: Copiás solo el escenario que cambia y perdés los otros en el archive
- ❌ **No leer specs existentes**: Escribís un delta que contradice el comportamiento actual
- ❌ **Scenarios no testeables**: "El sistema debería ser rápido" no es testeable; "responde en <200ms" sí
