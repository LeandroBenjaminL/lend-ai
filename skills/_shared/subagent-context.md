# Sub-Agent Context Protocol

Sub-agents get a FRESH context with NO memory of previous interactions. The orchestrator controls what context they receive.

## Non-SDD Tasks (general delegation)

- **Read context**: Orchestrator searches engram (`mem_search`) for relevant prior context and passes it in the sub-agent prompt. Sub-agent does NOT search engram itself.
- **Write context**: Sub-agent MUST save significant discoveries, decisions, or bug fixes to engram via `mem_save` before returning. Sub-agent has full detail — save before returning, not after.
- Always add to sub-agent prompt: `"If you make important discoveries, decisions, or fix bugs, save them to engram via mem_save with project: '{project}'."`
- **Skills**: Orchestrator resolves compact rules from the registry and injects them as `## Project Standards (auto-resolved)` in the sub-agent prompt. Sub-agents do NOT read SKILL.md files — they receive rules pre-digested.

## SDD Phases

Each phase has explicit read/write rules:

| Phase | Reads | Writes |
|-------|-------|--------|
| `sdd-explore` | nothing | `explore` |
| `sdd-propose` | exploration (optional) | `proposal` |
| `sdd-spec` | proposal (required) | `spec` |
| `sdd-design` | proposal (required) | `design` |
| `sdd-tasks` | spec + design (required) | `tasks` |
| `sdd-apply` | tasks + spec + design + apply-progress (if exists) | `apply-progress` |
| `sdd-verify` | spec + tasks + apply-progress | `verify-report` |
| `sdd-archive` | all artifacts | `archive-report` |

For phases with required dependencies, sub-agent reads directly from the backend — orchestrator passes artifact references (topic keys or file paths), NOT content itself.

## Strict TDD Forwarding (MANDATORY)

When launching `sdd-apply` or `sdd-verify` sub-agents, the orchestrator MUST:

1. Search for testing capabilities: `mem_search(query: "sdd-init/{project}", project: "{project}")`
2. If the result contains `strict_tdd: true`:
   - Add to the sub-agent prompt: `"STRICT TDD MODE IS ACTIVE. You MUST follow strict-tdd.md. Do NOT fall back to Standard Mode."`
   - This is NON-NEGOTIABLE. Do not rely on the sub-agent discovering this independently.
3. If the search fails or `strict_tdd` is not found, do NOT add the TDD instruction.

## Apply-Progress Continuity (MANDATORY)

When launching `sdd-apply` for a continuation batch (not the first batch):

1. Search for existing apply-progress: `mem_search(query: "sdd/{change-name}/apply-progress", project: "{project}")`
2. If found, add to the sub-agent prompt: `"PREVIOUS APPLY-PROGRESS EXISTS at topic_key 'sdd/{change-name}/apply-progress'. You MUST read it first via mem_search + mem_get_observation, merge your new progress with the existing progress, and save the combined result. Do NOT overwrite — MERGE."`
3. If not found (first batch), no special instruction needed.

This prevents progress loss across batches.

## Artifact Store Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| `engram` | Persistent memory across sessions, no filesystem artifacts | Default. Solo work, fast iteration. |
| `openspec` | File-based artifacts in `openspec/` directory | Team projects, committable artifacts, git history. |
| `hybrid` | Both engram + openspec | Cross-session recovery + team sharing. Higher token cost. |
| `none` | Return results inline only | Quick explorations, throwaway changes. |
