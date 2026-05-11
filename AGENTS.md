# Lend.Ai — Agent Skills Index

Unified AI agent ecosystem: Data Analysis, Frontend Development, DevOps, and Git/GitHub.

When working on this project, load the relevant skill BEFORE writing code.

Naming convention:
- `lend-ai-*` skills are repo-specific (workflow, identity)
- `data-*` skills belong to the Data Analysis domain
- `frontend-*` skills belong to the Frontend domain
- `devops-*` and unprefixed names are transversal/portable

## How to use

1. Check the **Trigger** column to find the skill matching your task
2. Load the skill by reading the SKILL.md file at the indicated path
3. Follow ALL the patterns and rules in the loaded skill
4. Multiple skills can be applied simultaneously

## Ecosystem Agents

| Agent | Role | Primary | Sub-agents |
|--------|-----|---------|-------------|
| `lend-ai` | General ecosystem orchestrator | ✅ | data-analyst, frontend-senior, devops, git-github, commits-real, lend-ai-engram, lend-ai-testing |
| `data-analyst` | Data analysis, ML, EDA, reporting | ❌ (sub) | data-explorer, data-modeler, data-reporter, etc. |
| `frontend-senior` | Frontend development, React, CSS, testing | ❌ (sub) | framework-architect, ui-crafter, styling-engineer, etc. |
| `devops` | DevOps, infrastructure, CI/CD, security, cloud, SRE | ❌ (sub) | docker-engineer, ci-cd-pilot, cloud-architect, db-admin, infra-sre, security-auditor, network-engineer, gitops-engineer, backup-engineer, perf-engineer |
| `git-github` | Commits, PRs, issues, branches, releases, versioning, Git, GitHub | ❌ (sub) | commits-real, branch-pr, chained-pr, issue-creation, gitops-engineer, shared-git-data |
| `engram-keeper` | Memory keeper — organizes, consolidates, audits Engram constantly | ❌ (sub) | engram-memory-system, lend-ai-engram |

## Global Skills (lend-ai orchestrator)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `lend-ai-persona` | Al iniciar sesión — identidad AISHA Engine, tono rioplatense, LEND-Protocol, Menú del Senior | [`profiles/lend-ai/persona.md`](profiles/lend-ai/persona.md) |
| `lend-ai-workflow` | Al planificar trabajo, definir flujo — reglas de comportamiento senior, skills globales obligatorias | [`profiles/lend-ai/workflow.md`](profiles/lend-ai/workflow.md) |
| `engram-memory-system` | Al clasificar, organizar y guardar memoria en Engram — árbol de clasificación, topic_keys, scope | [`skills/engram-memory-system/SKILL.md`](skills/engram-memory-system/SKILL.md) |
| `senior-orchestrator` | Al orquestar modelos, decidir tiers, planear arquitectura | [`skills/senior-orchestrator/SKILL.md`](skills/senior-orchestrator/SKILL.md) |

