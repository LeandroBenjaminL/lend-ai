---
name: lend-ai-delegation
description: >
  Reglas de delegación del ecosistema — árbol de decisión, triggers
  de delegación automática y mecanismo con task() + agent-router MCP.
  Trigger: Cuando necesitás decidir a qué sub-agente delegar una tarea.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# LEND.AI — Delegation Protocol

Regla de oro: Si matchea dominio, DELEGÁ. No ejecutes vos.

## Árbol de Delegación

| Dominio | Sub-agente | task() call |
|---------|-----------|-------------|
| Data/ML/ETL/EDA/Reportes | data-analyst | `task('data-analyst', '...')` |
| Frontend/React/CSS/UX/TS | frontend-senior | `task('frontend-senior', '...')` |
| Infra/CI/CD/Docker/Cloud/Seguridad | devops | `task('devops', '...')` |
| Git/PRs/Commits/Issues | commits-real | `task('commits-real', '...')` |
| Memoria/Engram | engram-keeper | `task('engram-keeper', '...')` |
| Testing/Calidad | lend-ai-testing | `task('lend-ai-testing', '...')` |
| Docs/Documentación | lend-ai-docs | `task('lend-ai-docs', '...')` |
| Auto-mejora/Patrones | growth-engine | `task('growth-engine', '...')` |
| Mejora paralela (10 perspectivas) | enhance-engine | `task('enhance-engine', '...')` |
| Contenido/LinkedIn | content-engine | `task('content-engine', '...')` |
| SDD (cualquier fase) | sdd-init..sdd-archive | `task('sdd-<fase>', '...')` |
| Revisión adversarial | judgment-day | `task('judgment-day', '...')` |
| PRs encadenados (>400 líneas) | chained-pr | `task('chained-pr', '...')` |
| Creación de issues | issue-creation | `task('issue-creation', '...')` |
| Branch + PR workflow | branch-pr | `task('branch-pr', '...')` |

## Triggers de Delegación Automática

No preguntes — delegá directamente cuando:

1. **4-file rule**: la tarea requiere leer 4+ archivos → delegá exploración
2. **Multi-file write**: tocar 2+ archivos → delegá writer
3. **Pre-commit/PR**: antes de commit o PR tras cambios → delegá review fresco
4. **Error de entorno**: error de MCP o dependencia → delegá auditoría
5. **Long-session**: ~20 tool calls sin delegar → delegá a growth-engine
6. **Fresh review**: revisión adversarial → judgment-day

## Mecanismo

- Usá `task('agent-name', instructions)` para spawnear sub-agentes
- Pasá instrucciones claras: qué hacer, archivos involucrados, contexto relevante
- Si no sabés qué agente: llamá `resolve_task(descripción)` del MCP agent-router
- Esperá el resultado del sub-agente antes de continuar
- Nunca ejecutes trabajo de dominio directamente

## Post-delegación

- Recibí el resultado del sub-agente
- Verificá que completó lo pedido
- Guardá en Engram: qué se delegó, a quién, resultado
- Si el resultado necesita iteración, re-delegá
