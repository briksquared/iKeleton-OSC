# Old Brik V J — harvest playbook (1,739 repos → nightly VJ)

Your archive lives under `audio/ableton/github/` (see **`audio/ableton/SOURCES.md`**).

| Archive | Scale | Use for BRIKVJ |
|---------|-------|----------------|
| **control-tooling** | 16 repos | Live OSC/MCP — automate sets while building compositions |
| **max-for-live** | 27+ repos | Generators, **px-stream** (Live→visual transitions), TDAbleton cousins |
| **_sweep2** | 920 repos | Long-tail M4L, `.als` templates, drum tools |
| **_sweep3/touchdesigner** | 88 repos | **601 .tox**, **329 .toe** — scenes, mapping, Hydra, Brioch |
| **_sweep3/visuals** | 135 repos | Reference (Three.js, Processing VJ — ideas, not perform file) |

## Machine-readable index

```powershell
.\brikvj\scripts\scan_harvest_for_brikvj.ps1        # full index → HARVEST_INDEX.json
.\brikvj\scripts\scan_harvest_for_brikvj.ps1 -Quick # faster sample
```

Open **`HARVEST_INDEX.json`** → `priorityPicks` = VJ-relevant paths tagged by role (`projection_mapping`, `layer_mixer`, `post_fx`, …).

## What replaces Resolume / MadMapper / HeavyM

| Product feature | BRIKVJ stack |
|-----------------|--------------|
| Layers A/B + crossfade | `parts/comper.tox` → `old_brik_vj/mixer/layer_comper` |
| Columns / clips | Brioch **scenes 1–6** in `BRIKVJ.toe` + `parts/scene_*.tox` |
| Audio reactive | Brioch `analyseAudio` + `parts/audioAnalysisTime.tox` |
| FX chain | feedback, datamosh, kaleid, distortion, bloom (`sync_harvest_extended.ps1`) |
| Projection mapping | Brioch **kantanMapper** (`/project1/mapping`) — already in perform `.toe` |
| Output / record | `perform_out`, `parts/outputrecording.tox`, tekt `outputrecording2` |
| Tempo / levels from Live | User Library **TDAbleton** + `fix_ableton_tda_paths.ps1` |
| Presets / scenes memory | tekt `presetslot.tox` (extra tier) |

## Scripts (run order when refreshing)

1. `sync_harvest_parts.ps1` — core 13 `.tox` + `PARTS.json`
2. `sync_harvest_extended.ps1` — FX / utility `.tox` in `parts/extra/`
3. `fix_brikvj_brioch_toe.ps1` — Windows-safe `Documents\...\BRIKVJ.toe`
4. `fix_ableton_tda_paths.ps1` — both `.als` → your TDAbleton folder
5. `install_ableton_harvest_place.ps1` — **Places → BRIKVJ Harvest** in Live
6. Inside TD (once per rebuild): `old_brik_vj_all_in_one.py` → Save

## Ableton compositions (multi-set plan)

| Set | Path | Role |
|-----|------|------|
| **BRIKVJ_Composition_01.als** | `Documents/.../BRIKVJ/ableton/compositions/` | Full arrangement (drums + FX racks + TDA_Master) |
| **BRIKVJ_Drums_TDAbleton.als** | same `ableton/` | TDAbleton demo layout, TD sync |
| **BRIKVJ_DrumLoop.als** | same | Minimal loop + TDA |

Add **Composition_02**, **03** by duplicating `compositions/01` folder template (same track groups, new samples).

## TouchDesigner perform file

**Single SSOT:** `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe` (Brioch + Windows patch).

Do **not** open iKeleton `NewProject.toe` for nightly VJ — use harvest **inside** Brioch + optional `/project1/old_brik_vj` stack.

Spelling: **Brik**, not Brick.