## Data Analysis Skills (data-analyst)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `data-analysis` | Al analizar datasets — Data Leakage Check, correlación, EDA con rigor estadístico, 3 opciones (visual / test hipótesis / PCA) | [`skills/data-analysis/SKILL.md`](skills/data-analysis/SKILL.md) |
| `data-cleaning` | Al limpiar datos — Null Anatomy (MCAR/MAR/MNAR), outliers con IQR, imputación inteligente, fuzzy matching | [`skills/data-cleaning/SKILL.md`](skills/data-cleaning/SKILL.md) |
| `data-visualization` | Al crear gráficos — elegir el tipo correcto según la historia, exploratorio vs publicable, Plotly vs Matplotlib | [`skills/data-visualization/SKILL.md`](skills/data-visualization/SKILL.md) |
| `data-profiling` | Al recibir un dataset nuevo — ydata-profiling, pandera, reporte de calidad en minutos | [`skills/data-profiling/SKILL.md`](skills/data-profiling/SKILL.md) |
| `data-question` | Al definir preguntas de negocio — SMART, frenar ambigüedad, alinear análisis con objetivos | [`skills/data-question/SKILL.md`](skills/data-question/SKILL.md) |
| `data-design` | Al diseñar estrategia de análisis — elegir enfoque (SQL/Python/Híbrido), pipeline, herramientas | [`skills/data-design/SKILL.md`](skills/data-design/SKILL.md) |
| `data-validation` | Al validar esquemas — pandera, great expectations, contratos de datos | [`skills/data-validation/SKILL.md`](skills/data-validation/SKILL.md) |
| `data-verify` | Al verificar resultados antes de presentar — reproducibilidad, sanity checks, regla del titular | [`skills/data-verify/SKILL.md`](skills/data-verify/SKILL.md) |
| `ml-modeling` | Al entrenar modelos — Baseline First, Stratified K-Fold, SHAP > feature_importances_, Optuna > GridSearch | [`skills/ml-modeling/SKILL.md`](skills/ml-modeling/SKILL.md) |
| `time-series-analysis` | Al trabajar con series temporales — Prophet, statsmodels, descomposición, estacionariedad, forecasting | [`skills/time-series-analysis/SKILL.md`](skills/time-series-analysis/SKILL.md) |
| `statistical-testing` | Al hacer tests de hipótesis — elegir test según datos, p-value con cuidado, tamaño del efecto | [`skills/statistical-testing/SKILL.md`](skills/statistical-testing/SKILL.md) |
| `sql-analysis` | Al hacer consultas SQL — CTEs, window functions, JOINs, EXPLAIN ANALYZE, índices | [`skills/sql-analysis/SKILL.md`](skills/sql-analysis/SKILL.md) |
| `database-connections` | Al conectar a bases de datos — SQLAlchemy, PostgreSQL, MySQL, SQLite, .env para secrets | [`skills/database-connections/SKILL.md`](skills/database-connections/SKILL.md) |
| `etl-pipelines` | Al construir pipelines ETL/ELT — idempotente, logging, checkpoint, incremental | [`skills/etl-pipelines/SKILL.md`](skills/etl-pipelines/SKILL.md) |
| `reporting` | Al generar reportes — Markdown/Quarto, HTML+Jinja2, PDF con ReportLab, automatizable | [`skills/reporting/SKILL.md`](skills/reporting/SKILL.md) |
| `streamlit` | Al crear dashboards — st.cache_data, Plotly interactivo, deploy en Streamlit Cloud | [`skills/streamlit/SKILL.md`](skills/streamlit/SKILL.md) |
| `file-formats` | Al leer/guardar datos multi-formato — CSV, Parquet, Feather, Excel, JSON. Elegí el formato correcto | [`skills/file-formats/SKILL.md`](skills/file-formats/SKILL.md) |
| `notebook-integration` | Al trabajar con Jupyter — Run All antes de commitear, nbstripout, Quarto > .ipynb | [`skills/notebook-integration/SKILL.md`](skills/notebook-integration/SKILL.md) |
| `python-environment` | Al gestionar entornos Python — venv, Poetry, Conda, .env, requirements congelados | [`skills/python-environment/SKILL.md`](skills/python-environment/SKILL.md) |
| `regex-data` | Al limpiar texto con regex — extracción, validación, fuzzy matching, performance con re.compile | [`skills/regex-data/SKILL.md`](skills/regex-data/SKILL.md) |
| `shared-git-data` | Al versionar proyectos de datos — DVC, nbstripout, .gitignore, commits semánticos | [`skills/shared-git-data/SKILL.md`](skills/shared-git-data/SKILL.md) |
| `shared-api-integration` | Al consumir APIs REST — requests Session, timeout, rate limiting, .env para secrets | [`skills/shared-api-integration/SKILL.md`](skills/shared-api-integration/SKILL.md) |
| `web-scraping` | Al extraer datos de sitios web — BeautifulSoup, Playwright, robots.txt, rate limiting | [`skills/web-scraping/SKILL.md`](skills/web-scraping/SKILL.md) |

