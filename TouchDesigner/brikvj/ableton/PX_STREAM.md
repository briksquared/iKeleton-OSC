# px-stream M4L (35 devices) — Live-side visuals bridge

Installed to **User Library → Places → BRIKVJ Harvest → M4L → px-stream**.

Use on **return tracks** or **instrument tracks** that feed the house mix (not instead of TouchDesigner — alongside it):

| Use | Suggested track (Composition template) |
|-----|----------------------------------------|
| Transition wipes / pixel FX on drums | **Drums IDM** send → px-stream return |
| Sidechain-style hits from rack | **Rack Sub** + **TDA_Level** + light px-stream on send |
| Stream-only flair | **TD return** bus — mute in FOH, record to OBS with Spout **BRIKVJ** |

TD master remains **`perform_out`** / **Spout BRIKVJ** / **NDI BRIKVJ-Main** (`brikvj_broadcast`).

Synesthesia-style surround: **M4L/SynaesthesiaFlow** on a dedicated track; reference shaders in harvest `TDSynaesthesia/Synaesthesia.toe`.
