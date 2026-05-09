<#
.SYNOPSIS
    Data-Analyst Ecosystem — Windows Installer

.DESCRIPTION
    Instala la suite de análisis de datos para agentes AI en Windows.
    Skills, MCPs, agentes y configuraciones para OpenCode.

    Soporta múltiples métodos de instalación:
      scoop   → Scoop bucket install (si está disponible)
      binary  → Descarga binario comprimido desde GitHub Releases
      git     → git clone del repositorio (default)

.PARAMETER Method
    Método de instalación: auto (default), scoop, binary, git

.PARAMETER Dir
    Directorio de instalación (default: ~\.data-analyst)

.PARAMETER Branch
    Rama de GitHub (default: main, solo para método git)

.PARAMETER Version
    Tag de release (default: latest, solo para método binary)

.EXAMPLE
    .\scripts\install.ps1
    .\scripts\install.ps1 -Method scoop
    .\scripts\install.ps1 -Method binary -Dir C:\tools\data-analyst
    .\scripts\install.ps1 -Branch develop -Method git
#>

#Requires -Version 5.1

param(
    [ValidateSet('auto', 'scoop', 'binary', 'git')]
    [string]$Method = 'auto',

    [string]$Dir = '',

    [string]$Branch = 'main',

    [string]$Version = 'latest'
)

# ============================================================================
# Configuración
# ============================================================================

$Script:GithubOwner = 'LeandroBenjaminL'
$Script:GithubRepo = 'data-analyst-ecosystem'
$Script:InstallDir = if ($Dir) { $Dir } else { Join-Path $env:USERPROFILE '.data-analyst' }
$Script:InstallMethod = $Method
$Script:GithubBranch = $Branch
$Script:InstallVersion = $Version
$Script:BackupPath = $null

# ============================================================================
# Colores (soporte para PowerShell ISE, terminal, y pipes)
# ============================================================================

$Script:HasColor = $host.UI.RawUI.ForegroundColor -ne $null -and $host.Name -ne 'Windows PowerShell ISE Host'

function Write-Info {
    if ($Script:HasColor) { Write-Host "[info]    " -NoNewline -ForegroundColor Blue }
    else { Write-Host "[info]    " -NoNewline }
    Write-Host $args
}

function Write-Success {
    if ($Script:HasColor) { Write-Host "[ok]      " -NoNewline -ForegroundColor Green }
    else { Write-Host "[ok]      " -NoNewline }
    Write-Host $args
}

function Write-Warn {
    if ($Script:HasColor) { Write-Host "[warn]    " -NoNewline -ForegroundColor Yellow }
    else { Write-Host "[warn]    " -NoNewline }
    Write-Host $args
}

function Write-Error {
    if ($Script:HasColor) { Write-Host "[error]   " -NoNewline -ForegroundColor Red }
    else { Write-Host "[error]   " -NoNewline }
    Write-Host $args
}

function Write-Fatal {
    Write-Error $args
    exit 1
}

function Write-Step {
    Write-Host ""
    if ($Script:HasColor) { Write-Host "==>" -NoNewline -ForegroundColor Cyan }
    else { Write-Host "==>" -NoNewline }
    Write-Host " $($args -join ' ')"
}

function Write-Substep {
    Write-Host "  > $($args -join ' ')"
}

# ============================================================================
# Banner
# ============================================================================

