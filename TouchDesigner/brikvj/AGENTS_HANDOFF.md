# Agent handoff — BRIKVJ

**Read first:** [AGENT_TD_POLICY.md](AGENT_TD_POLICY.md) — **never launch TouchDesigner unless the user explicitly asked in this message.**

**Full handoff (2026-10-29):** [logs/HANDOFF_DETAILED_2026-10-29.md](logs/HANDOFF_DETAILED_2026-10-29.md) — paths, OOM, incidents, 16 commits, roadmap step 2+.  
**Incidents:** [logs/INCIDENT_LOG_2026-10-29.md](logs/INCIDENT_LOG_2026-10-29.md). **Git manifest:** [logs/GIT_COMMIT_MANIFEST_2026-10-29.md](logs/GIT_COMMIT_MANIFEST_2026-10-29.md).

Run **`scripts/brikvj_session_start.ps1`** → **`logs/SESSION_BRIEF.md`** + **`logs/CONTINUITY.json`** + **`logs/ROADMAP_STATUS.md`**.

Also read: [NEXT_SESSION_OPERATIONS.md](NEXT_SESSION_OPERATIONS.md), [BRIKVJ_ROADMAP.md](BRIKVJ_ROADMAP.md), [WORKLOG.md](WORKLOG.md), [USER_REQUESTS.md](USER_REQUESTS.md), [ERRORS.md](ERRORS.md), [BUG_REGISTRY.md](BUG_REGISTRY.md).

## One-line state (2026-10-29)

| Item | Value |
|------|-------|
| Live toe | `Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe` — **9_792_596 B** |
| Last mega | `project.save() OK`, no Traceback — see `Documents\...\logs\build.log` |
| Fork | `briksquared/iKeleton-OSC` @ `ca601bd+` on `fork/main` |
| Roadmap | Step **1 done**; next **#2 quiet open (user)** |
| OOM | Use `BRIKVJ_LOW_MEMORY.flag` + `MAX_HYDRA=8` before next mega |

Rebuild (one TD launch max, user must ask): `run_once_unattended.ps1 -ForceResolumeRebuild -AllowTouchDesignerLaunch` or Textport **`TEXTPORT_MEGA.txt`**.

## If user sees popups on open (step 2)

1. Note dialog count in WORKLOG.
2. `scripts/patch_brikvj_quiet_open.ps1` (toe size guard).
3. TD Preferences → Dialogs → Operator Errors → Textport; newer .tox → Accept.

## If build fails or OOM

- `Documents\...\logs\build.log` — snapshot in kit: `logs/build.log.snapshot`
- OOM: create `Documents\...\BRIKVJ\BRIKVJ_LOW_MEMORY.flag`, sync scripts, wait for free RAM
- `scan_tox_build_versions.ps1` → `parts/TOX_BUILDS.json` (77 newer on 2023 host)

## Next work (roadmap order)

1. User quiet-open check (step 2)
2. MOTU 3–4 + td_errors ↓ (step 3)
3. td2023 resaves for wired tox (step 4)
4. FX integrate colorizer/warmth; fix gater/spinpulser wires (steps 5 + build.log warnings)
5. RB-004 lazy Hydra verify in saved toe
