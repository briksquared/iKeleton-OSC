# Glitch / strobe / fluid harvest → brikvj/parts/glitch_fluid/
$ErrorActionPreference = "Stop"
$Sweep = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner"
$Out = Join-Path $PSScriptRoot "..\parts\glitch_fluid"
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$map = @(
    # okVJ — glitch / strobe / flashy
    @{ src = "okVJ-Shared\fxRack\oldFX\strobe_fx.tox"; dst = "strobe_fx.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\chaser.tox"; dst = "chaser.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\pixel_push.tox"; dst = "pixel_push.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\decimate.tox"; dst = "decimate.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\gridify.tox"; dst = "gridify.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\dither.tox"; dst = "dither.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\feedback_fx.tox"; dst = "feedback_fx.tox" }
    @{ src = "okVJ-Shared\fxRack\oldFX\displace_fx.tox"; dst = "displace_fx.tox" }
    @{ src = "okVJ-Shared\fxRack\imagFX\fluidLike.tox"; dst = "fluid_like.tox" }
    @{ src = "okVJ-Shared\fxRack\imagFX\particlize.tox"; dst = "particlize.tox" }
    @{ src = "okVJ-Shared\fxRack\fxStacks\toonFXStack.tox"; dst = "toon_fx_stack.tox" }
    @{ src = "okVJ-Shared\Mapping\inputMapStrober.tox"; dst = "input_map_strober.tox" }
    # TDX — fluids & particles
    @{ src = "TDX-components-shared\Sims\2D grid fluid\2D grid fluid solver.tox"; dst = "fluid_2d_solver.tox" }
    @{ src = "TDX-components-shared\Sims\3DGridPOP\gridFLUID3D.tox"; dst = "fluid_3d_grid.tox" }
    @{ src = "TDX-components-shared\Sims\simple2DFluidSim\2D grid fluid solver.tox"; dst = "fluid_2d_simple.tox" }
    @{ src = "TDX-components-shared\POPs\Fractals\flowField.tox"; dst = "flow_field.tox" }
    @{ src = "TDX-components-shared\POPs\Particle Life\POP_life_comp.tox"; dst = "particle_life.tox" }
    @{ src = "TDX-components-shared\POPs\Fractals\strangeTrig.tox"; dst = "strange_trig.tox" }
    @{ src = "LysergiqFluid\Lysergiq_Fluid.tox"; dst = "lysergiq_fluid.tox" }
    @{ src = "asdf\gens\fluid_sim.tox"; dst = "fluid_sim.tox" }
    # tdx-rnd — analog glitch
    @{ src = "tdx-rnd\analog\tdx-crt\tdx-crt.tox"; dst = "tdx_crt.tox" }
    @{ src = "tdx-rnd\analog\tdx-modulation\tdx-modulation.tox"; dst = "tdx_modulation.tox" }
    @{ src = "tdx-rnd\analog\tdx-datamosh\tdx_datamosh.tox"; dst = "tdx_datamosh_alt.tox" }
    # Extra reactive scenes (flashy)
    @{ src = "TDAudioAnalysis\WispyTunnel.tox"; dst = "scene_wispy_tunnel_root.tox" }
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
    Write-Host "OK glitch_fluid/$($item.dst)"
}

@{ pack = "glitch_fluid"; count = $copied.Count; files = $copied; generated = (Get-Date).ToString("o") } |
    ConvertTo-Json -Depth 3 | Set-Content (Join-Path $Out "GLITCH_FLUID.json") -Encoding utf8
Write-Host "Glitch/fluid pack: $($copied.Count) components"