function Show-Banner {
    Write-Host ""
    if ($Script:HasColor) { Write-Host "   ╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan }
    else { Write-Host "   ╔═══════════════════════════════════════════════╗" }
    Write-Host "   ║                                               ║"
    Write-Host "   ║    ____        _        ____        _       _   _"
    Write-Host "   ║   |  _ \  __ _| |_ __ _|  _ \  __ _| |_ ___| |_(_)_ __   __ _"
    Write-Host "   ║   | | | |/ _` | __/ _` | | | |/ _` | __/ __| __| | '_ \ / _` |"
    Write-Host "   ║   | |_| | (_| | || (_| | |_| | (_| | || (__| |_| | | | | (_| |"
    Write-Host "   ║   |____/ \__,_|\__\__,_|____/ \__,_|\__\___|\__|_|_| |_|\__, |"
    Write-Host "   ║                                                        |___/"
    Write-Host "   ║"
    Write-Host "   ╚═══════════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "  Data-Analyst Ecosystem — Skills, MCPs, Agentes para AI"
    Write-Host "  $($Script:GithubOwner)/$($Script:GithubRepo)"
    Write-Host ""
}

# ============================================================================
# Detección de plataforma y arquitectura
# ============================================================================

function Detect-Platform {
    Write-Step "Detectando plataforma"

    $Script:OS = "windows"
    $Script:OSLabel = "Windows"

    # Detectar arquitectura
    $arch = $env:PROCESSOR_ARCHITECTURE
    switch -Wildcard ($arch) {
        'AMD64' { $Script:Arch = 'x86_64'; $Script:ArchLabel = 'x86_64 (amd64)' }
        'ARM64' { $Script:Arch = 'arm64';  $Script:ArchLabel = 'arm64' }
        default { $Script:Arch = $arch;    $Script:ArchLabel = $arch }
    }

    Write-Success "Plataforma: $($Script:OSLabel) | Arquitectura: $($Script:ArchLabel)"
}

# ============================================================================
# Detección automática del método de instalación
# ============================================================================

function Detect-Method {
    if ($Script:InstallMethod -ne 'auto') {
        Write-Success "Método: $($Script:InstallMethod) (forzado por flag)"
        return
    }

    # 1. Scoop
    if (Get-Command scoop -ErrorAction SilentlyContinue) {
        $bucketUrl = "https://github.com/$($Script:GithubOwner)/scoop-bucket"
        if (scoop bucket list 2>$null | Select-String -Pattern $Script:GithubOwner) {
            $Script:InstallMethod = 'scoop'
            Write-Success "Método: scoop (Scoop detectado)"
            return
        }
        Write-Substep "scoop detectado pero sin bucket — probando binary..."
    }

    # 2. Binary download
    $apiUrl = "https://api.github.com/repos/$($Script:GithubOwner)/$($Script:GithubRepo)/releases/$($Script:InstallVersion)"
    try {
        $null = Invoke-WebRequest -Uri $apiUrl -Method Head -UseBasicParsing -ErrorAction Stop
        $Script:InstallMethod = 'binary'
        Write-Success "Método: binary (GitHub Releases disponible)"
        return
    } catch {
        # fall through
    }

    # 3. Git clone (fallback)
    $Script:InstallMethod = 'git'
    Write-Info "Método: git (fallback universal)"
}

# ============================================================================
# Prerequisitos
# ============================================================================

function Check-Prerequisites {
    Write-Step "Verificando prerequisitos"

    $missing = @()

    # Git (necesario para método git)
    if ($Script:InstallMethod -eq 'git') {
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            $missing += "git"
        }
    }

    # curl / Invoke-WebRequest
    if (-not (Get-Command curl -ErrorAction SilentlyContinue)) {
        # PowerShell tiene Invoke-WebRequest nativo
        Write-Success "PowerShell WebRequest disponible (nativo)"
    } else {
        Write-Success "curl disponible"
    }

    # Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        # Probar python3
        if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
            $missing += "python (https://python.org)"
        }
    } else {
        $pyVer = & python --version 2>&1
        Write-Success "Python $pyVer disponible"
    }

    # pip
    if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
        if (-not (Get-Command pip3 -ErrorAction SilentlyContinue)) {
            $missing += "pip"
        }
    }

    # Node.js
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        $missing += "node (https://nodejs.org)"
    } else {
        $nodeVer = & node --version 2>&1
        Write-Success "Node.js $nodeVer disponible"
    }

    # npx
    if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
        $missing += "npx"
    }

    if ($missing.Count -gt 0) {
        Write-Fatal "Faltan herramientas requeridas: $($missing -join ', '). Instalalas y reintentá."
    }

    # Tar (para extraer binarios)
    if (-not (Get-Command tar -ErrorAction SilentlyContinue)) {
        Write-Warn "tar no encontrado — necesario para método binary. Probá instalar via 'git' o instalá tar."
    }

    Write-Success "Git, Python, Node.js disponibles"
}

