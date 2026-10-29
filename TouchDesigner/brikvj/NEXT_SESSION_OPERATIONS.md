# BRIKVJ — operations runbook (deepest execution layer)

**Stack of plans:**

| Level | Document | Use when |
|-------|----------|----------|
| 0 | Personal store `BRIKVJ_NEXT_CHAT.md` | Paste prompt only |
| 1 | [NEXT_SESSION_PLAN.md](NEXT_SESSION_PLAN.md) | 5-minute triage |
| 2 | [NEXT_SESSION_PLAN_DEEP.md](NEXT_SESSION_PLAN_DEEP.md) | Architecture + research protocol |
| 3 | **This file** | Exact commands, sprints, milestones |
| Queue | [RESEARCH_BACKLOG.md](RESEARCH_BACKLOG.md) | Track RB-xxx status |

---

## A. Session bootstrap (copy/paste block)

```powershell
$Repo = "C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC"
$Scripts = "$Repo\TouchDesigner\brikvj\scripts"
cd $Scripts
git -C $Repo pull fork main
.\sync_scripts_to_documents.ps1
.\brikvj_gap_report.ps1          # → logs/GAPS_REPORT.md
.\brikvj_research_diff.ps1       # → logs/RESEARCH_DIFF.md
Get-Process TouchDesigner -ErrorAction SilentlyContinue | Select-Object Id
(Get-Item "$env:USERPROFILE\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe").Length
```

Read in order: `GAPS_REPORT.md` → `RESEARCH_DIFF.md` → `RESEARCH_BACKLOG.md` → DEEP §6 backlog IDs.

---

## B. Milestones (definition of “BRIKVJ finished enough”)

| Milestone | Criteria | Verify |
|-----------|----------|--------|
| **M1 Stable open** | 0 error dialogs on open | User or quiet patch + kantan text |
| **M2 Stack saved** | Mega save OK in build.log | grep mega + save |
| **M3 Show bus** | Router 0/1/2 wired, perform_out cooks | verify_brikvj_stack.ps1 |
| **M4 Harvest useful** | ≥30 scenes or FX loaded without wire errors | build.log FX loaded line |
| **M5 Live optional** | TDA mapper OR ableton link without crash | one bridge tested |
| **M6 Kit clean** | fork pushed, WORKLOG dated | git log -1 |

You do **not** need M5 for local VJ; user wants M1–M4 + research lab usable.

---

## C. Sprint types (pick one per session)

### Sprint P0 — Stop the pain (30–90 min)

```powershell
.\patch_brikvj_quiet_open.ps1
# TD closed:
.\run_once_unattended.ps1 -ForceResolumeRebuild
.\remove_brikvj_autostart_from_toe.ps1
..\scripts\verify_brikvj_stack.ps1   # from repo; or Documents copy
.\brikvj_gap_report.ps1
```

**Exit:** gap report gaps ≤1 (git dirty OK).

### Sprint R — Research → integrate (2–4 hr)

1. `brikvj_refresh_all.ps1` (optional, network)
2. `scan_harvest_for_brikvj.ps1 -Quick`
3. `scan_tox_build_versions.ps1`
4. `brikvj_research_diff.ps1` — pick 2 unwired tox that match a Resolume gap ([FEATURE_MATRIX.md](FEATURE_MATRIX.md))
5. Add to appropriate `sync_harvest_*.ps1` + loader Python
6. Mega build (unattended)
7. Update `RESEARCH_BACKLOG.md` row → `done` + WORKLOG

**Reject criteria:** newer than 2023 without td2023; HEAVY_TOX_SKIP; duplicates existing FX.

### Sprint A — Ableton / Patchworks (isolated, risky)

Only if user confirms no video call / VPN touch.

```powershell
# One script per run inside TD after mega:
# brikvj_tda_mapper_bridge.py  OR  brikvj_ableton_link.py
# NEVER brikvj_live_levels_drive.py in same session until proven stable
```

Document result in WORKLOG; rollback = re-run mega without that step enabled.

### Sprint D — Docs-only (no TD)

- Refresh FEATURE_MATRIX counts from code (SCENE_DEFS length, FX_DEFS length)
- Transcript search (see §F)
- Commit backlog / DEEP updates

---

## D. Subsystem command map

