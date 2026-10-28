# One TD launch max: build via RUN_BUILD.flag + autostart, poll build.log only, verify once after exit.
# Does NOT toeexpand in a loop (that was lagging the machine).
param(
    [switch]$SkipBriochFix
)

$ErrorActionPreference = "Stop"
$Td = "C:\Program Files\Derivative\TouchDesigner\bin\TouchDesigner.exe"
$ToeExpand = "C:\Program Files\Derivative\TouchDesigner\bin\toeexpand.exe"
$ToeCollapse = "C:\Program Files\Derivative\TouchDesigner\bin\toecollapse.exe"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$Flag = Join-Path $Base "RUN_BUILD.flag"
$Here = $PSScriptRoot
$Verify = Join-Path $Here "verify_brikvj_stack.ps1"
$Inject = Join-Path $Here "inject_brikvj_build_autostart.py"
$Log = Join-Path $Base "logs\build.log"
$Lock = Join-Path $Base "logs\build.lock"

if (Test-Path $Lock) {
    Write-Host "Build already running (logs\build.lock). Exiting."
    exit 3
}

$ea0 = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
Get-Process TouchDesigner -ErrorAction SilentlyContinue | Stop-Process -Force
$ErrorActionPreference = $ea0
Start-Sleep 2

New-Item -ItemType Directory -Force -Path (Split-Path $Lock) | Out-Null
New-Item -ItemType File -Force -Path $Lock | Out-Null
try {
    & "$Here\sync_scripts_to_documents.ps1"
    if (-not $SkipBriochFix -and (Get-Item $Toe).Length -lt 2000000) {
        & "$Here\fix_brikvj_brioch_toe.ps1"
    } elseif ((Get-Item $Toe).Length -ge 2000000) {
        $ErrorActionPreference = "SilentlyContinue"
        & $Verify | Out-Null
        $ErrorActionPreference = "Stop"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Stack already saved in BRIKVJ.toe."
            exit 0
        }
    }

    Remove-Item "$Toe.dir", "$Toe.toc" -Force -ErrorAction SilentlyContinue
    Push-Location $Base
    $ErrorActionPreference = "Continue"
    & $ToeExpand "BRIKVJ.toe" | Out-Null
    Pop-Location
    & python $Inject $Toe
    if ($LASTEXITCODE -ne 0) { throw "inject autostart failed" }
    Push-Location $Base
    & $ToeCollapse "BRIKVJ.toe" | Out-Null
    Pop-Location
    Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
    if ((Get-Item $Toe).Length -lt 100000) { throw "toecollapse failed" }

    Remove-Item $Log -Force -ErrorAction SilentlyContinue
    New-Item -ItemType File -Force -Path $Flag | Out-Null

    Write-Host "Single unattended TD run (minimized) — polling build.log only..."
    $p = Start-Process -FilePath $Td -ArgumentList "`"$Toe`"" -WindowStyle Minimized -PassThru
    $deadline = (Get-Date).AddMinutes(25)
    $done = $false
    $failed = $false
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Seconds 8
        if ($p.HasExited) { break }
        if (-not (Test-Path $Log)) { continue }
        $raw = Get-Content $Log -Raw -ErrorAction SilentlyContinue
        if ($raw -match "all-in-one finished") { $done = $true; break }
        if ($raw -match "Traceback") { $failed = $true; break }
    }

    if (-not $p.HasExited) {
        Start-Sleep -Seconds 15
        if (-not $p.HasExited) {
            $p.CloseMainWindow() | Out-Null
            Start-Sleep -Seconds 10
            if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
        }
    }

    if (Test-Path $Log) {
        Write-Host "--- build.log (tail) ---"
        Get-Content $Log -Tail 20
    }

    if ($failed -or -not $done) {
        if (-not (Test-Path $Log)) { Write-Host "No build.log — autostart did not run." }
        exit 1
    }

    Start-Sleep -Seconds 2
    & $Verify
    if ($LASTEXITCODE -ne 0) { exit 1 }

    & "$Here\remove_brikvj_autostart_from_toe.ps1" | Out-Null
    & "$Here\install_manual_build_into_toe.ps1" | Out-Null
    Write-Host "BRIKVJ stack saved."
    exit 0
}
finally {
    Remove-Item $Lock -Force -ErrorAction SilentlyContinue
}