# ============================================================================
# Backup snapshot antes de modificar
# ============================================================================

function Run-Backup {
    Write-Step "Backup snapshot (pre-modificación)"

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupDir = Join-Path $Script:InstallDir ".backup-$timestamp"

    if (Test-Path $Script:InstallDir) {
        try {
            New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
            # Backup de archivos de configuración
            $itemsToBackup = @('.env', 'opencode.json', 'skills', 'scripts', 'agents', 'mcp-servers', 'commands', 'docs', 'data', 'AGENTS.md', 'models.json', 'requirements.txt')
            foreach ($item in $itemsToBackup) {
                $itemPath = Join-Path $Script:InstallDir $item
                if (Test-Path $itemPath) {
                    if (Test-Path $itemPath -PathType Container) {
                        Copy-Item -Path $itemPath -Destination $backupDir -Recurse -Force -ErrorAction SilentlyContinue
                    } else {
                        Copy-Item -Path $itemPath -Destination $backupDir -Force -ErrorAction SilentlyContinue
                    }
                }
            }
            $Script:BackupPath = $backupDir
            Write-Success "Snapshot guardado en: $backupDir"
        } catch {
            Write-Warn "No se pudo crear backup: $_"
        }
    } else {
        Write-Info "No había instalación previa para backupear"
    }
}

# ============================================================================
# Instalar vía Scoop
# ============================================================================

function Install-Scoop {
    Write-Step "Instalando via Scoop"

    # Asegurar bucket
    $bucketName = "$($Script:GithubOwner)-bucket"
    $bucketUrl = "https://github.com/$($Script:GithubOwner)/scoop-bucket"

    # Verificar si el bucket ya está agregado
    $buckets = scoop bucket list 2>$null
    if (-not ($buckets | Select-String -Pattern $bucketName)) {
        Write-Substep "Agregando bucket $bucketName..."
        scoop bucket add $bucketName $bucketUrl 2>&1 | Out-Null
        if (-not $?) {
            Write-Warn "No se pudo agregar el bucket. Intentando método git..."
            Install-Git
            return
        }
    }

    # Instalar/actualizar
    $appName = "$bucketName/$($Script:GithubRepo)"
    $installedApps = scoop list 2>$null

    if ($installedApps | Select-String -Pattern $Script:GithubRepo) {
        Write-Info "Data-Analyst ya instalado via scoop. Actualizando..."
        scoop update $appName 2>&1 | Out-Null
        if (-not $?) {
            Write-Warn "No se pudo actualizar via scoop"
        }
    } else {
        scoop install $appName 2>&1 | Out-Null
        if (-not $?) {
            Write-Warn "scoop install falló. Intentando método git..."
            Install-Git
            return
        }
    }

    # Scoop instala en ~\scoop\apps, crear symlink si es posible
    if (-not (Test-Path $Script:InstallDir)) {
        $scoopDir = Join-Path $env:USERPROFILE "scoop\apps\$($Script:GithubRepo)\current"
        if (Test-Path $scoopDir) {
            if (Get-Command New-Item -ErrorAction SilentlyContinue) {
                # En Windows moderno podemos crear symlinks con New-Item -ItemType SymbolicLink
                try {
                    New-Item -ItemType SymbolicLink -Path $Script:InstallDir -Target $scoopDir -Force | Out-Null
                } catch {
                    # Fallback: junction point
                    cmd /c mklink /J "$($Script:InstallDir)" "$scoopDir" 2>$null | Out-Null
                }
            }
        }
    }

    Write-Success "Scoop instalación completada"
}

# ============================================================================
# Instalar vía binary download desde GitHub Releases
# ============================================================================

