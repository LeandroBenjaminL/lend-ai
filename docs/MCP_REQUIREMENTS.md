# Lend.Ai — MCP Requirements

## Auto (no config needed)

| MCP | Notes |
|-----|-------|
| `engram` | engram CLI |
| `sequential-thinking` | npx |
| `web-search` | npx (duckduckgo-mcp-server) |
| `agent-router` | Python + FastMCP SDK |
| `model-router` | Python + FastMCP SDK |

## System deps needed

| MCP | Install |
|-----|---------|
| `ocr` | `sudo apt install tesseract-ocr` |

## API tokens needed in `.env`

| MCP | Env var | Where to get it |
|-----|---------|-----------------|
| `github` | `GITHUB_TOKEN` | GitHub Settings → Developer settings → Personal access tokens |
| `notion` | `NOTION_TOKEN` | Notion → Settings → Integrations → New integration |
| `google-drive` | Google credentials | Google Cloud Console → APIs & Services |

Edit `~/.lend-ai/.env` and add your tokens after installation.
