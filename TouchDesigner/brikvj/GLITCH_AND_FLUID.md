# Glitch · strobe · fluid — your BRIKVJ lane

Tuned for **IDM / flashy / automatic** nights (Patchworks **106-idm-glitch-ratchet** vibe).

## What you already have in **BRIKVJ.toe** (Brioch)

| Keys | Scene |
|------|--------|
| **1** | L-system tree |
| **2** | Mesh vertex glitch |
| **3** | Mesh particles |
| **4** | Displaced bubbles |
| **5** | Reaction–diffusion |
| **6** | (Brioch scene 6) |

Post: **mirrors, bloom, kick strobe, optical flow** — Ctrl+A…P in Brioch README.

## Harvest stack (`old_brik_vj` after build)

**Glitch / flash:** datamosh, okVJ glitch+strobe stacks, CRT, pixel push, decimate, chaser, dither, stutter, halftone, spectral blur.

**Fluid / particles:** 2D/3D fluid solvers, Lysergiq fluid, flow field, particle life, fluid-like imagFX, Brioch mesh particles.

**Automatic mode:** `brikvj_autopilot` Execute DAT — on **kick** → pulse strobes + random scene; every **~3s** → new scene index.

## One-shot build (TouchDesigner)

```text
brikvj_refresh_all.ps1   # on disk first
```

Then in TD Textport / Text DAT → **`old_brik_vj_all_in_one.py`** → Run → **Save**.

## Manual controls (when you override autopilot)

| Target | What |
|--------|------|
| `old_brik_vj/scenes/scene_switch` | **0–11** scenes (glitch + fluid slots) |
| `old_brik_vj/fx/fx_switch` | **0** = full FX, **1** = dry |
| `old_brik_vj/fx/ok_strobe`, `strobe_fx`, `tdx_crt` | Turn up for harder flash |
| `brikvj_autopilot` | `par.active = 0` to stop auto |
| Brioch **kick strobe** | Still on kick from `analyseAudio` |

## Ableton (same energy)

**Places → BRIKVJ Harvest:** Momentary FX, Granulator Loop Fucker, **px-stream** (35 M4L visuals — shaders, kaleidoscope, pixel FX).

**TDA_Master** on master → TD sees tempo + levels.

## Drop your own clips

`Documents\TouchDesigner\BRIKVJ\media\clips\` — mp4/mov/png; rebuild or re-run suite script to refresh `clip_deck` paths.

Parts on disk: `brikvj/parts/glitch_fluid/` (**24+** `.tox` after sync).
