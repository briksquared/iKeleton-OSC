# Machine-readable gap report for next-session triage → logs/GAPS_REPORT.md (kit + Documents).
param(
    [string]$BrikHome = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
)
$ErrorActionPreference = "Continue"
$KitRoot = Split-Path $PSScriptRoot -Parent
$OutKit = Join-Path $KitRoot "logs\GAPS_REPORT.md"
$OutLive = Join-Path $BrikHome "logs\GAPS_REPORT.md"
$Toe = Join-Path $BrikHome "BRIKVJ.toe"
$gaps = New-Object System.Collections.Generic.List[string]
$ok = New-Object System.Collections.Generic.List[string]

function Note-Ok($s) { $ok.Add($s) }
function Note-Gap($s) { $gaps.Add($s) }

if (-not (Test-Path $Toe)) { Note-Gap "MISSING live toe: $Toe" }
else {
    $len = (Get-Item $Toe).Length
    if ($len -lt 2000000) { Note-Gap "Toe small ($len B) — likely Brioch-only; run mega build" }
    elseif ($len -lt 4000000) { Note-Ok "Toe $len B — partial stack possible" }
    else { Note-Ok "Toe $len B — expanded stack likely saved" }
}

if (Get-Process TouchDesigner -ErrorAction SilentlyContinue) {
    Note-Gap "TouchDesigner running — skip unattended build; use capture or wait"
} else { Note-Ok "TouchDesigner not running — OK for run_once_unattended" }

foreach ($f in @("RUN_BUILD.flag", "logs\build.lock")) {
    $p = Join-Path $BrikHome $f
    if (Test-Path $p) { Note-Gap "Stale or active: $p" }
}

$buildLog = Join-Path $BrikHome "logs\build.log"
if (-not (Test-Path $buildLog)) {
    Note-Gap "No build.log — mega/fast build never ran or logs cleared"
} else {
    $tail = Get-Content $buildLog -Tail 15 -ErrorAction SilentlyContinue
    $raw = Get-Content $buildLog -Raw -ErrorAction SilentlyContinue
    if ($raw -match "Traceback") { Note-Gap "build.log contains Traceback — open log and fix script" }
    if ($raw -match "\[BRIKVJ mega\] project\.save\(\) OK") { Note-Ok "Last mega build saved project" }
    elseif ($raw -match "\[BRIKVJ resolume\] project\.save\(\) OK") { Note-Ok "Last resolume build saved project" }
    else { Note-Gap "build.log missing project.save() OK — rebuild needed" }
}

$toxIdx = Join-Path $KitRoot "parts\TOX_BUILDS.json"
if (Test-Path $toxIdx) {
    $j = Get-Content $toxIdx -Raw | ConvertFrom-Json
    Note-Ok "TOX_BUILDS: $($j.count) indexed, $($j.newerCount) newer than host"
    if ($j.newerCount -gt 50) { Note-Gap "Many newer tox — expect skips or dialogs unless td2023/ resaves" }
} else { Note-Gap "Missing parts/TOX_BUILDS.json — run scan_tox_build_versions.ps1" }

$harvest = Join-Path $KitRoot "parts\harvest_pick\HARVEST_PICK.json"
if (Test-Path $harvest) {
    $h = Get-Content $harvest -Raw | ConvertFrom-Json
    Note-Ok "harvest_pick: $($h.count) files on disk"
} else { Note-Gap "Run sync_harvest_from_index.ps1" }

if (Test-Path (Join-Path $BrikHome "logs\td_errors.txt")) {
    $n = (Get-Content (Join-Path $BrikHome "logs\td_errors.txt") | Measure-Object -Line).Lines
    if ($n -gt 40) { Note-Gap "td_errors.txt has $n lines — Brioch/audio/mesh; run patch_brikvj_quiet_open + MOTU 3-4" }
    else { Note-Ok "td_errors.txt $n lines" }
} else { Note-Gap "No td_errors.txt — run capture_brikvj_errors.ps1 when TD available" }

$repo = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC"
if (Test-Path $repo) {
    Push-Location $repo
    $st = git status -sb 2>$null | Select-Object -First 1
    Pop-Location
    if ($st -match '\?\?| M | M') { Note-Gap "iKeleton-OSC git dirty: $st" }
    else { Note-Ok "iKeleton-OSC git: $st" }
}

$md = @"
# BRIKVJ gap report (generated $(Get-Date -Format o))

Run: ``scripts/brikvj_gap_report.ps1`` — then read [NEXT_SESSION_PLAN.md](../NEXT_SESSION_PLAN.md).

## Gaps ($($gaps.Count))

$(if ($gaps.Count) { ($gaps | ForEach-Object { "- $_" }) -join "`n" } else { "- (none flagged)" })

## OK ($($ok.Count))

$(($ok | ForEach-Object { "- $_" }) -join "`n")

## Suggested next command

``````powershell
& "$PSScriptRoot\sync_scripts_to_documents.ps1"
& "$PSScriptRoot\brikvj_gap_report.ps1"
# if TD closed and gaps include rebuild:
& "$PSScriptRoot\run_once_unattended.ps1" -ForceResolumeRebuild
``````
"@

New-Item -ItemType Directory -Force -Path (Split-Path $OutKit) | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $BrikHome "logs") -ErrorAction SilentlyContinue | Out-Null
$md | Set-Content $OutKit -Encoding utf8
$md | Set-Content $OutLive -Encoding utf8
Write-Host "Wrote $OutKit and $OutLive"
if ($gaps.Count) { exit 1 } else { exit 0 }