| Subsystem | Verify | Fix | Extend |
|-----------|--------|-----|--------|
| Brioch audio | td_errors analyseAudio | fix_brikvj_brioch_toe, audiodevin 3-4 | old_brik_vj_audio.py |
| Kantan boot | toeexpand execute1.text | inject_kantan_boot / patch quiet | — |
| Resolume stack | old_brik_vj in verify | brikvj_resolume_stack.py | SCENE_DEFS, FX_DEFS |
| Harvest scenes | scene_switch indices | harvest_scene_expansion | harvest_pick filter |
| Lab | brikvj_lab/out | research_lab.py | lazy cook (RB-004) |
| Router | source_switch 3 inputs | integrate_brioch.py | perform keys `\` |
| Tox compat | TOX_BUILDS.json | td_load_tox skip | resave_tox_for_td2023 |
| Automation | boot_trace, build.log | inject autostart size | run_once + dismiss dialogs |

---

## E. Failure → action matrix

| Symptom | First read | First action |
|---------|------------|--------------|
| N Error dialogs | ERRORS.md §10 | patch_brikvj_quiet_open |
| N newer tox dialogs | ERRORS.md §11 | Accept pref + skip list |
| build Traceback | build.log last 30 lines | fix script; mega again |
| verify missing old_brik_vj | integrate not run | mega from integrate step |
| TD crash mid-build | build.log cut | remove live_levels; mega without Ableton steps |
| inject too long | Python ValueError | shorten ON_START in inject_brikvj_build_autostart |
| toe 936 KB | GAPS_REPORT | full mega unattended |
| git push 403 origin | — | push fork only |

---

## F. Transcript & context mining

Path: `%USERPROFILE%\.cursor\projects\c-Users-briks-Desktop-GitHub\agent-transcripts\a38c1ae0-2c81-46db-8e9e-4ef553e7f5be.jsonl`

Search strings (ripgrep in agent workspace):

```
dialog|kantan|cook\(force
mega|harvest_pick|TOX_BUILDS
commit|fork|iKeleton
MOTU|3-4|audiodevin
perform_out|router
user_query
```

Extract **user_query** lines for intent changes not yet in USER_REQUESTS.md.

---

## G. Agent routing (which tool when)

| Task | Approach |
|------|----------|
| Find .tox in sweep | `scan_harvest_for_brikvj.ps1`, HARVEST_INDEX.json |
| Find unwired parts | `brikvj_research_diff.ps1` |
| Patch toe binary | expand → python inject → collapse (never hand-edit .toe) |
| Long git status | Scope to `iKeleton-OSC` only, not whole Desktop/GitHub |
| UI popups during build | dismiss_td_dialogs.ps1 (already in run_once) |
| “What would Resolume do?” | RESOLUME_MAP.md, VJ_FEATURE_PARITY.md |

---

## H. New-chat prompt (operations / deepest)

```text
BRIKVJ continuation — operations mode.

1. git pull fork main; read TouchDesigner/brikvj/NEXT_SESSION_OPERATIONS.md (this file).
2. Run sync_scripts_to_documents.ps1, brikvj_gap_report.ps1, brikvj_research_diff.ps1.
3. If GAPS_REPORT shows P0 issues, run Sprint P0 (section C) with evidence after each command.
4. Else run Sprint R: integrate 1–2 items from RESEARCH_DIFF unwired list; update RESEARCH_BACKLOG.
5. WORKLOG + commit + push fork.

SSOT: Documents\TouchDesigner\BRIKVJ. No Textport requests to user.
```

---

## I. Index of all BRIKVJ docs

| File | Role |
|------|------|
| README.md | Entry |
| WORKLOG.md | History |
| USER_REQUESTS.md | User intent |
| AGENTS_HANDOFF.md | Short agent entry |
| ERRORS.md | Popups / failures |
| WHERE_IS_BRIKVJ.md | Paths |
| REPO_POLICY.md | Git vs Documents |
| BUILD.md | Build entry points |
| HARVEST_PLAYBOOK.md | Archive scale |
| FEATURE_MATRIX.md | Resolume parity (may lag code) |
| logs/GAPS_REPORT.md | Auto triage |
| logs/RESEARCH_DIFF.md | Auto unwired tox |

Last updated: 2026-10-29.
