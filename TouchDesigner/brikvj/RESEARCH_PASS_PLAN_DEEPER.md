# BRIKVJ — deepest research pass plan

**Run first:** `scripts/brikvj_research_pass.ps1` (includes taxonomy)  
**Outputs:** `logs/RESEARCH_PASS.md`, `logs/RESEARCH_TAXONOMY.md`, `logs/RESEARCH_DIFF.md`, `logs/BUG_SCAN.md`

This document is the **second layer** below [RESEARCH_PASS_PLAN.md](RESEARCH_PASS_PLAN.md): full unwired taxonomy, transcript intent, scored integration matrix, **18 execution steps**.

---

## A. Transcript intent (preserved themes)

Source: Cursor `a38c1ae0-2c81-46db-8e9e-4ef553e7f5be` — must remain true in all plans:

| Theme | Plan implication |
|-------|------------------|
| Agent runs builds, not handoff | Mega/unattended/Textport automation; no “paste this yourself” |
| Old Brik V J / BRIKVJ naming | Spelling **Brik**; SSOT Documents |
| Harvest from `_sweep3/touchdesigner` | 123 unwired is **inventory**, not a wire-all target |
| Glitch + generative + audio-reactive | F3 FX + F4 lab + Brioch analyseAudio |
| Ableton ↔ TD | F6 RB-005/006; MOTU/Eurorack 3–4 |
| Resolume-class stack | F1–F2 scenes/clips/FX/router |
| No dialog spam | B-DLG-* mitigations; Accept prefs |
| No TD launch loops | AGENT_TD_POLICY; one headless/GUI per build |
| Deeper planning + research passes | This file + taxonomy script |
| GPU transient | B-GPU-001 / RB-011 watch |

Update [USER_REQUESTS.md](USER_REQUESTS.md) when new `user_query` themes appear.

---

## B. Unwired taxonomy (research pass)

**Rule:** ~**76%** of unwired paths are **Hydra** → **lab lazy load (RB-004)**, not `scene_switch`.

See **`logs/RESEARCH_TAXONOMY.md`** for exact counts per category:

| Category | Typical action |
|----------|----------------|
| `hydra_lab` | Index in lab; cook on switch index only |
| `okvj_shared` | Score → FX_DEFS or expansion (td2023) |
| `brioch_pick` | Dedupe against existing SCENE_DEFS |
| `mapping_output` | F5 dome/map tooling |
| `audio_reactive` | Bind to analyseAudio / bands |
| `other_generative` | 1–2 per session max |

**Never:** wire all 123 in one mega (dialogs, GPU, cook time).

---

## C. Scored integration matrix (next 10)

Score 0–5 each dimension; integrate if **≥14** ([DEEPER §6](NEXT_SESSION_PLAN_DEEPER.md)).

| Priority | Tox / item | Scene | FX | Lab | Map | Notes |
|----------|------------|-------|-----|-----|-----|-------|
| P1 | okVJ-Shared_colorizer | | ● | | | After td2023 check |
| P1 | okVJ-Shared_analogueWarmthFXStack | | ● | | | Warmth gap |
| P2 | okVJ-Shared_dome_preview | | | | ● | Fulldome |
| P2 | okVJ-Shared_halftone (in suite wired) | | done | | | k_half slot |
| P3 | brioch stroboscope pick | ●? | | | | Dedupe `scene_stroboscope` |
| P3 | Hydra modules (bulk) | | | ● | | RB-004 lazy |
| P4 | constructOutputMap | | | | ● | Research |
| P4 | px-stream M4L (RB-009) | | | | | Live side |
| P5 | okVJ buttons / autoSaver (RB-010) | | | | | UI widgets |
| P5 | td2023 batch (RB-001) | all | all | all | | 77 newer |

---

## D. Bug × feature dependency graph

```
P0 clean build.log ──► S1 mega once
        │
        ├──► M1 quiet open (dialogs)
        │
        ├──► P1 td_errors (MOTU 3-4) ──► audio-reactive quality
        │
        ├──► P1 td2023 (77 newer) ──► safe okVJ integrate
        │
        └──► F2/F3 wire 2 tox/session ──► F4 lazy Hydra
                      │
                      └──► F6 Live bridges (last)
```

---

## E. Eighteen-step program (finer than 12 sessions)

| Step | Work | Evidence |
|------|------|----------|
| 1 | One mega save (headless/minimized OK) | No Traceback in build.log |
| 2 | User confirms ≤1 version dialog on open | M1 |
| 3 | MOTU 3-4 + td_errors resnapshot | Lines ↓ |
| 4 | Resave 5 **used** tox to td2023 | Files in parts/*/td2023/ |
| 5 | Integrate colorizer OR warmth | FX_DEFS + mega |
| 6 | Integrate 2 harvest_pick scenes | expansion log |
| 7 | RB-004 spec: lab cook deferral | Code in research_lab.py |
| 8 | RB-004 impl: switch index only | Open toe GPU stable |
| 9 | KEYBOARD_MAP vs scene_switch max | Doc match |
| 10 | FEATURE_MATRIX = RESEARCH_PASS counts | Doc commit |
| 11 | kantan / dome_preview eval | WORKLOG |
| 12 | TDA mapper smoke RB-005 | Custom Par moves scene |
| 13 | Ableton link RB-006 one test | No crash |
| 14 | preset_bank + hub labels | perform UX |
| 15 | OSC 7000 + mapper doc | Live prep |
| 16 | Full RESEARCH_TAXONOMY review | Categories trend down |
| 17 | BUG_REGISTRY all fixed/mitigated | Scan clean |
| 18 | Optional RB-008 repo split | User decision |

---

## F. Code review pass (research-ordered)

| # | File | Finding to verify |
|---|------|-------------------|
| 1 | All mega steps | try/except or non-throwing |
| 2 | `brikvj_research_lab.py` | Eager Hydra cook? |
| 3 | `brikvj_resolume_stack.py` | FX chain td_top_out |
| 4 | `brikvj_td_helpers.py` | newer skip before loadTox |
| 5 | inject scripts | blob size / collapse guard |
| 6 | `run_once_unattended.ps1` | single launch + dismiss |
| 7 | `live_levels_drive` | absent from mega STEPS |

---

## G. Research pass cadence

| When | Command |
|------|---------|
| Every chat start | `brikvj_research_pass.ps1` |
| After mega save | Same + compare build.log |
| Before harvest wire | `brikvj_research_taxonomy.ps1` + TOX_BUILDS |
| Monthly | Re-run `scan_harvest_for_brikvj.ps1` |

---

## H. New-chat prompt (deepest)

```text
BRIKVJ deepest research: brikvj_research_pass.ps1 → RESEARCH_PASS_PLAN_DEEPER.md + RESEARCH_TAXONOMY.md. Execute next step from §E table. Score integrations §C. One TD launch max. Update BUG_REGISTRY + RESEARCH_BACKLOG + push fork.
```

Last updated: 2026-10-29.
