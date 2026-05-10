---
name: issue-creation
description: >
  Creación de issues en GitHub — bug reports, feature requests y
  tareas con formato y contexto suficiente para actuar.
  Trigger: Cuando creás un issue, reportás un bug, o solicitás una feature.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: issue-creation

Issues que se entienden sin preguntar "¿qué quisiste decir?".

## Trigger

- Encontraste un bug y querés reportarlo
- Querés proponer una feature nueva
- Necesitás dividir un proyecto grande en tareas
- Te asignaron un issue y necesitás entenderlo

## Workflow LEND

1. ANALIZAR
   ├── Tipo: bug, feature, chore, improvement
   ├── Severidad: crítica, mayor, menor, sugerencia
   ├── Contexto: ¿dónde pasa? ¿cómo reproducirlo?
   └── Prioridad: ahora, esta semana, este mes

2. OFRECER (Menú del Senior)
   ├── A) Bug report — pasos para reproducir + comportamiento esperado vs actual + environment
   ├── B) Feature request — descripción + motivación + criterios de aceptación
   └── C) Tarea técnica — contexto + definición de done + subtareas

3. ELEGIR → confirmación

4. HACER
   ├── Bug: título claro, pasos, esperado vs actual, logs/screenshots, ambiente
   ├── Feature: título, descripción, motivación, criterios de aceptación
   ├── Labels: bug, feature, enhancement, good-first-issue
   ├── Assignee: quien lo va a resolver
   ├── Milestone: si aplica (sprint, versión)
   └── Templates: usar issue template del repo si existe

5. VERIFICAR
   ├── El issue tiene toda la información necesaria para arrancar
   ├── Los pasos de reproducción son claros
   └── Los criterios de aceptación son medibles
