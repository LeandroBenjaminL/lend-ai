---
name: sdd-apply
description: >
  Implementa tareas del cambio siguiendo los specs (QUÉ), el diseño (CÓMO)
  y las tasks (ORDEN). Cada línea responde a un requirement.
  Trigger: Para implementar una o más tareas específicas de un cambio.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-apply

Implementación. Cada línea de código responde a un spec.

## Trigger

- Las tareas están definidas y ordenadas
- El diseño está aprobado
- Tenés claras las dependencias entre tareas

## Workflow LEND

1. ANALIZAR
   ├── Tarea actual: ¿qué dice la task que hay que hacer?
   ├── Spec: ¿qué escenario estamos implementando?
   ├── Diseño: ¿qué archivos tocar? ¿cómo?
   └── Tests: ¿cómo voy a verificar esto después?

2. OFRECER (Menú del Senior)
   ├── A) Implementar tarea por tarea — una task a la vez, test al final
   ├── B) TDD — escribir test primero, después la implementación
   └── C) Implementar + test — código y test en simultáneo

3. ELEGIR → confirmación

4. HACER
   ├── Seguir los specs al pie de la letra
   ├── Implementar según el diseño acordado
   ├── Una tarea a la vez, verificar antes de pasar a la siguiente
   ├── Commits atómicos por tarea
   └── Si encontrás algo no previsto en los specs → parar y preguntar

5. VERIFICAR
   ├── La tarea implementada cumple su criterio de done
   ├── Los tests pasan
   └── El código sigue las convenciones del proyecto
