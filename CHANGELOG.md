# Changelog

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
