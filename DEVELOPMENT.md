# Development

## Quick Start

```bash
# Python 3.10+ required
python -m venv .venv           # Create virtual environment
source .venv/bin/activate      # Activate (Linux/macOS)
.venv\Scripts\activate         # Activate (Windows)

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Optional: dev deps (ruff, pytest, mypy)

# Copy environment config
cp .env.template .env
# Edit .env with your tokens (GitHub, Notion, Google Drive)

# Run basic checks
ruff check .                   # Lint all Python files
ruff format . --check          # Check formatting
pytest                         # Run all tests
pytest --cov=src               # Tests with coverage
pytest -k "model"              # Filtered tests
```

## Project Architecture

The ecosystem follows a **3-level agent hierarchy**:

| Layer | Role | Examples |
|-------|------|----------|
| **N1 — System Skills** | Always loaded in primary chat. Define persona, memory, workflow. | `lend-ai-persona`, `lend-ai-mentor`, `commits-real` |
| **N2 — Domain Supervisors** | Receive tasks from orchestrator, spawn sub-agents. | `data-analyst`, `frontend-senior`, `devops` |
| **N3 — Specialists** | Execute concrete tasks. No further delegation. | `data-cleaning`, `ml-modeling`, `ui-crafter` |

Key files:
- [`AGENTS.md`](AGENTS.md) — Skills index, session workflow protocol
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — Folder structure, agent tree, tiers, MCP servers
- [`skills/`](skills/) — All skill definitions (SKILL.md + resources)
- [`agents/manifests/`](agents/manifests/) — YAML manifests per agent
- [`opencode.json`](opencode.json) — Agent definitions, tool permissions, MCP config, skills
- [`model-routing.config.json`](model-routing.config.json) — Tier-to-model mapping, overrides

## Common Workflows

### Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter (name, description, trigger) and full instructions.
2. Register the skill in [`AGENTS.md`](AGENTS.md) — add a row to the skills table.
3. If the skill needs a dedicated sub-agent, add an entry in [`opencode.json`](opencode.json) under `agent` with `mode: "subagent"`.
4. Optionally add a tier mapping in `model-routing.config.json` → `skills` section.
5. Run `python3 scripts/skill-health-check.py` to validate consistency.

**Reference**: Existing skills at `skills/lend-ai-docs/SKILL.md` follow the standard structure.

### Adding a New Agent

1. Create `agents/manifests/<agent-name>.yaml` with agent metadata and sub-agent references.
2. Add the agent entry in [`opencode.json`](opencode.json) under `agent`:
   - Set `mode: "subagent"` and `hidden: true`
   - Configure `tools` (bash, edit, read, write, delegate, etc.)
   - Add `skills` array referencing existing skill names
   - Add `permission.task` entries for sub-agents it can spawn (`"*": "allow"` for all, or explicit allowlist)
3. If it needs a tier assignment, add an override in `model-routing.config.json` → `overrides.agents`.
4. Update [`AGENTS.md`](AGENTS.md) if it's a domain supervisor (N2) visible to the user.

### Adding a New MCP Server

1. Write the server script in `mcp-servers/<name>.py` (or use a stdio/remote server).
2. Add an entry in [`opencode.json`](opencode.json) under `mcp`:
   - **Local (stdio)**: `{ "type": "local", "command": ["python", "mcp-servers/<name>.py"] }`
   - **Remote HTTP**: `{ "type": "remote", "url": "https://..." }`
   - **npx-based**: `{ "type": "local", "command": ["npx", "-y", "package-name"] }`
3. Restart opencode for the new MCP to be available.
4. Test with: `python3 mcp-servers/<name>.py` (it should start without errors).

### Changing Model Tiers

The model routing system maps tasks to LLM tiers (T1–T5) to balance cost and quality.

```bash
# View current active tier and all model assignments
python3 scripts/model-commands.py list

# View all available tiers and their models
python3 scripts/model-commands.py tiers

# Set an override for a specific agent
python3 scripts/model-commands.py set-agent <agent-name> <tier>

# Set an override for a specific skill
python3 scripts/model-commands.py set-skill <skill-name> <tier>

# Reset an agent or skill to its profile default (removes override)
python3 scripts/model-commands.py reset-agent <agent-name>
python3 scripts/model-commands.py reset-skill <skill-name>
```

