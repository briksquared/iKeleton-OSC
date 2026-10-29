# BRIKVJ — deepest execution plan (do the work)

**Not a handoff essay.** This file tells the **next agent to execute**, not re-plan.

## Start (60 seconds)

```powershell
cd TouchDesigner\brikvj\scripts
git -C ..\..\..\.. pull fork main
.\brikvj_session_start.ps1
```

Read in order:

1. `logs/OPEN_WORK_QUEUE.md` — **Session 1 tasks in order**
2. `logs/CONTINUITY.json` — sprint + milestones
3. [ADD_FEATURES.md](ADD_FEATURES.md) — when adding scenes/FX/steps

Meta/discovery: [NEXT_SESSION_PLAN_DEEPER.md](NEXT_SESSION_PLAN_DEEPER.md). Commands: [NEXT_SESSION_OPERATIONS.md](NEXT_SESSION_OPERATIONS.md).

## Finish rule

Do **Session 1** items until `brikvj_gap_report.ps1` exit **0** and `build.log` has **no Traceback**. Then Session 2+.

**Never launch TouchDesigner** unless the user explicitly asked — [AGENT_TD_POLICY.md](AGENT_TD_POLICY.md). Fix scripts + sync; user runs Textport mega when ready.

## Current known P0 (fix before new features)

| ID | Fix |
|----|-----|
| BLD-001 | `brikvj_tda_mapper_bridge.py` — non-fatal; `td_create_op` (kit synced) |
| GAP | **You:** one open → Textport `TEXTPORT_MEGA.txt` → Save (agent does not auto-launch TD) |
| GAP | `patch_brikvj_quiet_open.ps1` + MOTU 3–4 if `td_errors.txt` large |

Regenerate queue after changes: `brikvj_open_work_queue.ps1`.

## New-chat prompt (execute)

```text
BRIKVJ execute: session_start → OPEN_WORK_QUEUE Session 1 until gap exit 0 and no build Traceback. Then one P1 from queue. ADD_FEATURES.md for any new scene/FX. WORKLOG + push fork. No Textport asks.
```

Last updated: 2026-10-29.
