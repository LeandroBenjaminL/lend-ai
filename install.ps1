# ============================================================================
# Lend.Ai — Windows Installer
# Ecosistema unificado de agentes AI para Windows
#
# Usage (PowerShell como admin):
#   irm https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.ps1 | iex
#
# O descargar y ejecutar:
#   ./install.ps1
# ============================================================================

param(
    [string]$Branch = "main",
    [string]$InstallDir = "$env:USERPROFILE\.lend-ai"
)

$ErrorActionPreference = "Stop"
$GITHUB_OWNER = "LeandroBenjaminL"
$GITHUB_REPO = "lend-ai"
$ENGRAM_VERSION = "1.15.13"
$ENGRAM_PORT = "7437"

# ============================================================================
# Banner
# ============================================================================

Write-Host ""
Write-Host "   ╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "   ║   Lend.Ai — Windows Installer          ║" -ForegroundColor Cyan
Write-Host "   ║   v0.6.2                                     ║" -ForegroundColor Cyan
Write-Host "   ╚═══════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# Logging
# ============================================================================

function info    { Write-Host "[info]    $args" -ForegroundColor Blue }
function success { Write-Host "[ok]      $args" -ForegroundColor Green }
function warn    { Write-Host "[warn]    $args" -ForegroundColor Yellow }
function error   { Write-Host "[error]   $args" -ForegroundColor Red }
function step    { Write-Host ""; Write-Host "==> $args" -ForegroundColor Cyan }
function substep { Write-Host "  > $args" -ForegroundColor DarkCyan }

# ============================================================================
# Step 1: Prerequisites
# ============================================================================

step "Verificando prerequisitos"

$missing = @()

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    $missing += "git (https://git-scm.com)"
}
if (-not (Get-Command python3 -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    warn "Python no encontrado — algunas funciones no estaran disponibles"
}

if ($missing.Count -gt 0) {
    error "Faltan herramientas criticas: $($missing -join ', ')"
    Write-Host "  Instalalas y reintenta."
    exit 1
}

success "Git y Python disponibles"

# ============================================================================
# Step 2: Create directories
# ============================================================================

step "Creando estructura de directorios"

$dirs = @(
    $InstallDir,
    "$InstallDir\bin",
    "$InstallDir\mcp-servers",
    "$env:USERPROFILE\.engram"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
        substep "Creado: $d"
    }
}

success "Estructura lista"

# ============================================================================
# Step 3: Install Engram
# ============================================================================

step "Instalando Engram v$ENGRAM_VERSION"

$engramBin = "$InstallDir\bin\engram.exe"
$engramUrl = "https://github.com/Gentleman-Programming/engram/releases/download/v$ENGRAM_VERSION/engram_$ENGRAM_VERSION`_windows_amd64.zip"
$engramZip = "$env:TEMP\engram.zip"

if (Test-Path $engramBin) {
    $current = & $engramBin version 2>$null
    if ($current -match $ENGRAM_VERSION) {
        success "Engram v$ENGRAM_VERSION ya instalado"
    } else {
        warn "Version anterior: $current. Actualizando a v$ENGRAM_VERSION..."
        Remove-Item $engramBin -Force
    }
}

if (-not (Test-Path $engramBin)) {
    substep "Descargando $engramUrl"
    Invoke-WebRequest -Uri $engramUrl -OutFile $engramZip

    substep "Extrayendo..."
    Expand-Archive -Path $engramZip -DestinationPath $env:TEMP\engram-extract -Force
    Copy-Item "$env:TEMP\engram-extract\engram.exe" $engramBin -Force

    Remove-Item $engramZip -Force
    Remove-Item "$env:TEMP\engram-extract" -Recurse -Force

    success "Engram v$ENGRAM_VERSION instalado en $engramBin"
}

# Add to PATH for this session
$env:Path = "$InstallDir\bin;" + $env:Path

# ============================================================================
# Step 4: Clone/Update lend-ai repo
# ============================================================================

step "Clonando $GITHUB_OWNER/$GITHUB_REPO"

$repoPath = "$InstallDir\repo"

