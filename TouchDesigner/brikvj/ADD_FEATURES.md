# How to add features to BRIKVJ

Runtime SSOT: `Documents\TouchDesigner\BRIKVJ\`. Edit scripts in **git** under `TouchDesigner/brikvj/scripts/`, then `sync_scripts_to_documents.ps1`, then rebuild.

## 1. New scene (harvest or generative)

1. Copy or sync the `.tox` into `parts/generative/` or `parts/harvest_pick/` (`sync_harvest_generative.ps1`, `sync_harvest_from_index.ps1`).
2. Check version: `scan_tox_build_versions.ps1` → if `newerThanHost`, resave with `resave_tox_for_td2023.py` or skip via `TOX_NEWER_BUILD_SKIP` in `brikvj_td_helpers.py`.
3. Wire in **one** loader:
   - Core deck: `brikvj_resolume_stack.py` → `SCENE_DEFS` tuple `(label, tox_path_or_name)`.
   - Extra bank: `brikvj_harvest_scene_expansion.py` → picks from `HARVEST_PICK.json` (auto) or extend filter.
4. Rebuild: **you** open `BRIKVJ.toe` → Textport paste `TEXTPORT_MEGA.txt` → Save. Unattended launch only if you explicitly ask the agent (`-AllowTouchDesignerLaunch`). See [AGENT_TD_POLICY.md](AGENT_TD_POLICY.md).
5. Keys: `brikvj_perform_controls.py` scene up/down; max index must match `scene_switch` inputs — update [KEYBOARD_MAP.md](KEYBOARD_MAP.md).

## 2. New FX in the chain

1. Put `.tox` under `parts/` (often `generative` or `glitch_fluid`).
2. Add to `brikvj_resolume_stack.py` → `FX_DEFS` (unique name; dedupe warnings in `build.log` mean duplicate entries).
3. Mega rebuild + `verify_brikvj_stack.ps1`.

## 3. Research / lab (router input 2)

1. Sync into `parts/research/` (`sync_harvest_research.ps1`).
2. `brikvj_research_lab.py` — Hydra list or `tools_switch` entries.
3. Rebuild; perform with `\` to router **2**.

## 4. New build step (Python hook)

1. Add `scripts/brikvj_my_feature.py` with a `run()` or top-level side effects (pattern: print `[BRIKVJ …]` logs).
2. Append filename to `STEPS` in `old_brik_vj_mega.py` (order matters: integrate before perform, avoid crashy scripts with live stack).
3. Use `parent.create("operatorType", "name")` **strings** for new OP types (avoids `NameError` outside Textport).
4. Sync + mega build; confirm no `Traceback` in `logs/build.log`.

## 5. Live / Ableton (optional)

- TDA Mapper: `brikvj_tda_mapper_bridge.py` (Custom Par on `old_brik_vj`).
- Ableton Link: `brikvj_ableton_link.py` — **one bridge per session**; do not use `brikvj_live_levels_drive.py` until stable.

## 6. Discover what to add next

```powershell
scripts\brikvj_session_start.ps1
```

Read `logs/OPEN_WORK_QUEUE.md` (Sessions 1–3), `logs/RESEARCH_DIFF.md` (unwired tox), [RESEARCH_BACKLOG.md](RESEARCH_BACKLOG.md). Score candidates: [NEXT_SESSION_PLAN_DEEPER.md](NEXT_SESSION_PLAN_DEEPER.md) §6.

## 7. Save to git

Commit under `TouchDesigner/brikvj/` only (not the 6 MB `.toe`). Push **`fork`**, not upstream `origin`.