function Install-Binary {
    Write-Step "Instalando via binary download"

    # Detectar asset según OS y arquitectura
    $osSuffix = "windows"
    $archSuffix = if ($Script:Arch -eq 'x86_64') { 'amd64' } else { 'arm64' }

    $apiUrl = "https://api.github.com/repos/$($Script:GithubOwner)/$($Script:GithubRepo)/releases/$($Script:InstallVersion)"
    Write-Substep "Consultando release: $apiUrl"

    try {
        $releaseData = Invoke-RestMethod -Uri $apiUrl -UseBasicParsing -ErrorAction Stop
    } catch {
        Write-Warn "No se pudo obtener información de la release ($_). Cayendo a git clone..."
        Install-Git
        return
    }

    # Buscar asset: {repo}-windows-{arch}.zip o .tar.gz
    $expectedName = "$($Script:GithubRepo)-$osSuffix-$archSuffix"
    $asset = $releaseData.assets | Where-Object { $_.name -like "$expectedName*" -and ($_.name -like '*.zip' -or $_.name -like '*.tar.gz') } | Select-Object -First 1

    if (-not $asset) {
        # Fallback: cualquier .zip
        $asset = $releaseData.assets | Where-Object { $_.name -like '*.zip' } | Select-Object -First 1
    }

    if (-not $asset) {
        # Fallback: cualquier .tar.gz
        $asset = $releaseData.assets | Where-Object { $_.name -like '*.tar.gz' } | Select-Object -First 1
    }

    if (-not $asset) {
        Write-Info "No se encontró asset para binary download. Cayendo a git clone..."
        Install-Git
        return
    }

    $downloadUrl = $asset.browser_download_url
    $assetName = $asset.name

    # Buscar checksum
    $checksumAsset = $releaseData.assets | Where-Object { $_.name -like '*checksum*' -or $_.name -like '*sha256*' } | Select-Object -First 1

    # Temp folder
    $tmpDir = Join-Path $env:TEMP "data-analyst-install-$(Get-Random)"
    New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null
    $archivePath = Join-Path $tmpDir $assetName

    try {
        # Descargar
        Write-Substep "Descargando $assetName..."
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($downloadUrl, $archivePath)
    } catch {
        Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Warn "Fallo la descarga. Cayendo a git clone..."
        Install-Git
        return
    }

    # Verificar checksum
    if ($checksumAsset) {
        Write-Substep "Verificando checksum SHA256..."
        $checksumUrl = $checksumAsset.browser_download_url
        $checksumFile = Join-Path $tmpDir "checksums.txt"
        try {
            $webClient.DownloadFile($checksumUrl, $checksumFile)
            $checksums = Get-Content $checksumFile
            $expectedHash = ($checksums | Where-Object { $_ -like "*$assetName*" } | ForEach-Object { $_ -split '\s+' | Select-Object -First 1 }) -replace '[\s\(\)]', ''

            if ($expectedHash) {
                $actualHash = (Get-FileHash -Path $archivePath -Algorithm SHA256).Hash.ToLower()
                if ($actualHash -eq $expectedHash.ToLower()) {
                    Write-Success "Checksum SHA256 verificado correctamente"
                } else {
                    Write-Warn "Checksum no coincide. Esperado: $expectedHash, Obtenido: $actualHash"
                    Write-Warn "Continuando igual — el asset se verificó contra GitHub API"
                }
            } else {
                Write-Substep "No hay checksum para este asset — saltando verificación"
            }
        } catch {
            Write-Substep "No se pudo descargar checksum — saltando verificación"
        }
    } else {
        Write-Substep "Verificación SHA256 saltada (no hay checksum en la release)"
    }

    # Extraer
    Write-Substep "Extrayendo en $($Script:InstallDir)..."
    try {
        New-Item -ItemType Directory -Path $Script:InstallDir -Force | Out-Null

        if ($assetName -like '*.zip') {
            Expand-Archive -Path $archivePath -DestinationPath $Script:InstallDir -Force
        } elseif ($assetName -like '*.tar.gz') {
            if (Get-Command tar -ErrorAction SilentlyContinue) {
                tar -xzf $archivePath -C $Script:InstallDir --strip-components=1 2>$null
                if (-not $?) {
                    # Fallback: tar sin strip-components
                    tar -xzf $archivePath -C $Script:InstallDir 2>$null
                    # Mover contenido si hay un solo directorio
                    $dirs = Get-ChildItem -Path $Script:InstallDir -Directory
                    if ($dirs.Count -eq 1 -and $dirs[0].Name -ne '.') {
                        Get-ChildItem -Path $dirs[0].FullName | Move-Item -Destination $Script:InstallDir -Force
                        Remove-Item -Path $dirs[0].FullName -Recurse -Force
                    }
                }
            } else {
                Write-Warn "tar no disponible — no se puede extraer .tar.gz. Cayendo a git..."
                Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
                Install-Git
                return
            }
        }
    } catch {
        Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Warn "Fallo la extracción. Cayendo a git clone..."
        Install-Git
        return
    }

    Remove-Item -Path $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Success "Binary instalado en $($Script:InstallDir)"
}

