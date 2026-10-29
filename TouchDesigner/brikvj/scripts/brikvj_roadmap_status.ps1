# 18-step program status → logs/ROADMAP_STATUS.md + INTEGRATION_QUEUE.json
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$Steps = @(
    @{ id = 1;  name = "One mega save"; done = $false; test = "build_clean" },
    @{ id = 2;  name = "Quiet open user check"; done = $false; test = "manual" },
    @{ id = 3;  name = "MOTU 3-4 td_errors down"; done = $false; test = "td_errors" },
    @{ id = 4;  name = "td2023 resave batch (5 used)"; done = $false; test = "manual" },
    @{ id = 5;  name = "Integrate colorizer OR warmth"; done = $false; test = "manual" },
    @{ id = 6;  name = "Integrate 2 harvest scenes"; done = $false; test = "manual" },
    @{ id = 7;  name = "RB-004 lazy Hydra spec"; done = $false; test = "manual" },
    @{ id = 8;  name = "RB-004 lazy Hydra impl"; done = $false; test = "manual" },
    @{ id = 9;  name = "KEYBOARD_MAP vs scene_switch"; done = $false; test = "manual" },
    @{ id = 10; name = "FEATURE_MATRIX synced"; done = $false; test = "manual" },
    @{ id = 11; name = "dome_preview eval"; done = $false; test = "manual" },
    @{ id = 12; name = "TDA mapper RB-005"; done = $false; test = "manual" },
    @{ id = 13; name = "Ableton link RB-006"; done = $false; test = "manual" },
    @{ id = 14; name = "preset_bank + hub"; done = $false; test = "manual" },
    @{ id = 15; name = "OSC + mapper doc"; done = $false; test = "manual" },
    @{ id = 16; name = "Taxonomy review"; done = $false; test = "manual" },
    @{ id = 17; name = "BUG_REGISTRY clean"; done = $false; test = "manual" },
    @{ id = 18; name = "Optional repo split RB-008"; done = $false; test = "manual" }
)

$buildLog = Join-Path $Live "logs\build.log"
$buildClean = $false
if (Test-Path $buildLog) {
    $bl = Get-Content $buildLog -Raw
    if ($bl -notmatch "Traceback" -and $bl -match "project\.save\(\) OK") { $buildClean = $true }
}
if ($buildClean) { $Steps[0].done = $true }

$tdErr = Join-Path $Live "logs\td_errors.txt"
if (Test-Path $tdErr) {
    $n = (Get-Content $tdErr | Measure-Object -Line).Lines
    if ($n -le 25) { $Steps[2].done = $true }
}

$fm = Get-Content (Join-Path $Kit "FEATURE_MATRIX.md") -Raw -ErrorAction SilentlyContinue
if ($fm -match "29.*FX_DEFS") { $Steps[9].done = $true }

$next = ($Steps | Where-Object { -not $_.done } | Select-Object -First 1)

$queue = @(
    @{ rank = 1; tox = "okVJ-Shared_colorizer.tox"; category = "okvj_shared"; action = "FX_DEFS after td2023 check" },
    @{ rank = 2; tox = "okVJ-Shared_analogueWarmthFXStack.tox"; category = "okvj_shared"; action = "FX_DEFS" },
    @{ rank = 3; tox = "okVJ-Shared_dome_preview.tox"; category = "mapping_output"; action = "F5 eval" },
    @{ rank = 4; tox = "brioch-audio-reactive-vjing_stroboscope.tox"; category = "brioch_pick"; action = "dedupe scene_stroboscope" },
    @{ rank = 5; tox = "(56 hydra modules)"; category = "hydra_lab"; action = "RB-004 lazy — no scene_switch bulk" },
    @{ rank = 6; tox = "parts/vj_suite/audio_crossover.tox"; category = "audio_reactive"; action = "audio bridge" }
)

$md = @"
# BRIKVJ roadmap status (generated $(Get-Date -Format o))

Program: [RESEARCH_PASS_PLAN_DEEPER.md](../RESEARCH_PASS_PLAN_DEEPER.md) section E.

**Next step:** $(if ($next) { "#$($next.id) $($next.name)" } else { "All auto-checks passed — pick manual step" })

| Step | Done | Milestone |
|------|:----:|-----------|
$(($Steps | ForEach-Object { "| $($_.id) | $(if ($_.done) { 'yes' } else { '**no**' }) | $($_.name) |" }) -join "`n")

## Auto checks

| Check | Result |
|-------|--------|
| build.log clean | $buildClean |
| td_errors <= 25 lines | $($Steps[2].done) |

## Integration queue (top 6)

| Rank | Target | Action |
|------|--------|--------|
$(($queue | ForEach-Object { "| $($_.rank) | $($_.tox) | $($_.action) |" }) -join "`n")

Refresh: ``brikvj_roadmap_status.ps1`` after each session.
"@

$json = @{ generated_at = (Get-Date -Format o); next_step = $next.id; steps = $Steps; integration_queue = $queue } | ConvertTo-Json -Depth 5

foreach ($dir in @((Join-Path $Kit "logs"), (Join-Path $Live "logs"))) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $md | Set-Content (Join-Path $dir "ROADMAP_STATUS.md") -Encoding utf8
    $json | Set-Content (Join-Path $dir "INTEGRATION_QUEUE.json") -Encoding utf8
}
Write-Host "ROADMAP_STATUS next=$($next.id)"
exit 0
