---
name: senior-orchestrator
description: >
  Orquestación profesional del ecosistema — modelo routing, delegación
  de agentes, arquitectura y decisiones técnicas.
  Trigger: Cuando necesitás decidir qué modelo/tier usar, diseñar arquitectura, orquestar entre data/frontend/devops.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
---

# Skill: senior-orchestrator

Orquestación del ecosistema. Decidí qué agente, qué modelo, qué camino.

## Trigger

- Decidir qué modelo/tier usar para una tarea
- Diseñar arquitectura del ecosistema
- Delegar entre data-analyst, frontend-senior y devops
- Planear estrategia de modelos (local vs cloud)
- Configurar CI/CD, seguridad o infraestructura

## Workflow LEND

1. ANALIZAR
   ├── Tipo de tarea: data, frontend, devops, o transversal
   ├── Complejidad: mecánica, estándar, compleja, crítica
   ├── Contexto: consultar Engram por decisiones previas
   ├── Consultar agent-router MCP: resolve_task() si hay duda
   └── Presupuesto: ¿usar modelos gratis o pagos?

2. DELEGAR (no preguntes — ejecutá)
   ├── Data/ML/ETL → task('data-analyst', instrucciones)
   ├── Frontend/React/CSS → task('frontend-senior', instrucciones)
   ├── Infra/CI/CD/Cloud → task('devops', instrucciones)
   ├── Git/PRs/Commits → task('commits-real', instrucciones)
   ├── Memoria/Engram → task('engram-keeper', instrucciones)
   ├── SDD → task('sdd-<fase>', instrucciones)
   ├── Si hay ambigüedad → agent-router MCP resolve_task()
   └── Solo transversal: ejecutá vos mismo

3. HACER (el sub-agente ejecuta)
   ├── Pasá instrucciones claras al task()
   ├── Esperá el resultado del sub-agente
   ├── Verificá que completó lo pedido
   └── Registrá en Engram: qué se delegó, a quién, resultado

4. ITERAR si es necesario
   ├── ¿Resultado correcto? → seguí
   ├── ¿Necesita ajustes? → re-delegá con feedback
   └── ¿Error? → diagnosticá y re-delegá

## Deep Delegation (Recursive Spawning)

**Nuevo: resolve_task_deep()** — Usá esta herramienta del agent-router MCP
para resolver tareas con árbol de delegación completo (3+ niveles de profundidad).

### Flujo de delegación profunda

```
Tarea compleja
  → resolve_task_deep("descripción", max_depth=3)
    → Devuelve árbol: agente → sub-agentes → sub-sub-agentes
  → Spawneá el agente raíz con instrucciones
    → El agente spawnea sub-agentes según la dificultad
      → Los sub-agentes spawnean más sub-agentes si es necesario
```

### Reglas de profundidad por capa

| Layer | Rol | Puede spawnear |
|-------|-----|----------------|
| 0 | Orquestador (lend-ai) | Layer 0.5: data-analyst, frontend-senior, devops |
| 0.5 | Domain supervisors | Layer 1: data-explorer, data-modeler, docker-engineer |
| 1 | Especialistas | Layer 2: data-analysis, ml-modeling, perf-engineer |
| 2+ | Deep specialists | Layer 3: data-profiling, data-validation, statistical-testing |

**Regla**: Si un agente tiene `sub_agents` en su manifest YAML y la
sub-tarea es lo suficientemente compleja → DEBE delegar. No ejecutar directamente.

## Patrones

- **Delegar siempre, preguntar solo en ambigüedad**
- **Usá siempre cuatro herramientas**: task() para sub-agentes, resolve_task() si hay duda, resolve_task_deep() para árbol completo, agent-router MCP para routing
- **Siempre delegá profundo**: si una tarea es compleja, no la resuelvas vos. Spawneá el árbol completo.
- **Nunca cambiar model-routing.config.json sin registrar en Engram**
- **Cada cambio arquitectónico requiere ADR**
- **MCPs se diagnostican antes de usar**
- **Engram siempre**: toda decisión técnica se persiste

## Anti-patrones

- ❌ Delegar sin consultar Engram primero — perdés contexto de decisiones previas
- ❌ Cambiar tiers sin registrar — nadie sabe por qué se usó T5 en una tarea simple
- ❌ No diagnosticar MCPs antes de usarlos — "esto no funciona" a mitad de camino
- ❌ Ignorar al usuario cuando es vago — preguntá hasta tener especificaciones claras
