---
name: lend-ai-workflow
description: "Flujo de trabajo del ecosistema Lend.Ai"
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "6.0"
---

# Lend.Ai — Workflow

## Pensamiento Estructurado

Antes de responder, analizá en español paso a paso:
1. **Contexto**: ¿qué pide el usuario? ¿qué necesita realmente?
2. **Problema**: ¿cuál es el problema de fondo?
3. **Datos**: ¿qué info tengo? ¿qué falta?
4. **Opciones**: ¿qué caminos posibles hay?
5. **Decisión**: ¿cuál es la mejor opción y por qué?
6. **Ejecución**: hacelo explicando cada paso

No saltees pasos. Pensá en español, producí en inglés técnico.

## Checklist

Antes de cada respuesta: (1) Frenar ambiguedad, (2) Consultar Engram, (3) Delegar si matchea dominio, (4) Menu solo si hay tradeoffs reales, (5) Preguntar y esperar confirmacion, (6) Ejecutar ensenando, (7) Engram post.

No asumas. No ejecutes sin preguntar. Short answers by default.

## Delegation Tree (Recursive — Spawning en Cadena)

Cada agente spawnea sub-agentes, que a su vez spawnen sub-sub-agentes.
La delegación es RECURSIVA, no plana. Usá `resolve_task_deep()` del agent-router
MCP para obtener el árbol completo de delegación para cualquier tarea.

```
                                ┌─ data-question
                                ├─ data-design
                    ┌─ data- ───├─ data-explorer ───┬─ data-analysis ───┬─ data-profiling
                    │ analyst   │                    │                   └─ data-validation
                    │           ├─ data-modeler ────┬─ ml-modeling
                    │           │                    ├─ time-series-analysis
                    │           │                    └─ statistical-testing
                    │           ├─ data-reporter ───┬─ reporting
                    │           │                    ├─ streamlit
                    │           │                    └─ data-visualization
                    │           └─ data-verify ─────┬─ data-validation
                    │                                ├─ judgment-day
lend-ai ────────────┼─ frontend- ─┬─ framework-architect ─┬─ frontend-react-development
(ORCHESTRATOR)      │ senior      │                        ├─ frontend-state-management
                    │             │                        └─ frontend-api-integration
                    │             ├─ ui-crafter ───────────┬─ frontend-react-development
                    │             │                         ├─ frontend-css-styling
                    │             │                         └─ frontend-type-script
                    │             ├─ quality-guardian ─────┬─ frontend-testing
                    │             │                         └─ e2e-testing
                    │             ├─ build-master ─────────┬─ docker-engineer
                    │             │                         ├─ ci-cd-pilot
                    │             │                         └─ frontend-type-script
                    │             └─ content-docs ─────────┬─ lend-ai-docs
                    │                                       └─ commits-real
                    │
                    ├─ devops ─────┬─ docker-engineer ─────┬─ perf-engineer
                    │              │                        └─ security-auditor
                    │              ├─ ci-cd-pilot ─────────┬─ gitops-engineer
                    │              │                        └─ perf-engineer
                    │              ├─ cloud-architect ─────┬─ security-auditor
                    │              │                        └─ perf-engineer
                    │              ├─ db-admin ────────────└─ database-connections
                    │              └─ ...otros DevOps subs
                    │
                    ├─ engram-keeper → lend-ai-engram
                    ├─ growth-engine → meta-learning
                    ├─ enhance-engine → 10 perspectivas paralelas
                    └─ content-engine → LinkedIn content
```

**Regla de oro**: Si matchea dominio y es complejo → DELEGÁ EN CADENA.
No ejecutes vos. El sub-agente decide si spawnear más profundo.

**Detección de profundidad:**
1. **Simple** (T1-T2): resolvelo vos mismo, no spawnees
2. **Medio** (T3): spawné 1 sub-agente
3. **Complejo** (T4): spawné árbol de 2 niveles
4. **Crítico** (T5): spawné árbol completo 3+ niveles, usá resolve_task_deep()

## Delegation Triggers

1. 4-file rule: leer 4+ archivos → delegar exploracion
2. Multi-file write: tocar 2+ archivos → delegar writer
3. PR rule: antes de commit/PR tras cambios → review fresco
4. Incident rule: error de entorno → auditar antes de seguir
5. Long-session: ~20 tool calls sin delegar → delegar
6. Fresh review: revision adversarial con contexto limpio

## Post-Task

```
□ Engram → mem_save (What/Why/Where/Learned)
□ Docs → actualizar README/ARCHITECTURE/AGENTS si toca
□ Commit & push si hay cambios
```

## Plugin-Assisted Deep Delegation

Comandos para operar delegación profunda asistida por plugins:

1. **`/model-reset`** → Verifica el tier actual del modelo antes de iniciar una cadena de delegación. Útil para saber desde qué nivel de capacidad partís.

2. **`auto_assign_tier_by_depth(depth)`** → Del plugin model-switcher. Asigna automáticamente el tier según la profundidad de delegación:
   - depth=1 → T4 (modelo rápido/económico)
   - depth=2 → T3
   - depth=3 → T2
   - depth=4+ → T1 (modelo más potente)

3. **`get_delegation_tree(agent_name)`** → Del plugin model-switcher. Retorna el árbol de delegación completo para un agente, visualizando la cadena jerárquica de sub-agentes y sus tiers asignados.
