# Changelog

## [0.7.0] - 2026-05-16

### Added
- **Pre-push hook**: tests corren automáticamente antes de cada push. `feat(git): pre-push hook runs tests before push, fix model-router tier dir`
- **.gitattributes**: normalización de line endings para multiplataforma.

### Changed
- **System prompt**: comprimido de 731 a ~500 chars. Skills reducidas de 9 a 5. Perfiles comprimidos. Token overhead reducido ~40%.
- **MCPs final**: se eliminaron filesystem, puppeteer, slack, postgres, mysql, sqlite, smtp-email. Quedan 9 MCPs: engram, sequential-thinking, web-search, github, context7, google-drive, notion, ocr, agent-router, model-router.
- **Permissions**: todos los domain agents pasaron de `* deny` a `* allow` para delegación sin fricción.
- **Sub-agent types**: `* allow` en lugar de lista manual de 30+ tipos.
- **Notion MCP**: reemplazado wrapper PowerShell por `npx easy-notion-mcp` directo.
- **Installers**: escaping de backslashes fix para Windows, placeholder `{LEND_AI_HOME}` para paths dinámicos.

### Fixed
- **model-router.py**: tier directory detection for agent manifests.
- **pre-push hook**: executable permissions for Linux (`chmod +x`).

## [0.6.3] - 2026-05-16

### Added
- **CI enforcement**: `ci.yml` — tests must pass before push or merge. `pytest tests/ -v` mandatory gate.

### Fixed
- **Ruff E501**: line too long en test files corregidos.
- **Manifests huérfanos**: 11 manifests y 24 directorios stub removidos.

## [0.6.2] - 2026-05-16

### Changed
- **System prompt**: de 2119 chars narrativos a 731 chars de checklist ejecutable. 7 pasos obligatorios: Engram, Preguntar, Esperar, 3 Opciones, Enseñar, Ejecutar, Cerrar. Sin párrafos explicativos — solo pasos que no se pueden saltar.

## [0.6.1] - 2026-05-16

### Added
- **Content Engine** (`skills/content-engine/SKILL.md`): meta-skill que analiza Engram, trackea mejoras, sincroniza documentación y genera contenido profesional (LinkedIn posts, case studies, tips técnicos). Registrado como sub-agente con manifest YAML.
- **Mentor Protocol** (`skills/lend-ai-mentor/SKILL.md`): protocolo completo de 147 líneas con 4 partes — perfil de usuario, protocolo de proyecto, comportamiento de profesor (preguntar 3+, 3 opciones, enseñar, exigir claridad), y voz dinámica del usuario.
- **User profile en Engram**: perfil auto-acumulable con topic_key user-profile/leandro. Aprende vocabulario, preferencias técnicas, estilo de comunicación. Se actualiza después de cada interacción.
- **ENGRAM FIRST**: Engram promovido a regla #1 absoluta en system prompt. mem_context al iniciar, mem_search antes de decidir, mem_save después de cada acción.

### Changed
- **System prompt**: de 1156 a 2119 chars con TODO el protocolo mentor inline. Engram sanctuary, user profile, project protocol, profesor behavior (P1-P4), post-task automation, voz dinámica.
- **lend-ai.yaml**: sub_agents de 2 a 13 (agregados devops, git-github, engram-keeper, growth-engine, enhance-engine, content-engine, commits-real, lend-ai-engram, lend-ai-testing, lend-ai-docs, judgment-day).
- **model-routing.config.json**: agents section poblado con tiers para content-engine, growth-engine, enhance-engine, lend-ai-docs, lend-ai-engram, lend-ai-testing, judgment-day.
- **skills auto-load**: de 9 a 11 skills (agregados lend-ai-mentor como #1, content-engine).
- **update.sh**: ahora reemplaza `{LEND_AI_HOME}` al copiar opencode.json (fix MCPs rotos).

### Fixed
- **CI tests**: 2 tests fallando por frontend-mentor (deprecado desde v0.4.0). Reemplazado por frontend-senior. 62/62 tests verdes.
- **lend-ai-persona SKILL.md**: era un stub vacío ("andá a leer profiles/lend-ai/persona.md"). Ahora tiene contenido real con teaching gates, post-task, MCPs.
- **AGENTS.md**: ruta de lend-ai-persona corregida de profiles/ a skills/.

## [0.6.0] - 2026-05-15

### Added
- **engram-wrapper.sh**: wrapper para ejecutar engram en SSH no-interactivo. Homebrew PATH detection automático.
- **/engram-server command**: verifica estado del servidor Engram remoto (Tailscale, SSH, keepalive, MCP).
- **/engram-optimize command**: escanea y corrige topic_keys, tipos, scopes y duplicados en Engram.
- **Engram memory system v2**: jerarquía completa de topic_keys como carpetas virtuales (architecture/, bugfix/, pattern/, discovery/, config/, decision/, learning/, preference/, session/). 40+ topic_keys en 9 áreas.
- **Guardado automático en Engram**: regla #1 del system prompt. Disparadores por tipo de evento. Sin preguntar al usuario.
- **Perfil de usuario auto-acumulable**: user_preference + scope:personal + topic_key preference/<area> para cada preferencia detectada.

### Changed
- **System prompt rediseñado 3 veces**: de reglas genéricas → reglas duras → voz de profesor. Ahora suena a profesor, no a instructivo.
- **Skills del agente lend-ai**: de 3 a 9 (agregadas lend-ai-docs, lend-ai-engram, lend-ai-testing, judgment-day, growth-engine, enhance-engine).
- **Modelo**: subido de T3 a T4 para mejor seguimiento de instrucciones complejas.
- **Regla #1 unificada**: Engram + GitHub en un solo flujo: guardar memoria → actualizar docs → commit → push.
- **engram-wrapper.sh**: ahora detecta engram via `command -v` con fallback a Homebrew.

### Fixed
- **CHANGELOG**: no se actualizaba con los cambios (este entry es la prueba).
- **System prompt**: antes era una lista de instrucciones, ahora tiene voz de profesor.
- **Skills no cargadas**: lend-ai-docs, lend-ai-engram, lend-ai-testing, judgment-day, growth-engine, enhance-engine existían como permisos pero no como skills cargadas.

## [0.5.3] - 2026-05-15

### Added
- **update.sh**: script de actualización segura — git pull, backup de opencode.json, verificación de MCPs (FastMCP, psycopg2), revisión de tokens de entorno, conteo de agentes, recordatorio de sync Engram. No sobrescribe `.env`, no rompe configuración existente.
- **Auto-stash en update.sh**: detecta archivos dirty de sesiones anteriores y los stash antes del pull para evitar conflictos.
- **Teaching Gates in system prompt**: 4 reglas de comportamiento inline en description de opencode.json: 3 opciones siempre, preguntar y esperar, enseñar mientras ejecutás, Post-Task Automation.
- **growth-engine + enhance-engine como task types**: registrados en task permissions y como agentes en opencode.json. Ahora se pueden spawnear via `task()`.

### Changed
- update.sh ahora detecta `SCRIPT_DIR` para funcionar desde cualquier directorio de checkout (no solo `~/.lend-ai`).
- System prompt: de título genérico a reglas de comportamiento explícitas.

### Fixed
- **tests**: 2 tests fallando por `frontend-mentor` (deprecado desde v0.4.0). Reemplazado por `frontend-senior`.
- update.sh: `{LEND_AI_HOME}` placeholder se reemplaza al copiar opencode.json.

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