Or edit `model-routing.config.json` directly:

| Tier | Model | Cost | Use |
|------|-------|------|-----|
| T1 | MiniMax Free | Free | Reading, exploration, profiling |
| T2 | Big Pickle | Free | Daily simple tasks |
| T3 | MiniMax Free | Free | Balanced default for most work |
| T4 | DeepSeek V4 Flash | Low | Complex tasks (ML, design) |
| T5 | DeepSeek V4 Pro | High | Architecture, critical decisions |

Profiles (`eco`, `balanced`, `rapido`, `power`) batch-override the `default_tier` and specific skill/agent tiers. Switch the active profile by editing `model-routing.config.json` → `active_profile`, then restart opencode.

## Health Checks

### Skill Ecosystem Health

```bash
python3 scripts/skill-health-check.py
```

Validates:
- Every SKILL.md is present and parseable in `skills/<name>/`
- Every skill referenced in `opencode.json` and `model-routing.config.json` has a valid directory
- AGENTS.md entries match existing skills
- No orphan skills (present on disk but not registered)

**How to fix failures**:
- `missing SKILL.md` → Create the skill directory with a valid SKILL.md (see existing skills for template)
- `unregistered skill` → Add the skill reference to `opencode.json` → `agent.<name>.skills` array
- `orphan skill` → Either register it or delete the directory
- `invalid YAML` → Fix syntax in the offending SKILL.md frontmatter

### Agent Router Health

```bash
python3 mcp-servers/agent-router.py --health
```

### Model Router Health

```bash
python3 mcp-servers/model-router.py list
python3 mcp-servers/model-router.py get-tier
```

## Debugging

### MCP Servers

```bash
# List all MCP server implementations
ls mcp-servers/

# Test an individual MCP server
python3 mcp-servers/agent-router.py --health
python3 mcp-servers/model-router.py list
python3 mcp-servers/model-router.py get-tier

# If a server fails to start, check:
# 1. Required Python packages are installed (pip list | grep mcp)
# 2. The script has no syntax errors (python3 -c "compile(open('mcp-servers/<name>.py').read(), '<name>', 'exec')")
# 3. Environment variables are set in .env (for servers that need them)
```

### Sub-Agent Failures

When a sub-agent fails to run or is not found:

1. **Check agent definition** — Is the agent defined in `opencode.json` under `agent`?
2. **Check task permissions** — The parent agent's `permission.task` must include `"<sub-agent-name>": "allow"`. Missing permissions are the most common cause of sub-agent failures.
3. **Check skill references** — The sub-agent needs `skills` array in its config to load the right instructions.
4. **Check YAML manifest** — If using `agents/manifests/`, ensure the YAML is valid and matches the agent name.
5. **Check model tier** — Run `python3 scripts/model-commands.py list` and verify the agent has a tier assigned (either via profile default or override).

### Agent Router

```bash
# Test agent resolution
python3 mcp-servers/agent-router.py --health

# Resolve a specific task to an agent (from within opencode)
# Use the agent-router MCP tool resolve_task()
```

## Engram Recovery

Engram is the persistent memory system (SQLite + FTS5).

### Database Location

```
~/.engram/engram.db       # Main database
~/.engram/engram.db-wal   # Write-ahead log (can be deleted safely if DB is closed)
~/.engram/engram.db-shm   # Shared memory file (deleted automatically)
~/.engram/chunks/          # Large binary storage — never delete manually
```

### Backup

```bash
# Windows (PowerShell)
powershell -File scripts/backup-engram.ps1

# Linux/macOS
bash scripts/backup.sh create
```

Backups are stored in `backups/engram/` with timestamped folders. The script keeps the last 7 backups automatically.

### Recovery from Corruption

