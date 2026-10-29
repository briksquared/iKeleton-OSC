# BRIKVJ — next session plan (start here in a new chat)

Purpose: any new Cursor chat (or agent) can **verify state → discover gaps → finish work** without re-deriving context. Read this file first, then [AGENTS_HANDOFF.md](AGENTS_HANDOFF.md) and [WORKLOG.md](WORKLOG.md).

---

## 0. Non-negotiables (user)

- **Live SSOT:** `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\` (toe, scripts, parts, logs) — not iKeleton-OSC paths at runtime.
- **Git kit:** `TouchDesigner/brikvj/` in repo `briksquared/iKeleton-OSC` → sync with `scripts/sync_scripts_to_documents.ps1`.
- **Spelling:** Brik, not Brick. **Agent runs builds** — do not ask user to paste Textport for errors.
- **Do not** kill TD in loops, open a second TD while user has one open, or touch Media Stack launcher/VPN unless asked.
- **Dialog ban:** user must not close 10+ modals — run `patch_brikvj_quiet_open.ps1` after bad injects; skip newer `.tox` via `TOX_BUILDS.json`.

---

## 1. First 5 minutes (evidence, not vibes)

Run with **TouchDesigner closed** unless user explicitly has a session open.

| Step | Command / action | Pass if |
|------|------------------|---------|
| Sync kit → Documents | `scripts/sync_scripts_to_documents.ps1` | No copy-to-self error (kit uses repo path when Documents scripts = dst) |
| Toe size | `(Get-Item Documents\...\BRIKVJ.toe).Length` | ≫ 3 MB if mega/resolume saved; ~936 KB = Brioch-only, needs build |
| Stack verify | `scripts/verify_brikvj_stack.ps1` | `old_brik_vj`, router, broadcast, kantanMapper OK |
| Errors snapshot | `scripts/capture_brikvj_errors.ps1` or read `logs/td_errors.txt` | Trend down after quiet-open + MOTU 3–4 |
| Git | `cd .../iKeleton-OSC && git status -sb && git log -1` | Clean or intentional WIP; fork `main` current |

Log findings in chat with **one line of evidence each** (exit code, byte size, log tail).

---

## 2. Known unfinished (prioritized)

### P0 — User pain / blockers

1. **Confirm quiet open** — kantan `execute1` must not `cook(force=True, recurse=True)`. If popups return: `patch_brikvj_quiet_open.ps1`, re-check expanded `execute1.text`.
2. **Mega build baked into live toe** — Documents toe may be ~6 MB (quiet patch) but mega 26-step may not have completed unattended. Run `run_once_unattended.ps1 -ForceResolumeRebuild` (TD closed); expect `build.log` → `[BRIKVJ mega] project.save() OK`.
3. **Autostart inject size** — `inject_brikvj_build_autostart.py` onStart must stay under execute DAT blob limit (~564 bytes). After inject, do not leave `brikvj_build_autostart` in toe for daily use — `remove_brikvj_autostart_from_toe.ps1` + keep `brikvj_dialog_prefs`.

### P1 — Stack quality

4. **FX chain wire warnings** — `build.log` had `wire: list index out of range` / duplicate kaleid-bloom slots in `brikvj_resolume_stack.py` FX_DEFS — dedupe and fix input indices.
5. **Mac / invalid paths in saved stack** — `audit_brikvj_toe.ps1` after `fix_brikvj_brioch_toe.ps1`; mesh `importselect` geometry, Brioch asset paths.
6. **TD 2023 vs 2025 tox** — `parts/TOX_BUILDS.json` (187 indexed, 132 newer): run `resave_tox_for_td2023.py` once in TD with Accept newer pref, or expand `td2023/` resaves for okVJ/harvest picks actually used in build.
7. **`brikvj_glitch_autopilot.py`** — `%` format fixed (`frame %% every`); confirm installed in saved toe after rebuild.

### P2 — “More stuff” (user goal)

8. **Harvest_pick → scenes** — only ~14 non-Hydra slots in `brikvj_harvest_scene_expansion.py`; 105 picks on disk — curate TD2023-safe list, second scene bank or column.
9. **Research lab** — router index **2**; document in `op('brikvj_hub').text`; optional UI to browse without loading all Hydra on cook.
10. **Live / Patchworks** — `brikvj_ableton_link.py`, `brikvj_patchworks_audio_routes.py`, `brikvj_tda_mapper_bridge.py` in mega path but crash-prone (`live_levels` removed from fast path) — test one at a time with try/except in mega only.
11. **Repo naming** — user dislikes product under iKeleton-OSC long-term; optional future: dedicated **BRIKVJ** repo + mirror only (see REPO_POLICY.md).

### P3 — Not in git

12. **Live 6.2 MB toe** — only on disk in Documents; not in GitHub (intentional). Optional: dated export `BRIKVJ.toe` to user backup drive, not fork.

---

## 3. Discovery workflow (“what still needs doing?”)

Use this when the list above is stale.

### A. Logs (fast)

```powershell
Get-Content Documents\TouchDesigner\BRIKVJ\logs\build.log -Tail 40
Get-Content Documents\TouchDesigner\BRIKVJ\logs\boot_trace.txt -ErrorAction SilentlyContinue
Get-Content Documents\TouchDesigner\BRIKVJ\logs\td_errors.txt -Head 30
```

- Traceback in build.log → fix named script, re-run mega step only if possible else full unattended.
- Many Brioch NoneType errors → audio not routed (audiodevin 3–4, analyseAudio file paths) before blaming harvest.

### B. Harvest research (medium)

```powershell
scripts\brikvj_refresh_all.ps1          # refresh parts from _sweep3
scripts\scan_harvest_for_brikvj.ps1     # HARVEST_INDEX.json
scripts\scan_tox_build_versions.ps1     # TOX_BUILDS.json
```

- Read `HARVEST_INDEX.json` → `priorityPicks` for roles: `audio_reactive`, `post_fx`, `generative`, `projection_mapping`.
- Grep `_sweep3/touchdesigner` for new clones since last sync (user adds GitHub folders over time).
- **Rule:** no `loadTox` without `td_load_tox()` + build index; prefer `parts/*/td2023/`.

### C. Toe / stack audit (slow, TD closed)

```powershell
scripts\fix_brikvj_brioch_toe.ps1       # no -InjectBuildAutostart unless building
scripts\audit_brikvj_toe.ps1
scripts\verify_brikvj_stack.ps1
```

### D. Cursor / transcript (context recovery)

- Transcript: `%USERPROFILE%\.cursor\projects\c-Users-briks-Desktop-GitHub\agent-transcripts\a38c1ae0-2c81-46db-8e9e-4ef553e7f5be.jsonl`
- Search: `mega`, `dialog`, `kantan`, `RUN_BUILD`, `harvest`, `verify`.

### E. User-facing docs to keep updated

After substantive work, append [WORKLOG.md](WORKLOG.md) dated section; update [ERRORS.md](ERRORS.md) for new failure modes.

---

## 4. Execution playbook (default order)

**Goal: finish mega stack in Documents toe without modal spam.**

1. `sync_scripts_to_documents.ps1`
2. `brikvj_refresh_all.ps1` (optional if harvesting)
3. TD **closed** → `run_once_unattended.ps1 -ForceResolumeRebuild`
   - Starts `dismiss_td_dialogs.ps1` in background during build
   - Polls `build.log` for `[BRIKVJ mega] finished` / `project.save() OK`
4. On success: `remove_brikvj_autostart_from_toe.ps1` (keeps dialog prefs + quiet kantan if scripts updated)
5. `verify_brikvj_stack.ps1`
6. `capture_brikvj_errors.ps1` — paste summary, not raw 70 lines to user
7. User opens toe once — if zero modals, done; else `patch_brikvj_quiet_open.ps1`

**Manual fallback (TD open, user ok with one run):** Textport → `TEXTPORT_MEGA.txt` → Save.

---

## 5. Research tasks (when “what should we add?”)

| Question | Where to look |
|----------|----------------|
| New .tox to borrow | `_sweep3/touchdesigner`, `HARVEST_INDEX.json`, okVJ / tektshared / synthesaurio |
| Ableton ↔ TD | `ableton/ABLETON.md`, Patchworks manuals, `brikvj_ableton_link.py` |
| Perform / keys | `KEYBOARD_MAP.md`, `brikvj_perform_controls.py` |
| Resolume parity | `RESOLUME_MAP.md`, `VJ_FEATURE_PARITY.md`, `FEATURE_MATRIX.md` |
| TD API / dialog prefs | Expand debug.toe, TD Python `ui.preferences` in Textport once, document keys in ERRORS.md |

For each candidate .tox: toeexpand → read `.build` → if newer than 2023.12370, add to skip list or td2023 resave before wiring into stack.

---

## 6. Done definition (session can stop when)

- [ ] `verify_brikvj_stack.ps1` exit 0 on Documents toe
- [ ] User can open `BRIKVJ.toe` without batch error dialogs (quiet patch + prefs)
- [ ] `build.log` shows mega completed at least once after last kit change
- [ ] Kit changes committed + pushed to `fork` on `briksquared/iKeleton-OSC`
- [ ] WORKLOG.md updated with date + evidence lines

---

## 7. Prompt to paste in a new chat

```text
Continue BRIKVJ (Old Brik V J). Read TouchDesigner/brikvj/NEXT_SESSION_PLAN.md and AGENTS_HANDOFF.md in briksquared/iKeleton-OSC. Live SSOT is Documents\TouchDesigner\BRIKVJ. Verify stack and logs, then finish P0 items (quiet open, mega build saved, no dialog spam). Sync kit, run unattended mega if TD closed, commit/push to fork. Do not ask me to paste Textport.
```

---

## 8. Remotes

| Remote | URL | Push |
|--------|-----|------|
| `fork` | github.com/briksquared/iKeleton-OSC | Yes |
| `origin` | gwangyu-lee/iKeleton-OSC | No (403) |

Last kit push documented in WORKLOG: commit `42abb3c` (mega stack + docs + harvest parts).
