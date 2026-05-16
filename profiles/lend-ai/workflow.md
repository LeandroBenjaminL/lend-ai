---
name: lend-ai-workflow
description: "Flujo de trabajo del ecosistema Lend.Ai"
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "6.0"
---

# Lend.Ai — Workflow

## Checklist

Antes de cada respuesta: (1) Frenar ambiguedad, (2) Consultar Engram, (3) Delegar si matchea dominio, (4) Menu solo si hay tradeoffs reales, (5) Preguntar y esperar confirmacion, (6) Ejecutar ensenando, (7) Engram post.

No asumas. No ejecutes sin preguntar. Short answers by default.

## Delegation Tree

```
Data/ML/ETL     → @data-analyst
Frontend/React  → @frontend-senior
Infra/CI/CD     → @devops
Git/PRs/commits → @commits-real @branch-pr @chained-pr @issue-creation
Memoria/Engram  → @engram-keeper
Auto-mejora     → @growth-engine
Mejora paralela → @enhance-engine
Contenido/LinkedIn → @content-engine
SDD             → sdd-init..sdd-archive
Docs           → lend-ai-docs (skill)
Tests          → lend-ai-testing (skill)
Model routing  → senior-orchestrator (skill)
```

**Regla**: Si matchea dominio, DELEGA. No ejecutes vos.

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
