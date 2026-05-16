# Lend.Ai

[![CI](https://github.com/LeandroBenjaminL/lend-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/LeandroBenjaminL/lend-ai/actions/workflows/ci.yml)

> Unified AI agent ecosystem: Data Analysis, Frontend Development, DevOps, and SDD. Running on OpenCode with a hierarchical skill system, sub-agents, and tiered models (T1-T5) for cost-quality optimization.

Lend.Ai is a production-grade AI agent ecosystem that orchestrates **88 agents**, **73 skills**, and **17 MCPs** across four domains. It runs on [OpenCode](https://opencode.ai) and provides a senior mentor experience with automatic personality loading, memory persistence via Engram, and a spec-driven development (SDD) workflow.

## CI Rule

**Tests must pass before push or merge.** If `ci.yml` fails, fix the issue before pushing.

```bash
# Run tests locally before pushing
pip install -r requirements.txt
pytest tests/ -v
```

## Quick Install

**Linux / macOS:**
```bash
curl -sL https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.ps1 | iex
```

Or manually:
```bash
git clone https://github.com/LeandroBenjaminL/lend-ai.git
cd lend-ai
./install.sh        # Linux/macOS
./install.ps1       # Windows
```

## Update

**Linux / macOS:**
```bash
./update.sh
```

**Windows:**
```powershell
./update.ps1
```

The update script:
1. Stashes local changes automatically
2. Pulls the latest version
3. Backs up and updates opencode.json
3. Verifica MCPs Python y tokens de entorno
4. Revisa consistencia de agentes

## Architecture

```
lend-ai (orchestrator — 13 direct sub-agents)
├── data-analyst         → data analysis, ML, ETL, reporting (9 sub-agents)
├── frontend-senior      → React, TypeScript, CSS, testing (10 sub-agents)
├── devops               → infrastructure, CI/CD, cloud, security (10 sub-agents)
├── engram-keeper        → persistent memory management
├── commits-real         → unified commits, docs, versioning
├── lend-ai-engram       → memory context management
├── lend-ai-testing      → tests, CI, coverage
├── lend-ai-docs         → Google-style docstrings, ADR, architecture docs
├── growth-engine        → meta-learning, pattern detection, ecosystem improvement
├── enhance-engine       → parallel improvement from 10 perspectives
├── content-engine       → Engram analysis, doc sync, LinkedIn content
├── lend-ai-mentor       → project protocol + professor behavior + user profile
└── judgment-day         → adversarial code review
```

Each orchestrator has an explicit **Arsenal** mapping: Core Protocols (always-on), Domain Sub-agents (when to spawn), and Task Skills (when to load, with exact file paths).

## Stats

| Metric | Value |
|--------|-------|
| Version | v0.7.0 |
| Agents | 88 |
| Skills | 73 (all with LEND Protocol) |
| Shared Protocols | 5 |
| MCPs | 9 |
| CI | Passing required before push |
| Commits | 3-level ceremony (direct, quick PR, full review) |

## Stack

- **Python 3.10+** for data science and infrastructure scripts
- **TypeScript 5.x** for frontend
- **OpenCode** as the agent platform
- **Models**: DeepSeek, Minimax via T1-T5 tiers (free + paid)
- **Engram** for persistent memory between sessions
- **9 MCPs**: engram, sequential-thinking, web-search, github, context7, google-drive, notion, ocr, agent-router, model-router

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
| **Transversal** | commits-real, branch-pr, chained-pr, issue-creation, shared-git-data |
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
- The **Senior Menu**: 3 options when real tradeoffs exist, direct answers otherwise
- **LEND Protocol**: Analyze → Options → Choose → Execute → Verify
- **Teaching method**: explain before, narrate during, summarize after
- **Engram always**: consult before, save after every change

## License

MIT © 2026 Leandro Benjamin L.
