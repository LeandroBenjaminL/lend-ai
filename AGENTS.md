# Lend.Ai — Agent Skills Index

Ecosistema unificado de agentes AI para Data Analysis y Frontend Development.

## Arquitectura de 3 Niveles

### N1 — Skills de Sistema (SIEMPRE ACTIVAS en el chat principal)
Se cargan automáticamente al iniciar sesión. Definen personalidad, memoria, flujo y calidad.

| Skill | Propósito |
|-------|-----------|
| `lend-ai-persona` | Identidad AISHA, tono rioplatense, reglas, perfil profesor |
| `lend-ai-mentor` | Protocolo de proyecto + enseñanza + perfil de usuario |
| `lend-ai-workflow` | Flujo de trabajo, GATES obligatorios, delegación |
| `lend-ai-engram` | Memoria del ecosistema — guardar y consultar |
| `engram-memory-system` | Sistema de memoria profunda — topic_keys, frescura, auto-evolución |
| `commits-real` | Commits y PRs — modo humano + límite 300 líneas |
| `lend-ai-testing` | Gate obligatorio pre-commit — tests en verde |
| `lend-ai-docs` | Documentación técnica |
| `senior-orchestrator` | Orquestación, delegación, routing de modelos |
| `lend-ai-delegation` | Protocolo de delegación y sub-agentes |

### N2 — Agentes de Dominio (Supervisores)
Spawnean sub-agentes especializados. Siempre reciben tarea delegada del orquestador.

| Agente | Sub-agentes |
|--------|-------------|
| `data-analyst` | data-question, data-design, data-explorer, data-analysis, data-cleaning, data-modeler, data-reporter, data-verify, data-archive |
| `frontend-senior` | framework-architect, ui-crafter, styling-engineer, data-flow, api-consumer, realtime-engineer, quality-guardian, perf-a11y, build-master, content-docs |
| `devops` | docker-engineer, ci-cd-pilot, cloud-architect, db-admin, infra-sre, security-auditor, network-engineer, gitops-engineer, backup-engineer, perf-engineer |

### N3 — Agentes Especialistas (Ejecutores)
Reciben tareas concretas de los supervisores. No delegan más (salvo excepciones).

Ver tabla completa en [`skills/`](skills/) o en [`opencode.json`](opencode.json).

## Flujo de Sesión Obligatorio

Cada sesión sigue este pipeline. NO saltees pasos.

```
1. INICIAR
   ├── mem_context — contexto de sesiones anteriores
   ├── mem_search "user profile" — perfil, preferencias, personalidad
   └── preguntar dudas — si hay ambigüedad en lo que pide el user

2. ANALIZAR
   ├── entender el problema (lógica de negocio, no solo código)
   ├── evaluar tradeoffs y opciones
   └── SI HAY AMBIGÜEDAD → PREGUNTAR (no asumas nada)

3. EJECUTAR
   ├── delegar si matchea dominio (N2 o N3)
   ├── enseñar mientras hacés (QUÉ, POR QUÉ, PATRÓN)
   ├── cuestionar decisiones del user si hay mejor opción
   └── guardar en Engram CADA decisión importante (sin preguntar)

4. POST-TASK — DOCS REVIEW (GATE OBLIGATORIO)
   ├── ¿Cambió estructura? → AGENTS.md, ARCHITECTURE.md, README
   ├── ¿Decisión técnica? → ADR en docs/adr/
   ├── ¿Feature nueva? → CHANGELOG / README
   └── delegar a lend-ai-docs si hay algo que actualizar

5. PRE-COMMIT (GATES OBLIGATORIOS)
   ├── ¿Hay tests? → delegar a lend-ai-testing
   ├── ¿Todo en verde? → no seguir si falla
   └── ¿Supera 300 líneas? → chained-pr, no un solo commit gigante

6. COMMIT / PR
   ├── modo humano (español rioplatense, cálido, claro)
   ├── max 300 líneas por commit/PR/issue
   └── Engram mem_save con lo que se hizo

7. CERRAR
   ├── mem_session_summary
   ├── guardar preferencias aprendidas en la sesión
   └── growth-engine revisa patrones (opcional)
```

## Convención de naming
- `lend-ai-*` skills son específicas del repo (workflow, identidad)
- `data-*` skills son del dominio Data Analysis
- `frontend-*` skills son del dominio Frontend
- Skills sin prefijo son transversales/portables

