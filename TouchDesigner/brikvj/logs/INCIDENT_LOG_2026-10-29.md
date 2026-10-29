# BRIKVJ incident log (2026-10-29)

Structured record for agents. Registry IDs cross-link [BUG_REGISTRY.md](../BUG_REGISTRY.md).

---

## INC-2026-10-29-001 — Toe truncated by quiet patch

| Field | Value |
|-------|-------|
| Severity | P0 |
| Status | closed (mitigated) |
| Bug ID | B-INJ-001 |
| Symptom | `BRIKVJ.toe` collapsed to 0 bytes after patch attempt |
| Recovery | Restored from `.bkp109`; added collapse size guard in `patch_brikvj_quiet_open.ps1` |
| Prevention | Never patch without pre/post byte count; refuse if shrink > threshold |

---

## INC-2026-10-29-002 — Mega Traceback (prefs import)

| Field | Value |
|-------|-------|
| Severity | P0 |
| Status | closed |
| Bug ID | B-LOG-001 |
| Symptom | `ModuleNotFoundError` for `brikvj_td_ui_prefs_snippet` inside TD `exec()` |
| Fix | Inlined `PREF_EXECS` in `brikvj_accept_newer_tox_pref.py` |
| Evidence | Documents `build.log`: all 26 steps, `project.save() OK`, no Traceback |

---

## INC-2026-10-29-003 — Agent TouchDesigner launch storm

| Field | Value |
|-------|-------|
| Severity | P0 policy |
| Status | closed |
| Bug ID | B-TD-002 |
| Symptom | ~30 TD GUI launches in one session |
| Fix | `AGENT_TD_POLICY.md`; `-AllowTouchDesignerLaunch` gate on unattended scripts |
| User expectation | **One launch per explicit user request** when implementing builds |

---

## INC-2026-10-29-004 — Modal spam on open

| Field | Value |
|-------|-------|
| Severity | P0/P1 |
| Status | mitigated (user verify step 2) |
| Bug ID | B-DLG-001, B-DLG-002 |
| Symptom | ~10 Error + version mismatch dialogs per open |
| Fix stack | quiet patch, kantan onStart, dialog prefs DAT, accept-newer pref step in mega |
| Open work | Roadmap **step 2** — user counts dialogs on next open |

---

## INC-2026-10-29-005 — Transient GPU dialog

| Field | Value |
|-------|-------|
| Severity | P2 |
| Status | watch |
| Bug ID | B-GPU-001, RB-011 |
| Symptom | GPU/driver message (transient) |
| Action | Capture exact text if repeats; ERRORS.md playbook |

---

## INC-2026-10-29-006 — OOM (Susanna)

| Field | Value |
|-------|-------|
| Severity | P1 |
| Status | watch |
| Bug ID | B-OOM-001 |
| Symptom | “Susanna ran out of memory” during/after mega |
| Context | Full mega including `brikvj_research_lab.py`; previously MAX_HYDRA=32 |
| Data loss | **Unlikely** — mega log shows `project.save() OK` |
| Mitigation | MAX_HYDRA=8; LAZY_HYDRA; `BRIKVJ_LOW_MEMORY.flag` skips 4 mega steps |
| Next | Do not relaunch TD until RAM free; use flag for next mega if user requests rebuild |

---

## INC-2026-10-29-007 — Autostart surprise builds

| Field | Value |
|-------|-------|
| Severity | P1 |
| Status | closed |
| Symptom | Execute DATs could trigger build on project open |
| Fix | `remove_brikvj_autostart_from_toe.ps1` on Documents toe (9792596 B) |
| Note | Re-run only if autostart re-injected deliberately |

---

## INC-2026-10-29-008 — Resolume FX partial load

| Field | Value |
|-------|-------|
| Severity | P1 |
| Status | open |
| Bug ID | B-LOG-002 (partial) |
| Symptom | FX loaded 24/30; gater/spinpulser missing TOP; wire index errors |
| Owner | `brikvj_resolume_stack.py` |
| Evidence | `build.log` lines 4–8; `logs/build.log.snapshot` |
