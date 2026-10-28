# Bitwig + BRIKVJ (same desk, same TD)

Patchworks SSOT: **22-wiring**, **14-nektar** (T6 deep integration in Bitwig).

## Audio (unchanged)

TouchDesigner still listens to **MOTU M4 inputs 3–4** (Knead rack sub). Bitwig can be the mix master while TD reacts to the same analog feed — no extra cable if the rack hits M4 before or parallel to the DAW.

## Control

| Path | Notes |
|------|--------|
| **T6 → Bitwig** | Preferred hands-on mix/device control during a Bitwig-led set |
| **T6 → Live + TDAbleton** | Use when you need **TDA_Master** / **TDA_Level** / **TDA_Mapper** into TD |
| **TD OSC** | Port **7000** (`brikvj_osc_control.py`) — DAW-agnostic scene/clip/router |
| **TD keyboard** | `KEYBOARD_MAP.md` — works with any DAW open or closed |

## Practical setups

1. **Bitwig perform, TD visuals:** Bitwig out → M4 → monitors; TD audio in **3–4** from rack; no TDAbleton required; autopilot + rack audio drive FX.
2. **Hybrid:** Bitwig mix + Live background with **TDA_Master** only (minimal Live set); avoid two MIDI clock masters on M4 (see 22-wiring).
3. **Composition templates** in `ableton/compositions/` are Live-specific; duplicate the *track roles* in Bitwig (Rack Sub, IDM drums, etc.) manually.