## Frontend Skills (frontend-senior)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `frontend-react-development` | Al crear componentes React — Server/Client Component, composición, hooks, estados visibles | [`skills/frontend-react-development/SKILL.md`](skills/frontend-react-development/SKILL.md) |
| `frontend-css-styling` | Al estilar componentes — Tailwind vs CSS Modules, Container Queries, mobile-first | [`skills/frontend-css-styling/SKILL.md`](skills/frontend-css-styling/SKILL.md) |
| `frontend-type-script` | Al escribir TypeScript — strict mode, satisfies, discriminated unions, evitar any | [`skills/frontend-type-script/SKILL.md`](skills/frontend-type-script/SKILL.md) |
| `frontend-api-integration` | Al consumir APIs desde el front — TanStack Query, fetch, optimistic updates, manejo de errores | [`skills/frontend-api-integration/SKILL.md`](skills/frontend-api-integration/SKILL.md) |
| `frontend-state-management` | Al manejar estado global — Zustand vs Redux vs Context, selectores, persist | [`skills/frontend-state-management/SKILL.md`](skills/frontend-state-management/SKILL.md) |
| `frontend-testing` | Al testear frontend — Vitest + Testing Library, Playwright, MSW, pirámide de tests | [`skills/frontend-testing/SKILL.md`](skills/frontend-testing/SKILL.md) |
| `frontend-responsive-design` | Al diseñar responsive — Container Queries, clamp(), Grid + auto-fit, mobile-first | [`skills/frontend-responsive-design/SKILL.md`](skills/frontend-responsive-design/SKILL.md) |
| `frontend-web-performance` | Al optimizar performance — Core Web Vitals, Lighthouse, dynamic imports, bundle analysis | [`skills/frontend-web-performance/SKILL.md`](skills/frontend-web-performance/SKILL.md) |

## DevOps Skills (devops)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `docker-engineer` | Al containerizar apps — Dockerfile multi-stage, compose, non-root, healthcheck, K8s | [`skills/docker-engineer/SKILL.md`](skills/docker-engineer/SKILL.md) |
| `ci-cd-pilot` | Al automatizar pipelines — GitHub Actions, caching, matrix builds, secrets management | [`skills/ci-cd-pilot/SKILL.md`](skills/ci-cd-pilot/SKILL.md) |
| `cloud-architect` | Al diseñar infra cloud — Terraform, AWS/GCP/Azure, tagging, estado remoto, mínimo privilegio | [`skills/cloud-architect/SKILL.md`](skills/cloud-architect/SKILL.md) |
| `infra-sre` | Al monitorear servicios — Prometheus/Grafana, RED/USE method, SLIs/SLOs, runbooks | [`skills/infra-sre/SKILL.md`](skills/infra-sre/SKILL.md) |
| `security-auditor` | Al escanear vulnerabilidades — SAST/DAST, secret scanning, hardening, OWASP, compliance | [`skills/security-auditor/SKILL.md`](skills/security-auditor/SKILL.md) |

| `network-engineer` | Al configurar DNS, proxies, firewalls, SSL, CDN — Nginx, Caddy, Cloudflare, balanceo | [`skills/network-engineer/SKILL.md`](skills/network-engineer/SKILL.md) |
| `gitops-engineer` | Al diseñar branching strategy, releases, versionado — trunk-based, GitHub Flow, conventional commits | [`skills/gitops-engineer/SKILL.md`](skills/gitops-engineer/SKILL.md) |
| `backup-engineer` | Al diseñar backups, disaster recovery — 3-2-1, RPO/RTO, restic, pg_dump | [`skills/backup-engineer/SKILL.md`](skills/backup-engineer/SKILL.md) |
| `perf-engineer` | Al hacer load testing, profiling — k6, Lighthouse, cProfile, EXPLAIN ANALYZE | [`skills/perf-engineer/SKILL.md`](skills/perf-engineer/SKILL.md) |
| `db-admin` | Al administrar bases de datos — PostgreSQL, MySQL, Redis, índices, migraciones, replicación | [`skills/db-admin/SKILL.md`](skills/db-admin/SKILL.md) |

## Transversal Skills

