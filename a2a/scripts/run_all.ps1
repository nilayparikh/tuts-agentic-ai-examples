# scripts/run_all.ps1 — Full end-to-end scenario runner
# Usage: .\scripts\run_all.ps1
# Run from: _examples/a2a/
#
# Runs all three lessons in order:
#   1. Lesson 05 — standalone QA agent (qa_agent.py)
#   2. Lesson 06 — A2A server (started as background job on port 10001)
#   3. Lesson 07 — A2A client (sends 4 test questions to the server)
#
# Cleans up the background server at the end.

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$ServerPort = 10001
$ServerJob = $null

# ── Banner ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   A2A Examples — Full Scenario Run             ║" -ForegroundColor Cyan
Write-Host "║   Lessons 05 → 06 → 07                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Load .env ─────────────────────────────────────────────────
$EnvFile = Join-Path (Split-Path -Parent $Root) ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "❌ .env not found at $EnvFile" -ForegroundColor Red
    Write-Host "   Run .\scripts\setup.ps1 first."
    exit 1
}
Get-Content $EnvFile | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        [System.Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim())
    }
}
Write-Host "✅ Loaded $EnvFile" -ForegroundColor Green

if (-not $env:GITHUB_TOKEN) {
    Write-Host "❌ GITHUB_TOKEN not set in .env" -ForegroundColor Red
    exit 1
}
Write-Host "✅ GITHUB_TOKEN configured" -ForegroundColor Green
Write-Host ""

# ══════════════════════════════════════════════════════════════
# LESSON 05 — Standalone QA Agent
# ══════════════════════════════════════════════════════════════
Write-Host "━━━ LESSON 05 — Standalone QA Agent ━━━" -ForegroundColor Magenta
Write-Host ""

$Lesson05Src = Join-Path $Root "lessons\05-first-a2a-agent\src"
Set-Location $Lesson05Src

Write-Host "Running qa_agent.py (3 test questions)..." -ForegroundColor Gray
& $Python qa_agent.py
Write-Host ""
Write-Host "✅ Lesson 05 complete" -ForegroundColor Green
Write-Host ""

# ══════════════════════════════════════════════════════════════
# LESSON 06 — Start A2A Server in background
# ══════════════════════════════════════════════════════════════
Write-Host "━━━ LESSON 06 — Starting A2A Server ━━━" -ForegroundColor Magenta
Write-Host ""

$ServerSrc = Join-Path $Root "lessons\06-a2a-server\src"

# Start server as background job
$ServerJob = Start-Job -ScriptBlock {
    param($Python, $Src, $Token)
    $env:GITHUB_TOKEN = $Token
    Set-Location $Src
    & $Python server.py
} -ArgumentList $Python, $ServerSrc, $env:GITHUB_TOKEN

Write-Host "Server starting (job #$($ServerJob.Id))..." -ForegroundColor Gray

# Wait for server to become ready
$MaxWait = 20
$Ready = $false
for ($i = 1; $i -le $MaxWait; $i++) {
    Start-Sleep -Seconds 1
    try {
        $null = Invoke-RestMethod -Uri "http://localhost:${ServerPort}/.well-known/agent.json" -TimeoutSec 2
        $Ready = $true
        break
    } catch { }
    Write-Host "  Waiting for server... ($i/${MaxWait}s)" -ForegroundColor Gray
}

if (-not $Ready) {
    Write-Host "❌ Server did not start within ${MaxWait}s" -ForegroundColor Red
    Stop-Job $ServerJob -ErrorAction SilentlyContinue
    Remove-Job $ServerJob -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "✅ Server ready at http://localhost:${ServerPort}" -ForegroundColor Green

# Verify Agent Card
$Card = Invoke-RestMethod -Uri "http://localhost:${ServerPort}/.well-known/agent.json"
Write-Host "   Agent: $($Card.name) v$($Card.version)"
Write-Host "   Skills: $($Card.skills | ForEach-Object { $_.name } | Join-String -Separator ', ')"
Write-Host ""

# ══════════════════════════════════════════════════════════════
# LESSON 07 — Client Tests
# ══════════════════════════════════════════════════════════════
Write-Host "━━━ LESSON 07 — A2A Client Tests ━━━" -ForegroundColor Magenta
Write-Host ""

$Questions = @(
    "What is the annual deductible?",
    "How much is the monthly premium?",
    "Are cosmetic procedures covered?",
    "How do I file a claim?",
    "What is NOT covered by this policy?"
)

$Passed = 0
$Failed = 0

foreach ($Question in $Questions) {
    $MsgId = [System.Guid]::NewGuid().ToString("N")
    $ReqId = [System.Guid]::NewGuid().ToString("N")

    $Body = @{
        jsonrpc = "2.0"
        id      = $ReqId
        method  = "message/send"
        params  = @{
            message = @{
                role      = "user"
                parts     = @(@{ kind = "text"; text = $Question })
                messageId = $MsgId
            }
        }
    } | ConvertTo-Json -Depth 10

    try {
        $Response = Invoke-RestMethod `
            -Uri "http://localhost:${ServerPort}" `
            -Method POST `
            -ContentType "application/json" `
            -Body $Body `
            -TimeoutSec 60

        $Text = $Response.result.status.message.parts[0].text
        Write-Host "Q: $Question" -ForegroundColor Yellow
        if ($Text) {
            $Short = $Text.Substring(0, [Math]::Min(180, $Text.Length))
            Write-Host "A: $Short$(if ($Text.Length -gt 180) { '...' })" -ForegroundColor White
            $Passed++
        } else {
            Write-Host "A: (empty response)" -ForegroundColor Gray
            $Failed++
        }
    } catch {
        Write-Host "Q: $Question" -ForegroundColor Yellow
        Write-Host "ERROR: $_" -ForegroundColor Red
        $Failed++
    }
    Write-Host ""
}

# ── Results ────────────────────────────────────────────────────
Write-Host "━━━ Results ━━━" -ForegroundColor Magenta
Write-Host "  Passed: $Passed / $($Questions.Count)" -ForegroundColor $(if ($Failed -eq 0) { "Green" } else { "Yellow" })
if ($Failed -gt 0) {
    Write-Host "  Failed: $Failed" -ForegroundColor Red
}

# ── Cleanup ────────────────────────────────────────────────────
Write-Host ""
Write-Host "Stopping server..." -ForegroundColor Gray
if ($ServerJob) {
    Stop-Job $ServerJob -ErrorAction SilentlyContinue
    Remove-Job $ServerJob -ErrorAction SilentlyContinue
    Write-Host "✅ Server stopped" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   All scenarios complete!                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
