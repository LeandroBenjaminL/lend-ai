# Changelog

## [0.5.3] - 2026-05-15

### Added
- **update.sh**: script de actualización segura — git pull, backup de opencode.json, verificación de MCPs (FastMCP, psycopg2), revisión de tokens de entorno, conteo de agentes, recordatorio de sync Engram. No sobrescribe `.env`, no rompe configuración existente.
- **Auto-stash en update.sh**: detecta archivos dirty de sesiones anteriores y los stash antes del pull para evitar conflictos.

### Changed
- update.sh ahora detecta `SCRIPT_DIR` para funcionar desde cualquier directorio de checkout (no solo `~/.lend-ai`).

## [0.5.2] - 2026-05-14

### Added
- **@enhance-engine**: nuevo sub-agente de mejora paralela. Recibe input, lanza 10 sub-agentes simultáneos (performance, quality, security, architecture, testing, documentation, error handling, accessibility, UX, maintainability), consolida resultados.
- **Post-Task Automation**: workflow obligatorio después de cada cambio: Engram → Docs check → Commit & Push → Spawn growth-engine
- **System prompt inline**: checklist, árbol de decisión, 16 MCPs y delegation triggers comprimidos en `description` de opencode.json

### Changed
- opencode.json: enhance-engine agregado como subagent con permisos y config
- Árbol de decisión: nueva rama "mejora desde múltiples ángulos" → @enhance-engine
- workflow.md: sección Post-Task Automation agregada al final

### Added
- **Strict TDD Module** (`skills/sdd-apply/strict-tdd.md`): Three Laws, RED-GREEN-REFACTOR-TRIANGULATE, TDD evidence table, test layer selection
- **Apply-Progress MERGE Protocol**: prevents batch-N from destroying batch-(N-1) work
- **Workload Enforcement**: sdd-apply gate checks Review Workload Forecast before writing code
- **Chain Strategy Support** in sdd-apply: stacked-to-main, feature-branch-chain
- **Decision Gates** in chained-pr: 4 conditions → stacked PRs, feature branch chain, or size:exception
- **Chain Context template** in chained-pr: dependency diagram, review budget, PR ordering

### Changed
- `sdd-apply/SKILL.md`: 48→160 lines with ORCHESTRATOR GATE, persistence contract, TDD gate, chain strategies
- `sdd-archive/SKILL.md`: 48→120 lines with pre-flight check, archive report template, return envelope
- `chained-pr/SKILL.md`: 53→105 lines with activation contract, two chain strategies, output contract
- Orchestrator YAMLs: skills wired (data-analyst: 0→25, frontend-senior: 0→12, devops: 2→15)
- Agent personas: Arsenal sections added to all 5 orchestrator sub-agents

### Fixed
- data-analyst + frontend-senior YAMLs had zero skills declared (personas referenced them but YAML didn't)
- README + AGENTS.md synced to v0.5.0 with updated stats, architecture, shared protocols

### Added
- **Skill Resolver Protocol** (`skills/_shared/skill-resolver.md`): inyección de compact rules en sub-agentes, feedback loop, compaction-safe
- **Sub-agent Context Protocol** (`skills/_shared/subagent-context.md`): quién lee/escribe en cada fase SDD, artifact store modes, TDD forwarding
- **SDD Phase Common Protocol** (`skills/_shared/sdd-phase-common.md`): return envelope, artifact persistence, workload guard
- **Output Style** (`profiles/lend-ai/output-style.md`): response length contract, core principle, behavior rules
- **Persona Scope**: separación explícita entre tono de chat y artefactos generados
- **Delegation Triggers**: 6 reglas de parada (4-file rule, multi-file write, PR rule, incident, long-session, fresh review)
- **Proactive Save Triggers**: 11 categorías donde mem_save es obligatorio sin que el usuario lo pida
- **Cognitive Load Patterns** en lend-ai-docs: lead with answer, progressive disclosure, chunking, signposting, recognition over recall, review empathy
- **Comment/Voice Rules** en commits-real: work-unit splits, comment formula, PR review doc guidelines
- **Review Workload Forecast** en sdd-tasks: guard lines, delivery strategies (4 modos)
- **Decision Gates + Compliance Matrix** en sdd-verify: veredict PASS/PASS WITH WARNINGS/FAIL
- **Preset System** documentado en ARCHITECTURE (4 profiles + model routing)

### Changed
- `profiles/lend-ai/persona.md`: agregado Persona Scope + Contextual Skill Loading
- `profiles/lend-ai/workflow.md`: agregados 6 Delegation Triggers
- `skills/engram-memory-system/SKILL.md`: agregados Proactive Save Triggers
- `skills/commits-real/SKILL.md`: agregados work-unit splits, voice rules, comment formula, PR budget
- `skills/lend-ai-docs/SKILL.md`: agregados cognitive load patterns, default doc shape
- `skills/sdd-tasks/SKILL.md`: agregados Review Workload Forecast, delivery strategies
- `skills/sdd-verify/SKILL.md`: agregados decision gates, compliance matrix, return envelope
- `ARCHITECTURE.md`: agregados preset system, backup, shared protocols

### Inspired by
- [Gentle-AI](https://github.com/Gentleman-Programming/gentle-ai) — SDD orchestrator protocol, persona scope, skill resolver, delegation triggers, workload guard

## [0.4.0] - 2026-05-13

### Changed
- lend-ai sub_agents sincronizados: 9 agentes (se agregó commits-real, lend-ai-engram, lend-ai-testing, lend-ai-docs)
- frontend-mentor unificado con frontend-senior: se eliminó la duplicación, frontend-senior ahora tiene MCPs y sub-agentes completos
- frontend-senior promovido a T4-reasoning en model-router
- data-design, data-etl, data-reporter: sub-agentes actualizados (referencias a deprecados reemplazadas)

### Removed
- Skills deprecadas eliminadas: work-unit-commits, comment-writer, cognitive-doc-design
- Manifests y directorios de agentes deprecados removidos
- frontend-mentor.yaml eliminado (unificado con frontend-senior)

### Fixed
- 0 referencias rotas a sub-agentes en health check
- Arquitectura de agentes: 100 agentes, 77 válidos, 46 warnings (solo MCPs en hojas)

## [0.3.0] - 2026-05-10

### Added
- Sub-agentes transversales: lend-ai-engram, lend-ai-testing, lend-ai-docs
- Skill de documentación multi-archivo con Google-style docstrings y ADR
- Skill de tests con CI/CD (GitHub Actions, pytest, cobertura)
- Skill de gestión de memoria Engram
- Flujo senior (LEER → ANALIZAR → PREGUNTAR → DECIDIR → RESOLVER → ENGRAM)
- README.md, CONTRIBUTING.md, ARCHITECTURE.md, DEVELOPMENT.md, CHANGELOG.md
- docs/adr/ con primeras decisiones arquitectónicas

### Fixed
- Permisos de task actualizados para compartir skills entre agentes
- opencode.json con entries de los nuevos sub-agentes

## [0.2.0] - 2026-05-09

### Added
- Skills compartidas: shared-api-integration, shared-git-data
- Sistema de model routing por tiers (T1-T5)
- Scripts de modelo: model-commands.py, model-picker.py
- Comandos /model (set, reset, list, switch)

### Fixed
- Schema de opencode.json corregido para compatibilidad con OpenCode

## [0.1.0] - 2026-05-08

### Added
- Creación del ecosistema Lend.Ai
- Agentes: lend-ai (orquestador), data-analyst, frontend-senior
- 30+ skills iniciales (data-*, frontend-*, sdd-*)
- Tests iniciales (62 tests)
- install.sh con setup automatizado
