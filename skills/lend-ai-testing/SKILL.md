---
name: lend-ai-testing
description: >
  Testing y calidad de código — tests unitarios, CI, cobertura, y
  estándares de calidad del ecosistema.
  Trigger: Al escribir tests, configurar CI, o revisar calidad de código.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: lend-ai-testing

Calidad de código. Tests que duelen cuando fallan, no cuando los escribís.

## Trigger

- Terminaste de escribir código y necesitás testearlo
- Vas a configurar o modificar el CI
- Querés medir cobertura o mejorarla
- Un test existente falla y hay que debuggearlo

## Workflow LEND

1. ANALIZAR
   ├── Stack: pytest, vitest, go test?
   ├── Tipo: unitario, integración, E2E?
   ├── Cobertura actual: ¿está configurada? ¿mínimo aceptable?
   └── CI: ¿ya hay pipeline? ¿corre en cada PR?

2. OFRECER (Menú del Senior)
   ├── A) Tests unitarios — pytest + coverage para funciones críticas
   ├── B) Integración — tests que cruzan módulos, API real o mockeada
   └── C) Suite completa — unit + integración + CI pipeline en GitHub Actions

3. ELEGIR → confirmación

4. HACER
   ├── pytest: test_*.py, assert, fixtures, parametrize
   ├── Cobertura: pytest --cov, mínimo 80% en líneas críticas
   ├── CI: workflow que corre tests + lint + coverage report
   ├── Tests aislados: cada test independiente, sin estado compartido
   └── Nombres descriptivos: test_cuando_condicion_entonces_resultado

5. VERIFICAR
   ├── pytest pasa sin errores
   ├── Cobertura cumple el mínimo
   └── CI corre automáticamente en cada PR
