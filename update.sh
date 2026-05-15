#!/usr/bin/env bash
# ============================================================================
# Lend.Ai — Update Script
# Actualiza el ecosistema sin romper MCPs ni configs existentes.
#
# Usage:
#   ./update.sh
#   # o desde cualquier lugar:
#   ${LEND_AI_HOME}/update.sh
# ============================================================================

set -euo pipefail

# ============================================================================
# Config
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEND_AI_HOME="${LEND_AI_HOME:-}"
if [ -z "${LEND_AI_HOME}" ]; then
    if [ -d "${HOME}/.lend-ai" ]; then
        LEND_AI_HOME="${HOME}/.lend-ai"
    elif [ -f "${SCRIPT_DIR}/opencode.json" ]; then
        LEND_AI_HOME="${SCRIPT_DIR}"
    else
        echo "No se encuentra LEND.AI. Especificá LEND_AI_HOME o ejecutá install.sh primero."
        echo "  curl -sL https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.sh | bash"
        exit 1
    fi
fi
OPENCODE_CONFIG="${HOME}/.config/opencode/opencode.json"
OPENCODE_BACKUP="${HOME}/.config/opencode/opencode.json.backup.$(date +%Y%m%d-%H%M%S)"
LEND_ENV="${LEND_AI_HOME}/.env"
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# ============================================================================
# Colores
# ============================================================================

setup_colors() {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'
}
setup_colors

info()    { echo -e "${BLUE}[info]${NC}    $*"; }
success() { echo -e "${GREEN}[ok]${NC}      $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC}    $*"; }
error()   { echo -e "${RED}[error]${NC}   $*" >&2; }

# ============================================================================
# 1. Check current state
# ============================================================================

echo -e "\n${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Lend.Ai — Update v0.5.2                      ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}\n"

if [ ! -d "${LEND_AI_HOME}" ]; then
    error "No se encuentra LEND.AI en ${LEND_AI_HOME}"
    echo "Ejecutá install.sh primero:"
    echo "  curl -sL https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.sh | bash"
    exit 1
fi

cd "${LEND_AI_HOME}"

CURRENT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

info "Lend.Ai home: ${LEND_AI_HOME}"
info "Branch:       ${CURRENT_BRANCH}"
info "Commit:       ${CURRENT_COMMIT}"

# ============================================================================
# 2. Check for unpushed changes
# ============================================================================

if ! git diff --quiet HEAD 2>/dev/null; then
    warn "Tenés cambios locales sin commitear (archivos de otra sesión):"
    git status --short | head -10
    echo ""
    info "Se van a stash para que el pull sea limpio."
    git stash --include-untracked || true
fi

# ============================================================================
# 3. Git pull
# ============================================================================

echo ""
step "Pulling latest changes..."

if ! git pull origin "${CURRENT_BRANCH}" 2>/dev/null; then
    error "Git pull falló. Revisá si hay conflictos."
    exit 1
fi

NEW_COMMIT=$(git rev-parse --short HEAD)
if [ "$CURRENT_COMMIT" != "$NEW_COMMIT" ]; then
    success "Actualizado: ${CURRENT_COMMIT} → ${NEW_COMMIT}"
    echo ""
    git log --oneline "${CURRENT_COMMIT}..${NEW_COMMIT}" 2>/dev/null | head -20
else
    info "Ya estás en la última versión (${CURRENT_COMMIT})."
fi

# ============================================================================
# 4. Backup and update opencode.json
# ============================================================================

echo ""
step "Updating opencode.json..."

if [ -f "${OPENCODE_CONFIG}" ]; then
    cp "${OPENCODE_CONFIG}" "${OPENCODE_BACKUP}"
    info "Backup creado: ${OPENCODE_BACKUP}"
fi

cp "${LEND_AI_HOME}/opencode.json" "${OPENCODE_CONFIG}"
success "opencode.json actualizado en ~/.config/opencode/"

# ============================================================================
# 5. Check MCP dependencies
# ============================================================================

echo ""
step "Verifying MCPs..."

MCP_OK=0
MCP_FAIL=0

# Python MCPs
if python3 -c "from mcp.server.fastmcp import FastMCP" &>/dev/null 2>&1; then
    success "FastMCP SDK — agent-router, model-router"
    ((MCP_OK++))
else
    warn "FastMCP SDK — corré: pip install mcp"
    ((MCP_FAIL++))
fi

if python3 -c "import psycopg2" &>/dev/null 2>&1; then
    success "psycopg2 — postgres MCP"
    ((MCP_OK++))
else
    warn "psycopg2 — corré: pip install psycopg2-binary"
    ((MCP_FAIL++))
fi

# Environment variables
if [ -f "${LEND_ENV}" ]; then
    if grep -q "GITHUB_TOKEN=" "${LEND_ENV}" 2>/dev/null && ! grep -q "GITHUB_TOKEN=$" "${LEND_ENV}" 2>/dev/null; then
        success "GITHUB_TOKEN configurado — github MCP"
        ((MCP_OK++))
    else
        warn "GITHUB_TOKEN vacío — github MCP necesita token en .env"
        ((MCP_FAIL++))
    fi
    if grep -q "NOTION_TOKEN=" "${LEND_ENV}" 2>/dev/null && ! grep -q "NOTION_TOKEN=$" "${LEND_ENV}" 2>/dev/null; then
        success "NOTION_TOKEN configurado — notion MCP"
        ((MCP_OK++))
    else
        warn "NOTION_TOKEN vacío — notion MCP necesita token en .env"
        ((MCP_FAIL++))
    fi
    if grep -q "SMTP_HOST=" "${LEND_ENV}" 2>/dev/null && ! grep -q "SMTP_HOST=$" "${LEND_ENV}" 2>/dev/null; then
        success "SMTP configurado — smtp-email MCP"
        ((MCP_OK++))
    else
        info "SMTP sin configurar — smtp-email no disponible (opcional)"
    fi
else
    warn "No se encontró .env — los MCPs que requieren tokens no funcionarán"
fi

echo ""
if [ "$MCP_FAIL" -eq 0 ]; then
    success "${MCP_OK} MCPs verificados, 0 fallos"
else
    warn "${MCP_OK} MCPs OK, ${MCP_FAIL} MCPs necesitan atención"
fi

# ============================================================================
# 6. Check agent manifests vs opencode.json
# ============================================================================

echo ""
step "Checking agent consistency..."

MANIFEST_COUNT=$(ls "${LEND_AI_HOME}/agents/manifests/"*.yaml 2>/dev/null | wc -l)
CONFIG_AGENTS=$(grep -c '"description"' "${OPENCODE_CONFIG}" 2>/dev/null || echo "?")

info "${MANIFEST_COUNT} agent manifests en disco"
info "Config actualizada con todos los agentes"

# ============================================================================
# 7. Engram sync reminder
# ============================================================================

echo ""
step "Engram sync..."

if [ -d "${HOME}/.engram/.git" ]; then
    info "Engram data tiene repo git en ~/.engram/"
    echo "  Recordá sincronizar: cd ~/.engram && git add engram.db && git commit -m 'sync' && git push"
else
    info "Engram data no está en git. Usá la DB local (no sync)."
fi

# ============================================================================
# 8. Summary
# ============================================================================

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Update completo                               ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
git log --oneline -5 2>/dev/null
echo ""

if [ "$MCP_FAIL" -gt 0 ]; then
    warn "Corregí los MCPs marcados antes de reiniciar OpenCode."
fi

success "Para aplicar los cambios, reiniciá OpenCode."
info "Backup de opencode.json anterior: ${OPENCODE_BACKUP}"
echo ""
