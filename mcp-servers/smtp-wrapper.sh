#!/usr/bin/env bash
# Wrapper para @souluanf/mcp-smtp: carga credenciales SMTP desde .env
set -a
source "$(dirname "$0")/../.env"
set +a
exec npx -y @souluanf/mcp-smtp@latest
