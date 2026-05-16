<#
.SYNOPSIS
    Creates a Windows Scheduled Task that runs backup-engram.ps1 daily at 3 AM.

.DESCRIPTION
    The task is named "LendAi-EngramBackup" and executes:
        powershell.exe -File "<project>\scripts\backup-engram.ps1"

    Only runs on Windows — exits silently otherwise.
    Idempotent: if the task already exists, it is updated in-place.

.EXAMPLE
    .\scripts\setup-engram-backup.ps1
#>

$ErrorActionPreference = "Stop"

if ($env:OS -ne "Windows_NT") {
    Write-Host "[SKIP] Not Windows — scheduled task not created."
    exit 0
}

$projectRoot  = "C:\Users\leand\Documents\PROYECTOS\lend-ai"
$scriptPath   = Join-Path -Path $projectRoot -ChildPath "scripts\backup-engram.ps1"
$taskName     = "LendAi-EngramBackup"

try {
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        Write-Host "[ERR] Backup script not found: $scriptPath"
        exit 1
    }

    $action = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

    $trigger = New-ScheduledTaskTrigger -Daily -At 03:00

    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -MultipleInstances IgnoreNew

    Register-ScheduledTask -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Settings $settings `
        -Force | Out-Null

    Write-Host "[OK] Scheduled task '$taskName' created — runs daily at 03:00"
    exit 0
}
catch {
    Write-Host "[ERR] $($_.Exception.Message)"
    exit 1
}
