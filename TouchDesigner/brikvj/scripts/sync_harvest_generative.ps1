# Generative + audio-reactive harvest → parts/generative/ (TD 2023–friendly clones where possible)
$ErrorActionPreference = "Stop"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = Join-Path (Split-Path $PSScriptRoot -Parent) "parts\generative"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$map = @(
    @{ src = "synthesaurio_td\gen\space_field.tox"; dst = "space_field.tox" }
    @{ src = "synthesaurio_td\gen\vintage_stars.tox"; dst = "vintage_stars.tox" }
    @{ src = "synthesaurio_td\gen\blueSky.tox"; dst = "blue_sky.tox" }
    @{ src = "synthesaurio_td\gen\agentTrails.tox"; dst = "agent_trails.tox" }
    @{ src = "synthesaurio_td\utility\audioAnalysis_ss.tox"; dst = "audio_analysis_ss.tox" }
    @{ src = "synthesaurio_td\utility\KodeLife_glsl.tox"; dst = "kodelife_glsl.tox" }
    @{ src = "ml-arts-voice-plasma\touchdesigner\voice-plasma.tox"; dst = "voice_plasma.tox" }
    @{ src = "tektshared\spiral.tox"; dst = "spiral.tox" }
    @{ src = "tektshared\spinpulser.tox"; dst = "spinpulser.tox" }
    @{ src = "tektshared\audiobandanalysis.tox"; dst = "audiobandanalysis.tox" }
    @{ src = "tektshared\codev2.tox"; dst = "codev2.tox" }
    @{ src = "tektshared\gater.tox"; dst = "gater.tox" }
    @{ src = "tektshared\paramsmoother.tox"; dst = "param_smoother.tox" }
    @{ src = "touchdesigner-audio-reactive\audioAnalysisTime.tox"; dst = "audio_analysis_time.tox" }
    @{ src = "TDAudioAnalysis\WispyTunnel.tox"; dst = "wispy_tunnel_td.tox" }
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
    Write-Host "OK generative/$($item.dst)"
}

@{ pack = "generative"; count = $copied.Count; files = $copied; generated = (Get-Date).ToString("o") } |
    ConvertTo-Json -Depth 3 | Set-Content (Join-Path $Out "GENERATIVE.json") -Encoding utf8
Write-Host "Generative pack: $($copied.Count) components"
