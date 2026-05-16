# ============================================================================
# Lend.Ai — Windows Update Script
# Actualiza el ecosistema sin romper MCPs ni configs existentes.
#
# Usage:
#   ./update.ps1
# ============================================================================

param(
    [string]$InstallDir = "$env:USERPROFILE\.lend-ai"
)

$ErrorActionPreference = "Stop"
$OPENCODE_CONFIG = "$env:USERPROFILE\.config\opencode\opencode.json"
$BACKUP_TIMESTAMP = Get-Date -Format "yyyyMMdd-HHmmss"

# ============================================================================
# Logging
# ============================================================================

function info    { Write-Host "[info]    $args" -ForegroundColor Blue }
function success { Write-Host "[ok]      $args" -ForegroundColor Green }
function warn    { Write-Host "[warn]    $args" -ForegroundColor Yellow }
function error   { Write-Host "[error]   $args" -ForegroundColor Red }
function step    { Write-Host ""; Write-Host "==> $args" -ForegroundColor Cyan }

# ============================================================================
# 1. Check current state
# ============================================================================

Write-Host ""
Write-Host "   ╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "   ║   Lend.Ai — Windows Update                    ║" -ForegroundColor Cyan
Write-Host "   ╚═══════════════════════════════════════════════╝" -ForegroundColor Cyan

if (-not (Test-Path "$InstallDir\.git")) {
    error "No se encuentra Lend.Ai en $InstallDir"
    info "Ejecutá install.ps1 primero"
    exit 1
}

Push-Location $InstallDir

$currentCommit = & git rev-parse --short HEAD 2>$null
$currentBranch = & git rev-parse --abbrev-ref HEAD 2>$null

info "Lend.Ai home: $InstallDir"
info "Branch:       $currentBranch"
info "Commit:       $currentCommit"

# ============================================================================
# 2. Stash local changes
# ============================================================================

$hasChanges = & git diff --quiet HEAD 2>$null
if (-not $?) {
    warn "Tenés cambios locales sin commitear:"
    & git status --short
    info "Se van a stash para que el pull sea limpio."
    & git stash --include-untracked 2>$null
}

# ============================================================================
# 3. Git pull
# ============================================================================

step "Pulling latest changes..."

try {
    & git pull origin $currentBranch 2>&1 | Out-Null
    if (-not $?) { throw "Git pull falló" }
} catch {
    error "Git pull falló. Revisá si hay conflictos."
    Pop-Location
    exit 1
}

$newCommit = & git rev-parse --short HEAD
if ($currentCommit -ne $newCommit) {
    success "Actualizado: $currentCommit → $newCommit"
    & git log --oneline "$currentCommit..$newCommit" 2>$null | Select-Object -First 20
} else {
    info "Ya estás en la última versión ($currentCommit)."
}

# ============================================================================
# 4. Backup and update opencode.json
# ============================================================================

step "Updating opencode.json..."

if (Test-Path $OPENCODE_CONFIG) {
    $backupFile = "$OPENCODE_CONFIG.backup.$BACKUP_TIMESTAMP"
    Copy-Item $OPENCODE_CONFIG $backupFile
    info "Backup creado: $backupFile"
}

# Copy with placeholder replacement for Windows paths
$configStr = Get-Content "$InstallDir\opencode.json" -Raw
$configStr = $configStr -replace '{LEND_AI_HOME}', $InstallDir
Set-Content $OPENCODE_CONFIG $configStr -Encoding UTF8
success "opencode.json actualizado en $OPENCODE_CONFIG"

# ============================================================================
# 5. Check MCP dependencies
# ============================================================================

step "Verificando MCPs..."

$mcpOk = 0
$mcpFail = 0

# Python MCPs
try {
    $null = python -c "from mcp.server.fastmcp import FastMCP" 2>$null
    success "FastMCP SDK — agent-router, model-router"
    $mcpOk++
} catch {
    warn "FastMCP SDK — corré: pip install mcp"
    $mcpFail++
}

try {
    $null = python -c "import psycopg2" 2>$null
    success "psycopg2 — postgres MCP"
    $mcpOk++
} catch {
    warn "psycopg2 — corré: pip install psycopg2-binary"
    $mcpFail++
}

# Environment variables
$envFile = "$InstallDir\.env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile -Raw
    if ($envContent -match "GITHUB_TOKEN=[^`n`r\s]") {
        success "GITHUB_TOKEN configurado — github MCP"
        $mcpOk++
    } else {
        warn "GITHUB_TOKEN vacío — github MCP necesita token en .env"
        $mcpFail++
    }
    if ($envContent -match "NOTION_TOKEN=[^`n`r\s]") {
        success "NOTION_TOKEN configurado — notion MCP"
        $mcpOk++
    } else {
        warn "NOTION_TOKEN vacío — notion MCP necesita token en .env"
        $mcpFail++
    }
} else {
    warn "No se encontró .env — los MCPs que requieren tokens no funcionarán"
}

Write-Host ""
if ($mcpFail -eq 0) {
    success "$mcpOk MCPs verificados, 0 fallos"
} else {
    warn "$mcpOk MCPs OK, $mcpFail MCPs necesitan atención"
}

# ============================================================================
# 6. Summary
# ============================================================================

Write-Host ""
Write-Host "   ╔═══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "   ║   Update completo                             ║" -ForegroundColor Green
Write-Host "   ╚═══════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

& git log --oneline -5 2>$null

Write-Host ""
if ($mcpFail -gt 0) {
    warn "Corregí los MCPs marcados antes de reiniciar OpenCode."
}
success "Para aplicar los cambios, reiniciá OpenCode."

Pop-Location
