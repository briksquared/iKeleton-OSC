# VJ-suite harvest → brikvj/parts/vj_suite/ (okVJ FX, TDAudioAnalysis scenes, TDDjay clips, TDX projection)
$ErrorActionPreference = "Stop"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = Join-Path $PSScriptRoot "..\parts\vj_suite"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$map = @(
    # okVJ — Resolume-class FX stacks + compositor
    @{ src = "okVJ-Shared\fxRack\fxStacks\glitchFXStack.tox"; dst = "okvj_glitch_stack.tox" }
    @{ src = "okVJ-Shared\fxRack\fxStacks\strobeFXStack.tox"; dst = "okvj_strobe_stack.tox" }
    @{ src = "okVJ-Shared\fxRack\fxStacks\feedbackFXStack.tox"; dst = "okvj_feedback_stack.tox" }
    @{ src = "okVJ-Shared\fxRack\fxStacks\displacementFXStack.tox"; dst = "okvj_displace_stack.tox" }
    @{ src = "okVJ-Shared\fxRack\fxStacks\compositor.tox"; dst = "okvj_compositor.tox" }
    @{ src = "okVJ-Shared\fxRack\fxStacks\ditherDirt.tox"; dst = "okvj_dither_dirt.tox" }
    @{ src = "okVJ-Shared\fxRack\imagFX\pxlSorter.tox"; dst = "okvj_pixel_sort.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\halftone.tox"; dst = "okvj_halftone.tox" }
    @{ src = "okVJ-Shared\Stand Alone UI Components\audioAnalysis.tox"; dst = "okvj_audio_analysis.tox" }
    @{ src = "okVJ-Shared\Generators\shaderChanger\shaderChanger.tox"; dst = "okvj_shader_changer.tox" }
    # TDAudioAnalysis — extra reactive scenes
    @{ src = "TDAudioAnalysis\ext-tox\Effects\WispyTunnel.tox"; dst = "scene_wispy_tunnel.tox" }
    @{ src = "TDAudioAnalysis\ext-tox\Effects\PaintMarbling.tox"; dst = "scene_paint_marbling.tox" }
    @{ src = "TDAudioAnalysis\ext-tox\Effects\Wheels.tox"; dst = "scene_wheels.tox" }
    @{ src = "TDAudioAnalysis\ext-tox\AudioAnalysis\Crossover.tox"; dst = "audio_crossover.tox" }
    # TDDjayPro — clip / artwork loaders (DJ deck metaphor)
    @{ src = "TDDjayPro\imageLoaders.tox"; dst = "clip_image_loaders.tox" }
    # TDX — projection / blur
    @{ src = "TDX-components-shared\TOPs\Projection\cubeMap2Projection.tox"; dst = "projection_cubemap.tox" }
    @{ src = "TDX-components-shared\TOPs\spectralBlur\spectralBlur.tox"; dst = "fx_spectral_blur.tox" }
    @{ src = "TDX-components-shared\POPs\pixelSorter\pixelSorter.tox"; dst = "fx_pixel_sorter_pop.tox" }
    @{ src = "touchdesigner-reflect-refract\GlassPass.tox"; dst = "fx_glass_pass.tox" }
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
    Write-Host "OK vj_suite/$($item.dst)"
}

@{ suite = "vj_suite"; count = $copied.Count; files = $copied; generated = (Get-Date).ToString("o") } |
    ConvertTo-Json -Depth 3 | Set-Content (Join-Path $Out "SUITE.json") -Encoding utf8
Write-Host "VJ suite: $($copied.Count) components"
