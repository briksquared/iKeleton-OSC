# Classify all unwired .tox → logs/RESEARCH_TAXONOMY.md (full list, not diff head-only)
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Out = Join-Path $Kit "logs\RESEARCH_TAXONOMY.md"
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\RESEARCH_TAXONOMY.md"

$pyFiles = @(
    "brikvj_resolume_stack.py", "brikvj_harvest_scene_expansion.py", "brikvj_research_lab.py",
    "brikvj_glitch_fluid_layers.py", "brikvj_overlay_generative.py",
    "sync_harvest_generative.ps1", "sync_harvest_research.ps1", "sync_harvest_extended.ps1", "sync_harvest_parts.ps1"
)
$code = ($pyFiles | ForEach-Object {
    $p = Join-Path $PSScriptRoot $_
    if (Test-Path $p) { Get-Content $p -Raw } else { "" }
}) -join "`n"

function Test-Referenced($name) {
    $base = [System.IO.Path]::GetFileName($name)
    return ($code -match [regex]::Escape($base))
}

$unwired = @()
foreach ($sub in @("generative", "harvest_pick", "research", "extra", "glitch_fluid", "vj_suite")) {
    $dir = Join-Path $Kit "parts\$sub"
    if (-not (Test-Path $dir)) { continue }
    Get-ChildItem $dir -Filter "*.tox" -File | ForEach-Object {
        if (-not (Test-Referenced $_.Name)) {
            $unwired += [PSCustomObject]@{
                rel = "parts/$sub/$($_.Name)".Replace("\", "/")
                name = $_.Name
                bucket = $sub
            }
        }
    }
}

function Get-Category($name) {
    $n = $name.ToLower()
    if ($n -match 'hydra|ojack-hydra') { return 'hydra_lab' }
    if ($n -match 'okvj|okvj-shared') { return 'okvj_shared' }
    if ($n -match 'brioch') { return 'brioch_pick' }
    if ($n -match 'audio|fft|spectrum|band') { return 'audio_reactive' }
    if ($n -match 'dome|fulldome|projection|map') { return 'mapping_output' }
    if ($n -match 'record|ndi|spout|stream') { return 'io_stream' }
    return 'other_generative'
}

$groups = @{}
foreach ($u in $unwired) {
    $cat = Get-Category $u.name
    if (-not $groups[$cat]) { $groups[$cat] = New-Object System.Collections.Generic.List[string] }
    $groups[$cat].Add($u.rel)
}

$md = @"
# BRIKVJ unwired taxonomy (generated $(Get-Date -Format o))

**Total unwired:** $($unwired.Count) — do **not** bulk-wire; use [RESEARCH_PASS_PLAN_DEEPER.md](../RESEARCH_PASS_PLAN_DEEPER.md) scoring.

| Category | Count | Integrate via |
|----------|------:|---------------|
$(($groups.GetEnumerator() | Sort-Object { $_.Value.Count } -Descending | ForEach-Object {
    $via = switch ($_.Key) {
        'hydra_lab' { 'brikvj_research_lab.py lazy RB-004' }
        'okvj_shared' { 'FX_DEFS / SCENE_DEFS / td2023' }
        'brioch_pick' { 'dedupe SCENE_DEFS first' }
        'mapping_output' { 'F5 / broadcast / kantan' }
        'audio_reactive' { 'audio COMP or bind' }
        default { 'score DEEPER section 6' }
    }
    "| $($_.Key) | $($_.Value.Count) | $via |"
}) -join "`n")

## Full lists by category

$(foreach ($kv in ($groups.GetEnumerator() | Sort-Object Name)) {
    "### $($kv.Key) ($($kv.Value.Count))`n"
    ($kv.Value | Sort-Object | ForEach-Object { "- $_" }) -join "`n"
    "`n"
})
"@

foreach ($p in @($Out, $Live)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $p) | Out-Null
    $md | Set-Content $p -Encoding utf8
}
Write-Host "RESEARCH_TAXONOMY.md total=$($unwired.Count)"
exit 0
