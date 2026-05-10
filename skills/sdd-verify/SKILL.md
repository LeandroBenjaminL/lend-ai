---
name: sdd-verify
description: >
  Quality gate del ciclo SDD. Verifica que la implementación sea completa,
  correcta y cumpla los specs. Tests REALES, no análisis estático.
  Trigger: Después de sdd-apply para verificar el cambio antes de archivar.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-verify

Verificación SDD. Un spec solo está cumplido cuando hay un test que pasó.

## Trigger

- La implementación está completa
- Antes de archivar el cambio
- El orquestador pide validación antes de mergear

## Workflow LEND

1. ANALIZAR
   ├── Specs: ¿qué escenarios dijimos que íbamos a cumplir?
   ├── Implementación: ¿qué se hizo realmente?
   ├── Tests: ¿cada escenario tiene un test que pasa?
   └── Gaps: ¿hay algo que no se implementó o no funciona?

2. OFRECER (Menú del Senior)
   ├── A) Auto-verify — correr tests existentes, verificar contra specs
   ├── B) Review cruzado — que otro agente (judgment-day) revise código y tests
   └── C) Verificación completa — tests + review + validación manual de escenarios

3. ELEGIR → confirmación

4. HACER
   ├── Correr test suite completo
   ├── Verificar cada escenario de los specs contra la implementación
   ├── Si hay escenarios sin test → crearlos
   ├── Si hay tests que fallan → diagnosticar y corregir
   ├── Documentar: scenarios PASS/FAIL, cobertura, issues encontrados
   └── Decidir: ¿aprobado, aprobado con warnings, o rechazado?

5. VERIFICAR
   ├── Todos los escenarios critical tienen test que pasa
   ├── No hay regresiones (tests que antes pasaban y ahora no)
   └── El reporte de verificación está documentado
