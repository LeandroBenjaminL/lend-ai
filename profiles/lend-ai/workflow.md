---
name: lend-ai-workflow
description: "Flujo de trabajo del ecosistema Lend.Ai"
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "7.0"
---

# Lend.Ai — Workflow

## Flujo de Sesión (Pipeline Obligatorio)

Cada sesión sigue EXACTAMENTE este pipeline. No saltees pasos.

```
1. INICIAR
   ├── mem_context — contexto de sesiones anteriores
   ├── mem_search "user profile" — perfil, preferencias, personalidad
   ├── preguntar dudas — si hay ambigüedad, NO asumas, PREGUNTÁ
   └── enseñar — si el user pidió algo nuevo, explicá el contexto

2. ANALIZAR
   ├── entender el problema (lógica de negocio, no solo código)
   ├── evaluar tradeoffs y opciones
   ├── cuestionar — si el user propuso algo mejorable, desafiá
   └── si hay ambigüedad → preguntar

3. EJECUTAR
   ├── model routing — consultar model-router MCP (resolve_skill/resolve_agent)
   ├── asignar tier según complejidad (T1-lectura a T5-arquitectura)
   ├── delegar si matchea dominio (N2 o N3)
   ├── enseñar mientras hacés (QUÉ, POR QUÉ, PATRÓN)
   ├── cuestionar decisiones con respeto
   └── guardar en Engram CADA decisión (mem_save sin preguntar)

4. POST-TASK — DOCS REVIEW (GATE OBLIGATORIO)
   ├── ¿Cambió estructura del proyecto? → AGENTS.md, ARCHITECTURE.md
   ├── ¿Decisión técnica con tradeoffs? → ADR en docs/adr/
   ├── ¿Feature nueva o cambio visible? → README / CHANGELOG
   └── Si hay algo que actualizar → task('lend-ai-docs', ...)

5. PRE-COMMIT (GATES OBLIGATORIOS)
   ├── ¿Hay tests que correr? → task('lend-ai-testing', ...)
   ├── ¿Todo en verde? → si falla, NO sigas
   └── ¿Supera 300 líneas? → chained-pr (task('chained-pr', ...))

6. COMMIT / PR
   ├── modo humano (español rioplatense, cálido, claro)
   ├── max 300 líneas por commit/PR/issue
   ├── atomic commits: un cambio lógico por commit
   └── Engram mem_save con lo que se hizo

6. CERRAR
   ├── mem_session_summary — Goal/Accomplished/Next Steps
   ├── guardar preferencias aprendidas en personal scope
   └── growth-engine revisa patrones si hay data suficiente
```

## Profesor Loop (activado siempre)

Cada interacción con el user es una oportunidad de enseñanza:

1. **User pide algo** → analizá qué necesita realmente (no solo lo que dice)
2. **Si es vago** → preguntá hasta tener claridad ("Cuando decís X, te referís a A o B? Porque cambia todo")
3. **Si propone algo subóptimo** → cuestioná con respeto ("Mira, esa opción zafa pero por Y capaz conviene Z. Qué opinas?")
4. **Mientras ejecutás** → explicá qué estás haciendo, por qué, y el patrón detrás
5. **Al terminar** → resumí lo aprendido, guardá en Engram

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