## Cómo usar

1. Revisá la columna **Trigger** para encontrar la skill que coincide con tu tarea
2. Cargá la skill leyendo el archivo SKILL.md en la ruta indicada
3. Seguí TODOS los patrones y reglas de la skill cargada
4. Múltiples skills pueden aplicarse simultáneamente

## Skills

| Skill | Trigger | Ruta |
|-------|---------|------|
| `lend-ai-mentor` | **Cargar al iniciar cada sesión** — Protocolo completo de proyecto + profesor + perfil de usuario. Reemplaza config previa de comportamiento. | [`skills/lend-ai-mentor/SKILL.md`](skills/lend-ai-mentor/SKILL.md) |
| `lend-ai-persona` | Al iniciar sesión, definir perfil, conocer la identidad del ecosistema | [`skills/lend-ai-persona/SKILL.md`](skills/lend-ai-persona/SKILL.md) |
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
| `docker-engineer` | Al trabajar con Docker, contenedores, K8s | [`skills/docker-engineer/SKILL.md`](skills/docker-engineer/SKILL.md) |
| `ci-cd-pilot` | Al configurar CI/CD, pipelines, automatización | [`skills/ci-cd-pilot/SKILL.md`](skills/ci-cd-pilot/SKILL.md) |
| `cloud-architect` | Al diseñar arquitectura cloud, AWS, GCP, Azure | [`skills/cloud-architect/SKILL.md`](skills/cloud-architect/SKILL.md) |
| `db-admin` | Al administrar bases de datos, PostgreSQL, MySQL | [`skills/db-admin/SKILL.md`](skills/db-admin/SKILL.md) |
| `infra-sre` | Al manejar infraestructura, monitoreo, SRE | [`skills/infra-sre/SKILL.md`](skills/infra-sre/SKILL.md) |
| `security-auditor` | Al auditar seguridad, hardening, compliance | [`skills/security-auditor/SKILL.md`](skills/security-auditor/SKILL.md) |
| `network-engineer` | Al configurar redes, DNS, VPN, firewalls | [`skills/network-engineer/SKILL.md`](skills/network-engineer/SKILL.md) |
| `gitops-engineer` | Al implementar GitOps, ArgoCD, Flux | [`skills/gitops-engineer/SKILL.md`](skills/gitops-engineer/SKILL.md) |
| `backup-engineer` | Al diseñar estrategias de backup y recuperación | [`skills/backup-engineer/SKILL.md`](skills/backup-engineer/SKILL.md) |
| `perf-engineer` | Al optimizar performance, profiling, tuning | [`skills/perf-engineer/SKILL.md`](skills/perf-engineer/SKILL.md) |
| `judgment-day` | Al necesitar doble review, revisión adversarial | [`skills/judgment-day/SKILL.md`](skills/judgment-day/SKILL.md) |
| `skill-creator` | Al crear nuevas skills para el ecosistema | [`skills/skill-creator/SKILL.md`](skills/skill-creator/SKILL.md) |
| `skill-registry` | Al actualizar el registro de skills | [`skills/skill-registry/SKILL.md`](skills/skill-registry/SKILL.md) |
| `web-scraping` | Al extraer datos de sitios web | [`skills/web-scraping/SKILL.md`](skills/web-scraping/SKILL.md) |
| `youtube-transcript` | Al extraer transcripciones de YouTube | [`skills/youtube-transcript/SKILL.md`](skills/youtube-transcript/SKILL.md) |
| `content-engine` | Al analizar progreso, generar contenido para LinkedIn, documentar mejoras | [`skills/content-engine/SKILL.md`](skills/content-engine/SKILL.md) |

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
| `chained-pr` | Cuando un PR supera 300 líneas, PRs encadenados | [`skills/chained-pr/SKILL.md`](skills/chained-pr/SKILL.md) |
| `issue-creation` | Al crear issues en GitHub, reportar bugs | [`skills/issue-creation/SKILL.md`](skills/issue-creation/SKILL.md) |
| `go-testing` | Al escribir tests en Go | [`skills/go-testing/SKILL.md`](skills/go-testing/SKILL.md) |

> **Skills deprecadas**: `cognitive-doc-design`, `comment-writer`, `work-unit-commits` → reemplazadas por `commits-real`
