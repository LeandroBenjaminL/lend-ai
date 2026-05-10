---
name: sdd-tasks
description: >
  Divide el cambio en tareas concretas, ordenadas por dependencia y
  agrupadas por fase. Cada tarea es accionable y verificable.
  Trigger: Después de sdd-design para desglosar el cambio en tareas.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-tasks

Desglose en tareas. Cada tarea se completa en una sesión.

## Trigger

- El diseño está aprobado
- Necesitás dividir el trabajo en pasos accionables
- Varias personas van a trabajar en paralelo

## Workflow LEND

1. ANALIZAR
   ├── Diseño: ¿qué archivos tocar? ¿en qué orden?
   ├── Dependencias: ¿qué tareas bloquean a otras?
   ├── Tamaño: cada tarea < 1 sesión de trabajo
   └── Fases: preparación, implementación, tests, documentación

2. OFRECER (Menú del Senior)
   ├── A) Tareas lineales — secuencia de pasos, una atrás de otra
   ├── B) Tareas con dependencias — árbol de tareas con bloqueos
   └── C) Tareas paralelizables — múltiples tracks independientes

3. ELEGIR → confirmación

4. HACER
   ├── Cada tarea: título + descripción + archivos afectados + criterio de done
   ├── Orden: por dependencias (primero lo que bloquea a lo demás)
   ├── Tamaño: cada tarea completable en < 1 hora de código
   ├── Formato: "Implementar X en archivo Y haciendo Z"
   └── Checklist: al completar, marcar y pasar a la siguiente

5. VERIFICAR
   ├── Todas las tareas juntas cubren el diseño completo
   ├── No hay tareas que dependan de sí mismas
   └── Cada tarea tiene un criterio de "done" claro
