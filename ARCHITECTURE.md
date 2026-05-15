# Architecture

## Folder structure

```
lend-ai/
├── agents/manifests/    → YAML manifests for each agent
│   ├── lend-ai/         → Main orchestrator
│   ├── data-analyst/    → Data agent
│   ├── frontend-senior/ → Agente frontend
│   ├── devops/         → DevOps agent
│   ├── git-github/      → Git/GitHub agent
│   ├── engram-keeper/    → Memory keeper
│   └── ... (100+ agentes)
├── commands/            → Slash command documentation
├── data/                → Analysis data (gitignored)
├── docs/                → Guides and detailed documentation
├── mcp-servers/         → Custom MCP servers
├── openspec/            → SDD specifications
├── profiles/lend-ai/    → Identity and workflow profiles
├── registry/            → Central agent registry
├── schemas/             → Validation schemas
├── update.sh            → Safe update script (pull, backup, MCP check)
├── install.sh           → First-time installer
├── scripts/             → Utility scripts (model picker, etc)
├── skills/              → Skills with LEND Protocol
│   ├── data-*/          → Data analysis (23 skills)
│   ├── frontend-*/      → Frontend (8 skills)
│   ├── docker-engineer… → DevOps (5 skills)
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
├── git-github
│   ├── commits-real
│   ├── branch-pr
│   ├── chained-pr
│   ├── issue-creation
│   ├── gitops-engineer
│   └── shared-git-data
├── engram-keeper
│   └── lend-ai-engram
├── commits-real
├── lend-ai-engram
├── lend-ai-testing
└── lend-ai-docs
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
- `filesystem` — Project file access
- `github`, `slack`, `notion`, `google-drive` — External integrations
- `postgres`, `sqlite` — Databases
- `ocr`, `puppeteer`, `web-search` — Utilities
