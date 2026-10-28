# Old Brik V J ↔ Ableton Live (Patchworks desk)

Full gear map: **`../PATCHWORKS_INTEGRATION.md`**. VJ parity: **`../VJ_FEATURE_PARITY.md`**.

From **Patchworks** (`23-computer`, `22-wiring`, `14-nektar`, `15-motu-m4`, `RIG.md`): Live + **Nektar T6** (MCU in Live); **M4** hub; **Knead → 3–4**, **Buddy → 1–2**; Sugar Bytes **DrumComputer / Factory / Cyclop**; visuals on **rack sub-mix**, not an APC clip grid.

## Live one-time

1. [TDAbleton](https://docs.derivative.ca/TDAbleton) — add **TouchDesigner** as a Control Surface in Live Preferences.
2. User Library → **TDAbleton**:
   - **`TDA_Master.amxd`** on the master track (session sync)
   - **`TDA_Level.amxd`** on tracks you want as level sends (DrumComputer, Factory, Cyclop, printed rack stems)
   - **`TDA_MIDI.amxd`** only if you route T6 or other MIDI into TD on purpose
3. Optional reference set: `BRIKVJ_TDAbleton_reference.als` (strip any controller maps you do not use).

## TouchDesigner

After **`old_brik_vj_all_in_one.py`**, **TDAbleton** lives under `old_brik_vj/live/tdAbleton` (or run **`brikvj_ableton_link.py`**). Connect while **BRIKVJ_Composition_01.als** (or 02) is open.

Map **TDA_Level** on Rack Sub, Drums, Cyclop, Factory → CHOPs under `old_brik_vj/live_levels/*` (see Harvest **GEAR.md**).

New night set: `scripts/new_brikvj_composition.ps1 -From 1 -To 3`

**Beat → glitch:** use the template in `old_brik_vj/live_beat_pulse` on tdAbleton’s beat channel (CHOP Execute) to pulse datamosh.

## Bitwig

Same M4 routing and TD project. T6 deep integration lives in Bitwig; TDAbleton is Live-first — run visuals from TD while Bitwig drives audio, or use Live as the TDAbleton host alongside Bitwig via M4 loopback (your call).

## Audio paths (Patchworks wiring)

| Source | Path |
|--------|------|
| Eurorack (default) | Knead → **M4 in 3–4** → TD rack_in |
| Buddy mix | **M4 in 1–2** (optional; change `USE_RACK` in `old_brik_vj_audio.py`) |
| Live mix | TDA_Level → TDAbleton (no extra cable) |

See `patchworks/source/manuals/22-wiring.md`.
