# Security Policy

## Scope

Lend.Ai orchestrates MCP servers with access to:
- **GitHub API** (tokens, repos, issues, PRs)
- **Google Drive** (documents, sheets, files)
- **Notion** (pages, databases)
- **Engram** (local SQLite memory database)
- **File system** (read/write/execute access)

All security practices apply to the `lend-ai` repository and its ecosystem.

## Reporting a Vulnerability

If you discover a security vulnerability in Lend.Ai, **do not open a public issue**.

Instead, report it privately via email to the repository owner at the address listed in the commit history. You should expect an acknowledgment within 48 hours and a remediation plan within 7 days.

## Token Security

- **Never commit tokens** to the repository. All secrets go in `.env` (gitignored).
- The `.env.template` file documents required environment variables without real values.
- Regularly rotate tokens configured in Google Drive, Notion, and GitHub integrations.
- If a token is exposed, revoke it immediately and rotate all tokens that share the same scope.

## MCP Server Security

- All MCP servers run locally via stdio or connect to first-party APIs with OAuth.
- No MCP server listens on network ports by default.
- Review MCP server code before adding new ones to `opencode.json`.
- Third-party MCPs (npx-based) should be pinned to specific versions.

## CI/CD Security

- All CI workflows in `.github/workflows/` run in isolated Ubuntu runners.
- Secrets are injected via GitHub Actions secrets, never hardcoded.
- Workflow files must pass `test_ci_workflows.py` validation before merge.

## Dependencies

- Python dependencies are pinned in `requirements.txt` and `requirements-dev.txt`.
- Review dependency updates for breaking changes or security patches.
- Run `pip audit` or equivalent before major dependency upgrades.

## Data Privacy

- Engram SQLite database stores session memory locally on the host machine.
- No telemetry or usage data is sent to external services.
- Google Drive and Notion access follow OAuth scopes — limit to minimum required.
