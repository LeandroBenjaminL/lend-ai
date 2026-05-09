#!/usr/bin/env bash
# Wrapper para easy-notion-mcp: carga NOTION_TOKEN desde .env
set -a
source "$(dirname "$0")/../.env"
set +a
exec npx -y easy-notion-mcp
