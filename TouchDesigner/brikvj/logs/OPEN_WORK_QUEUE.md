# BRIKVJ open work queue (generated 2026-10-29T08:33:29.4602225-05:00)

Auto: `scripts/brikvj_open_work_queue.ps1`. Read with [NEXT_SESSION_PLAN_DEEPEST.md](../NEXT_SESSION_PLAN_DEEPEST.md).

**Total items:** 11 | **Next agent:** do Session 1 top to bottom, then re-run `brikvj_session_start.ps1`.

## Session 1 — Finish / stop pain (P0)

- **BLD-001** [P0] Mega step failed: old_brik_vj_mega.py
  - Do: Fix scripts\old_brik_vj_mega.py; sync; user Textport TEXTPORT_MEGA.txt + Save (no auto TD launch)
  - Evidence: tdError: Unknown operator type. Value:'parexecuteDAT' Type:<class 'str'>.

- **GAP-1** [P0] build.log contains Traceback — open log and fix script
  - Do: See NEXT_SESSION_OPERATIONS.md failure matrix
  - Evidence: build.log contains Traceback — open log and fix script

## Session 2 — Compat + stack quality (P1)

- **GAP-2** [P1] Many newer tox — expect skips or dialogs unless td2023/ resaves
  - Do: See NEXT_SESSION_OPERATIONS.md failure matrix
  - Evidence: Many newer tox — expect skips or dialogs unless td2023/ resaves

- **GAP-3** [P1] td_errors.txt has 71 lines — Brioch/audio/mesh; run patch_brikvj_quiet_open + MOTU 3-4
  - Do: See NEXT_SESSION_OPERATIONS.md failure matrix
  - Evidence: td_errors.txt has 71 lines — Brioch/audio/mesh; run patch_brikvj_quiet_open + MOTU 3-4

- **RB-001** [P1] td2023 resave for okVJ stacks used in build
  - Do: RESEARCH_BACKLOG + DEEPER §6 scoring
  - Evidence: RB-001

- **RB-003** [P1] harvest_pick â†’ second scene bank (14+ slots)
  - Do: RESEARCH_BACKLOG + DEEPER §6 scoring
  - Evidence: RB-003

- **RB-004** [P1] Lazy Hydra lab (no cook-all on open)
  - Do: RESEARCH_BACKLOG + DEEPER §6 scoring
  - Evidence: RB-004

## Session 3 — Research + integrate (P2)

- **GAP-4** [P2] iKeleton-OSC git dirty: ## main...origin/main [ahead 9]
  - Do: See NEXT_SESSION_OPERATIONS.md failure matrix
  - Evidence: iKeleton-OSC git dirty: ## main...origin/main [ahead 9]

- **RES-001** [P2] Wire scored unwired tox (sample)
  - Do: parts\harvest_pick\brioch-audio-reactive-vjing_meshExhibitDeformed.2.tox; parts\harvest_pick\brioch-audio-reactive-vjing_meshExhibitDeformed.tox; parts\harvest_pick\brioch-audio-reactive-vjing_stroboscope.tox; parts\harvest_pick\HydraTD_HydraTD.tox; parts\harvest_pick\ojack-hydra-td_hydra.tox; parts\harvest_pick\ojack-hydra-td_hydra_a.tox; parts\harvest_pick\ojack-hydra-td_hydra_add.tox; parts\harvest_pick\ojack-hydra-td_hydra_b.tox
  - Evidence: RESEARCH_DIFF.md

- **DISC-001** [P2] DEEPER §4 discovery pass
  - Do: transcript + USER_REQUESTS diff
  - Evidence: WORKLOG entry

## Full ordered queue

| ID | P | Kind | Title |
|----|---|------|-------|
| BLD-001 | P0 | build | Mega step failed: old_brik_vj_mega.py |
| GAP-1 | P0 | gap | build.log contains Traceback — open log and fix script |
| GAP-2 | P1 | gap | Many newer tox — expect skips or dialogs unless td2023/ resa |
| GAP-3 | P1 | gap | td_errors.txt has 71 lines — Brioch/audio/mesh; run patch_br |
| RB-001 | P1 | backlog | td2023 resave for okVJ stacks used in build |
| RB-003 | P1 | backlog | harvest_pick â†’ second scene bank (14+ slots) |
| RB-004 | P1 | backlog | Lazy Hydra lab (no cook-all on open) |
| RB-006 | P1 | backlog | Ableton link without crash |
| RB-007 | P1 | backlog | Mac/importselect path audit clean |
| GAP-4 | P2 | gap | iKeleton-OSC git dirty: ## main...origin/main [ahead 9] |
| RES-001 | P2 | integrate | Wire scored unwired tox (sample) |
