# scripts/setup.ps1 — One-time environment setup (Windows)
# Usage: .\scripts\setup.ps1
# Run from: _examples/a2a/

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$ExamplesRoot = Split-Path -Parent $Root

Write-Host "=== A2A Examples — Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# ── .env check ────────────────────────────────────────────────
$EnvFile = Join-Path $ExamplesRoot ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "⚠  .env file not found at $EnvFile" -ForegroundColor Yellow
    Write-Host "   Copy .env.example → .env and fill in GITHUB_TOKEN:"
    Write-Host "   Copy-Item `"$ExamplesRoot\.env.example`" `"$ExamplesRoot\.env`""
    exit 1
}

$EnvContent = Get-Content $EnvFile -Raw
if ($EnvContent -notmatch "GITHUB_TOKEN=.+") {
    Write-Host "❌ GITHUB_TOKEN not set in $EnvFile" -ForegroundColor Red
    Write-Host "   Get a GitHub PAT at https://github.com/settings/tokens"
    exit 1
}
Write-Host "✅ .env found with GITHUB_TOKEN" -ForegroundColor Green

# ── Create .venv ───────────────────────────────────────────────
Set-Location $Root
if (-not (Test-Path ".venv")) {
    Write-Host ""
    Write-Host "Creating .venv with uv..." -ForegroundColor Cyan
    uv venv .venv --python 3.11
} else {
    Write-Host "✅ .venv already exists" -ForegroundColor Green
}

# ── Install dependencies ───────────────────────────────────────
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Cyan
uv pip install -r requirements.txt

# ── Register Jupyter kernel ────────────────────────────────────
Write-Host ""
Write-Host "Registering Jupyter kernel 'a2a-examples'..." -ForegroundColor Cyan
& ".venv\Scripts\python.exe" -m ipykernel install --user --name a2a-examples --display-name "A2A Examples (Python 3.11)"

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  Start the A2A server:  .\scripts\run_server.ps1"
Write-Host "  Run Lesson 05:         .\scripts\run_lesson05.ps1"
Write-Host "  Run all scenarios:     .\scripts\run_all.ps1"
