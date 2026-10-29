# BRIKVJ worklog (agent + user session)

Chronological record of what was built for **Old Brik V J** on TouchDesigner **2023.12370**, with runtime SSOT in `Documents\TouchDesigner\BRIKVJ\` (see [WHERE_IS_BRIKVJ.md](WHERE_IS_BRIKVJ.md), [REPO_POLICY.md](REPO_POLICY.md)).

## 2026-10-29 — Plan execution (no TD launch)

- RB-002: deduped `FX_DEFS`; FX chain wires via `td_top_out` (fixes COMP wire errors).
- `brikvj_tda_mapper_bridge.py`: `td_create_op` + try/except (no mega Traceback).
- Scripts synced to Documents; `compileall` exit 0.
- **Pending user:** one Textport mega save to refresh `build.log` without Traceback.

## 2026-10-29 — Dialog prefs + safe quiet patch

- Restored `BRIKVJ.toe` from `.bkp109` after a failed patch attempt (toe collapse guard added).
- Re-applied `patch_brikvj_quiet_open.ps1` → **8764772 B**; kantan early Accept-newer prefs + `000_brikvj_dialog_prefs` (newer/older .tox).
- Agents: **one** TD launch per explicit user ask; no retry loops ([AGENT_TD_POLICY.md](AGENT_TD_POLICY.md)).

## 2026-10-29 — No auto TD launch (user policy)

- [AGENT_TD_POLICY.md](AGENT_TD_POLICY.md): agents must not start TouchDesigner unless user explicitly asks.
- `run_once_unattended.ps1` / `brikvj_headless_build.ps1` / `capture_brikvj_errors.ps1` require `-AllowTouchDesignerLaunch` to start TD.
- Fixed `brikvj_tda_mapper_bridge.py` (`create("parexecuteDAT", …)`); [ADD_FEATURES.md](ADD_FEATURES.md) for adding scenes/FX.

## 2026-10-29 — DEEPER continuity layer

- Added [NEXT_SESSION_PLAN_DEEPER.md](NEXT_SESSION_PLAN_DEEPER.md): autonomous loop, 7-channel discovery engine, closure graph, candidate scoring, end-of-session ritual, anti-patterns.
- `brikvj_session_start.ps1` now writes `logs/CONTINUITY.json` + sprint picker (P0/R/D).
- [PLAN_INDEX.md](PLAN_INDEX.md) level 4; personal store `BRIKVJ_NEXT_CHAT.md` updated.
- Evidence: `brikvj_session_start.ps1` → SESSION_BRIEF + CONTINUITY (125 unwired, sprint P0, gap exit 1).

## User intent (preserved)

- **Resolume-class** nightly VJ: clips, scenes, FX, mapping, perform, Ableton/Patchworks integration.
- **Agent does the work** — no “paste Textport yourself”; automated build, error capture, unattended runs.
- **Spelling: Brik**, not Brick. Product name **BRIKVJ** / Old Brik V J.
- **Do not** treat `iKeleton-OSC` / `_sweep2` as the live show path; git kit mirrors to Documents.
- **Keep building**: more harvest from cloned GitHubs (`_sweep3/touchdesigner`), generative, audio-reactive, perform mode, mega all-in-one for show + practice + research.
- **Stop modal spam**: user had to close ~10–11 dialogs every open — must be fixed in automation, not left on user.
- **Commit/push everything** (2026-10-29): document all of the above + kit state before Cursor monthly cap.

## Major deliverables (kit in this folder)

| Area | What |
|------|------|
| **Build pipelines** | `old_brik_vj_mega.py` (26 steps), `old_brik_vj_fast.py`, `old_brik_vj_all_in_one.py` → mega |
| **Resolume stack** | `brikvj_resolume_stack.py` — clips, ~20 scenes, 30+ FX, audio analysis |
| **Harvest** | `sync_harvest_*`, `parts/generative`, `parts/harvest_pick` (~105), `parts/research`, `TOX_BUILDS.json` |
| **Lab / research** | `brikvj_research_lab.py`, Hydra browser, tools switch, router input **2** |
| **Perform** | `brikvj_perform_mode.py`, `brikvj_perform_controls.py`, `KEYBOARD_MAP.md` |
| **Automation** | `run_once_unattended.ps1`, `sync_scripts_to_documents.ps1`, inject autostart (RUN_BUILD.flag) |
| **Quiet open** | `patch_brikvj_quiet_open.ps1` — kantan execute no longer `cook(force=True, recurse=True)` |
| **Tox 2025 vs 2023** | `td_load_tox` skip + `scan_tox_build_versions.ps1`, `dismiss_td_dialogs.ps1`, `brikvj_dialog_prefs` |
| **Errors** | `capture_brikvj_errors.ps1`, `td_dump_errors.py`, [ERRORS.md](ERRORS.md) |

## Known runtime state (last verified ~2026-10-28)

- Live toe: `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe` (~**6.2 MB** after quiet-open patch).
- Stack verify: `old_brik_vj`, `brikvj_router`, `brikvj_broadcast`, `kantanMapper` present after resolume/mega builds.
- Unattended mega build: failed once (autostart blob too long; toe.dir cleanup); later fixes in `inject_brikvj_build_autostart.py` + `Clear-ToeExpandArtifacts`.
- **Root cause of ~10 Error dialogs on open:** `mapping/kantanMapper/ui/execute1` forced full recursive cook → Brioch ops error before MOTU audio. Fixed by `inject_kantan_boot.py` + `patch_brikvj_quiet_open.ps1`.

## Commands (operator)

```powershell
# Sync kit → Documents
TouchDesigner\brikvj\scripts\sync_scripts_to_documents.ps1

# Full harvest refresh
TouchDesigner\brikvj\scripts\brikvj_refresh_all.ps1

# Unattended mega build (TD must be closed)
TouchDesigner\brikvj\scripts\run_once_unattended.ps1 -ForceResolumeRebuild

# Stop startup error popups
TouchDesigner\brikvj\scripts\patch_brikvj_quiet_open.ps1

# In TD Textport
# scripts\TEXTPORT_MEGA.txt
```

## Logs (runtime, not in git by default)

See [logs/README.md](logs/README.md). Live paths under `Documents\TouchDesigner\BRIKVJ\logs\`.

## Cursor transcript

Full agent JSONL: `%USERPROFILE%\.cursor\projects\c-Users-briks-Desktop-GitHub\agent-transcripts\a38c1ae0-2c81-46db-8e9e-4ef553e7f5be.jsonl`
