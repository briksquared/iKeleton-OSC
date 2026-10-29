# Old Brik V J — feature matrix (vs Resolume / MadMapper / HeavyM)

**Stale warning:** recount from `brikvj_resolume_stack.py` after changes. Default build: **`old_brik_vj_mega.py`** (not suite-only).

| Capability | Resolume-like | BRIKVJ source |
|------------|---------------|---------------|
| **Audio-reactive scenes** | Columns | Brioch **6** in `.toe` + **7** harvested scene `.tox` in suite build |
| **Clip / media players** | Clip deck | **8** `moviefilein` slots (`clip_deck/clip_switch`) + TDDjay `imageLoaders` |
| **Layer A/B crossfade** | Layers | TDX `comper.tox` + okVJ `compositor.tox` |
| **Master FX chain** | Effects | **15+** serial FX (feedback, kaleid, datamosh, bloom, stutter, okVJ stacks, spectral blur) + **fx_switch** bypass |
| **Projection mapping** | Output slices | Brioch **kantanMapper** + TDX **cubeMap2Projection** + fulldome sim |
| **Live tempo / levels** | — | TDAbleton M4L + `rack_in` MOTU 3–4 |
| **Preset / scene memory** | Cues | tekt `presetslot` + okVJ UI widgets (optional) |
| **Record perform** | Recording | `outputrecording` + v2 |
| **Hydra / generative** | Generators | ojack **hydra.tox** + shader changer |
| **DJ / deck metadata** | — | TDDjayPro loaders (optional) |
| **Ableton composition** | — | **3** `.als` + **Places/BRIKVJ Harvest** racks + optional **px-stream** M4L (35 devices) |

## TouchDesigner run order (once per rebuild)

1. `brikvj_refresh_all.ps1`
2. Open `BRIKVJ.toe`
3. Text DAT → **`brikvj_suite_build.py`** → Run Script
4. Text DAT → **`old_brik_vj_audio.py`** → Run Script
5. Text DAT → **`brikvj_integrate_brioch.py`** → Run Script
6. **Save**

## Controls (after build)

| Control | Path / action |
|---------|----------------|
| Scene column | `old_brik_vj/scenes/scene_switch` index **0–6** |
| Clip column | `old_brik_vj/clip_deck/clip_switch` index **0–7** |
| Layer blend | `old_brik_vj/mixer/layer_comper` |
| FX bypass | `old_brik_vj/fx/fx_switch` (0=FX on, 1=dry) |
| Brioch vs suite | `brikvj_router/source_switch` (0=Brioch, 1=harvest stack) |
| Mapping UI | `/project1/mapping/kantanMapper` |
| Brioch scenes | Keys **1–6**, **F1** Perform |

## Harvest scale (your archive)

See **`audio/ableton/SOURCES.md`**: **1,739** repos, **601** `.tox`, **1,634** `.amxd`. Index: **`HARVEST_INDEX.json`**.
