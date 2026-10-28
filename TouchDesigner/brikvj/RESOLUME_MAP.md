# BRIKVJ ↔ Resolume (what replaces what)

Built from **`_sweep3/touchdesigner`** harvest into `brikvj/parts/`. Re-sync with `scripts/sync_harvest_parts.ps1`.

| Resolume idea | BRIKVJ piece | Source repo |
|---------------|--------------|-------------|
| **Layer A / B crossfade** | `comper.tox` → `old_brik_vj/mixer/layer_comper` | TDXComponents |
| **Column / clip visuals** | `scene_a/b/c` (stroboscope, mesh exhibit, hydra) | brioch + ojack-hydra-td |
| **Full scene pack** | Open `briochSceno.beta.toe` (path in `parts/PARTS.json`), copy networks into a scene slot | brioch-audio-reactive-vjing |
| **Audio FFT / bands** | `audioAnalysisTime.tox` + `freqbandctrl2.tox` | touchdesigner-audio-reactive + tektshared |
| **Glitch / feedback / datamosh** | `Double_Feedback`, `tdx_datamosh`, `distortion`, `kaleidoscope` | touchdesigner-audio-reactive, tdx-rnd, tektshared |
| **Color grade** | `color_curves.tox` | TDXComponents |
| **Main output** | `perform_out` | TouchDesigner Perform |
| **Record set** | `outputrecording.tox` | tektshared |
| **Tempo / Live levels** | `old_brik_vj/live/tdAbleton` + M4L User Library | tdableton (Derivative) |
| **Rack audio (default)** | MOTU M4 **in 3–4** → `rack_in` | Patchworks wiring |

## Your desk (Patchworks)

- **Audio in:** Knead → M4 3–4 ([`22-wiring.md`](../../../../../../patchworks/source/manuals/22-wiring.md))
- **Keys / DAW:** Nektar T6 + Live/Bitwig — not APC clip grid ([`23-computer.md`](../../../../../../patchworks/source/manuals/23-computer.md))

## Harvest inventory

88 folders under `audio/ableton/github/_sweep3/touchdesigner/`. First integrated set is in `parts/PARTS.json`. More repos (SynaesthesiaFlow-TDAbleton, HydraTD, TDDjayPro, etc.) can be added to `sync_harvest_parts.ps1` as we pick parts.
