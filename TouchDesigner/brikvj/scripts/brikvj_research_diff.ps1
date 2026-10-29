# Compare harvest on disk vs Python loaders → logs/RESEARCH_DIFF.md (find work automatically).
$ErrorActionPreference = "Continue"
$Kit = Split-Path $PSScriptRoot -Parent
$Out = Join-Path $Kit "logs\RESEARCH_DIFF.md"
$Live = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\RESEARCH_DIFF.md"

$pyFiles = @(
    "brikvj_resolume_stack.py",
    "brikvj_harvest_scene_expansion.py",
    "brikvj_research_lab.py",
    "brikvj_glitch_fluid_layers.py",
    "brikvj_overlay_generative.py",
    "sync_harvest_parts.ps1",
    "sync_harvest_extended.ps1",
    "sync_harvest_generative.ps1",
    "sync_harvest_research.ps1"
)
$code = ($pyFiles | ForEach-Object {
    $p = Join-Path $PSScriptRoot $_
    if (Test-Path $p) { Get-Content $p -Raw -ErrorAction SilentlyContinue } else { "" }
}) -join "`n"

function Test-Referenced($name) {
    $base = [System.IO.Path]::GetFileName($name)
    return ($code -match [regex]::Escape($base))
}

$unwired = @()
foreach ($sub in @("generative", "harvest_pick", "research", "extra", "glitch_fluid", "vj_suite", "parts")) {
    $dir = if ($sub -eq "parts") { $Kit } else { Join-Path $Kit "parts\$sub" }
    if (-not (Test-Path $dir)) { continue }
    Get-ChildItem $dir -Filter "*.tox" -File -ErrorAction SilentlyContinue | ForEach-Object {
        if (-not (Test-Referenced $_.Name)) {
            $rel = $_.FullName.Substring($Kit.Length).TrimStart("\")
            $unwired += $rel
        }
    }
}

$idxPath = Join-Path $Kit "parts\TOX_BUILDS.json"
$newer = @()
if (Test-Path $idxPath) {
    $idx = Get-Content $idxPath -Raw | ConvertFrom-Json
    foreach ($prop in $idx.files.PSObject.Properties) {
        if ($prop.Value.newerThanHost) { $newer += $prop.Name }
    }
}

$md = @"
# BRIKVJ research diff (generated $(Get-Date -Format o))

Auto-generated: **tox on disk not referenced** in loader scripts + **newer-than-2023** paths.

## Unwired .tox ($($unwired.Count))

Use for RESEARCH_BACKLOG candidates. Integrate only after TOX_BUILDS check + td2023 resave if needed.

$(if ($unwired.Count -gt 80) {
    ($unwired | Select-Object -First 80 | ForEach-Object { "- $_" }) -join "`n"
    "`n- ... and $($unwired.Count - 80) more (run script locally for full list)"
} elseif ($unwired.Count) {
    ($unwired | ForEach-Object { "- $_" }) -join "`n"
} else { "- (all listed parts referenced in loader scripts — or no parts dir)" })

## Newer than host ($($newer.Count))

From ``parts/TOX_BUILDS.json``. Resave or skip before loadTox.

$(($newer | Select-Object -First 40 | ForEach-Object { "- $_" }) -join "`n")
$(if ($newer.Count -gt 40) { "`n- ... $($newer.Count - 40) more" })

## Next actions

1. Pick 1–3 unwired tox matching a FEATURE_MATRIX gap → sync script + SCENE_DEFS/FX_DEFS/lab
2. Run ``scan_tox_build_versions.ps1`` if index stale
3. ``old_brik_vj_mega.py`` after integration
4. Update RESEARCH_BACKLOG.md status

See NEXT_SESSION_OPERATIONS.md § Research sprint.
"@

New-Item -ItemType Directory -Force -Path (Split-Path $Out) | Out-Null
$md | Set-Content $Out -Encoding utf8
New-Item -ItemType Directory -Force -Path (Split-Path $Live) -ErrorAction SilentlyContinue | Out-Null
$md | Set-Content $Live -Encoding utf8
Write-Host "Wrote $Out ($($unwired.Count) unwired, $($newer.Count) newer)"
exit 0
