# Lend.Ai — Agent Skills Index

Ecosistema unificado de agentes AI para Data Analysis, Frontend Development y DevOps.

Cuando trabajes en este proyecto, cargá la skill relevante ANTES de escribir código.

Convención de naming:
- `lend-ai-*` skills son específicas del repo (workflow, identidad)
- `data-*` skills son del dominio Data Analysis
- `frontend-*` skills son del dominio Frontend
- Skills sin prefijo son transversales/portables

## Cómo usar

1. Revisá la columna **Trigger** para encontrar la skill que coincide con tu tarea
2. Cargá la skill leyendo el archivo SKILL.md en la ruta indicada
3. Seguí TODOS los patrones y reglas de la skill cargada
4. Múltiples skills pueden aplicarse simultáneamente

## Agentes del Ecosistema

| Agente | Rol | Primary | Sub-agentes |
|--------|-----|---------|-------------|
| `lend-ai` | Orquestador general del ecosistema | ✅ | data-analyst, frontend-senior, devops, commits-real, lend-ai-engram, lend-ai-testing |
| `data-analyst` | Análisis de datos, ML, EDA, reporting | ❌ (sub) | data-explorer, data-modeler, data-reporter, etc. |
| `frontend-senior` | Desarrollo frontend, React, CSS, testing | ❌ (sub) | framework-architect, ui-crafter, styling-engineer, etc. |
| `devops` | DevOps, infraestructura, CI/CD, seguridad, cloud, SRE | ❌ (sub) | docker-engineer, ci-cd-pilot, cloud-architect, db-admin, infra-sre, security-auditor, network-engineer, gitops-engineer, backup-engineer, perf-engineer |

## Skills

| Skill | Trigger | Ruta |
|-------|---------|------|
| `lend-ai-persona` | Al iniciar sesión, definir perfil, conocer la identidad del ecosistema | [`profiles/lend-ai/persona.md`](profiles/lend-ai/persona.md) |
| `engram-memory-system` | Al clasificar, organizar y guardar memoria en Engram — árbol de clasificación, topic_keys, scope | [`skills/engram-memory-system/SKILL.md`](skills/engram-memory-system/SKILL.md) |
| `lend-ai-workflow` | Al planificar trabajo, definir flujo, decidir entre data o frontend | [`profiles/lend-ai/workflow.md`](profiles/lend-ai/workflow.md) |
| `data-analyst` | Cuando necesitás ser el profesor senior de datos — análisis, EDA, ML | [`skills/data-analyst/SKILL.md`](skills/data-analyst/SKILL.md) |
| `frontend-senior` | Cuando necesitás ser el mentor senior de frontend — React, CSS, UX | [`skills/frontend-senior/SKILL.md`](skills/frontend-senior/SKILL.md) |
| `senior-orchestrator` | Cuando necesitás orquestar modelos, decidir tiers, planear arquitectura | [`skills/senior-orchestrator/SKILL.md`](skills/senior-orchestrator/SKILL.md) |
| `commits-real` | Al escribir commits, PRs, issues, documentación | [`skills/commits-real/SKILL.md`](skills/commits-real/SKILL.md) |
| `lend-ai-engram` | Al guardar o consultar memoria en Engram | [`skills/lend-ai-engram/SKILL.md`](skills/lend-ai-engram/SKILL.md) |
| `lend-ai-testing` | Al escribir tests, configurar CI, revisar calidad | [`skills/lend-ai-testing/SKILL.md`](skills/lend-ai-testing/SKILL.md) |
| `lend-ai-docs` | Al escribir documentación, docstrings, ADR, ARCHITECTURE.md | [`skills/lend-ai-docs/SKILL.md`](skills/lend-ai-docs/SKILL.md) |
| `data-analysis` | Al analizar datasets, manipular DataFrames, cálculos numéricos | [`skills/data-analysis/SKILL.md`](skills/data-analysis/SKILL.md) |
| `data-cleaning` | Al limpiar datos, manejar nulos, duplicados, outliers | [`skills/data-cleaning/SKILL.md`](skills/data-cleaning/SKILL.md) |
| `data-visualization` | Al crear gráficos y visualizaciones | [`skills/data-visualization/SKILL.md`](skills/data-visualization/SKILL.md) |
| `data-profiling` | Al recibir un dataset nuevo, profiling automático | [`skills/data-profiling/SKILL.md`](skills/data-profiling/SKILL.md) |
| `data-question` | Al definir preguntas de negocio, hipótesis, objetivos | [`skills/data-question/SKILL.md`](skills/data-question/SKILL.md) |
| `data-design` | Al diseñar estrategia de análisis, elegir enfoque | [`skills/data-design/SKILL.md`](skills/data-design/SKILL.md) |
| `data-validation` | Al validar esquemas, garantizar calidad de datos | [`skills/data-validation/SKILL.md`](skills/data-validation/SKILL.md) |
| `data-verify` | Al verificar resultados de análisis antes de presentar | [`skills/data-verify/SKILL.md`](skills/data-verify/SKILL.md) |
| `ml-modeling` | Al entrenar modelos ML, regresión, clasificación | [`skills/ml-modeling/SKILL.md`](skills/ml-modeling/SKILL.md) |
| `time-series-analysis` | Al trabajar con series temporales, forecasting | [`skills/time-series-analysis/SKILL.md`](skills/time-series-analysis/SKILL.md) |
| `statistical-testing` | Al hacer tests de hipótesis, tests estadísticos | [`skills/statistical-testing/SKILL.md`](skills/statistical-testing/SKILL.md) |
| `sql-analysis` | Al hacer consultas SQL, joins, window functions | [`skills/sql-analysis/SKILL.md`](skills/sql-analysis/SKILL.md) |
| `database-connections` | Al conectar a bases de datos, SQLAlchemy | [`skills/database-connections/SKILL.md`](skills/database-connections/SKILL.md) |
| `etl-pipelines` | Al construir pipelines ETL/ELT | [`skills/etl-pipelines/SKILL.md`](skills/etl-pipelines/SKILL.md) |
| `frontend-react-development` | Al desarrollar componentes React, hooks, patrones | [`skills/frontend-react-development/SKILL.md`](skills/frontend-react-development/SKILL.md) |
| `frontend-css-styling` | Al trabajar con CSS, Tailwind, Grid/Flexbox | [`skills/frontend-css-styling/SKILL.md`](skills/frontend-css-styling/SKILL.md) |
| `frontend-type-script` | Al escribir TypeScript, tipos, genéricos | [`skills/frontend-type-script/SKILL.md`](skills/frontend-type-script/SKILL.md) |
| `frontend-api-integration` | Al consumir APIs, TanStack Query, fetch | [`skills/frontend-api-integration/SKILL.md`](skills/frontend-api-integration/SKILL.md) |
| `frontend-state-management` | Al manejar estado, Zustand, Redux, Context | [`skills/frontend-state-management/SKILL.md`](skills/frontend-state-management/SKILL.md) |
| `frontend-testing` | Al escribir tests frontend, Vitest, Testing Library | [`skills/frontend-testing/SKILL.md`](skills/frontend-testing/SKILL.md) |
| `frontend-responsive-design` | Al diseñar responsive, mobile-first | [`skills/frontend-responsive-design/SKILL.md`](skills/frontend-responsive-design/SKILL.md) |
| `frontend-web-performance` | Al optimizar performance, Core Web Vitals | [`skills/frontend-web-performance/SKILL.md`](skills/frontend-web-performance/SKILL.md) |
| `shared-api-integration` | Al consumir APIs REST, requests, integración genérica | [`skills/shared-api-integration/SKILL.md`](skills/shared-api-integration/SKILL.md) |
| `shared-git-data` | Al versionar datasets, git para data science | [`skills/shared-git-data/SKILL.md`](skills/shared-git-data/SKILL.md) |
| `judgment-day` | Al necesitar doble review, revisión adversarial | [`skills/judgment-day/SKILL.md`](skills/judgment-day/SKILL.md) |
| `skill-creator` | Al crear nuevas skills para el ecosistema | [`skills/skill-creator/SKILL.md`](skills/skill-creator/SKILL.md) |
| `skill-registry` | Al actualizar el registro de skills | [`skills/skill-registry/SKILL.md`](skills/skill-registry/SKILL.md) |
| `web-scraping` | Al extraer datos de sitios web | [`skills/web-scraping/SKILL.md`](skills/web-scraping/SKILL.md) |
| `youtube-transcript` | Al extraer transcripciones de YouTube | [`skills/youtube-transcript/SKILL.md`](skills/youtube-transcript/SKILL.md) |

