# Copy curated harvest racks/M4L into Ableton User Library → Places/BRIKVJ Harvest
$ErrorActionPreference = "Stop"
$Place = "C:\Users\briks\Documents\Ableton\User Library\Places\BRIKVJ Harvest"
New-Item -ItemType Directory -Force -Path $Place, "$Place\Racks", "$Place\Sets", "$Place\Samples", "$Place\M4L\px-stream", "$Place\M4L\SynaesthesiaFlow" | Out-Null

$syna = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\SynaesthesiaFlow-TDAbleton\3D Surround Mapper"
if (Test-Path $syna) {
    Get-ChildItem $syna -Filter "*.amxd" -Recurse | Copy-Item -Destination "$Place\M4L\SynaesthesiaFlow\" -Force
    Write-Host "-> M4L/SynaesthesiaFlow"
}

$pxSrc = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\max-for-live\px-stream\devices"
if (Test-Path $pxSrc) {
    Get-ChildItem $pxSrc -Filter "*.amxd" | Copy-Item -Destination "$Place\M4L\px-stream\" -Force
    Write-Host "-> M4L/px-stream ($((Get-ChildItem "$Place\M4L\px-stream\*.amxd").Count) devices)"
}

$rackDir = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\racks-presets\ableton-live-racks-and-misc-resources\Individual Racks"
Get-ChildItem $rackDir -Filter "YYYIKES*128*Drum*.adg" -ErrorAction SilentlyContinue | ForEach-Object {
    Copy-Item $_.FullName "$Place\Racks\$($_.Name)" -Force
    Write-Host "-> Racks\$($_.Name)"
}
Get-ChildItem $rackDir -Filter "YYYIKES*Momentary*.adg" -ErrorAction SilentlyContinue | ForEach-Object {
    Copy-Item $_.FullName "$Place\Racks\$($_.Name)" -Force
    Write-Host "-> Racks\$($_.Name)"
}
Get-ChildItem $rackDir -Filter "YYYIKES*Granulator*.adg" -ErrorAction SilentlyContinue | ForEach-Object {
    Copy-Item $_.FullName "$Place\Racks\$($_.Name)" -Force
    Write-Host "-> Racks\$($_.Name)"
}

$sampleCandidates = @(
    "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\ableton\samples\brikvj_drum_loop.mp3",
    "C:\Users\briks\Documents\Ableton\User Library\Samples\brikvj_drum_loop.mp3"
)
foreach ($s in $sampleCandidates) {
    if (Test-Path $s) { Copy-Item $s "$Place\Samples\brikvj_drum_loop.mp3" -Force; break }
}
$kickCandidates = @(
    "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\ableton\samples\brikvj_kick_808.wav",
    "C:\Users\briks\Documents\Ableton\User Library\Samples\brikvj_kick_808.wav"
)
foreach ($k in $kickCandidates) {
    if (Test-Path $k) { Copy-Item $k "$Place\Samples\brikvj_kick_808.wav" -Force; break }
}

$gearReadme = @"
# BRIKVJ Harvest — Patchworks gear (manual load)

Sugar Bytes (installed in Live, not copied here):
- **DrumComputer** — Drums IDM track
- **Cyclop** — bass / lead
- **Factory** — semi-modular + arp

Per track: **TDA_Level.amxd** (User Library/TDAbleton) → map to TD ``old_brik_vj/live_levels/*``.
Master: **TDA_Master.amxd** (required).

Sets: ``Documents/TouchDesigner/BRIKVJ/ableton/compositions/``
"@
Set-Content -Path "$Place\GEAR.md" -Value $gearReadme -Encoding UTF8

Write-Host "BRIKVJ Harvest place: $Place"
Write-Host "In Live: Places -> BRIKVJ Harvest (see GEAR.md)"
