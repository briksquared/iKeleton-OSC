# BRIKVJ — research pass plan (deepest roadmap)

**Purpose:** One document that ties **research evidence** → **bugs** → **features** → **12 sessions**.  
**Evidence refresh:** `scripts/brikvj_research_pass.ps1` → `logs/RESEARCH_PASS.md` (no TouchDesigner required).

**User intent SSOT:** [USER_REQUESTS.md](USER_REQUESTS.md)  
**Parity SSOT:** [VJ_FEATURE_PARITY.md](VJ_FEATURE_PARITY.md)  
**Archive scale:** [HARVEST_PLAYBOOK.md](HARVEST_PLAYBOOK.md), `HARVEST_INDEX.json` (**2946** indexed, **235** priority, **531** archive `.tox`)

---

## 1. Research pass protocol (run every planning session)

```powershell
cd TouchDesigner/brikvj/scripts
git pull fork main
./brikvj_research_pass.ps1
```

Read outputs in order:

1. `logs/RESEARCH_PASS.md` — measured counts + candidates  
2. `logs/BUG_SCAN.md` — auto bugs  
3. `logs/RESEARCH_DIFF.md` — unwired / newer  
4. `logs/GAPS_REPORT.md` — triage  
5. [RESEARCH_BACKLOG.md](RESEARCH_BACKLOG.md) — RB-xxx queue  

**Discovery channels (manual, 15–30 min when planning “deeper”):**

| # | Channel | Action |
|---|---------|--------|
| 1 | Code measure | SCENE_DEFS / FX_DEFS / mega STEPS (RESEARCH_PASS auto) |
| 2 | Unwired taxonomy | Split Hydra (~50+) vs okVJ vs brioch duplicates |
| 3 | TOX_BUILDS | `scan_tox_build_versions.ps1` — never wire newer without td2023 |
| 4 | Parity ◐ rows | Map to F5/F6 or RB row |
| 5 | Transcript | `a38c1ae0-2c81-46db-8e9e-4ef553e7f5be` — search `user_query`, GPU, dialog |
| 6 | Sweep roles | `scan_harvest_for_brikvj.ps1 -Quick` — match `roles` to gaps |
| 7 | Live logs | `build.log`, `td_errors.txt` after **one** mega save |

**Scoring unwired tox (integrate only if ≥14):** [NEXT_SESSION_PLAN_DEEPER.md](NEXT_SESSION_PLAN_DEEPER.md) §6.

---

## 2. Measured stack (2026-10-29 research pass)

| Layer | Count | Notes |
|-------|------:|-------|
| Core scenes (`SCENE_DEFS`) | **20** | + Brioch **6** keys in `.toe` |
| Harvest scene expansion | **≤14** | `harvest_pick`, skips Hydra prefix |
| FX chain slots (`FX_DEFS`) | **29** | serial; bypass `fx_switch` |
| Mega pipeline steps | **26** | non-fatal per step |
| `parts/harvest_pick` on disk | **105** | HARVEST_PICK.json |
| Unwired `.tox` (all parts) | **123** | majority Hydra modules → **lab**, not scene_switch |
| Newer than TD 2023.12370 | **77** | RB-001 |
| Live `BRIKVJ.toe` | **~8.76 MB** | quiet-open + dialog prefs applied |

**Implication:** Do **not** wire all 123 unwired into perform. Route Hydra to **RB-004 lazy lab**; wire **2–3 okVJ/brioch picks per session** after scoring.

---

## 3. Bug program (research-verified)

| ID | Sev | Research note | Session |
|----|-----|---------------|---------|
| B-LOG-001 | P0 | Stale Traceback until one mega | S1 |
| B-LOG-002 | P1 | 8 wire lines pre-fix; verify post-mega | S1 |
| B-TD-001 | P1 | analyseAudio NoneType — audio not ready | S2 |
| B-TOX-001 | P1 | 77 newer — dialog + skip policy | S2–S3 |
| B-DLG-* | mitigated | kantan + `000_brikvj_dialog_prefs` | verify S1 open |
| B-GPU-001 | watch | transient; RB-011 | S2 |
| B-TDA-001 | mitigated | bridge non-fatal | S5 Live |

Full table: [BUG_REGISTRY.md](BUG_REGISTRY.md).

---

## 4. Feature program (research-aligned)

