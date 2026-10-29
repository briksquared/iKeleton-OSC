# Full research pass → logs/RESEARCH_PASS.md (kit + Documents). No TouchDesigner.
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
$OutKit = Join-Path $Kit "logs\RESEARCH_PASS.md"
$OutLive = Join-Path $Live "logs\RESEARCH_PASS.md"

& "$PSScriptRoot\brikvj_research_diff.ps1" | Out-Null
& "$PSScriptRoot\brikvj_bug_scan.ps1" | Out-Null
& "$PSScriptRoot\brikvj_gap_report.ps1" | Out-Null
$gapExit = $LASTEXITCODE

$rs = Get-Content (Join-Path $Kit "scripts\brikvj_resolume_stack.py") -Raw
$sceneN = ([regex]::Matches($rs, '(?m)^\s+\("[^"]+",\s*(?:PARTS|SUITE|GLITCH|GEN|EXTRA)')).Count
$fxBlock = [regex]::Match($rs, 'FX_DEFS = \((.*?)\n\)', 'Singleline').Groups[1].Value
$fxN = ([regex]::Matches($fxBlock, '(?m)^\s+\(')).Count
$megaRaw = Get-Content (Join-Path $Kit "scripts\old_brik_vj_mega.py") -Raw
$megaBlock = [regex]::Match($megaRaw, 'STEPS = \((.*?)\n\)', 'Singleline').Groups[1].Value
$megaN = ([regex]::Matches($megaBlock, '"brikvj_[^"]+\.py"')).Count
& "$PSScriptRoot\brikvj_research_taxonomy.ps1" | Out-Null
$tax = Get-Content (Join-Path $Kit "logs\RESEARCH_TAXONOMY.md") -Raw -ErrorAction SilentlyContinue
$taxRows = if ($tax) { [regex]::Matches($tax, '\|\s+\w+\S*\s+\|\s+\d+\s+\|').Count } else { 0 }

$diff = Get-Content (Join-Path $Kit "logs\RESEARCH_DIFF.md") -Raw
$unwired = if ($diff -match 'Unwired \.tox \((\d+)\)') { [int]$Matches[1] } else { 0 }
$newer = if ($diff -match 'Newer than host \((\d+)\)') { [int]$Matches[1] } else { 0 }
$hydraUn = ([regex]::Matches($diff, 'ojack-hydra|HydraTD_')).Count
$briochUn = ([regex]::Matches($diff, 'brioch-audio-reactive')).Count
$okvjUn = ([regex]::Matches($diff, 'okVJ-Shared')).Count

$idxPath = Join-Path $Kit "HARVEST_INDEX.json"
$harvestStats = "missing"
if (Test-Path $idxPath) {
    $j = Get-Content $idxPath -Raw | ConvertFrom-Json
    $harvestStats = "indexed $($j.totalIndexed), priority $($j.brikvjPriorityCount), archive tox $($j.counts.tox)"
}

$toeLen = if (Test-Path "$Live\BRIKVJ.toe") { (Get-Item "$Live\BRIKVJ.toe").Length } else { 0 }
$openRb = ([regex]::Matches((Get-Content (Join-Path $Kit "RESEARCH_BACKLOG.md") -Raw), '\|\s*open\s*\|')).Count

$candidates = @(
    "| okVJ-Shared_colorizer.tox | FX | color grade gap | check TOX_BUILDS |",
    "| okVJ-Shared_analogueWarmthFXStack.tox | FX | warmth stack | td2023 if newer |",
    "| okVJ-Shared_dome_preview.tox | output | fulldome prep | RB-003 bank |",
    "| brioch-audio-reactive-vjing_stroboscope.tox | scene | compare to scene_stroboscope | dedupe |",
    "| okVJ-Shared_constructOutputMap.tox | map | kantan adjunct | research only |"
)

$md = @"
# BRIKVJ research pass (generated $(Get-Date -Format o))

Auto: ``scripts/brikvj_research_pass.ps1``. Strategy: [RESEARCH_PASS_PLAN.md](../RESEARCH_PASS_PLAN.md).

## Measured kit (code SSOT)

| Metric | Value | Source |
|--------|------:|--------|
| SCENE_DEFS | $sceneN | ``brikvj_resolume_stack.py`` |
| FX_DEFS | $fxN | same |
| Mega steps | $megaN | ``old_brik_vj_mega.py`` |
| harvest_scene_expansion MAX | 14 | ``brikvj_harvest_scene_expansion.py`` |
| Live toe bytes | $toeLen | Documents BRIKVJ.toe |
| Unwired .tox | $unwired | RESEARCH_DIFF |
| Newer than 2023 | $newer | RESEARCH_DIFF / TOX_BUILDS |
| Unwired Hydra-ish lines (in diff head) | ~$hydraUn | prefer lab lazy RB-004 |
| Unwired okVJ-Shared (in diff head) | ~$okvjUn | FX/scene candidates |
| Unwired brioch picks (in diff head) | ~$briochUn | dedupe vs SCENE_DEFS |
| HARVEST_INDEX | $harvestStats | HARVEST_INDEX.json |
| RESEARCH_BACKLOG open | $openRb | RESEARCH_BACKLOG.md |
| gap_report exit | $gapExit | GAPS_REPORT.md |

## Parity snapshot

See [VJ_FEATURE_PARITY.md](../VJ_FEATURE_PARITY.md). **●** = in stack; **◐** = partial (plan targets below).

| Gap (◐) | Plan ID |
|---------|---------|
| HAP / codec tuning | DOC only — drop HAP in ``media/clips/`` |
| Text / logo TOP | F6 — TD Text + kantan |
| Synesthesia preset port | F6 — reference Synaesthesia.toe |
| MadMapper masking depth | F5 — kantan shapes audit |
| SMPTE / DMX | out of scope unless user asks |

## Integration candidates (next 5 — score before wire)

| Tox | Role | Notes |
|-----|------|-------|
$($candidates -join "`n")

## Bug scan (linked)

See [logs/BUG_SCAN.md](BUG_SCAN.md) and [BUG_REGISTRY.md](../BUG_REGISTRY.md).

## Recommended next sprint

$(if ($gapExit -ne 0) { "**P0** — one mega save (headless/minimized once) then re-run this script." } else { "**R** — integrate top 2 scored non-Hydra tox; update RESEARCH_BACKLOG." })

## Doc ladder after this pass

1. RESEARCH_PASS.md (this file)
2. RESEARCH_PASS_PLAN.md (12-session roadmap)
3. RESEARCH_PASS_PLAN_DEEPER.md (taxonomy + transcript + 18-step program)
4. logs/RESEARCH_TAXONOMY.md ($taxRows categories)
5. MASTER_PLAN.md
"@

foreach ($p in @($OutKit, $OutLive)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $p) | Out-Null
    $md | Set-Content $p -Encoding utf8
}
Write-Host "RESEARCH_PASS.md (unwired=$unwired scenes=$sceneN fx=$fxN)"
exit 0
