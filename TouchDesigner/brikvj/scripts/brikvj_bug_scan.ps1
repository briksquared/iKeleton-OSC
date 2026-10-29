# Aggregate known failures → logs/BUG_SCAN.md + append to BUG_REGISTRY sources
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Out = Join-Path $Kit "logs\BUG_SCAN.md"
$OutLive = Join-Path $Live "logs\BUG_SCAN.md"

$bugs = New-Object System.Collections.Generic.List[string]

function Add-Bug($id, $sev, $summary, $fix) {
    $bugs.Add("| $id | $sev | $summary | $fix |")
}

$buildLog = Join-Path $Live "logs\build.log"
if (Test-Path $buildLog) {
    $bl = Get-Content $buildLog -Raw
    if ($bl -match "Traceback") {
        $script = if ($bl -match 'File "[^"]+\\([^\\]+\.py)"') { $Matches[1] } else { "?" }
        Add-Bug "B-LOG-001" "P0" "build.log Traceback ($script)" "Fix script; one headless/minimized mega save"
    }
    $wires = ([regex]::Matches($bl, "\[BRIKVJ resolume\] wire:")).Count
    if ($wires -gt 3) { Add-Bug "B-LOG-002" "P1" "resolume wire errors ($wires lines)" "td_top_out FX chain (RB-002); rebuild" }
}

$tdErr = Join-Path $Live "logs\td_errors.txt"
if (Test-Path $tdErr) {
    $n = (Get-Content $tdErr | Measure-Object -Line).Lines
    if ($n -gt 20) {
        Add-Bug "B-TD-001" "P1" "td_errors.txt $n lines (Brioch analyseAudio/mesh)" "MOTU 3-4; quiet open; no force cook"
    }
}

if (Test-Path (Join-Path $Kit "parts\TOX_BUILDS.json")) {
    $j = Get-Content (Join-Path $Kit "parts\TOX_BUILDS.json") -Raw | ConvertFrom-Json
    if ($j.newerCount -gt 40) {
        Add-Bug "B-TOX-001" "P1" "$($j.newerCount) tox newer than 2023" "td2023 resaves RB-001; Accept pref"
    }
}

Add-Bug "B-GPU-001" "P2" "Transient GPU/driver dialog (user report)" "One TD instance; NVIDIA perf mode; note exact text if repeats"

$md = @"
# BRIKVJ bug scan (generated $(Get-Date -Format o))

Run: ``scripts/brikvj_bug_scan.ps1``. Full registry: [BUG_REGISTRY.md](../BUG_REGISTRY.md).

| ID | Sev | Summary | Fix |
|----|-----|---------|-----|
$(if ($bugs.Count) { $bugs -join "`n" } else { "| — | — | No auto-detected bugs | — |" })

## Next code review targets

- ``old_brik_vj_mega.py`` step list vs ``BUILD.md``
- ``brikvj_live_levels_drive.py`` (crash history — keep out of mega)
- ``FEATURE_MATRIX.md`` stale counts → recount from ``brikvj_resolume_stack.py``
"@

foreach ($p in @($Out, $OutLive)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $p) | Out-Null
    $md | Set-Content $p -Encoding utf8
}
Write-Host "BUG_SCAN.md ($($bugs.Count) rows)"
exit 0
