# Lend.Ai — MCP Requirements

Each MCP server needs certain dependencies to work.

## Auto (no config needed)

| MCP | Notes |
|-----|-------|
| `engram` | engram CLI |
| `sequential-thinking` | npx |
| `filesystem` | npx, path set during install |
| `web-search` | npx (duckduckgo-mcp-server) |
| `sqlite` | npx |
| `agent-router` | Python + FastMCP SDK |
| `model-router` | Python + FastMCP SDK |

## System deps needed

| MCP | Install |
|-----|---------|
| `ocr` | `sudo apt install tesseract-ocr` |
| `puppeteer` | `sudo apt install chromium-browser` |

## Running service needed

| MCP | Needs |
|-----|-------|
| `postgres` | PostgreSQL server running + psycopg2 (auto-installed) |

## API tokens needed in `.env`

| MCP | Env var | Where to get it |
|-----|---------|-----------------|
| `github` | `GITHUB_TOKEN` | GitHub Settings → Developer settings → Personal access tokens |
| `notion` | `NOTION_TOKEN` | Notion → Settings → Integrations → New integration |
| `slack` | Slack tokens | Slack API → Your apps → OAuth tokens |
| `google-drive` | Google credentials | Google Cloud Console → APIs & Services |
| `smtp-email` | SMTP_HOST, SMTP_USER, SMTP_PASS | Your email provider |

Edit `~/.lend-ai/.env` and add your tokens after installation.
