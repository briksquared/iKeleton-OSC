# BRIKVJ — detailed agent handoff (2026-10-29)

**Purpose:** Single long-form continuity document after mega save, OOM on Susanna, dialog/automation work, and fork push.  
**Cursor transcript:** `a38c1ae0-2c81-46db-8e9e-4ef553e7f5be` ([agent-transcripts folder on this machine](file:///C:/Users/briks/.cursor/projects/c-Users-briks-Desktop-GitHub/agent-transcripts/a38c1ae0-2c81-46db-8e9e-4ef553e7f5be.jsonl)).

---

## 0. Read order (next chat)

| Priority | File | Why |
|----------|------|-----|
| 1 | [AGENT_TD_POLICY.md](../AGENT_TD_POLICY.md) | **No TD launch** unless user explicitly asks in that message |
| 2 | [logs/SESSION_BRIEF.md](SESSION_BRIEF.md) | Auto snapshot from `brikvj_session_start.ps1` |
| 3 | [logs/CONTINUITY.json](CONTINUITY.json) | Machine-readable same state |
| 4 | **This file** | Incidents, paths, commits, bans |
| 5 | [logs/ROADMAP_STATUS.md](ROADMAP_STATUS.md) | 18-step program — **next step #2** |
| 6 | [NEXT_SESSION_OPERATIONS.md](../NEXT_SESSION_OPERATIONS.md) | Commands to execute |
| 7 | [BUG_REGISTRY.md](../BUG_REGISTRY.md) + [ERRORS.md](../ERRORS.md) | OOM, GPU, dialogs, build |

**Bootstrap command (no TouchDesigner):**

```powershell
cd C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\scripts
git -C ..\..\..\.. pull fork main
.\brikvj_session_start.ps1
```

---

## 1. What BRIKVJ is (user intent)

- **Old Brik V J** — Resolume-class VJ stack on **TouchDesigner 2023.12370**.
- Integrated with **Brioch**, harvest from `_sweep3/touchdesigner`, **Ableton/Patchworks**, **MOTU M4**.
- **Spelling:** Brik, not Brick. Product folder name **BRIKVJ**.
- User wants **agents to run builds and fixes**, not “paste Textport yourself.”
- **Modal spam** (~10 dialogs on open) was unacceptable — mitigated via quiet patch + dialog prefs.
- **~30 TD launches** by a prior agent was unacceptable — gated behind `-AllowTouchDesignerLaunch`.

---

## 2. Path SSOT (critical)

| Role | Absolute path |
|------|----------------|
| **Live show / runtime** | `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\` |
| **Live project** | `...\BRIKVJ\BRIKVJ.toe` |
| **Live logs** | `...\BRIKVJ\logs\` (`build.log`, `td_errors.txt`, …) |
| **Git kit (scripts, parts, docs)** | `C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\` |
| **Git remote (push here)** | `fork` → `https://github.com/briksquared/iKeleton-OSC.git` branch `main` |
| **Upstream (do not push)** | `origin` → `gwangyu-lee/iKeleton-OSC` (403) |

**REPO_POLICY:** Do **not** treat the iKeleton-OSC tree as the live show home. Do **not** commit a stale `TouchDesigner/BRIKVJ.toe` at repo root (935880 B, 2026-10-28) — live toe is **9792596 B** (2026-10-29) under Documents only.

After kit edits: `scripts\sync_scripts_to_documents.ps1`.

---

## 3. Measured state (2026-10-29 ~09:30 local)

| Metric | Value | Evidence |
|--------|------:|----------|
| Live `BRIKVJ.toe` size | **9_792_596** bytes | `Get-Item` Documents toe; `RESEARCH_PASS.md` |
| `build.log` Traceback | **None** | Documents `logs/build.log` full read |
| Mega save | **OK** | Last line: `[BRIKVJ mega] project.save() OK` |
| Mega steps executed | **26** (full) | `build.log` step headers through `post_build_verify` |
| SCENE_DEFS | **20** | `brikvj_resolume_stack.py` |
| FX_DEFS | **30** | same (+ colorizer wired in kit) |
| FX loaded last mega | **24 / 30** | `build.log` resolume section |
| Unwired `.tox` | **122** | `logs/RESEARCH_DIFF.md` |
| Newer than TD 2023 | **77** | `parts/TOX_BUILDS.json` / diff |
| `td_errors.txt` lines | **71** | Brioch `analyseAudio` / mesh NoneType (B-TD-001) |
| TouchDesigner running | **False** | session_start |
| Git HEAD (fork) | **ca601bd** | low-memory mega + OOM docs |
| Roadmap step 1 | **done** | `logs/ROADMAP_STATUS.md` |
| **Next roadmap step** | **#2** | Quiet open — **user** verifies dialog count |

### 3.1 Last mega build warnings (not fatal)

From Documents `logs/build.log`:

- `[BRIKVJ resolume] wire: list index out of range` (×2)
- `[BRIKVJ resolume] no TOP in fx gater`
- `[BRIKVJ resolume] no TOP in fx spinpulser_fx`
- `[BRIKVJ resolume] FX loaded 24 / 30`

**Owner:** Resolume FX chain wiring — verify after next rebuild; `td_top_out` mitigated COMP-not-TOP (B-LOG-002).

### 3.2 Post-mega toe surgery (no TD)

`remove_brikvj_autostart_from_toe.ps1` (2026-10-29):

- Removed autostart Execute DATs (prevents surprise mega on open).
- Injected `000_brikvj_dialog_prefs` / quiet-open related prefs.
- Result toe **9792596 B** (Documents).

Kit copy at repo `TouchDesigner/BRIKVJ.toe` is **obsolete** — ignore for show.

---

## 4. Incidents timeline (this program)

### 4.1 Dialog spam (mitigated)

- **Symptom:** ~10 Error + newer/older `.tox` modals every open.
- **Fixes:** `patch_brikvj_quiet_open.ps1` (collapse size guard), `inject_kantan_boot.py`, `brikvj_accept_newer_tox_pref.py` (inlined `PREF_EXECS` — TD `exec()` cannot import snippet module), `000_brikvj_dialog_prefs` in toe.
- **Registry:** B-DLG-001, B-DLG-002.
- **Failure mode avoided:** `patch_brikvj_quiet_open` once truncated toe to **0 B** — restored from `.bkp109`; guard added (B-INJ-001).

### 4.2 Agent TD launch storm (policy)

- **Symptom:** ~30 TouchDesigner launches.
- **Fix:** [AGENT_TD_POLICY.md](../AGENT_TD_POLICY.md); `run_once_unattended.ps1`, headless build, error capture require **`-AllowTouchDesignerLaunch`**.
- **Registry:** B-TD-002.

### 4.3 Mega Traceback (fixed)

- **Symptom:** `ModuleNotFoundError` on prefs snippet during mega.
- **Fix:** Inline prefs in `brikvj_accept_newer_tox_pref.py`.
- **Registry:** B-LOG-001 → mitigated after save OK.

### 4.4 GPU dialog (watch)

- **Symptom:** Transient GPU/driver dialog (user).
- **Doc:** ERRORS.md GPU section; RB-011 open.

### 4.5 OOM — “Susanna ran out of memory” (watch)

- **Symptom:** Windows/TD OOM during or after heavy lab/Hydra load.
- **Likely:** RAM pressure from `brikvj_research_lab.py` (was MAX_HYDRA=32) + full mega.
- **Important:** Mega **still saved** before/at OOM boundary (`project.save() OK`).
- **Mitigations shipped (ca601bd):**
  - `MAX_HYDRA = 8` in `brikvj_research_lab.py`
  - `LAZY_HYDRA`: `allowCooking` only for lab index 0 (RB-004 in_progress)
  - `Documents\TouchDesigner\BRIKVJ\BRIKVJ_LOW_MEMORY.flag` (empty file) → `old_brik_vj_mega.py` skips: `research_lab`, `harvest_scene_expansion`, `glitch_fluid_layers`, `overlay_generative`
- **Registry:** B-OOM-001; ERRORS.md OOM section.
- **Do not:** Loop unattended megas after OOM without flag + free RAM.

---

## 5. Mega pipeline reference

**Entry:** `scripts/old_brik_vj_mega.py` — **FULL_STEPS** = 26 Python modules (see [BUILD.md](../BUILD.md)).

**LOW_MEMORY mode:** If `BRIKVJ_LOW_MEMORY.flag` exists next to live toe folder root (`Documents\...\BRIKVJ\`), mega skips 4 heavy steps (see §4.5).

**User unattended (only when user explicitly allows one launch):**

```powershell
cd ...\brikvj\scripts
.\run_once_unattended.ps1 -ForceResolumeRebuild -AllowTouchDesignerLaunch
```

**Manual:** Open toe → Textport → paste `scripts/TEXTPORT_MEGA.txt` → Save.

---

## 6. Research / roadmap automation

| Script | Output |
|--------|--------|
| `brikvj_research_pass.ps1` | `logs/RESEARCH_PASS.md`, refreshes taxonomy/roadmap hooks |
| `brikvj_research_taxonomy.ps1` | `logs/RESEARCH_TAXONOMY.md` |
| `brikvj_roadmap_status.ps1` | `logs/ROADMAP_STATUS.md` |
| `brikvj_bug_scan.ps1` | `logs/BUG_SCAN.md` |
| `brikvj_gap_report.ps1` | `logs/GAPS_REPORT.md` (exit **1** if any gap — expected while td_errors>40 and newer tox>50) |
| `brikvj_session_start.ps1` | Sync + all above + `SESSION_BRIEF.md` + `CONTINUITY.json` |

**18-step program:** [RESEARCH_PASS_PLAN_DEEPER.md](../RESEARCH_PASS_PLAN_DEEPER.md) §E — status in `ROADMAP_STATUS.md`.

**Open RESEARCH_BACKLOG (6 open/in_progress):** RB-001, RB-003, RB-004, RB-005, RB-011, RB-012 (+ deferred RB-008).

---

## 7. Git: commits on fork (16 ahead of upstream origin)

Pushed to **`fork/main`** on 2026-10-29 (includes `ca601bd`):

| Commit | Summary |
|--------|---------|
| fbee689 | Initial Old Brik VJ kit + build automation |
| 42abb3c | Mega stack, harvest packs, quiet-open, docs |
| 9f0fc9b … 15d725b | NEXT_SESSION plans, gap report |
| d63c3a6 … 48be739 | Operations runbook, DEEPER continuity |
| 886b374 | Dialog prefs, one TD launch policy, safe quiet-open |
| 34f79e2 | FX wiring, TDA bridge non-fatal, RB-002 |
| be3f3a2 … 6dd3a1d | MASTER_PLAN, BUG_REGISTRY, WORKLOG |
| 55489c2 … 0e2dca4 | Research pass, taxonomy, BRIKVJ_ROADMAP |
| **ca601bd** | **LOW_MEMORY mega, MAX_HYDRA=8, OOM docs, roadmap step 1** |

See also [logs/GIT_COMMIT_MANIFEST_2026-10-29.md](GIT_COMMIT_MANIFEST_2026-10-29.md).

---

## 8. Next agent actions (ordered)

### 8.1 Step 2 — Quiet open (USER)

- User opens **Documents** `BRIKVJ.toe` **once** when RAM is healthy.
- Count Error / newer `.tox` dialogs; note in WORKLOG.
- If spam returns: `patch_brikvj_quiet_open.ps1` (toe size guard), re-check kantan onStart prefs.

### 8.2 Step 3 — Audio / td_errors (AGENT + USER MOTU)

- MOTU outputs **3–4** per Brioch audio path.
- Goal: `td_errors.txt` ≤ 25 lines (roadmap auto check).
- Do not force-cook Brioch tree before audio valid (RB-012).

### 8.3 Step 4 — td2023 resaves (AGENT)

- RB-001: resave **used** newer tox to `td2023/` before wiring more okVJ.

### 8.4 Step 5–6 — Integrate (AGENT, one TD launch max when user OK)

- Colorizer / warmth FX (queue rank 1–2 in ROADMAP_STATUS).
- Two harvest scenes (dedupe Hydra vs SCENE_DEFS).

### 8.5 Resolume wire warnings (AGENT)

- Fix gater / spinpulser_fx TOP discovery; clip/comper index errors in `brikvj_resolume_stack.py`.

### 8.6 Memory-safe rebuild policy

- After OOM: create `BRIKVJ_LOW_MEMORY.flag`, sync scripts, **one** launch when user asks.
- Remove flag after successful lightweight save if user wants full lab back.

---

## 9. Hard bans (do not repeat)

1. Launch TouchDesigner without explicit user ask in **that** message.
2. `patch_brikvj_quiet_open` without toe size sanity check.
3. Commit live `BRIKVJ.toe` into iKeleton-OSC repo root stale copy.
4. `deleteFiles=true` on qBit (unrelated but household rule).
5. Media Stack Chrome/VPN thrashing during user calls (hands-off rules).
6. Push to `origin` (upstream 403) — use **`fork`**.

---

## 10. Snapshots in this commit

- `logs/build.log.snapshot` — copy of Documents mega log ending in `project.save() OK`.
- Auto-generated: `RESEARCH_PASS.md`, `RESEARCH_DIFF.md`, `GAPS_REPORT.md`, `BUG_SCAN.md`, `ROADMAP_STATUS.md`, `SESSION_BRIEF.md`, `CONTINUITY.json`.

---

## 11. New-chat paste block

```text
BRIKVJ handoff 2026-10-29: Read TouchDesigner/brikvj/logs/HANDOFF_DETAILED_2026-10-29.md + AGENT_TD_POLICY. SSOT Documents\TouchDesigner\BRIKVJ. Fork briksquared/iKeleton-OSC @ ca601bd+. Roadmap step 2 (user quiet open). No TD unless I say so. OOM: use BRIKVJ_LOW_MEMORY.flag for next mega.
```
