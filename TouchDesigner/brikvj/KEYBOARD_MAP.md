# BRIKVJ perform keyboard (Patchworks desk)

Click the TouchDesigner window before keys register.

| Key | Action |
|-----|--------|
| **1–6** | Brioch scenes (unchanged) |
| **7–9, 0** | Harvest `scene_switch` slots 6–9 |
| **[ / ]** | Previous / next harvest scene (0–11) |
| **- / =** | Previous / next clip column (0–7) |
| **\\** | Toggle `brikvj_router` (0 Brioch / 1 harvest FX stack) |
| **`** | Toggle FX chain bypass (`fx_switch`) |
| **F2** | Toggle `brikvj_autopilot` |
| **F3** | Toggle stream record (`brikvj_broadcast/stream_record`) |
| **F4** | Toggle Spout ingress vs main (`ingress_switch`) |
| **F1** | TouchDesigner Perform mode |

**Nektar T6 / Live:** use **TDA_Mapper.amxd** on a MIDI track → maps to Custom Parameters on `/project1/old_brik_vj` (Scene, Clip, Router, FxBypass, Autopilot). Run **`brikvj_tda_mapper_bridge.py`** once.

In TD: `op('brikvj_key_help').text` for the same list.
