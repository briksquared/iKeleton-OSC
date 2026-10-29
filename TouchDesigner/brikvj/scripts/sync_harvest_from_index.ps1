# Copy priority .tox from HARVEST_INDEX (td_sweep3) → parts/harvest_pick/
$ErrorActionPreference = "Stop"
$Index = Join-Path (Split-Path $PSScriptRoot -Parent) "HARVEST_INDEX.json"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = Join-Path (Split-Path $PSScriptRoot -Parent) "parts\harvest_pick"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

if (-not (Test-Path $Index)) {
    & "$PSScriptRoot\scan_harvest_for_brikvj.ps1" -Quick
}
$j = Get-Content $Index -Raw | ConvertFrom-Json
$skipNames = @(
    "okvj_audio_analysis.tox", "okvj_glitch_stack.tox", "okvj_strobe_stack.tox",
    "okvj_feedback_stack.tox", "okvj_displace_stack.tox", "okvj_dither_dirt.tox",
    "okvj_halftone.tox", "okvj_pixel_sort.tox", "okvj_compositor.tox",
    "okvj_shader_changer.tox", "fluid_3d_grid.tox"
)

$copied = @()
$seen = @{}
foreach ($pick in $j.priorityPicks) {
    if ($pick.ext -ne ".tox") { continue }
    if ($pick.root -ne "td_sweep3") { continue }
    if ($skipNames -contains $pick.file) { continue }
    $key = $pick.file.ToLower()
    if ($seen[$key]) { continue }
    $from = Join-Path $Sweep $pick.rel
    if (-not (Test-Path $from)) { continue }
    $dstName = ($pick.repo + "_" + $pick.file) -replace "[^a-zA-Z0-9._-]", "_"
    if ($dstName.Length -gt 80) { $dstName = $pick.file }
    $to = Join-Path $Out $dstName
    Copy-Item $from $to -Force
    $seen[$key] = $true
    $copied += $dstName
    if ($copied.Count -ge 120) { break }
}

@{ pack = "harvest_pick"; count = $copied.Count; files = $copied; generated = (Get-Date).ToString("o") } |
    ConvertTo-Json -Depth 3 | Set-Content (Join-Path $Out "HARVEST_PICK.json") -Encoding utf8
Write-Host "Harvest pick pack: $($copied.Count) components"
