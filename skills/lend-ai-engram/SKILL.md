---
name: lend-ai-engram
description: >
  Gestión de memoria del ecosistema — guarda, consulta y organiza
  información en Engram para mantener contexto permanente entre sesiones.
  Trigger: Al guardar o consultar memoria en Engram. AUTO-SAVE sin preguntar.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
---

# Skill: lend-ai-engram

Memoria del ecosistema. Si no está en engram, no pasó.

## Regla de ORO

**Guardá SIN PREGUNTAR.** No preguntes "¿guardo esto?". Guardalo. Siempre.
Usá topic_key para que se actualice solo si ya existe.

## Triggers de auto-save (sin preguntar)

| Cuándo | type | topic_key | scope |
|--------|------|-----------|-------|
| Cambiaste configuración | `config` | `config/<area>` | project |
| Encontraste y fixeaste un bug | `bugfix` | `bugfix/<area>` | project |
| Tomaste una decisión con tradeoffs | `decision` | `decision/<area>` | project |
| Descubriste algo no obvio | `discovery` | `discovery/<area>` | project |
| Identificaste un patrón reusable | `pattern` | `pattern/<area>` | project |
| El user dijo algo sobre cómo trabaja | `user_preference` | `preference/<area>` | personal |
| Definiste arquitectura | `architecture` | `architecture/<area>` | project |
| Terminaste una sesión | `session_summary` | — | project |
| Aprendizaje general | `learning` | `learning/<area>` | project |
| El user expresó una preferencia/estilo | `user_preference` | `preference/<area>` | personal |

## Workflow LEND (modo auto-save, sin menú)

1. DETECTAR
   ├── ¿Pasó algo relevante? (ver triggers arriba)
   ├── ¿Es project o personal?
   └── ¿Tiene topic_key para upsert?

2. GUARDAR (sin preguntar — directo)
   ├── Formato: **What**, **Why**, **Where**, **Learned**
   ├── Tipo: decision, bugfix, pattern, architecture, config, discovery, learning, user_preference
   ├── topic_key: siempre que evolucione en el tiempo
   └── scope: project para código/arquitectura, personal para preferencias del user

3. AL FINAL DE SESIÓN (no preguntar)
   ├── mem_session_summary con Goal/Accomplished/Next Steps/Relevant Files
   └── Guardar preferencias aprendidas durante la sesión

4. VERIFICACIÓN RÁPIDA
   ├── ¿Quedó guardado? sí → seguí
   └── ¿Hay conflicto? → mem_judge automático si confianza > 0.7, si no → preguntar
