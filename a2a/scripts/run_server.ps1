# scripts/run_server.ps1 — Start the Lesson 06 A2A server
# Usage: .\scripts\run_server.ps1
# Run from: _examples/a2a/
#
# The server runs until you press Ctrl+C.
# In run_all.ps1 it is started as a background job.

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$ServerSrc = Join-Path $Root "lessons\06-a2a-server\src"

Write-Host "=== Lesson 06 — A2A Server ===" -ForegroundColor Cyan
Write-Host ""

# ── Load .env ─────────────────────────────────────────────────
$EnvFile = Join-Path (Split-Path -Parent $Root) ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim())
        }
    }
    Write-Host "✅ Loaded $EnvFile" -ForegroundColor Green
}

if (-not $env:GITHUB_TOKEN) {
    Write-Host "❌ GITHUB_TOKEN not set!" -ForegroundColor Red
    exit 1
}

Write-Host "Starting QAAgent A2A server on http://localhost:10001" -ForegroundColor Green
Write-Host "Agent Card: http://localhost:10001/.well-known/agent.json"
Write-Host "Press Ctrl+C to stop."
Write-Host ""

Set-Location $ServerSrc
& $Python server.py