1. **Stop opencode** (close the session).
2. **Restore from latest backup** in `backups/engram/`:
   - Copy the timestamped backup folder's `engram.db` to `~/.engram/engram.db`
   - Delete `~/.engram/engram.db-wal` and `~/.engram/engram.db-shm` if present
3. **Verify integrity**: `python3 -c "import sqlite3; c=sqlite3.connect(r'~/.engram/engram.db'); c.execute('PRAGMA integrity_check'); print(c.fetchall())"`
4. **Restart opencode** — the session should load clean memory.

### Safety Rules

- **Never** delete `~/.engram/chunks/` manually — this can corrupt memory links.
- **Never** edit `engram.db` while opencode is running (WAL journal may be active).
- Always run `backup-engram.ps1` before any major upgrade or config change.
- If you see repeated "database disk image is malformed" errors, stop work immediately and restore from backup.

## Commands Reference

```bash
# ── Environment ─────────────────────────────────────────
python -m venv .venv                     # Create virtual environment
source .venv/bin/activate                # Activate (Linux/macOS)
.venv\Scripts\activate                   # Activate (Windows)
pip install -r requirements.txt          # Install deps
pip install -r requirements-dev.txt      # Install dev deps

# ── Lint & Format ──────────────────────────────────────
ruff check .                             # Lint all files
ruff format .                            # Auto-format
ruff format . --check                    # Check formatting

# ── Testing ─────────────────────────────────────────────
pytest                                   # Run all tests
pytest --cov=src                         # Tests with coverage
pytest -k "model"                        # Filter by keyword

# ── Model Routing ───────────────────────────────────────
python3 scripts/model-commands.py list               # View all tiers
python3 scripts/model-commands.py tiers              # Available tiers
python3 scripts/model-commands.py set-agent <a> <t>  # Override agent tier
python3 scripts/model-commands.py set-skill <s> <t>  # Override skill tier
python3 scripts/model-commands.py reset-agent <a>    # Remove agent override
python3 scripts/model-commands.py reset-skill <s>    # Remove skill override

# ── MCP Servers ────────────────────────────────────────
python3 mcp-servers/agent-router.py --health         # Test agent router
python3 mcp-servers/model-router.py list             # List models/tiers
python3 mcp-servers/model-router.py get-tier         # Show active tier

# ── Health Checks ──────────────────────────────────────
python3 scripts/skill-health-check.py                # Validate ecosystem

# ── Engram Backup ──────────────────────────────────────
powershell -File scripts/backup-engram.ps1   # Backup engram (Windows)
bash scripts/backup.sh create               # Full ecosystem backup (Linux/macOS)

# ── ADRs ───────────────────────────────────────────────
cp docs/adr/TEMPLATE.md docs/adr/XXX-titulo-breve.md  # New ADR
# Fill in: Context → Decision → Consequences → Status
```

## ADR (Architecture Decision Records)

Technical decisions are documented in `docs/adr/`.

### Active ADRs

| # | Decision | Status |
|---|----------|--------|
| 001 | Use pathlib instead of os.path | Accepted |
| 002 | Model tier system (T1–T5) | Accepted |
| 003 | OpenCode as agent platform | Accepted |
| 004 | Skills as executable sub-agents | Accepted |

### Creating an ADR

```bash
cp docs/adr/TEMPLATE.md docs/adr/XXX-descriptive-title.md
# Complete: Context → Decision → Consequences → Status
```

## Troubleshooting

### Agente no delega correctamente
```bash
# Verificar que agent-router está corriendo
python3 mcp-servers/agent-router.py --health

# Ver qué agentes están registrados
python3 scripts/model-commands.py list
```

### Engram no responde
```bash
# Verificar servidor Engram
bash engram-wrapper.sh --health

# Restaurar backup si hay corrupción
cp ~/.engram/engram.db.bak ~/.engram/engram.db
```

### Agregar un MCP nuevo
1. Agregar config en `opencode.json` bajo `mcp` (nota: no es mcpServers)
2. Agregar token necesario en `.env`
3. Documentar en `docs/MCP_REQUIREMENTS.md`
4. Correr `./update.sh` para verificar consistencia
```
