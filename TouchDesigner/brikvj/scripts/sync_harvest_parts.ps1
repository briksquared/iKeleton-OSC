# Copy harvested .tox into brikvj/parts/ (run after updating _sweep3 clones)
$ErrorActionPreference = "Stop"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = "C:\Users\briks\Documents\TouchDesigner\BRIKVJ\parts"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$map = @(
    @{ src = "touchdesigner-audio-reactive\audioAnalysisTime.tox"; dst = "audioAnalysisTime.tox"; repo = "touchdesigner-audio-reactive" }
    @{ src = "touchdesigner-audio-reactive\Double_Feedback.tox"; dst = "Double_Feedback.tox"; repo = "touchdesigner-audio-reactive" }
    @{ src = "tdx-rnd\analog\tdx-datamosh\tdx_datamosh.tox"; dst = "tdx_datamosh.tox"; repo = "tdx-rnd" }
    @{ src = "TDXComponents\release\comper-v2.1.0.tox"; dst = "comper.tox"; repo = "TDXComponents" }
    @{ src = "TDXComponents\release\color_curves-v3.0.0.tox"; dst = "color_curves.tox"; repo = "TDXComponents" }
    @{ src = "TD-TOPs-stacker\Release\TOPs_stacker_GLSL.tox"; dst = "TOPs_stacker_GLSL.tox"; repo = "TD-TOPs-stacker" }
    @{ src = "brioch-audio-reactive-vjing\toxes\stroboscope.tox"; dst = "scene_stroboscope.tox"; repo = "brioch-audio-reactive-vjing" }
    @{ src = "brioch-audio-reactive-vjing\toxes\meshExhibitDeformed.tox"; dst = "scene_mesh_exhibit.tox"; repo = "brioch-audio-reactive-vjing" }
    @{ src = "ojack-hydra-td\components\hydra\hydra.tox"; dst = "hydra.tox"; repo = "ojack-hydra-td" }
    @{ src = "tektshared\freqbandctrl2.tox"; dst = "freqbandctrl2.tox"; repo = "tektshared" }
    @{ src = "tektshared\kaleidoscope.tox"; dst = "kaleidoscope.tox"; repo = "tektshared" }
    @{ src = "tektshared\distortion.tox"; dst = "distortion.tox"; repo = "tektshared" }
    @{ src = "tektshared\outputrecording.tox"; dst = "outputrecording.tox"; repo = "tektshared" }
)

$manifest = @()
foreach ($item in $map) {
    $from = Join-Path $Sweep $item.src
    $to = Join-Path $Out $item.dst
    if (-not (Test-Path $from)) {
        Write-Warning "MISSING: $from"
        continue
    }
    Copy-Item $from $to -Force
    $manifest += [ordered]@{
        file = $item.dst
        repo = $item.repo
        source = $item.src
    }
    Write-Host "OK $($item.dst)"
}

$refToe = Join-Path $Sweep "brioch-audio-reactive-vjing\briochSceno.beta.toe"
$manifest += [ordered]@{
    file = "REFERENCE_briochSceno.beta.toe"
    repo = "brioch-audio-reactive-vjing"
    source = "briochSceno.beta.toe"
    path = $(if (Test-Path $refToe) { $refToe } else { $null })
    note = "Open separately to copy full scenes; not embedded in BRIKVJ.toe"
}

$manifest | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $Out "PARTS.json") -Encoding utf8
Write-Host "Wrote $(Join-Path $Out 'PARTS.json')"
