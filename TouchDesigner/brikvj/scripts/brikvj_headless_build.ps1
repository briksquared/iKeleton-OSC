# Inject build-on-start (safe toc), open TouchDesigner once, wait for stack + save.
# AGENTS: requires -AllowTouchDesignerLaunch (user must ask explicitly).
param([switch]$AllowTouchDesignerLaunch)
$ErrorActionPreference = "Stop"
$Td = "C:\Program Files\Derivative\TouchDesigner\bin\TouchDesigner.exe"
$ToeExpand = "C:\Program Files\Derivative\TouchDesigner\bin\toeexpand.exe"
$ToeCollapse = "C:\Program Files\Derivative\TouchDesigner\bin\toecollapse.exe"
$Base = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Toe = Join-Path $Base "BRIKVJ.toe"
$Here = $PSScriptRoot
$Verify = Join-Path $Here "verify_brikvj_stack.ps1"
$Inject = Join-Path $Here "inject_brikvj_build_autostart.py"

function Ensure-ToeSize {
    if (-not (Test-Path $Toe) -or (Get-Item $Toe).Length -lt 100000) {
        $bkp = Get-ChildItem (Join-Path $Base "BRIKVJ.toe.bkp*") | Sort-Object Length -Descending | Select-Object -First 1
        if (-not $bkp) { throw "BRIKVJ.toe missing/truncated and no .bkp found" }
        Copy-Item $bkp.FullName $Toe -Force
        Write-Host "Restored toe from $($bkp.Name)"
    }
}

function Inject-Autostart {
    Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
    Push-Location $Base
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $ToeExpand "BRIKVJ.toe" | Out-Null
    $ErrorActionPreference = $prev
    Pop-Location
    & python $Inject $Toe
    if ($LASTEXITCODE -ne 0) { throw "inject failed" }
    Push-Location $Base
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $ToeCollapse "BRIKVJ.toe" | Write-Host
    $ErrorActionPreference = $prev
    Pop-Location
    if ((Get-Item $Toe).Length -lt 100000) { throw "toecollapse truncated BRIKVJ.toe" }
    Remove-Item "$Toe.dir", "$Toe.toc" -Recurse -Force -ErrorAction SilentlyContinue
}

& "$Here\sync_scripts_to_documents.ps1"
Ensure-ToeSize

$verifyOk = $false
try {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $Verify *> $null
    if ($LASTEXITCODE -eq 0) { $verifyOk = $true }
} catch { }
if (-not $verifyOk) {
    Write-Host "Stack not in .toe — close TD, run CLEAN_AND_REOPEN.cmd, then TEXTPORT_BUILD.txt once (see ERRORS.md)."
    Write-Host "Autostart inject disabled (was causing Textport spam)."
    exit 1
}

$running = Get-Process TouchDesigner -ErrorAction SilentlyContinue
if ($running) {
    Write-Host "Close TouchDesigner first, then re-run BUILD_STACK.cmd"
    exit 2
}

if (-not $AllowTouchDesignerLaunch) {
    Write-Host "REFUSED: TouchDesigner not started. User opens BRIKVJ.toe or paste TEXTPORT_MEGA.txt. Agents need user OK for -AllowTouchDesignerLaunch."
    exit 5
}

Write-Host "Opening TouchDesigner — first start runs all-in-one + save (several minutes)..."
$p = Start-Process -FilePath $Td -ArgumentList "`"$Toe`"" -PassThru

$deadline = (Get-Date).AddMinutes(15)
$ok = $false
while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 10
    if ($p.HasExited) {
        Write-Warning "TouchDesigner exited (code $($p.ExitCode))"
        break
    }
    & powershell -NoProfile -ExecutionPolicy Bypass -File $Verify *> $null
    if ($LASTEXITCODE -eq 0) {
        $ok = $true
        break
    }
}

if (-not $ok) {
    Write-Host "Stack not verified yet — leave TD open, watch Textport for errors, or paste TEXTPORT_BUILD.txt and Save."
    exit 1
}

Start-Sleep -Seconds 5
if (-not $p.HasExited) {
    $p.CloseMainWindow() | Out-Null
    Start-Sleep -Seconds 8
    if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
}

& "$Here\fix_brikvj_brioch_toe.ps1" | Out-Null
Write-Host "BRIKVJ stack: OK"
exit 0
