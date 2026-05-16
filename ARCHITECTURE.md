# Architecture

## Folder structure

```
lend-ai/
├── agents/manifests/    → YAML manifests for each agent
│   ├── lend-ai.yaml     → Main orchestrator
│   ├── data-analyst.yaml → Data agent
│   ├── frontend-senior.yaml → Frontend agent
│   ├── devops.yaml      → DevOps agent
│   ├── engram-keeper.yaml → Memory keeper
│   └── ... (88+ agent manifests)
├── commands/            → Slash command documentation
├── data/                → Analysis data (gitignored)
├── docs/                → Guides and detailed documentation
├── mcp-servers/         → Custom MCP servers
├── openspec/            → SDD specifications
├── profiles/lend-ai/    → Identity and workflow profiles
├── registry/            → Central agent registry
├── schemas/             → Validation schemas
├── update.sh            → Safe update script (Linux/macOS)
├── update.ps1           → Safe update script (Windows)
├── install.sh           → First-time installer (Linux/macOS)
├── install.ps1          → First-time installer (Windows)
├── scripts/             → Utility scripts (model picker, etc)
├── skills/              → Skills with LEND Protocol
│   ├── data-*/          → Data analysis (23 skills)
│   ├── frontend-*/      → Frontend (8 skills)
│   ├── docker-engineer… → DevOps (10 skills)
│   ├── sdd-*/           → SDD (10 skills)
│   ├── commits-real,…   → Transversales (12 skills)
│   └── lend-ai-*/       → Skills del ecosistema
└── tests/               → Tests
```

## Agents

```
lend-ai (orchestrator)
├── data-analyst
│   ├── data-explorer
│   ├── data-modeler
│   ├── data-reporter
│   ├── data-etl
│   └── ...
├── frontend-senior
│   ├── framework-architect
│   ├── ui-crafter
│   ├── styling-engineer
│   └── ...
├── devops
│   ├── docker-engineer
│   ├── ci-cd-pilot
│   ├── cloud-architect
│   ├── db-admin
│   ├── infra-sre
│   ├── security-auditor
│   ├── network-engineer
│   ├── gitops-engineer
│   ├── backup-engineer
│   └── perf-engineer
├── engram-keeper
│   └── lend-ai-engram
├── growth-engine        → meta-learning, pattern detection
├── enhance-engine       → parallel improvement (10 perspectives)
├── content-engine       → Engram analysis, LinkedIn content
├── lend-ai-mentor       → project protocol, professor behavior
├── commits-real
├── lend-ai-engram
├── lend-ai-testing
├── lend-ai-docs
└── judgment-day         → adversarial review
```

## Models and Tiers

| Tier | Model | Cost | Use |
|------|--------|-------|-----|
| T1 | Minimax Free | Free | Mechanical tasks (cleaning, formatting) |
| T2 | Minimax Free | Free | Simple reports, validations |
| T3 | Big Pickle | Free | EDA, general analysis (default) |
| T4 | DeepSeek V4 Flash | Low | Architecture, complex ML |
| T5 | DeepSeek V4 Pro | High | Very difficult problems |

Ver `model-routing.config.json` y `scripts/model-commands.py`.

### Model Profiles (Preset System)

| Profile | Default Tier | Use |
|---------|-------------|-----|
| `free` | T3-balanced | Todo gratis, máximo ahorro |
| `balanced` | T3-balanced | Mayormente gratis, premium cuando vale la pena (activo) |
| `fast` | T2-fast | Rápido y barato, para tareas simples |
| `power` | T5-deep | Máxima potencia, reasoning profundo |
| `reasoning` | T4-reasoning | Para tareas que requieren razonamiento |

Cada profile puede tener overrides por skill. Ver `model-routing.config.json` → `profiles`.

### Backup & Recovery

- **Pre-commit hook**: GGA (Gentleman Git Audit) ejecuta review de código antes de cada commit
- **Model routing config**: respaldado en `model-routing.config.json` con schema validation
- **Agent manifests**: versionados en git, cada cambio deja trail en CHANGELOG
- **Engram**: memoria persistente con SQLite+FTS5, journal WAL, auto-checkpoint

## Shared Protocols

| Protocol | File | Purpose |
|----------|------|---------|
| Skill Resolver | `skills/_shared/skill-resolver.md` | Cómo inyectar skills en sub-agentes |
| Sub-agent Context | `skills/_shared/subagent-context.md` | Quién lee/escribe qué en cada fase |
| SDD Phase Common | `skills/_shared/sdd-phase-common.md` | Protocolo común para todas las fases SDD |
| Engram Convention | `skills/_shared/engram-convention.md` | Naming y recovery de artifacts |
| Persistence Contract | `skills/_shared/persistence-contract.md` | Modos de artifact store |

## Key technical decisions

| Decision | Chosen | Alternatives |
|----------|---------|--------------|
| Model routing | Custom tier system | OpenRouter, LiteLLM |
| Platform | OpenCode | Cline, Aider |
| Skill system | SKILL.md + YAML manifests | Prompts only |

## MCP Servers

- `engram` — Persistent memory between sessions
- `agent-router` — Agent resolution and routing
- `model-router` — Model assignment by tier
- `sequential-thinking` — Structured reasoning
- `web-search` — DuckDuckGo web search
- `context7` — Library documentation
- `github` — GitHub API integration
- `notion` — Notion API integration
- `google-drive` — Google Drive/Docs/Sheets/Slides
- `ocr` — Image text extraction
