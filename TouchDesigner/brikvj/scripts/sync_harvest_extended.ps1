# Tier-2 VJ parts (FX, utility, extra scenes) → brikvj/parts/extra/
$ErrorActionPreference = "Stop"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = Join-Path $PSScriptRoot "..\parts\extra"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$map = @(
    @{ src = "tektshared\bloom.tox"; dst = "bloom.tox" }
    @{ src = "tektshared\stutter.tox"; dst = "stutter.tox" }
    @{ src = "tektshared\echo.tox"; dst = "echo.tox" }
    @{ src = "tektshared\codev2.tox"; dst = "codev2.tox" }
    @{ src = "tektshared\colorshift.tox"; dst = "colorshift.tox" }
    @{ src = "tektshared\audiobandanalysis.tox"; dst = "audiobandanalysis.tox" }
    @{ src = "tektshared\presetslot.tox"; dst = "presetslot.tox" }
    @{ src = "tektshared\presetslotui.tox"; dst = "presetslotui.tox" }
    @{ src = "tektshared\outputrecording2.tox"; dst = "outputrecording2.tox" }
    @{ src = "brioch-audio-reactive-vjing\toxes\meshExhibitDeformed.2.tox"; dst = "scene_mesh_exhibit_v2.tox" }
    @{ src = "TouchDesigner-Fulldome-Simulator\FulldomeSimulator.tox"; dst = "fulldome_sim.tox" }
    @{ src = "HydraTD\HydraTD.tox"; dst = "hydra_td.tox" }
)

$copied = @()
foreach ($item in $map) {
    $from = Join-Path $Sweep $item.src
    $to = Join-Path $Out $item.dst
    if (-not (Test-Path $from)) {
        Write-Warning "MISSING: $from"
        continue
    }
    Copy-Item $from $to -Force
    $copied += $item.dst
    Write-Host "OK extra/$($item.dst)"
}
@{ tier = "extra"; files = $copied; generated = (Get-Date).ToString("o") } |
    ConvertTo-Json | Set-Content (Join-Path $Out "EXTRA.json") -Encoding utf8
