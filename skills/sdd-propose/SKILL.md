# Skill: sdd-propose

## Qué es

Crea la propuesta de cambio: el "qué y por qué". Es el contrato inicial entre lo que querés hacer y todo lo que sigue.

**El principio**: una propuesta no es una especificación. Es una declaración de intención que alinea a todos antes de invertir tiempo en specs y diseño.

## Trigger

El orquestador te llama después de exploration (o con input directo del usuario) para formalizar la idea como un change proposal.

## Workflow

### 1. Cargá el contexto
Leé lo que haya de exploration + el project context (`sdd-init/{project}`).

### 2. Creá el change folder (solo openspec/hybrid)
```
openspec/changes/{change-name}/proposal.md
```

### 3. Leé specs existentes
Si `openspec/specs/` tiene specs relevantes, leelos para entender el comportamiento actual que el cambio podría afectar.

### 4. Escribí proposal.md

```markdown
# Proposal: {Change Title}

## Intent
{Qué problema resuelve, por qué es necesario}

## Scope

### In Scope
- {deliverable concreto 1}

### Out of Scope
- {lo que NO estamos haciendo}

## Capabilities ← CONTRATO con sdd-spec

### New Capabilities
- `<name>`: {descripción} → se crea `specs/{name}/spec.md`

### Modified Capabilities
- `<name>`: {lo que cambia} → delta spec en el change folder

## Approach
{approach técnico de alto nivel}

## Risks
| Risk | Likelihood | Mitigation |

## Rollback Plan
{Cómo revertir si algo sale mal}

## Success Criteria
- [ ] {cómo sabemos que funciona}
```

### 5. Persistí
- artifact: `proposal`, topic_key: `sdd/{change-name}/proposal`

### 6. Devolvé summary
**Change**: {name}, **Intent**: {one-liner}, **Risk**: Bajo/Medio/Alto
**Next**: specs (sdd-spec) o design (sdd-design).

## Ejemplos

1. **"Add rate limiting"**: Intent = evitar abuso de API. Scope = middleware de rate limiting por IP. Out of scope = rate limiting por usuario (futuro). Capabilities: new `rate-limiting`.

2. **"Migrar a PostgreSQL"**: Intent = consistencia de datos y mejor tooling. Scope = schema, migraciones, adapter. Out of scope = migración de datos legacy. Rollback = volver al adapter anterior.

3. **"Logging estructurado"**: Intent = reemplazar console.log por structured logging. Scope = logger service, middleware. Capabilities: modified `logging` (cambia formato de output).

## Reglas

- **Siempre** completá la sección Capabilities — es el contrato con sdd-spec
- Investigá `openspec/specs/` primero para usar nombres de capabilities existentes
- New capabilities → spec completo nuevo. Modified → delta spec.
- Si nada cambia a nivel spec (refactor puro, config), escribí "None" explícito
- Máximo 450 words. Bullet points > prosa. Tablas > párrafos.
- Siempre incluí rollback plan y success criteria
- Si el change folder ya existe con proposal, leelo primero y actualizalo (no sobreescribas)

## Anti-patrones

- ❌ **Proposal sin intent claro**: No sabés por qué estás haciendo el cambio
- ❌ **Saltar Capabilities**: Después sdd-spec no sabe qué specs crear
- ❌ **Proposal sin rollback**: Si falla, no tenés plan de salida
- ❌ **Escribir una novela**: 450 words máx — es una thinking tool, no documentación
- ❌ **Scope creeps**: "Ya que estamos, agreguemos..." — out of scope existe por algo
