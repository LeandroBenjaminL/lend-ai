---
description: Router activo de modelos — elegí el tier según tarea, agente o skill
agent: data-analyst
subtask: true
model_router: mcp-servers/model-router.py
---

# 🎯 Router de Modelos

Este comando selecciona ACTIVAMENTE qué modelo usar según el contexto.

## Modos de uso

### `/models` — Mostrar estado actual
Mostrá el tier activo, el modelo actual y los disponibles.

### `/models skill <skill_name>` — Elegir modelo para una skill
Ej: `/models skill ml-modeling` → seleccioná T4 (DeepSeek Pro)

### `/models agent <agent_name>` — Elegir modelo para un sub-agente
Ej: `/models agent data-cleaning` → seleccioná T1 (Minimax Free)

### `/models tier <T1-T5>` — Forzar un tier
Ej: `/models tier T4` → forza DeepSeek Pro para la próxima tarea

### `/models list` — Listar todo el mapping
Mostrá las tablas completas de tiers, agentes y skills

## Lógica de selección automática

Cuando el usuario invoca un comando o carga una skill, USÁ esta lógica:

1. **Si se cargó una skill** → consultá su `model_tier` en la metadata
2. **Si se invocó un sub-agente** → consultá `models.json` → `llm_models.sub_agents[].tier`
3. **Si es tarea del día a día** → T3 (DeepSeek Medium)
4. **Si no hay match** → T3 por defecto

SKILLS A CARGAR: cognitive-doc-design

REGLAS:
- El tier elegido aplica SOLO para la conversación actual
- Mostrá siempre: "🟡 Usando T3 (DeepSeek Medium)" como feedback
- Si el usuario no especifica, usá la lógica automática de arriba

### set-tier

/models set-tier <T1|T2|T3|T4|T5>

Cambia el modelo activo para la conversación actual.
Ejecuta: python3 mcp-servers/model-router.py set-tier <TIER>

/models set-tier default

Vuelve al tier por defecto (T3).

## Implementación activa

Al ejecutar /models set-tier <T1-T5>, ejecutá:
  python3 mcp-servers/model-router.py set-tier <TIER>

Al ejecutar /models, mostrá:
  - El tier activo (python3 mcp-servers/model-router.py get-tier)
  - El mapping completo (python3 mcp-servers/model-router.py list)
