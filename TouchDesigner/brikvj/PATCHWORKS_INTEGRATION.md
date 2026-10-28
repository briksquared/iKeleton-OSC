# Patchworks desk → Ableton Live → TouchDesigner (Old Brik V J)

SSOT: [`patchworks/source/manuals/`](../../../../../../patchworks/source/manuals/) — especially **22-wiring**, **23-computer**, **14-nektar**, **15-motu-m4**, **RIG.md**.

Spelling: **Brik**, not Brick.

## One diagram (audio + control)

```text
[Eurorack Knead] ──► M4 IN 3–4 ──┬──► Live (record / TDA stems)
[Buddy: OP-1·Cycles·PO·mic] ──► M4 IN 1–2 ──┤
[Spark / pedals USB or line] ────────────────┤
                                             ├──► TD analyseAudio / rack_in (same 3–4 default)
Live MAIN + TDA_Master ──loopback/M4───────┘
[Nektar T6 USB] ──► Live (MCU) / Bitwig (deep) / Internal MIDI ──► Cycles (DIN)
[M4 MIDI OUT] ──► Model:Cycles · (MIDI→CV) ──► Pam's / rack
[BeatStep Pro] ──► rack CV/gates (desk seq, not Live clip grid)
[iPad Koala/Note] ──Link/USB/audio──► Live · M4
```

## Ableton Live — recommended track layout (Composition sets)

Use **`BRIKVJ_Composition_01.als`** as the template; duplicate for 02, 03…

| Track / group | Hardware / source | M4 | M4L / notes |
|---------------|-------------------|-----|-------------|
| **Rack Sub** | Knead → **in 3–4** | Ext In 3–4 | **TDA_Level** → TD; record armed for stems |
| **Buddy Sub** | OP-1, Cycles, PO, mic → Buddy → **in 1–2** | Ext In 1–2 | **TDA_Level** optional |
| **Drums IDM** | **DrumComputer** + harvest drum racks | Internal | Sugar Bytes + YYYIKES 128 Drum Starter |
| **Bass / lead** | **Cyclop** + **Factory** | Internal | TDA_Level on bus if sidechaining visuals |
| **Live pedal loop** | Resample rack/pedal via M4 loopback | Loopback | Print to clip for Arrangement |
| **TD return** | Optional mix-minus for stream | Loopback | Same clock as **TDA_Master** |
| **Master** | Full mix | Out 1–2 → Kali | **TDA_Master.amxd** (required) |

**Control surface:** Preferences → Link/MIDI → **TouchDesigner** + **Nektar T6** (MCU/generic for Live — see 14-nektar).

**Not using:** APC40 clip-grid template. **T6 pads** = your MIDI (TDA_MIDI or hardware), not Resolume-style columns.

## TouchDesigner — audio inputs (match wiring)

| `old_brik_vj_audio.py` | M4 channels | Patchworks default |
|------------------------|-------------|------------------|
| `USE_RACK = True` | **3–4** | Knead / rack sub-mix |
| `USE_RACK = False` | **1–2** | Buddy line sub-mix |

Run **`brikvj_patchworks_audio_routes.py`** in TD to apply without editing the script file.

## Bitwig (same visuals)

See **`brikvj/BITWIG.md`**. T6 **deep integration** in Bitwig; TD still listens to **M4 3–4** (or 1–2).
- Option A: Bitwig = mix master, Live open only for **TDAbleton** host.
- Option B: Both DAWs — only one drives **M4 MIDI master** (see 22-wiring clock section).

## Synesthesia-style Live bridge (harvest)

- Repo: `_sweep3/touchdesigner/SynaesthesiaFlow-TDAbleton` → **3D Surround Mapper** M4L (installed to Harvest place).
- Reference toe: `_sweep3/touchdesigner/TDSynaesthesia/Synaesthesia.toe` (study / borrow shaders — not daily perform file).

## Scripts

| Script | Purpose |
|--------|---------|
| `fix_ableton_tda_paths.ps1` | Your User Library TDAbleton paths in `.als` |
| `install_ableton_harvest_place.ps1` | Places → **BRIKVJ Harvest** (racks, px-stream, samples) |
| `brikvj_refresh_all.ps1` | Full harvest sync + toe patch |
| `brikvj_patchworks_audio_routes.py` | MOTU 3–4 vs 1–2 in TD |
| `brikvj_ableton_link.py` | TDAbleton COMP + beat→datamosh + `live_levels/*` |
| `brikvj_broadcast_outputs.py` | NDI/Spout/projectors/stream record |
| `new_brikvj_composition.ps1` | Duplicate composition folder + fix `.als` |
| `brikvj_perform_controls.py` | Keyboard layer + `brikvj_key_help` |
| `brikvj_preset_bank.py` | presetslot / HeavyM-style snapshots |
| `brikvj_tda_mapper_bridge.py` | TDA_Mapper → Scene/Clip/Router pars |
| `brikvj_project_on_start.py` | Execute DAT timeline + optional MOTU 3–4 |
| `sync_scripts_to_documents.ps1` | Mirror scripts → `Documents/.../BRIKVJ/scripts` |
| `brikvj_audio_bridge.py` | Brioch `analyseAudio` → harvest `audio_drive` |
| `brikvj_live_levels_drive.py` | TDA_Level CHOPs → FX parms (frameStart) |
| `brikvj_clip_media_refresh.py` | Fill clip deck from `media/clips/` |
| `brikvj_window_setup.py` | Window COMPs for main + projectors |
| `open_live_composition.ps1` | Launch Live with composition **01–03** |
| `verify_brikvj_stack.ps1` | **`CHECK_STACK.cmd`** — stack saved in `.toe`? |
| `brikvj_fx_audio_bind.py` | Rack RMS/kick → FX expressions |
| `brikvj_osc_control.py` | OSC **7000** → same targets as TDA_Mapper |
| `brikvj_post_build_verify.py` | Textport PASS/FAIL after all-in-one |

## Perform checklist

1. Wire **Knead → M4 3–4**, **Buddy → 1–2** (default topology, 22-wiring).
2. Open **Live** → `BRIKVJ_Composition_01.als` → confirm **TDA_Master** green.
3. **OPEN_BRIKVJ.cmd** → run **`old_brik_vj_all_in_one.py`** once if stack missing → Save.
4. **F1** Perform; Brioch **1–6**; harvest **`scene_switch`**; **kantanMapper** for projection.

See **`VJ_FEATURE_PARITY.md`** for Resolume / MadMapper / HeavyM / Synesthesia mapping.