# ============================================================================
# Instalar vía git clone
# ============================================================================

function Install-Git {
    Write-Step "Instalando via git clone"

    $repoUrl = "https://github.com/$($Script:GithubOwner)/$($Script:GithubRepo).git"
    $gitDir = Join-Path $Script:InstallDir ".git"

    if (Test-Path $gitDir) {
        Write-Info "Data-Analyst ya instalado. Actualizando..."
        Push-Location $Script:InstallDir
        try {
            & git fetch origin $Script:GithubBranch 2>$null
            if (-not $?) { Write-Warn "No se pudo actualizar (sin conexión?)" }
            & git reset --hard "origin/$($Script:GithubBranch)" 2>$null
            if (-not $?) { Write-Warn "No se pudo resetear a origin/$($Script:GithubBranch)" }
        } finally {
            Pop-Location
        }
        Write-Success "Actualizado a la última versión (rama $($Script:GithubBranch))"
    } else {
        Write-Info "Clonando repositorio..."
        $parentDir = Split-Path $Script:InstallDir -Parent
        if (-not (Test-Path $parentDir)) {
            New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        }

        & git clone --branch $Script:GithubBranch --depth 1 $repoUrl $Script:InstallDir 2>&1
        if (-not $?) {
            Write-Fatal "No se pudo clonar el repositorio. Verificá conexión a Internet."
        }
        Write-Success "Repositorio clonado en $($Script:InstallDir) (rama $($Script:GithubBranch))"
    }
}

# ============================================================================
# Instalar según método detectado/forzado
# ============================================================================

function Run-Install {
    switch ($Script:InstallMethod) {
        'scoop'  { Install-Scoop }
        'binary' { Install-Binary }
        'git'    { Install-Git }
        default  { Write-Fatal "Método desconocido: $($Script:InstallMethod)" }
    }

    Write-Success "Instalación completada en $($Script:InstallDir)"
}

# ============================================================================
# Configurar .env
# ============================================================================

function Setup-Env {
    Write-Step "Configurando credenciales"

    $envTemplate = Join-Path $Script:InstallDir ".env.template"
    $envFile = Join-Path $Script:InstallDir ".env"

    if (Test-Path $envFile) {
        Write-Info ".env ya existe, usando valores actuales"
    } else {
        if (Test-Path $envTemplate) {
            Copy-Item -Path $envTemplate -Destination $envFile
            Write-Info "Archivo .env creado desde template"
        } else {
            Write-Info "No hay .env.template — saltando configuración de credenciales"
            return
        }
    }

    # Preguntar credenciales (solo si no están configuradas)
    $envContent = Get-Content $envFile -Raw
    $hasValues = $envContent -match 'GITHUB_TOKEN=[^#\s]'

    if (-not $hasValues) {
        Write-Host ""
        Write-Info "Completá tus credenciales (dejá vacío para saltar):"
        Write-Host ""

        $inputGh = Read-Host "  Token de GitHub (para PRs, issues)"
        $inputNotion = Read-Host "  Token de Notion (para docs)"
        $inputPg = Read-Host "  Password de PostgreSQL"
        $inputMysql = Read-Host "  Password de MySQL"

        $lines = Get-Content $envFile
        $newLines = $lines | ForEach-Object {
            $line = $_
            if ($line -match '^# GITHUB_TOKEN=' -and $inputGh) { $line = "GITHUB_TOKEN=$inputGh" }
            elseif ($line -match '^# NOTION_TOKEN=' -and $inputNotion) { $line = "NOTION_TOKEN=$inputNotion" }
            elseif ($line -match '^# PG_PASSWORD=' -and $inputPg) { $line = "PG_PASSWORD=$inputPg" }
            elseif ($line -match '^# MYSQL_PASSWORD=' -and $inputMysql) { $line = "MYSQL_PASSWORD=$inputMysql" }
            elseif ($line -match '^# DEFAULT_LLM_TIER=') { $line = "DEFAULT_LLM_TIER=T3" }
            $line
        }
        $newLines | Set-Content $envFile

        Write-Success "Credenciales configuradas"
    } else {
        Write-Success "Credenciales ya configuradas"
    }
}

