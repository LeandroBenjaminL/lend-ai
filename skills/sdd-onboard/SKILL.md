# Skill: sdd-onboard

## Qué es

Guía al usuario por un ciclo SDD completo de principio a fin, usando su codebase real. Es aprender haciendo — no un tutorial teórico.

**El principio**: la mejor forma de aprender SDD es hacer un cambio real. El onboard busca algo chico, real y valioso en el proyecto del usuario, y recorre todas las fases.

## Trigger

El orquestador te llama para hacer onboarding de un usuario nuevo en el ciclo SDD.

## Workflow

### Fase 1: Bienvenida + Codebase Scan
Saludá, explicá que van a hacer un ciclo completo. Escaneá el codebase buscando una mejora real pero chica:

```
Criterios:
├── Scope chico (30-60 min)
├── Bajo riesgo (no breaking changes)
├── Valor real (no un juguete)
├── Spec-worthy (≥1 requirement, ≥2 scenarios)
└── Ejemplos: validación faltante, error inconsistente, utility extractable, TODO claro
```

Presentá 2-3 opciones. Dejá que el usuario elija.

### Fase 2: Explore (narrado)
```"Antes de comprometernos, investigamos el código."```
Investigate el área elegida. Explicá en lenguaje simple qué encontraste y qué hay que cambiar.

### Fase 3: Propose (narrado)
```"Escribimos QUÉ vamos a construir y POR QUÉ."```
Creá el change folder y proposal.md. Mostráselo al usuario — preguntá si quiere ajustar algo.

**Punto de pausa obligatorio**: esperá review del usuario antes de seguir.

### Fase 4: Specs (narrado)
```"Definimos QUÉ debe hacer el sistema, en términos testeables."```
Escribí delta specs con Given/When/Then. Explicá que cada escenario es un caso de test potencial.

### Fase 5: Design (narrado)
```"Decidimos CÓMO construirlo. Decisiones, rationale, archivos."```
Escribí design.md. Mostrá las decisiones clave y por qué se eligieron.

### Fase 6: Tasks (narrado)
```"Dividimos el trabajo en pasos concretos y verificables."```
Escribí tasks.md. Explicá que cada task debe ser específica y completable.

### Fase 7: Apply (narrado)
```"Ahora código de verdad. Tasks guían, specs dicen qué es 'done'."```
Implementá las tasks. Narrá cada una al completarla. Si TDD activo: explicá RED→GREEN→REFACTOR.

### Fase 8: Verify (narrado)
```"Verificamos que lo construido coincide con lo especificado."```
Corré tests, armá la compliance matrix. Mostrá qué scenarios pasaron y cuáles no.

### Fase 9: Archive (narrado)
```"Mergeamos delta specs a main specs y cerramos el cambio."```
Archivá el cambio. Mostrá dónde quedó el audit trail.

### Fase 10: Summary

```markdown
## Onboarding Complete!

**Change**: {name}
**Artifacts**: proposal (WHY), spec (WHAT), design (HOW), tasks (STEPS)
**Files changed**: {lista}

**The SDD cycle**: explore → propose → spec → design → tasks → apply → verify → archive

**When to SDD**: Features, APIs, architecture decisions → SDD first.
Small tweaks → just code.
```

## Ejemplos

1. **Onboarding con proyecto Express**: Encontrás un TODO de validación de email. Proponés crearlo como util. Ciclo completo en 45 min. El usuario ve todo el flujo SDD con código real.

2. **Onboarding con proyecto Python**: Error inconsistente en mensajes de error. Proponés centralizar en un módulo `errors.py`. Duración: 30 min. Ideal para primera vez.

3. **Onboarding con proyecto Go**: Falta middleware de logging. Proponés agregarlo siguiendo el patrón existente. Duración: 60 min. Muestra value real.

## Reglas

- **Cambio REAL** — no demo. Artifacts y código deben ser production-quality.
- Cada fase narrada: 1-3 oraciones. Enseñá, no des la cátedra.
- **Pausá después de Phase 3 (proposal)** — el usuario necesita revisar antes de seguir.
- Si el usuario propone su propio cambio, validá que cumpla "chico y seguro".
- Si algo bloquea (tests fallan, diseño poco claro, codebase complejo) → STOP y explicá.
- Adaptá el tono: usuario experimentado → menos explicación; nuevo → más contexto.
- Seguí los formatos de cada skill individual.

## Anti-patrones

- ❌ **Usar un ejemplo de juguete**: "Hagamos una calculadora" no sirve — no es el codebase real
- ❌ **No pausar en proposal**: El usuario necesita ver el contrato antes de seguir invirtiendo
- ❌ **Dar cátedra**: 3 oraciones por fase, no 10. El código enseña mejor que las palabras
- ❌ **Saltar fases**: "Esta vez no hacemos design" — el ciclo está diseñado completo por una razón
- ❌ **Ignorar blockers**: Si verify falla, no archives — enseñá por qué falla y cómo arreglarlo