## Skills SDD (Spec-Driven Development)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `sdd-init` | Al iniciar un nuevo proyecto/feature en un codebase | [`skills/sdd-init/SKILL.md`](skills/sdd-init/SKILL.md) |
| `sdd-explore` | Al investigar el codebase, explorar antes de diseñar | [`skills/sdd-explore/SKILL.md`](skills/sdd-explore/SKILL.md) |
| `sdd-propose` | Al tener una propuesta de cambio para revisión | [`skills/sdd-propose/SKILL.md`](skills/sdd-propose/SKILL.md) |
| `sdd-spec` | Al escribir especificaciones detalladas | [`skills/sdd-spec/SKILL.md`](skills/sdd-spec/SKILL.md) |
| `sdd-design` | Al diseñar la implementación técnica | [`skills/sdd-design/SKILL.md`](skills/sdd-design/SKILL.md) |
| `sdd-tasks` | Al descomponer especificaciones en tareas | [`skills/sdd-tasks/SKILL.md`](skills/sdd-tasks/SKILL.md) |
| `sdd-apply` | Al implementar cambios del diseño | [`skills/sdd-apply/SKILL.md`](skills/sdd-apply/SKILL.md) |
| `sdd-verify` | Al validar implementación contra especificaciones | [`skills/sdd-verify/SKILL.md`](skills/sdd-verify/SKILL.md) |
| `sdd-archive` | Al archivar artefactos de cambio completados | [`skills/sdd-archive/SKILL.md`](skills/sdd-archive/SKILL.md) |
| `sdd-onboard` | Al guiar a alguien por el ciclo SDD completo | [`skills/sdd-onboard/SKILL.md`](skills/sdd-onboard/SKILL.md) |

## Skills Transversales (PRs, Issues, Docs)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `branch-pr` | Al crear PRs, preparar cambios para review | [`skills/branch-pr/SKILL.md`](skills/branch-pr/SKILL.md) |
| `chained-pr` | Cuando un PR supera 400 líneas, PRs encadenados | [`skills/chained-pr/SKILL.md`](skills/chained-pr/SKILL.md) |
| `issue-creation` | Al crear issues en GitHub, reportar bugs | [`skills/issue-creation/SKILL.md`](skills/issue-creation/SKILL.md) |
| `go-testing` | Al escribir tests en Go | [`skills/go-testing/SKILL.md`](skills/go-testing/SKILL.md) |

> **Skills deprecadas**: `cognitive-doc-design`, `comment-writer`, `work-unit-commits` → reemplazadas por `commits-real`