if (Test-Path "$repoPath\.git") {
    substep "Repositorio existente. Actualizando..."
    Push-Location $repoPath
    git fetch origin $Branch
    git checkout $Branch
    git pull origin $Branch
    Pop-Location
    success "Repositorio actualizado"
} else {
    if (Test-Path $repoPath) {
        Remove-Item $repoPath -Recurse -Force
    }
    git clone -b $Branch "https://github.com/$GITHUB_OWNER/$GITHUB_REPO.git" $repoPath
    success "Repositorio clonado"
}

# ============================================================================
# Step 5: Configure opencode.json
# ============================================================================

step "Configurando opencode.json"

$opencodeConfig = "$env:USERPROFILE\.config\opencode\opencode.json"

if (-not (Test-Path (Split-Path $opencodeConfig -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $opencodeConfig -Parent) -Force | Out-Null
}

$sourceConfig = "$repoPath\opencode.json"

if (Test-Path $sourceConfig) {
    # Copy with path replacements for Windows
    $config = Get-Content $sourceConfig -Raw | ConvertFrom-Json

    # Replace Linux paths with Windows paths in MCP commands
    $configStr = Get-Content $sourceConfig -Raw
    $configStr = $configStr -replace '/home/lea/', "$env:USERPROFILE\"
    $configStr = $configStr -replace '/home/linuxbrew/.linuxbrew/bin/', "$InstallDir\bin\"
    $configStr = $configStr -replace '/usr/bin/python3', 'python'

    # Create backup if exists
    if (Test-Path $opencodeConfig) {
        Copy-Item $opencodeConfig "$opencodeConfig.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        substep "Backup creado"
    }

    $configStr | Set-Content $opencodeConfig -Encoding UTF8
    success "opencode.json configurado en $opencodeConfig"
} else {
    warn "No se encontro $sourceConfig"
}

# ============================================================================
# Step 6: Set env vars and PATH
# ============================================================================

step "Configurando variables de entorno"

$userEnvPath = "$env:USERPROFILE\.lend-ai\bin"
$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentUserPath -notlike "*$userEnvPath*") {
    substep "Agregando $userEnvPath al PATH de usuario"
    [Environment]::SetEnvironmentVariable("Path", "$currentUserPath;$userEnvPath", "User")
    $env:Path = "$env:Path;$userEnvPath"
}

success "PATH configurado"

# ============================================================================
# Step 7: Persistir engram en PATH
# ============================================================================

step "Persistiendo configuracion en PowerShell profile"

$profileDir = Split-Path $PROFILE -Parent
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$profileBlock = @"

# Lend.Ai — agregado por install.ps1
`$env:PATH = "`$env:USERPROFILE\.lend-ai\bin;`$env:PATH"
"@

if (-not (Test-Path $PROFILE)) {
    $profileBlock | Set-Content $PROFILE -Encoding UTF8
    success "PowerShell profile creado"
} else {
    $existing = Get-Content $PROFILE -Raw
    if ($existing -notlike "*lend-ai*") {
        Add-Content $PROFILE $profileBlock
        success "PowerShell profile actualizado"
    }
}

# ============================================================================
# Step 8: Verify installation
# ============================================================================

step "Verificando instalacion"

$refreshedPath = "$env:USERPROFILE\.lend-ai\bin;$env:PATH"
$env:Path = $refreshedPath

$engramVersion = & $engramBin version 2>$null
if ($LASTEXITCODE -eq 0) {
    success "Engram $engramVersion"
} else {
    warn "Engram no responde — reinicia la terminal"
}

if (Test-Path $repoPath) {
    success "Repositorio: $repoPath"
}

if (Test-Path $opencodeConfig) {
    success "opencode.json: $opencodeConfig"
}

# ============================================================================
# Done
# ============================================================================

Write-Host ""
Write-Host "   ╔═══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "   ║   Lend.Ai instalado en Windows          ║" -ForegroundColor Green
Write-Host "   ╚═══════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  Engram:    $engramBin" -ForegroundColor DarkGray
Write-Host "  Repo:      $repoPath" -ForegroundColor DarkGray
Write-Host "  Config:    $opencodeConfig" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  PROXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "  1. Cerrar y reabrir PowerShell"
Write-Host "  2. Ejecutar: engram version"
Write-Host "  3. Abrir opencode y probar: /mem-search test"
Write-Host "  4. Para actualizar: ./update.ps1"
Write-Host ""
