---
name: lend-ai-engram
description: >
  Gestión de memoria del ecosistema — guarda, consulta y organiza
  información en Engram para mantener contexto permanente entre sesiones.
  Trigger: Al guardar o consultar memoria en Engram.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: lend-ai-engram

Memoria del ecosistema. Si no está en engram, no pasó.

## Trigger

- Terminaste una decisión importante
- Encontraste y corregiste un bug
- El usuario expresó una preferencia
- Vas a empezar una tarea y necesitás contexto previo
- Finalizás una sesión

## Workflow LEND

1. ANALIZAR
   ├── ¿Qué pasó? decisión, bug, descubrimiento, preferencia, o fin de sesión
   ├── ¿Es project-scope o personal-scope? (preferencias del usuario → personal)
   ├── ¿Evoluciona en el tiempo? (topic_key sí) o es puntual (topic_key no)
   └── ¿Ya hay info similar en engram? consultar antes de guardar

2. OFRECER (Menú del Senior)
   ├── A) Guardar — mem_save con What/Why/Where/Learned
   ├── B) Consultar — mem_search por proyecto o tipo
   └── C) Resumen de sesión — mem_session_summary al finalizar

3. ELEGIR → confirmación

4. HACER
   ├── Formato: **What**, **Why**, **Where**, **Learned**
   ├── Tipo: decision, bugfix, pattern, architecture, config, discovery, learning
   ├── topic_key: solo si evoluciona (architecture/x, bugfix/x, pattern/x)
   ├── scope: project para código/arquitectura, personal para preferencias
   └── Al final de sesión: mem_session_summary con Goal/Accomplished/Next Steps

5. VERIFICAR
   ├── La entrada es clara y útil para el futuro
   ├── No duplica información existente
   └── El tipo y scope son correctos
