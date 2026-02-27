$Python = "y:\.sources\localm-tuts\a2a\_examples\a2a\.venv\Scripts\python.exe"
$ServerSrc = "y:\.sources\localm-tuts\a2a\_examples\a2a\lessons\06-a2a-server\src"
$LogOut = "$env:TEMP\diag_out.txt"
$LogErr = "$env:TEMP\diag_err.txt"

Write-Host "Starting server..."
$proc = Start-Process -FilePath $Python -ArgumentList "server.py" `
    -WorkingDirectory $ServerSrc `
    -RedirectStandardOutput $LogOut `
    -RedirectStandardError $LogErr `
    -NoNewWindow -PassThru

Write-Host "PID: $($proc.Id)"
Start-Sleep -Seconds 5

Write-Host "HasExited: $($proc.HasExited)"
Write-Host ""
Write-Host "=== STDERR ==="
Get-Content $LogErr -ErrorAction SilentlyContinue
Write-Host ""
Write-Host "=== Health Check ==="
try {
    $r = Invoke-RestMethod -Uri "http://localhost:10001/.well-known/agent.json" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "SUCCESS: $($r.name)"
} catch {
    Write-Host "FAIL type: $($_.Exception.GetType().FullName)"
    Write-Host "FAIL msg:  $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Host "HTTP status: $($_.Exception.Response.StatusCode.value__)"
    }
}

Write-Host ""
Write-Host "Stopping..."
Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
Write-Host "Done"
