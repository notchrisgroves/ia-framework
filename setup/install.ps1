# IA Framework Installer - Windows (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "IA Framework Installer" -ForegroundColor Blue
Write-Host "======================" -ForegroundColor Blue

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $ScriptDir
$ClaudeDir = Join-Path $RepoDir ".claude"
$TargetDir = Join-Path $env:USERPROFILE ".claude"

Write-Host "[INFO] Repository: $RepoDir"
Write-Host "[INFO] Target: $TargetDir"

# Handle existing ~/.claude
if (Test-Path $TargetDir) {
    $item = Get-Item $TargetDir -Force
    if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        $response = Read-Host "Existing symlink found. Replace? (y/N)"
        if ($response -eq 'y') { Remove-Item $TargetDir -Force }
        else { exit 0 }
    } else {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backup = "$env:USERPROFILE\.claude.backup.$timestamp"
        Move-Item $TargetDir $backup
        Write-Host "[OK] Backed up to: $backup" -ForegroundColor Green
    }
}

# Create symlink
try {
    New-Item -ItemType SymbolicLink -Path $TargetDir -Target $ClaudeDir -Force | Out-Null
    Write-Host "[OK] Created symlink" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Symlink failed. Enable Developer Mode or run as Admin" -ForegroundColor Red
    exit 1
}

# Copy .env.example
$EnvExample = Join-Path $RepoDir ".env.example"
$EnvTarget = Join-Path $env:USERPROFILE ".env"
if ((Test-Path $EnvExample) -and -not (Test-Path $EnvTarget)) {
    Copy-Item $EnvExample $EnvTarget
    Write-Host "[OK] Created ~/.env (add your API keys)" -ForegroundColor Green
}

# Create user directories
foreach ($dir in @("sessions", "plans", "output")) {
    $path = Join-Path $ClaudeDir $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}
Write-Host "[OK] Created user directories" -ForegroundColor Green

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "Next: Edit ~/.env to add your ANTHROPIC_API_KEY"