| Skill | Trigger | Ruta |
|-------|---------|------|
| `commits-real` | Al escribir commits, PRs, issues — conventional commits, semver, changelog | [`skills/commits-real/SKILL.md`](skills/commits-real/SKILL.md) |
| `lend-ai-engram` | Al guardar o consultar memoria en Engram — What/Why/Where/Learned, topic_key, scope | [`skills/lend-ai-engram/SKILL.md`](skills/lend-ai-engram/SKILL.md) |
| `lend-ai-testing` | Al escribir tests, configurar CI — pytest, cobertura, pipeline automatizado | [`skills/lend-ai-testing/SKILL.md`](skills/lend-ai-testing/SKILL.md) |
| `lend-ai-docs` | Al escribir documentación — Google-style docstrings, ADR, README, ARCHITECTURE | [`skills/lend-ai-docs/SKILL.md`](skills/lend-ai-docs/SKILL.md) |
| `judgment-day` | Al necesitar doble review — 2 jueces ciegos (seguridad + clean code), veredicto con acciones | [`skills/judgment-day/SKILL.md`](skills/judgment-day/SKILL.md) |
| `branch-pr` | Al crear PRs — issue-first, < 400 líneas, branch naming, descripción estructurada | [`skills/branch-pr/SKILL.md`](skills/branch-pr/SKILL.md) |
| `chained-pr` | Cuando un PR supera 400 líneas — PRs encadenados en secuencia lógica | [`skills/chained-pr/SKILL.md`](skills/chained-pr/SKILL.md) |
| `issue-creation` | Al crear issues — bug report, feature request, templates, criterios de aceptación | [`skills/issue-creation/SKILL.md`](skills/issue-creation/SKILL.md) |
| `go-testing` | Al escribir tests en Go — table-driven, parallel, Bubbletea testing | [`skills/go-testing/SKILL.md`](skills/go-testing/SKILL.md) |
| `skill-creator` | Al crear nuevas skills — template LEND, estructura skills/, registro en AGENTS.md | [`skills/skill-creator/SKILL.md`](skills/skill-creator/SKILL.md) |
| `skill-registry` | Al auditar skills — sync skills/ vs AGENTS.md vs manifests, detectar huérfanas | [`skills/skill-registry/SKILL.md`](skills/skill-registry/SKILL.md) |
| `youtube-transcript` | Al extraer transcripciones de YouTube — resumen estructurado, timestamps, análisis | [`skills/youtube-transcript/SKILL.md`](skills/youtube-transcript/SKILL.md) |

## SDD Skills (Spec-Driven Development)

| Skill | Trigger | Ruta |
|-------|---------|------|
| `sdd-init` | Al iniciar un proyecto nuevo — detectar stack, configurar persistencia, estructura SDD | [`skills/sdd-init/SKILL.md`](skills/sdd-init/SKILL.md) |
| `sdd-explore` | Al investigar código antes de proponer — leer, analizar impacto, consultar Engram | [`skills/sdd-explore/SKILL.md`](skills/sdd-explore/SKILL.md) |
| `sdd-propose` | Al tener una propuesta de cambio — contexto, alternativas, criterios de éxito | [`skills/sdd-propose/SKILL.md`](skills/sdd-propose/SKILL.md) |
| `sdd-spec` | Al escribir especificaciones — Given/When/Then, escenarios, casos borde, contract | [`skills/sdd-spec/SKILL.md`](skills/sdd-spec/SKILL.md) |
| `sdd-design` | Al diseñar la implementación — archivos, data flow, ADR, interfaces | [`skills/sdd-design/SKILL.md`](skills/sdd-design/SKILL.md) |
| `sdd-tasks` | Al descomponer en tareas — dependencias, tamaño, paralelización, criterio de done | [`skills/sdd-tasks/SKILL.md`](skills/sdd-tasks/SKILL.md) |
| `sdd-apply` | Al implementar cambios — TDD, commits atómicos, una tarea a la vez | [`skills/sdd-apply/SKILL.md`](skills/sdd-apply/SKILL.md) |
| `sdd-verify` | Al validar contra specs — tests reales, quality gate, reporte PASS/FAIL | [`skills/sdd-verify/SKILL.md`](skills/sdd-verify/SKILL.md) |
| `sdd-archive` | Al archivar cambios completados — sync specs, merge, changelog, Engram | [`skills/sdd-archive/SKILL.md`](skills/sdd-archive/SKILL.md) |
| `sdd-onboard` | Al guiar a alguien por SDD — cambio real, ciclo completo, aprendizaje práctico | [`skills/sdd-onboard/SKILL.md`](skills/sdd-onboard/SKILL.md) |

> **Deprecated skills**: `cognitive-doc-design`, `comment-writer`, `work-unit-commits` → replaced by `commits-real`
