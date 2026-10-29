# BRIKVJ research backlog

Living queue for **discover → evaluate → integrate**. Agent updates status when work completes.

**Protocol:** [NEXT_SESSION_PLAN_DEEP.md](NEXT_SESSION_PLAN_DEEP.md) §5.

| ID | Item | Status | Notes |
|----|------|--------|-------|
| RB-001 | td2023 resave for okVJ stacks used in build | open | 132 newer tox in index; dialog risk |
| RB-002 | Dedupe FX_DEFS in resolume stack | open | build.log wire warnings |
| RB-003 | harvest_pick → second scene bank (14+ slots) | open | 105 files; filter Hydra + newer |
| RB-004 | Lazy Hydra lab (no cook-all on open) | open | lab/h_0..h_31 embedded in toe |
| RB-005 | TDA mapper bridge smoke test | open | mega step; verify with Live |
| RB-006 | Ableton link without crash | open | avoid live_levels in same run |
| RB-007 | Mac/importselect path audit clean | open | audit_brikvj_toe failures |
| RB-008 | Dedicated BRIKVJ git repo | deferred | REPO_POLICY |
| RB-009 | px-stream / M4L visual transitions | candidate | max-for-live harvest |
| RB-010 | okVJ scene changer + autoSaver widgets | candidate | harvest_pick okVJ-Shared_* |

**Status values:** `open` | `in_progress` | `done` | `rejected` | `candidate`

**Integrate template (when closing an item):**

```
- Sync script: sync_harvest_*.ps1
- Loader: brikvj_*.py SCENE_DEFS or lab
- Evidence: build.log line + verify exit 0
- WORKLOG date
```
