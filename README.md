# Lend.Ai

> Unified AI agent ecosystem: Data Analysis, Frontend Development, DevOps, and Git/GitHub. Running on OpenCode with a hierarchical skill system, sub-agents, and tiered models (T1-T5) for cost-quality optimization.

Lend.Ai is a production-grade AI agent ecosystem that orchestrates **100 agents**, **70 skills**, and **17 MCPs** across four domains. It runs on [OpenCode](https://opencode.ai) and provides a senior mentor experience with automatic personality loading, memory persistence via Engram, and a spec-driven development (SDD) workflow.

## Quick Install

```bash
curl -sL https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/LeandroBenjaminL/lend-ai.git
cd lend-ai
chmod +x install.sh && ./install.sh
```

## Update

```bash
# Dentro del directorio lend-ai:
./update.sh
```

El update script:
1. Git pull de los últimos cambios
2. Backup y actualización de opencode.json
3. Verifica MCPs Python y tokens de entorno
4. Revisa consistencia de agentes

## Architecture

```
lend-ai (orchestrator — 9 direct sub-agents)
├── data-analyst         → data analysis, ML, ETL, reporting (9 sub-agents)
├── frontend-senior      → React, TypeScript, CSS, testing (10 sub-agents)
├── devops               → infrastructure, CI/CD, cloud, security (10 sub-agents)
├── git-github           → commits, PRs, issues, releases (5 sub-agents)
├── engram-keeper        → persistent memory management
├── commits-real         → unified commits, docs, versioning
├── lend-ai-engram       → memory context management
├── lend-ai-testing      → tests, CI, coverage
└── lend-ai-docs         → Google-style docstrings, ADR, architecture docs
```

Each orchestrator has an explicit **Arsenal** mapping: Core Protocols (always-on), Domain Sub-agents (when to spawn), and Task Skills (when to load, with exact file paths).

## Stats

| Metric | Value |
|--------|-------|
| Version | v0.5.0 |
| Agents | 100 |
| Skills | 70 (all with LEND Protocol) |
| Shared Protocols | 5 (skill-resolver, subagent-context, sdd-phase-common, engram-convention, persistence-contract) |
| MCPs | 17 |
| Commits | 3-level ceremony (direct, quick PR, full review) |

## Stack

- **Python 3.10+** for data science and infrastructure scripts
- **TypeScript 5.x** for frontend
- **OpenCode** as the agent platform
- **Models**: DeepSeek, Minimax, Qwen via T1-T5 tiers (free + paid)
- **Engram** for persistent memory between sessions
- **16 MCPs**: engram, filesystem, github, slack, notion, google-drive, postgres, sqlite, puppeteer, ocr, web-search, and more

## Enterprise Workflow

```
1. ISSUE     → create an issue describing the problem/feature
2. BRANCH    → git checkout -b type/issue-number-description
3. CODE      → implement changes
4. COMMIT    → conventional commits in English US
5. PR        → open PR with description, screenshots, testing
6. REVIEW    → assign reviewer, wait for approval
7. MERGE     → reviewer merges to main
8. DOCS      → update documentation if needed
9. ENGRAM    → save decisions and changes
```

All commits, PRs, issues, and documentation are in **English US**.

## Documentation

| File | Purpose |
|------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and agent hierarchy |
| [AGENTS.md](AGENTS.md) | Complete skill and agent index |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Development commands and ADRs |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [docs/MCP_REQUIREMENTS.md](docs/MCP_REQUIREMENTS.md) | MCP dependencies and token setup |
| [docs/](docs/) | Detailed guides |

## Key Protocols

| Protocol | File | Purpose |
|----------|------|---------|
| **Persona Scope** | `profiles/lend-ai/persona.md` | Separates chat tone from generated artifacts |
| **Skill Resolver** | `skills/_shared/skill-resolver.md` | Injects compact rules into sub-agent prompts |
| **Sub-agent Context** | `skills/_shared/subagent-context.md` | Who reads/writes in each SDD phase |
| **SDD Phase Common** | `skills/_shared/sdd-phase-common.md` | Return envelope, persistence, workload guard |
| **Delegation Triggers** | `profiles/lend-ai/workflow.md` | 6 mandatory stop rules for the orchestrator |
| **Output Style** | `profiles/lend-ai/output-style.md` | Response length contract and tone rules |

## Key Skills

| Domain | Skills |
|--------|--------|
| **Data Analysis** | data-analysis, data-cleaning, ml-modeling, time-series, sql-analysis, etl-pipelines, reporting, streamlit, web-scraping (23 total) |
| **Frontend** | frontend-react-development, frontend-css-styling, frontend-type-script, frontend-api-integration, frontend-testing, frontend-web-performance (8 total) |
| **DevOps** | docker-engineer, ci-cd-pilot, cloud-architect, infra-sre, security-auditor, network-engineer, gitops-engineer, backup-engineer, perf-engineer, db-admin (10 total) |
| **Git/GitHub** | commits-real, branch-pr, chained-pr, issue-creation, gitops-engineer, shared-git-data (6 total) |
| **SDD** | sdd-init → sdd-onboard (10 total) |
| **Global** | lend-ai-persona, engram-memory-system, senior-orchestrator, commits-real, judgment-day, skill-creator, skill-registry, and more |

All skills follow the **LEND Protocol**: Trigger → Analyze → Offer (3 options) → Choose → Execute → Verify.

## Commands

| Command | What it does |
|---------|--------------|
| `make test` | Run tests |
| `make lint` | Run linter (ruff) |
| `/model list` | View agents and skills with their models |
| `/model set agent <name> <tier>` | Change model for an agent |

## Personality

Lend.Ai loads automatically with the **AISHA Engine** personality:
- Senior mentor tone (Rioplatense Spanish)
- The **Senior Menu**: always 3 options with pros/cons
- **LEND Protocol**: Analyze → Options → Choose → Execute → Verify
- **Teaching method**: explain before, narrate during, summarize after
- **Engram always**: consult before, save after every change

## License

MIT © 2026 Leandro Benjamin L.
