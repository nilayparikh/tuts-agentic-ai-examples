# scripts/run_client.ps1 — Send test requests to a running A2A server
# Usage: .\scripts\run_client.ps1
# Run from: _examples/a2a/
#
# Requires: Lesson 06 server running on localhost:10001
#           Start it with: .\scripts\run_server.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$ClientSrc = Join-Path $Root "lessons\07-a2a-client\src"

Write-Host "=== Lesson 07 — A2A Client Tests ===" -ForegroundColor Cyan
Write-Host ""

# ── Check server is up ─────────────────────────────────────────
Write-Host "Checking http://localhost:10001/.well-known/agent.json ..." -ForegroundColor Gray
try {
    $AgentCard = Invoke-RestMethod -Uri "http://localhost:10001/.well-known/agent.json" -TimeoutSec 5
    Write-Host "✅ Server is running — Agent: $($AgentCard.name)" -ForegroundColor Green
    Write-Host "   Skills: $($AgentCard.skills | ForEach-Object { $_.name } | Join-String -Separator ', ')"
} catch {
    Write-Host "❌ Server not reachable at http://localhost:10001" -ForegroundColor Red
    Write-Host "   Start it first: .\scripts\run_server.ps1"
    exit 1
}
Write-Host ""

# ── Test questions via JSON-RPC curl-equivalent ───────────────
$Questions = @(
    "What is the annual deductible?",
    "How much is the monthly premium?",
    "Are cosmetic procedures covered?",
    "How do I file a claim?"
)

foreach ($Question in $Questions) {
    $MsgId = [System.Guid]::NewGuid().ToString("N")
    $ReqId = [System.Guid]::NewGuid().ToString("N")

    $Body = @{
        jsonrpc = "2.0"
        id = $ReqId
        method = "message/send"
        params = @{
            message = @{
                role = "user"
                parts = @(@{ kind = "text"; text = $Question })
                messageId = $MsgId
            }
        }
    } | ConvertTo-Json -Depth 10

    Write-Host "Q: $Question" -ForegroundColor Yellow

    try {
        $Response = Invoke-RestMethod -Uri "http://localhost:10001" `
            -Method POST `
            -ContentType "application/json" `
            -Body $Body `
            -TimeoutSec 30

        # Navigate: result.status.message.parts[0].text
        $Text = $Response.result.status.message.parts[0].text
        if ($Text) {
            Write-Host "A: $($Text.Substring(0, [Math]::Min(200, $Text.Length)))..." -ForegroundColor White
        } else {
            Write-Host "A: (no text in response)" -ForegroundColor Gray
            $Response | ConvertTo-Json -Depth 5 | Write-Host
        }
    } catch {
        Write-Host "ERROR: $_" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "✅ Client test complete." -ForegroundColor Green
