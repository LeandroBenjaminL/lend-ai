# Skill: sdd-verify

## Qué es

El quality gate del ciclo SDD. Verifica que la implementación sea completa, correcta y cumpla con los specs. Corré tests REALES, no análisis estático nomás.

**El principio**: un spec scenario solo es COMPLIANT cuando hay un test que PASÓ probando ese comportamiento. Que el código exista no es suficiente.

## Trigger

El orquestador te llama después de sdd-apply para verificar el cambio antes de archivar.

## Workflow

### 1. Determiná modo TDD
```
Leé testing capabilities:
├── strict_tdd: true + test runner → STRICT TDD MODE
│   Cargá skills/sdd-verify/strict-tdd-verify.md (steps extra)
├── strict_tdd: false o sin test runner → STANDARD VERIFY
│   (no cargues strict-tdd-verify.md — cero tokens)
└── El orquestador puede inyectar "STRICT TDD MODE IS ACTIVE" → autoritativo
```

### 2. Checkeá completitud
```
Leé tasks.md → tasks totales vs completadas [x]
├── CRITICAL si core tasks incompletas
└── WARNING si cleanup tasks incompletas
```

### 3. Checkeá correctitud (specs match)
```
POR CADA REQUIREMENT en specs/:
  Buscá evidencia en el código
  POR CADA SCENARIO:
  ├── GIVEN precondition → ¿manejado en código?
  ├── WHEN action → ¿implementado?
  ├── THEN outcome → ¿producido?
  └── Edge cases → ¿cubiertos?
```
Esto es análisis estático. La validación real con ejecución viene en Step 6.

### 4. Checkeá coherencia (design match)
```
POR CADA DECISION en design.md:
├── ¿Se usó el approach elegido?
├── ¿Se implementaron alternatives descartadas?
├── ¿Los file changes coinciden?
└── WARNING si hay desviación (puede ser mejora válida)
```

### 5. Checkeá testing

#### 5a. Análisis estático de tests
¿Existen tests por cada spec scenario? Happy paths, edge cases, error states.

#### 5b. Ejecutá tests (OBLIGATORIO)
```
Detectá test runner → ejecutalo → capturá:
├── Total, passed, failed, skipped
├── Exit code
└── CRITICAL si exit code != 0
```

#### 5c. Build & type check
```
Detectá build command:
├── Si falla → CRITICAL
├── Type errors → WARNING
└── Si no hay → WARNING (skip)
```

#### 5d. Coverage (si disponible)
Si hay coverage tool: ejecutalo. Reportá total %. Strict TDD: per-file coverage.

### 6. Spec Compliance Matrix (la validación más importante)

Cruzando CADA escenario de specs contra los resultados de tests:

| Resultado | Significado |
|-----------|-------------|
| ✅ COMPLIANT | Test existe y pasó |
| ❌ FAILING | Test existe pero falló (CRITICAL) |
| ❌ UNTESTED | No hay test (CRITICAL) |
| ⚠️ PARTIAL | Test pasa pero cubre parcialmente (WARNING) |

Un escenario solo es COMPLIANT si hay un test PASADO que lo prueba.

### 7. Persistí verify report
- artifact: `verify-report`, topic_key: `sdd/{change-name}/verify-report`

### 8. Devolvé summary

```markdown
## Verification Report
**Mode**: {Strict TDD | Standard}

### Completeness
| Tasks total | Complete | Incomplete |
|-------------|----------|------------|
| {N} | {N} | {N} |

### Build & Tests
**Build**: ✅ Passed / ❌ Failed
**Tests**: ✅ {N} passed / ❌ {N} failed / ⚠️ {N} skipped
**Coverage**: {N}% (threshold: {N}%)

### Spec Compliance Matrix
| Requirement | Scenario | Test | Result |
|-------------|----------|------|--------|
| REQ-01 | Happy path | `test.test()` | ✅ COMPLIANT |
| REQ-02 | Edge case | (none) | ❌ UNTESTED |

**Compliance**: {N}/{total} scenarios compliant

### Correctness (Static)
| Req | Status | Notes |

### Coherence (Design)
| Decision | Followed? | Notes |

### Issues
**CRITICAL**: {lista — must fix before archive}
**WARNING**: {lista — should fix}
**SUGGESTION**: {lista — nice to have}

### Verdict
{PASS / PASS WITH WARNINGS / FAIL}
```

## Reglas

- **Siempre** leé código fuente real — no te fíes de summaries
- **Siempre** ejecutá tests — análisis estático solo no alcanza
- Spec scenario COMPLIANT solo con test PASADO
- Primero contra SPECS (correctitud de comportamiento), después contra DESIGN (correctitud estructural)
- Sé objetivo — reportá lo QUE ES, no lo que debería ser
- CRITICAL → must fix before archive. WARNING → should fix. SUGGESTION → nice to have.
- **NO arregles issues** — solo reportalos. El orquestador decide.
- Si Strict TDD activo: `strict-tdd-verify.md` es OBLIGATORIO. Si no: ni lo leas.
- Usá cached testing capabilities de Engram/config — no redetectar cada vez.

## Anti-patrones

- ❌ **Verificar sin ejecutar tests**: "Parece que funciona" no es verification
- ❌ **Dar COMPLIANT sin test passed**: El código existe pero nadie probó que funcione
- ❌ **Aceptar CRITICAL issues**: Si algo falla, no se archiva — no lo dejés pasar
- ❌ **Fixear durante verify**: No es tu trabajo — reportá y devolvé la pelota
- ❌ **Saltarse la Spec Compliance Matrix**: Es el corazón del verify — sin eso no sabés si cumplís
