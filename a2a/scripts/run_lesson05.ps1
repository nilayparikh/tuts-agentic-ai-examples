# scripts/run_lesson05.ps1 — Run Lesson 05 standalone QA agent test
# Usage: .\scripts\run_lesson05.ps1
# Run from: _examples/a2a/

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Lesson05Src = Join-Path $Root "lessons\05-first-a2a-agent\src"

Write-Host "=== Lesson 05 — Standalone QA Agent ===" -ForegroundColor Cyan
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

Write-Host "Model: Phi-4 via GitHub Models"
Write-Host "Knowledge: data/insurance_policy.txt"
Write-Host ""

Set-Location $Lesson05Src
& $Python qa_agent.py
