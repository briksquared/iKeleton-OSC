# Index Ableton + TouchDesigner harvest for Old Brik V J (Resolume-class stack).
# Reads: audio/ableton/SOURCES.md sweep roots. Writes: brikvj/HARVEST_INDEX.json
param(
    [string]$OutJson = "$PSScriptRoot\..\HARVEST_INDEX.json",
    [switch]$Quick
)
$ErrorActionPreference = "Stop"
$Roots = @(
    @{ name = "control-tooling"; path = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\control-tooling"; tags = @("live_api", "osc", "mcp") }
    @{ name = "max-for-live"; path = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\max-for-live"; tags = @("m4l", "midi", "generators") }
    @{ name = "racks-presets"; path = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\racks-presets"; tags = @("adg", "adv", "racks") }
    @{ name = "sweep2"; path = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2"; tags = @("ableton_longtail") }
    @{ name = "td_sweep3"; path = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"; tags = @("touchdesigner", "vj") }
    @{ name = "visuals_sweep3"; path = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\visuals"; tags = @("visuals", "reference") }
)
$extAbleton = @(".amxd", ".adg", ".adv", ".als", ".alc", ".agr")
$extTd = @(".tox", ".toe")
$roleRules = @(
    @{ role = "live_td_sync"; pattern = "(?i)tdableton|tda_|TDAbleton|SynaesthesiaFlow" }
    @{ role = "audio_reactive"; pattern = "(?i)audio.?reactive|fft|spectra|beat|bpm|analyseAudio" }
    @{ role = "projection_mapping"; pattern = "(?i)kantan|mapper|projection|fulldome|uv.?map" }
    @{ role = "layer_mixer"; pattern = "(?i)comper|stacker|crossfade|layer" }
    @{ role = "post_fx"; pattern = "(?i)feedback|datamosh|kaleid|distort|bloom|strob|optical.?flow|glitch" }
    @{ role = "generative"; pattern = "(?i)hydra|reaction.?diff|lsystem|particle|mesh" }
    @{ role = "record_out"; pattern = "(?i)record|moviefileout|outputrecording" }
    @{ role = "live_control"; pattern = "(?i)ableton.?osc|ableton.?mcp|pylive|ableton-js|clyphx" }
    @{ role = "drums_groove"; pattern = "(?i)drum.?rack|drumbrain|regroove|groove|808" }
    @{ role = "midi_fx"; pattern = "(?i)midi.?morph|chord|arp|scale" }
    @{ role = "px_visuals"; pattern = "(?i)px-stream|visual|vj" }
)

function Get-Roles($relPath) {
    $roles = @()
    foreach ($r in $roleRules) {
        if ($relPath -match $r.pattern) { $roles += $r.role }
    }
    if ($roles.Count -eq 0) { $roles = @("uncategorized") }
    return ($roles | Select-Object -Unique)
}

$entries = @()
$counts = @{ amxd = 0; adg = 0; tox = 0; toe = 0; als = 0; other = 0 }

foreach ($root in $Roots) {
    if (-not (Test-Path $root.path)) { continue }
    $exts = $extAbleton + $extTd
    $files = Get-ChildItem $root.path -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $exts -contains $_.Extension.ToLower() }
    if ($Quick) { $files = $files | Select-Object -First 800 }
    foreach ($f in $files) {
        $rel = $f.FullName.Substring($root.path.Length).TrimStart("\")
        $ext = $f.Extension.ToLower()
        switch ($ext) {
            ".amxd" { $counts.amxd++ }
            ".adg" { $counts.adg++ }
            ".tox" { $counts.tox++ }
            ".toe" { $counts.toe++ }
            ".als" { $counts.als++ }
            default { $counts.other++ }
        }
        $entries += [ordered]@{
            root = $root.name
            repo = ($rel -split "\\")[0]
            file = $f.Name
            ext = $ext
            rel = $rel
            bytes = $f.Length
            roles = (Get-Roles $rel)
        }
    }
}

# Priority picks for BRIKVJ (curated — not exhaustive)
$picks = $entries | Where-Object {
    $_.roles -contains "projection_mapping" -or
    $_.roles -contains "layer_mixer" -or
    $_.roles -contains "post_fx" -or
    $_.roles -contains "audio_reactive" -or
    $_.roles -contains "live_td_sync" -or
    $_.roles -contains "generative" -or
    $_.roles -contains "px_visuals"
} | Sort-Object { $_.repo }, { $_.file }

$report = [ordered]@{
    generated = (Get-Date).ToString("o")
    source = "C:\Users\briks\Desktop\GitHub\audio\ableton\SOURCES.md harvest"
    counts = $counts
    totalIndexed = $entries.Count
    brikvjPriorityCount = @($picks).Count
    priorityPicks = @($picks | Select-Object -First 120)
    allEntries = if ($Quick) { @() } else { $entries }
}
$report | ConvertTo-Json -Depth 6 | Set-Content $OutJson -Encoding utf8
Write-Host "Wrote $OutJson — indexed $($entries.Count) files, $($picks.Count) priority VJ picks"
