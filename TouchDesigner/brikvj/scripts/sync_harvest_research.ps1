# Research / dev / show utilities → parts/research/
$ErrorActionPreference = "Stop"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = Join-Path (Split-Path $PSScriptRoot -Parent) "parts\research"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$map = @(
    @{ src = "TDDjayPro\djayPro.tox"; dst = "djay_pro.tox" }
    @{ src = "TDDjayPro\imageLoaders.tox"; dst = "image_loaders.tox" }
    @{ src = "TouchDesigner-Fulldome-Simulator\FulldomeSimulator.tox"; dst = "fulldome_sim.tox" }
    @{ src = "HydraTD\HydraTD.tox"; dst = "hydra_td.tox" }
    @{ src = "ojack-hydra-td\components\hydra\hydra.tox"; dst = "hydra_ojack.tox" }
    @{ src = "tektshared\presetslot.tox"; dst = "presetslot.tox" }
    @{ src = "tektshared\presetslotui.tox"; dst = "presetslotui.tox" }
    @{ src = "tektshared\outputrecording2.tox"; dst = "outputrecording2.tox" }
    @{ src = "synthesaurio_td\utility\KodeLife_glsl.tox"; dst = "kodelife_glsl.tox" }
    @{ src = "synthesaurio_td\utility\audioAnalysis_ss.tox"; dst = "audio_analysis_ss.tox" }
    @{ src = "touchdesigner-audio-reactive\audioAnalysisTime.tox"; dst = "audio_analysis_time.tox" }
    @{ src = "TD-TOPs-stacker\Release\TOPs_stacker_GLSL.tox"; dst = "tops_stacker_glsl.tox" }
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
    Write-Host "OK research/$($item.dst)"
}

@{ pack = "research"; count = $copied.Count; files = $copied; generated = (Get-Date).ToString("o") } |
    ConvertTo-Json -Depth 3 | Set-Content (Join-Path $Out "RESEARCH.json") -Encoding utf8
Write-Host "Research pack: $($copied.Count) components"