# ============================================================================
# Instalar dependencias Python
# ============================================================================

function Install-PythonDeps {
    Write-Step "Instalando dependencias Python"

    $pythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'python3' }
    $pipCmd = if (Get-Command pip -ErrorAction SilentlyContinue) { 'pip' } else { 'pip3' }

    $reqFile = Join-Path $Script:InstallDir "requirements.txt"
    if (Test-Path $reqFile) {
        & $pipCmd install -r $reqFile -q 2>&1 | Select-Object -Last 3
        Write-Success "Dependencias Python instaladas desde requirements.txt"
    } else {
        Write-Info "No hay requirements.txt — instalando paquetes core"
        & $pipCmd install mcp pyyaml pydantic pytest pandas numpy -q 2>&1 | Select-Object -Last 3
        Write-Success "Paquetes core instalados"
    }
}

# ============================================================================
# Cachear MCPs npm
# ============================================================================

function Cache-NpmMcps {
    Write-Step "Cacheando MCPs npm"

    $packages = @(
        "@modelcontextprotocol/server-sequential-thinking"
        "@modelcontextprotocol/server-filesystem"
        "@modelcontextprotocol/server-puppeteer"
        "@modelcontextprotocol/server-github"
        "duckduckgo-mcp-server"
        "mcp-sqlite"
    )

    foreach ($pkg in $packages) {
        Write-Host "  📦 $($pkg)..." -NoNewline
        $null = & npx -y $pkg --help 2>$null
        if (-not $?) { $null = & npx -y $pkg --version 2>$null }
        Write-Host "`r  ✅ $($pkg)"
    }

    Write-Success "MCPs npm cacheados"
}

# ============================================================================
# Configurar OpenCode (opcional)
# ============================================================================

