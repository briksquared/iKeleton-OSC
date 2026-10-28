# Live control harvest (OSC / API) — optional layer

BRIKVJ daily perform path: **TDAbleton** + **TDA_Mapper** + **Nektar T6** in Live (see `PATCHWORKS_INTEGRATION.md`).

Your archive **`audio/ableton/github/control-tooling`** (indexed in `HARVEST_INDEX.json`) includes AbletonOSC, MCP bridges, pylive, etc. Use when you want **set automation while building compositions**, not as a hard perform dependency.

| Goal | Harvest direction |
|------|-------------------|
| Remote clip/scene from script | AbletonOSC / Live API repos under `control-tooling` |
| Agent-driven set prep | MCP servers (same folder) — run with Live closed or on a copy `.als` |
| TD-only OSC | **`brikvj_osc_control.py`** — port **7000**, `/brikvj/scene`, `/brikvj/clip`, … |

TD bridge already exposes **Custom Parameters** via `brikvj_tda_mapper_bridge.py` — any OSC→CHOP→Parameter Execute can drive the same pars as **TDA_Mapper**.
