<#
.SYNOPSIS
    Backs up the Engram SQLite database to the project's backups/engram/ directory.

.DESCRIPTION
    Copies engram.db (and -shm, -wal sidecar files if present) from
    C:\Users\leand\.engram\ into a timestamped folder:
        backups/engram/engram-backup-YYYY-MM-DD_HHmmss/

    Keeps only the last 7 backups — older ones are pruned automatically.
    Logs each action to console.  Exit code 0 = success, 1 = failure.

    Idempotent — safe to run multiple times.

.EXAMPLE
    .\scripts\backup-engram.ps1
#>

$ErrorActionPreference = "Stop"

$sourceDir    = "$env:USERPROFILE\.engram"
$projectRoot  = "C:\Users\leand\Documents\PROYECTOS\lend-ai"
$backupRoot   = Join-Path -Path $projectRoot -ChildPath "backups\engram"

$timestamp    = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupDir    = Join-Path -Path $backupRoot -ChildPath "engram-backup-$timestamp"

try {
    # 1. Ensure backup root exists
    if (-not (Test-Path -LiteralPath $backupRoot)) {
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
        Write-Host "[OK] Created backup directory: $backupRoot"
    }

    # 2. Ensure source exists
    if (-not (Test-Path -LiteralPath $sourceDir)) {
        Write-Host "[ERR] Source directory not found: $sourceDir"
        exit 1
    }

    # 3. Create timestamped backup folder
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

    # 4. Copy database files
    $filesToCopy = @("engram.db", "engram.db-shm", "engram.db-wal")
    $copied = $false

    foreach ($file in $filesToCopy) {
        $src = Join-Path -Path $sourceDir -ChildPath $file
        if (Test-Path -LiteralPath $src) {
            $dst = Join-Path -Path $backupDir -ChildPath $file
            Copy-Item -LiteralPath $src -Destination $dst -Force
            Write-Host "[OK] Backed up: $file"
            $copied = $true
        }
    }

    if (-not $copied) {
        Write-Host "[WARN] No Engram database files found in $sourceDir"
        Remove-Item -LiteralPath $backupDir -Force -ErrorAction SilentlyContinue
        exit 1
    }

    Write-Host "[OK] Backup created: $backupDir"

    # 5. Prune — keep only last 7 backups
    $backups = Get-ChildItem -LiteralPath $backupRoot -Directory | Where-Object {
        $_.Name -match '^engram-backup-\d{4}-\d{2}-\d{2}_\d{6}$'
    } | Sort-Object CreationTime -Descending

    if ($backups.Count -gt 7) {
        $toDelete = $backups | Select-Object -Skip 7
        foreach ($dir in $toDelete) {
            Remove-Item -LiteralPath $dir.FullName -Recurse -Force
            Write-Host "[OK] Pruned old backup: $($dir.Name)"
        }
    } else {
        Write-Host "[OK] Backup count: $($backups.Count) / 7 (no prune needed)"
    }

    exit 0
}
catch {
    Write-Host "[ERR] $($_.Exception.Message)"
    exit 1
}
