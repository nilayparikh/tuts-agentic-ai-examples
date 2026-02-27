# scripts/run_notebooks.ps1 — Execute all notebooks via nbconvert
# Usage: .\scripts\run_notebooks.ps1 [-Lesson 05|06|07|all]
# Run from: _examples/a2a/
#
# Executes notebooks in-place, updating outputs.
# Note: Lesson 06 notebook explains server components but does NOT start
#       the server (that blocks). Lesson 07 requires the server running.

param(
    [string]$Lesson = "all"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$Python = Join-Path $Root ".venv\Scripts\python.exe"

Write-Host "=== A2A Examples — Run Notebooks ===" -ForegroundColor Cyan
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

function Invoke-Notebook {
    param([string]$NotebookPath, [string]$Label)

    if (-not (Test-Path $NotebookPath)) {
        Write-Host "  SKIP — not found: $NotebookPath" -ForegroundColor Yellow
        return
    }

    Write-Host "  Running $Label ..." -ForegroundColor Cyan
    $Cwd = Split-Path -Parent $NotebookPath

    try {
        & $Python -m nbconvert `
            --to notebook `
            --execute `
            --inplace `
            --ExecutePreprocessor.timeout=120 `
            --ExecutePreprocessor.kernel_name=a2a-examples `
            $NotebookPath `
            2>&1 | Out-Null
        Write-Host "  ✅ $Label complete" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ $Label failed: $_" -ForegroundColor Red
    }
}

$Lessons = @{
    "05" = @{
        label    = "Lesson 05 — QA Agent"
        notebook = Join-Path $Root "lessons\05-first-a2a-agent\src\qa_agent.ipynb"
    }
    "06" = @{
        label    = "Lesson 06 — A2A Server (components walkthrough)"
        notebook = Join-Path $Root "lessons\06-a2a-server\src\a2a_server.ipynb"
    }
    "07" = @{
        label    = "Lesson 07 — A2A Client"
        notebook = Join-Path $Root "lessons\07-a2a-client\src\a2a_client.ipynb"
    }
}

if ($Lesson -eq "all") {
    # Lesson 07 requires server running
    Write-Host "Note: Lesson 07 requires the A2A server running on localhost:10001" -ForegroundColor Yellow
    Write-Host "      If server is not running, Lesson 07 cells will fail gracefully." -ForegroundColor Yellow
    Write-Host ""

    foreach ($Key in @("05", "06", "07")) {
        $Entry = $Lessons[$Key]
        Invoke-Notebook -NotebookPath $Entry.notebook -Label $Entry.label
    }
} elseif ($Lessons.ContainsKey($Lesson)) {
    $Entry = $Lessons[$Lesson]
    Invoke-Notebook -NotebookPath $Entry.notebook -Label $Entry.label
} else {
    Write-Host "Unknown lesson: $Lesson. Use 05, 06, 07, or all." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Notebook run complete." -ForegroundColor Green