function Setup-OpenCodeConfig {
    Write-Step "Configurando OpenCode"

    $opencodeConfigDir = Join-Path $env:USERPROFILE ".config\opencode"

    # Verificar que OpenCode exista
    $opencodeCmd = Get-Command opencode -ErrorAction SilentlyContinue
    if (-not $opencodeCmd -and -not (Test-Path "$env:USERPROFILE\.opencode\bin\opencode.exe")) {
        Write-Warn "OpenCode no detectado. Saltando configuración."
        Write-Info "Podés configurar manualmente después:"
        Write-Info "  copy $($Script:InstallDir)\opencode.json %USERPROFILE%\.config\opencode\opencode.json"
        return
    }

    # Backup de configs existentes
    $opencodeJson = Join-Path $opencodeConfigDir "opencode.json"
    $tuiJson = Join-Path $opencodeConfigDir "tui.json"

    if (Test-Path $opencodeJson) {
        $backupDir = Join-Path $Script:InstallDir ".backup-opencode-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        Copy-Item -Path $opencodeJson -Destination $backupDir -Force -ErrorAction SilentlyContinue
        Write-Substep "Backup de opencode.json existente"
    }
    if (Test-Path $tuiJson) {
        if (-not (Test-Path $backupDir)) {
            $backupDir = Join-Path $Script:InstallDir ".backup-opencode-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
            New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        }
        Copy-Item -Path $tuiJson -Destination $backupDir -Force -ErrorAction SilentlyContinue
    }

    New-Item -ItemType Directory -Path $opencodeConfigDir -Force | Out-Null

    # opencode.json
    if (-not (Test-Path $opencodeJson)) {
        Write-Info "Creando opencode.json..."
        $templatePath = Join-Path $Script:InstallDir "opencode.json.template"
        $sourcePath = Join-Path $Script:InstallDir "opencode.json"

        if (Test-Path $templatePath) {
            $content = (Get-Content $templatePath -Raw) -replace '{DATA_ANALYST_HOME}', $Script:InstallDir
            Set-Content -Path $opencodeJson -Value $content
            Write-Success "opencode.json creado en $opencodeConfigDir"
        } elseif (Test-Path $sourcePath) {
            Copy-Item -Path $sourcePath -Destination $opencodeJson -Force
            Write-Success "opencode.json copiado a $opencodeConfigDir"
        } else {
            Write-Warn "No se encontró opencode.json para copiar"
        }
    } else {
        Write-Info "opencode.json ya existe. Si querés actualizarlo:"
        Write-Info "  copy $($Script:InstallDir)\opencode.json $opencodeConfigDir\opencode.json"
    }

    # tui.json
    if (-not (Test-Path $tuiJson)) {
        Write-Info "Creando tui.json con plugins..."
        $tuiContent = @'
{
  "plugin": [
    "opencode-sdd-engram-manage",
    "opencode-subagent-statusline"
  ]
}
'@
        Set-Content -Path $tuiJson -Value $tuiContent
        Write-Success "tui.json creado con plugins SDD + Subagent Monitor"
    } else {
        $tuiContent = Get-Content $tuiJson -Raw
        if ($tuiContent -notmatch 'opencode-subagent-statusline') {
            Write-Warn "Agregá 'opencode-subagent-statusline' a tu tui.json para ver sub-agentes"
        }
    }
}

# ============================================================================
# Verificar instalación
# ============================================================================

function Verify-Installation {
    Write-Step "Verificando instalación"

    $errors = 0

    # Verificar estructura
    $requiredDirs = @(
        "agents\manifests",
        "commands",
        "docs",
        "mcp-servers",
        "skills"
    )

    Write-Host "  Directorios:"
    foreach ($dir in $requiredDirs) {
        $dirPath = Join-Path $Script:InstallDir $dir
        if (Test-Path $dirPath) {
            if ($Script:HasColor) { Write-Host "  " -NoNewline; Write-Host "✅" -NoNewline -ForegroundColor Green; Write-Host " $dir" }
            else { Write-Host "  [ok] $dir" }
        } else {
            if ($Script:HasColor) { Write-Host "  " -NoNewline; Write-Host "❌" -NoNewline -ForegroundColor Red; Write-Host " $dir — no encontrado" }
            else { Write-Host "  [error] $dir — no encontrado" }
            $errors++
        }
    }

    # Verificar archivos clave
    $requiredFiles = @(
        "opencode.json",
        "AGENTS.md",
        "install.sh",
        "scripts\backup.sh",
        "scripts\install.ps1"
    )

    Write-Host "  Archivos clave:"
    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $Script:InstallDir $file
        if (Test-Path $filePath) {
            if ($Script:HasColor) { Write-Host "  " -NoNewline; Write-Host "✅" -NoNewline -ForegroundColor Green; Write-Host " $file" }
            else { Write-Host "  [ok] $file" }
        } else {
            if ($Script:HasColor) { Write-Host "  " -NoNewline; Write-Host "❌" -NoNewline -ForegroundColor Red; Write-Host " $file — no encontrado" }
            else { Write-Host "  [error] $file — no encontrado" }
            $errors++
        }
    }

    # Verificar herramientas
    Write-Host "  Herramientas:"
    $cmds = @('git', 'python', 'node')
    if (Get-Command python3 -ErrorAction SilentlyContinue) { $cmds[1] = 'python3' }
    foreach ($cmd in $cmds) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) {
            if ($Script:HasColor) { Write-Host "  " -NoNewline; Write-Host "✅" -NoNewline -ForegroundColor Green; Write-Host " $cmd" }
            else { Write-Host "  [ok] $cmd" }
        } else {
            if ($Script:HasColor) { Write-Host "  " -NoNewline; Write-Host "❌" -NoNewline -ForegroundColor Red; Write-Host " $cmd — no encontrado" }
            else { Write-Host "  [error] $cmd — no encontrado" }
            $errors++
        }
    }

    if ($errors -gt 0) {
        Write-Warn "$errors errores encontrados. Revisá la instalación."
    } else {
        Write-Success "Instalación verificada — todo en orden"
    }
}

