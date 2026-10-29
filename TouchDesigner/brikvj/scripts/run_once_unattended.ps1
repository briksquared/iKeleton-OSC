# One TD launch max: build via RUN_BUILD.flag + autostart, poll build.log only, verify once after exit.
# Does NOT toeexpand in a loop (that was lagging the machine).
param(
    [switch]$SkipBriochFix,
    [switch]$ForceResolumeRebuild
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
$Log = Join-Path $Base "logs\build.log"
$Trace = Join-Path $Base "logs\boot_trace.txt"
$Lock = Join-Path $Base "logs\build.lock"

function Clear-ToeExpandArtifacts {
    param([string]$ToePath)
    $dir = "$ToePath.dir"
    $toc = "$ToePath.toc"
    cmd /c "rd /s /q `"$dir`" 2>nul" | Out-Null
    Remove-Item $toc -Force -ErrorAction SilentlyContinue
}

if (Test-Path $Lock) {
    Write-Host "Stale build.lock — remove it if no build is running."
    exit 3
}

if (Get-Process TouchDesigner -ErrorAction SilentlyContinue) {
    Write-Host "TouchDesigner is already open. This script will NOT kill it or launch a second copy."
    Write-Host "Sync only:  sync_scripts_to_documents.ps1"
    Write-Host "Build inside open TD: paste Documents\TouchDesigner\BRIKVJ\scripts\TEXTPORT_BUILD.txt into the Textport, then Save."
    exit 4
}

New-Item -ItemType Directory -Force -Path (Split-Path $Lock) | Out-Null
New-Item -ItemType File -Force -Path $Lock | Out-Null
$dismissProc = $null
try {
    & "$Here\sync_scripts_to_documents.ps1"
    if (-not $SkipBriochFix -and (Get-Item $Toe).Length -lt 2000000) {
        & "$Here\fix_brikvj_brioch_toe.ps1" -InjectBuildAutostart
    } elseif ((Get-Item $Toe).Length -ge 2000000 -and -not $ForceResolumeRebuild) {
        $ErrorActionPreference = "SilentlyContinue"
        & $Verify | Out-Null
        $ErrorActionPreference = "Stop"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Stack already saved in BRIKVJ.toe. Use -ForceResolumeRebuild to re-run fast build."
            exit 0
        }
    }

    if ($ForceResolumeRebuild -or ((Get-Item $Toe).Length -ge 2000000)) {
        Clear-ToeExpandArtifacts $Toe
        Push-Location $Base
        $ErrorActionPreference = "Continue"
        & $ToeExpand "BRIKVJ.toe" | Out-Null
        Pop-Location
        & python (Join-Path $Here "inject_brikvj_build_autostart.py") $Toe
        Push-Location $Base
        & $ToeCollapse "BRIKVJ.toe" | Out-Null
        Pop-Location
        Clear-ToeExpandArtifacts $Toe
    }

    if ($SkipBriochFix) {
        Clear-ToeExpandArtifacts $Toe
        Push-Location $Base
        $ErrorActionPreference = "Continue"
        & $ToeExpand "BRIKVJ.toe" | Out-Null
        Pop-Location
        & python (Join-Path $Here "inject_brikvj_build_autostart.py") $Toe
        & python (Join-Path $Here "inject_kantan_boot.py") $Toe
        Push-Location $Base
        & $ToeCollapse "BRIKVJ.toe" | Out-Null
        Pop-Location
        Clear-ToeExpandArtifacts $Toe
    }
    if ((Get-Item $Toe).Length -lt 100000) { throw "BRIKVJ.toe truncated" }

    Remove-Item $Log, $Trace -Force -ErrorAction SilentlyContinue
    New-Item -ItemType File -Force -Path $Flag | Out-Null

    $ScanTox = Join-Path $Here "scan_tox_build_versions.ps1"
    if (Test-Path $ScanTox) {
        & $ScanTox -OnlySubdirs @("generative", "harvest_pick", "vj_suite", "extra", "glitch_fluid") 2>&1 | Out-Null
    }

    $Dismiss = Join-Path $Here "dismiss_td_dialogs.ps1"
    $dismissProc = $null
    if (Test-Path $Dismiss) {
        $dismissProc = Start-Process -FilePath "powershell.exe" -ArgumentList @(
            "-NoProfile", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", $Dismiss
        ) -PassThru
    }

    Write-Host "Single unattended TD run (minimized) — polling build.log only..."
    $p = Start-Process -FilePath $Td -ArgumentList "`"$Toe`"" -WindowStyle Minimized -PassThru
    $deadline = (Get-Date).AddMinutes(45)
    $done = $false
    $failed = $false
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Seconds 8
        if ($p.HasExited) { break }
        if (Test-Path $Trace) {
            $tr = Get-Content $Trace -Raw -ErrorAction SilentlyContinue
            if ($tr -notmatch '(^|\r?\n)2(\r?\n|$)') { continue }
        } elseif (-not (Test-Path $Log)) { continue }
        if (-not (Test-Path $Log)) { continue }
        $raw = Get-Content $Log -Raw -ErrorAction SilentlyContinue
        if ($raw -match "project\.save\(\) OK|\[BRIKVJ (resolume|mega)\] finished") { $done = $true; break }
        if ($raw -match "all-in-one finished") { $done = $true; break }
        if (Test-Path $Trace) {
            $tr2 = Get-Content $Trace -Raw -ErrorAction SilentlyContinue
            if ($tr2 -match "S") { $done = $true; break }
        }
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
        if (-not (Test-Path $Trace)) { Write-Host "No boot_trace — Execute onStart never ran." }
        elseif (-not (Test-Path $Log)) { Write-Host "boot_trace OK but no build.log — all-in-one failed before first log line." }
        elseif ($p.HasExited -and -not $failed) { Write-Host "TouchDesigner exited before all-in-one finished (crash or quit)." }
        if (Test-Path $Log) {
            Write-Host "--- build.log (full) ---"
            Get-Content $Log
        }
        if (Test-Path $Trace) {
            Write-Host "--- boot_trace ---"
            Get-Content $Trace
        }
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
    if ($dismissProc -and -not $dismissProc.HasExited) {
        Stop-Process -Id $dismissProc.Id -Force -ErrorAction SilentlyContinue
    }
    Remove-Item $Lock -Force -ErrorAction SilentlyContinue
}