### F1 — Show bus (baseline) ●

Router 0/1/2, kantan, perform_out, broadcast Spout/NDI — **verify** after S1 mega.

### F2 — Resolume deck depth

- Target: **≥34** scene switch inputs (20 + 14 expansion + headroom).  
- Keys: `KEYBOARD_MAP.md` hi index matches `scene_switch`.  
- Clips: **8** + `clip_media_refresh`.

### F3 — FX depth

- **29** FX defs; dedupe done (RB-002).  
- Next: okVJ **colorizer**, **analogueWarmth** if td2023-safe.

### F4 — Lab / research (Hydra)

- **123 unwired** mostly Hydra — **lazy cook** RB-004, not perform load.  
- Router **2** = `brikvj_lab`.

### F5 — Mapping / output polish ◐

- kantan slice audit; `constructOutputMap` / dome preview tox **research**.  
- Multi-projector: `brikvj_broadcast/projector_*`.

### F6 — Live / Patchworks ◐

- RB-005 TDA mapper (Custom Par wired).  
- RB-006 Ableton link — **exclude** `live_levels_drive` from mega.  
- MOTU **3–4** SSOT in on_start + audiodevin patch.

### F7 — Docs & repo hygiene

- Refresh [FEATURE_MATRIX.md](FEATURE_MATRIX.md) from RESEARCH_PASS counts.  
- REPO_POLICY / optional dedicated BRIKVJ repo RB-008 deferred.

---

## 5. Twelve-session execution map

| Session | Theme | Exit evidence |
|---------|--------|----------------|
| **S1** | P0 mega + verify | `build.log` no Traceback; `verify_brikvj_stack` 0 |
| **S2** | Quiet open + audio | User 0–1 modals; td_errors ↓; MOTU 3–4 |
| **S3** | RB-001 batch | 5 td2023 resaves for **used** tox |
| **S4** | F3 integrate | colorizer OR warmth in FX_DEFS + mega |
| **S5** | F2 integrate | 3 harvest_pick scenes scored |
| **S6** | RB-004 design | lab lazy cook spec + partial code |
| **S7** | RB-004 impl | open toe router 2 without cooking all Hydra |
| **S8** | F5 mapping | dome_preview or output map evaluated |
| **S9** | RB-005 | TDA mapper smoke with Live |
| **S10** | RB-006 | Ableton link one test |
| **S11** | F6 presets | preset_bank + hub_index labels |
| **S12** | Audit | RESEARCH_PASS all green; FEATURE_MATRIX updated |

**TD rule:** max **one** launch per session when build needed ([AGENT_TD_POLICY.md](AGENT_TD_POLICY.md)).

---

## 6. Code review backlog (research-ordered)

| Priority | File | Question |
|----------|------|----------|
| 1 | `old_brik_vj_mega.py` | Any step still throws uncaught? |
| 2 | `brikvj_research_lab.py` | Cook all Hydra on open? |
| 3 | `brikvj_ableton_link.py` | Safe in mega? |
| 4 | `brikvj_live_levels_drive.py` | **Keep out of STEPS** |
| 5 | `brikvj_perform_controls.py` | scene index max vs switch inputs |
| 6 | `inject_*` | blob size limits |
| 7 | `run_once_unattended.ps1` | single launch + dismiss |

---

## 7. New-chat prompt (research + execute)

```text
BRIKVJ research pass: run brikvj_research_pass.ps1. Read RESEARCH_PASS_PLAN.md + logs/RESEARCH_PASS.md. Execute current session from §5 table with evidence. One TD launch max if build required. Update RESEARCH_BACKLOG + BUG_REGISTRY + push fork.
```

---

## 8. Document map (planning stack)

| Depth | File |
|-------|------|
| 0 | `brikvj_research_pass.ps1` |
| 1 | `logs/RESEARCH_PASS.md` (auto) |
| 2 | **RESEARCH_PASS_PLAN.md** (this file) |
| 3 | [MASTER_PLAN.md](MASTER_PLAN.md) |
| 4 | [NEXT_SESSION_PLAN_DEEPER.md](NEXT_SESSION_PLAN_DEEPER.md) |
| 5 | [NEXT_SESSION_PLAN_DEEPEST.md](NEXT_SESSION_PLAN_DEEPEST.md) |

Last research revision: 2026-10-29.