# ============================================================================
# Próximos pasos
# ============================================================================

function Show-NextSteps {
    Write-Host ""
    if ($Script:HasColor) { Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Green }
    else { Write-Host "╔══════════════════════════════════════════╗" }
    if ($Script:HasColor) { Write-Host "║   ✅ Data-Analyst Ecosystem instalado    ║" -ForegroundColor Green }
    else { Write-Host "║   ✅ Data-Analyst Ecosystem instalado    ║" }
    if ($Script:HasColor) { Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Green }
    else { Write-Host "╚══════════════════════════════════════════╝" }
    Write-Host ""
    Write-Host "  📁 Instalado en:  $($Script:InstallDir)"
    Write-Host "  🔧 Método:        $($Script:InstallMethod)"

    if ($Script:BackupPath) {
        Write-Host "  💾 Backup:         $($Script:BackupPath)"
    }

    Write-Host ""
    Write-Host "🚀 Próximos pasos:"
    Write-Host ""
    Write-Host "  1. Revisá tus credenciales:"
    Write-Host "     notepad $($Script:InstallDir)\.env"
    Write-Host ""
    Write-Host "  2. Si no configuraste OpenCode todavía:"
    Write-Host "     copy $($Script:InstallDir)\opencode.json %USERPROFILE%\.config\opencode\opencode.json"
    Write-Host ""
    Write-Host "  3. Reiniciá OpenCode para que los plugins carguen"
    Write-Host "     La primera vez instala los plugins automáticamente"
    Write-Host ""
    Write-Host "  4. Usá el agente Data-Analyst:"
    Write-Host "     @data-analyst <tu consulta>"
    Write-Host ""
    Write-Host "  5. Atajos de teclado:"
    Write-Host "     Alt+B   → Ver sub-agentes activos"
    Write-Host "     Alt+K   → Gestión de perfiles SDD"
    Write-Host ""
    Write-Host "  6. Si algo sale mal, restaurá desde backup:"
    Write-Host "     robocopy $($Script:BackupPath) $($Script:InstallDir) /E"
    Write-Host ""
    Write-Host "📚 Documentación:"
    Write-Host "  https://github.com/$($Script:GithubOwner)/$($Script:GithubRepo)"
    Write-Host ""
}

# ============================================================================
# Post-instalación: sanity checks
# ============================================================================

function Post-InstallChecks {
    Write-Step "Post-instalación: verificaciones adicionales"

    # Verificar paquetes Python core
    $pythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'python3' }
    $pyCheck = & $pythonCmd -c "import yaml; import pydantic; print('OK')" 2>&1
    if ($pyCheck -eq 'OK') {
        Write-Success "Python: YAML + Pydantic importables"
    } else {
        Write-Warn "Python: algunos paquetes core no están instalados"
        Write-Substep "Corré: pip install pyyaml pydantic"
    }

    # Verificar que el template reemplazó vars
    $opencodeJson = Join-Path $Script:InstallDir "opencode.json"
    if (Test-Path $opencodeJson) {
        $content = Get-Content $opencodeJson -Raw
        if ($content -match '{DATA_ANALYST_HOME}') {
            Write-Warn "opencode.json tiene variables sin reemplazar"
        }
    }

    Write-Success "Post-instalación completada"
}

# ============================================================================
# Main
# ============================================================================

function Main {
    Show-Banner

    Detect-Platform
    Detect-Method
    Check-Prerequisites
    Run-Backup
    Run-Install
    Setup-Env
    Install-PythonDeps
    Cache-NpmMcps
    Setup-OpenCodeConfig
    Post-InstallChecks
    Verify-Installation
    Show-NextSteps
}

# Ejecutar
Main
