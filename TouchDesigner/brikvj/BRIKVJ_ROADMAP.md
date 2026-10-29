# BRIKVJ — consolidated roadmap (plan everything)

**One research command:**

```powershell
TouchDesigner/brikvj/scripts/brikvj_research_pass.ps1
TouchDesigner/brikvj/scripts/brikvj_roadmap_status.ps1
```

**Read in 3 minutes:**

| # | File | What |
|---|------|------|
| 1 | `logs/ROADMAP_STATUS.md` | **What to do next** (18-step checklist) |
| 2 | `logs/RESEARCH_PASS.md` | Numbers (20/29/26, 123 unwired, 77 newer) |
| 3 | `logs/RESEARCH_TAXONOMY.md` | **56 Hydra → lab**, 55 okVJ → scored FX |
| 4 | `logs/INTEGRATION_QUEUE.json` | Machine priority queue |
| 5 | [RESEARCH_PASS_PLAN_DEEPER.md](RESEARCH_PASS_PLAN_DEEPER.md) | Full strategy |

---

## North star

Resolume-class **Old Brik V J**: Brioch perform + **old_brik_vj** harvest stack + **brikvj_lab** on router 2; Ableton/MOTU optional; agent runs builds; **one TD open per mega**, not ten.

---

## Current state (research pass — refresh anytime)

| Signal | Typical value | Meaning |
|--------|---------------|---------|
| Toe size | ~8.76 MB | Mega stack saved in Documents |
| gap_report | exit 1 | Until build.log Traceback cleared |
| Unwired | 123 | **Not** a backlog to wire blindly |
| Hydra unwired | 56 | RB-004 lazy lab |
| okVJ unwired | 55 | 2 integrates/session max |
| Bugs (scan) | 5 | See BUG_REGISTRY |
| Open RB | 7+ | RESEARCH_BACKLOG |

---

## Execution order (never reorder 1–3)

1. **Fix kit** (Python in git) → `sync_scripts_to_documents.ps1`  
2. **One mega** (headless/minimized OK) → clean `build.log`  
3. **Integrate** from `INTEGRATION_QUEUE.json` rank 1–2 only  
4. **Research pass again** → update ROADMAP_STATUS  

---

## Feature lanes

| Lane | Target | Doc |
|------|--------|-----|
| Show | Router, kantan, perform, broadcast | VJ_FEATURE_PARITY ● rows |
| Deck | 20+14 scenes, 8 clips, 29 FX | ADD_FEATURES.md |
| Lab | 56 Hydra without open cook | RB-004 |
| Live | TDA mapper, Ableton link | RB-005/006 |
| UX | Dialogs, GPU, one launch | AGENT_TD_POLICY, ERRORS |

---

## Bug lanes

[BUG_REGISTRY.md](BUG_REGISTRY.md) — close P0 before new features.

---

## Planning stack (depth)

```
BRIKVJ_ROADMAP.md          ← you are here (index)
├── ROADMAP_STATUS.md      ← next step #
├── RESEARCH_PASS_PLAN_DEEPER.md
├── RESEARCH_PASS_PLAN.md
├── MASTER_PLAN.md
├── RESEARCH_PASS_PLAN_DEEPER / DEEPER / OPERATIONS
└── PLAN_INDEX.md
```

---

## New-chat prompt

```text
BRIKVJ: brikvj_research_pass.ps1 + brikvj_roadmap_status.ps1. Read BRIKVJ_ROADMAP.md and logs/ROADMAP_STATUS.md. Do next step only. One TD launch if step 1. push fork.
```

Updated: 2026-10-29.
