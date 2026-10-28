# VJ feature parity — Resolume · MadMapper · HeavyM · Synesthesia Live

**Old Brik V J** = Brioch perform `.toe` + harvest **`old_brik_vj`** stack.  
Legend: **●** in build/touch | **◐** Brioch or harvest part (wire in TD) | **○** configure/OS (NDI, Spout, DMX) | **—** not a goal / use dedicated tool

## Resolume Arena / Avenue

| Feature | Status | BRIKVJ |
|---------|--------|--------|
| Layer compositing (A/B) | ● | `comper.tox`, okVJ `compositor`, `mixer/layer_comper` |
| Column / clip triggers | ● | `clip_deck` (8×), Brioch keys **1–6**, `scene_switch` (12+) |
| Crossfader / blend modes | ● | comper Blend/Cross; `fx_switch` dry/wet |
| Video codecs / HAP | ◐ | TD `moviefilein`; drop files in `media/clips/` |
| Audio-linked BPM | ● | Brioch `analyseAudio`; TDAbleton **TDA_Master** |
| FFT / bass reactive | ● | analyseAudio, okVJ audio, freq bands, autopilot kick |
| Built-in FX (blur, glow, etc.) | ● | bloom, feedback, kaleid, datamosh, CRT, strobe stacks |
| Output / fullscreen | ● | `perform_out`, Perform mode **F1** |
| Multiple physical outputs | ● | `brikvj_broadcast/projector_1` … + kantanMapper slices |
| Projection mapping slices | ● | **kantanMapper** in Brioch `/project1/mapping` |
| DMX / lighting | ○ | Use QLC+ / Resolume DMX only if needed; not duplicated |
| NDI / Spout stream out | ● | `brikvj_broadcast` — Spout **BRIKVJ**, NDI **BRIKVJ-Main** |
| Recorder | ● | `outputrecording.tox`, v2, `moviefileout` |
| DMX timeline | — | Use Live arrangement + TD |
| Arena advanced (DMX, SMPTE) | ◐ | Live + M4 MIDI clock; SMPTE via TD if required |

## MadMapper

| Feature | Status | BRIKVJ |
|---------|--------|--------|
| Quad / surface warping | ● | kantanMapper freeform + rectangles |
| Masking | ◐ | kantanMapper shapes + alpha in comper |
| Multiple projectors | ◐ | Multiple outputs + mapper shapes |
| Syphon/Spout in | ● | `brikvj_broadcast/ingress_switch` (index 1 = external) |
| DMX / laser | ○ | External |
| Shader media | ● | Hydra, GLSL stacker, Brioch scenes |
| Audio reactive | ● | Same as above |
| UI for corner-pin | ● | kantanMapper UI (open in perform prep) |

## HeavyM

| Feature | Status | BRIKVJ |
|---------|--------|--------|
| Quick template scenes | ● | Brioch 6 + harvest scene `.tox` library |
| Audio bands drive visuals | ● | analyseAudio + TDA_Level |
| Easy perform UI | ● | `preset_bank` (presetslot UI), Perform, **KEYBOARD_MAP.md** |
| Particles / 3D | ● | mesh particles, particle life, fluids, POPs |
| Text / logo | ◐ | TD Text TOP + mapper |
| NDI | ● | Same as Resolume row (`brikvj_broadcast`) |

## Synesthesia Live

| Feature | Status | BRIKVJ |
|---------|--------|--------|
| Shader scene library | ● | Hydra + Brioch + TDAudioAnalysis scenes |
| Audio multiband | ● | Crossover, freqbandctrl, Brioch bands |
| Scene morph / auto | ● | `brikvj_autopilot`, comper crossfade |
| MIDI control | ● | **TDA_Mapper** → Custom Par on `old_brik_vj`; T6 via Live MIDI learn |
| Ableton sync | ● | TDAbleton + **TDA_Master** |
| Synesthesia-specific presets | ◐ | Reference `TDSynaesthesia/Synaesthesia.toe`; Flow M4L in Harvest |
| OSC / control | ● | **OSC port 7000** (`brikvj_osc_control.py`) + TDA_Mapper + harvest control-tooling |

## Patchworks gear → features

| Gear | Drives |
|------|--------|
| **MOTU M4** | All audio + MIDI clock hub; TD **3–4** rack |
| **Nektar T6** | Live transport/mixer; Bitwig deep; MIDI to Cycles |
| **BeatStep Pro** | Rack sequences (parallel to VJ) |
| **Eurorack** | Audio-reactive source (default VJ input) |
| **Sugar Bytes** | Live IDM layers + TDA_Level |
| **iPad Koala/Note** | Samples into Live → TD via levels |

## Close the gaps (your ongoing loop)

1. `brikvj_refresh_all.ps1`
2. TD: **`old_brik_vj_all_in_one.py`** → Save
3. Map projectors in **kantanMapper** once per venue
4. Assign **`brikvj_broadcast/projector_*`** in Window COMP per physical output
5. OBS: capture **Spout BRIKVJ** or **NDI BRIKVJ-Main**

Feature count target (harvest on disk): **13** core `.tox` + **19** vj_suite + **24** glitch_fluid + **6** Brioch scenes + **35** px-stream M4L + **3** YYYIKES racks.
