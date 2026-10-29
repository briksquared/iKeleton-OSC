# Offline toe audit + optional one minimized TD open to snapshot op.errors() — no build, no iKeleton paths.
# Default: no TD launch. Agents use -AllowTouchDesignerLaunch only when user explicitly asked.
param(
    [switch]$AllowTouchDesignerLaunch
)

$ErrorActionPreference = "Stop"
$Td = "C:\Program Files\Derivative\TouchDesigner\bin\TouchDesigner.exe"
$ToeExpand = "C:\Program Files\Derivative\TouchDesigner\bin\toeexpand.exe"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$Here = $PSScriptRoot
$Log = Join-Path $Base "logs\td_errors.txt"
$ReportPath = Join-Path $Base "logs\code_review.txt"

& "$Here\sync_scripts_to_documents.ps1" | Out-Host

$report = @()
$report += "=== BRIKVJ code review $(Get-Date -Format o) ==="

& powershell -NoProfile -ExecutionPolicy Bypass -File "$Here\audit_td_python_api.ps1"
$report += "audit_td_python_api: exit $LASTEXITCODE"
python -m compileall -q (Join-Path $Base "scripts") 2>&1 | ForEach-Object { $report += $_ }
if ($LASTEXITCODE -ne 0) { $report += "compileall: FAIL" } else { $report += "compileall: OK" }

Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
Push-Location $Base
$ea = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $ToeExpand "BRIKVJ.toe" | Out-Null
$ErrorActionPreference = $ea
Pop-Location

& powershell -NoProfile -ExecutionPolicy Bypass -File "$Here\audit_brikvj_toe.ps1" -Dir "$Toe.dir"
$report += "audit_brikvj_toe: exit $LASTEXITCODE"

Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue

if ($AllowTouchDesignerLaunch) {
    $running = Get-Process TouchDesigner -ErrorAction SilentlyContinue
    if ($running) {
        $report += "Closing existing TouchDesigner for one-shot error snapshot..."
        $running | Stop-Process -Force
        Start-Sleep -Seconds 3
    }
    Remove-Item $Log -Force -ErrorAction SilentlyContinue
        $bkp = "$Toe.pre_error_capture"
        Copy-Item $Toe $bkp -Force
        Push-Location $Base
        & $ToeExpand "BRIKVJ.toe" | Out-Null
        Pop-Location
        & python (Join-Path $Here "inject_td_error_snapshot.py") $Toe
        Push-Location $Base
        & "C:\Program Files\Derivative\TouchDesigner\bin\toecollapse.exe" "BRIKVJ.toe" | Out-Null
        Pop-Location
        Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Opening TouchDesigner minimized for error snapshot (no build)..."
        $p = Start-Process -FilePath $Td -ArgumentList "`"$Toe`"" -WindowStyle Minimized -PassThru
        $deadline = (Get-Date).AddMinutes(12)
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Seconds 5
            if (Test-Path $Log) { break }
            if ($p.HasExited) { break }
        }
        if (-not $p.HasExited) {
            Start-Sleep -Seconds 8
            try { $p.CloseMainWindow() | Out-Null } catch { }
            Start-Sleep -Seconds 5
            if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
        }
        if (Test-Path $Log) {
            $report += "--- td_errors.txt ---"
            $report += Get-Content $Log -Raw
        } else {
            $report += "FAIL: no td_errors.txt (boot_trace tail below)"
            if (Test-Path (Join-Path $Base "logs\boot_trace.txt")) {
                $report += Get-Content (Join-Path $Base "logs\boot_trace.txt") -Raw
            }
        }
        Copy-Item $bkp $Toe -Force
        Remove-Item $bkp -Force -ErrorAction SilentlyContinue
}

$report | Out-File -FilePath $ReportPath -Encoding utf8
Write-Host "Wrote $ReportPath"
Get-Content $ReportPath -Tail 30
