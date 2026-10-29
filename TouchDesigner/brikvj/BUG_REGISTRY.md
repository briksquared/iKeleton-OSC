# BRIKVJ bug registry

Living list. Auto-scan: `scripts/brikvj_bug_scan.ps1` → `logs/BUG_SCAN.md`.

**Severity:** P0 = blocks clean mega / show open · P1 = quality · P2 = intermittent / external

| ID | Status | Sev | Bug | Fix / owner |
|----|--------|-----|-----|-------------|
| B-LOG-001 | open | P0 | `build.log` contains Traceback (stale until next mega) | Kit fixes shipped; **one** TD mega save (headless/minimized OK) |
| B-LOG-002 | mitigated | P1 | Resolume FX wire to COMP not TOP | `td_top_out` in `build_fx` — verify on rebuild |
| B-TD-001 | open | P1 | Brioch `analyseAudio` NoneType (71+ td_errors lines) | MOTU **3–4**; `patch_brikvj_quiet_open`; audio before cook |
| B-TOX-001 | open | P1 | 77+ newer-than-2023 `.tox` | RB-001 td2023; dialog prefs on toe |
| B-DLG-001 | mitigated | P0 | ~10 Error dialogs on open (kantan force cook) | `inject_kantan_boot` + quiet patch |
| B-DLG-002 | mitigated | P1 | ~10 newer/older `.tox` modals | `000_brikvj_dialog_prefs` + kantan onStart |
| B-TDA-001 | mitigated | P1 | TDA mapper `parexecuteDAT` create fail | `td_create_op` + non-fatal bridge |
| B-GPU-001 | watch | P2 | Transient GPU dialog (went away) | Single TD launch; NVIDIA preferred GPU |
| B-TD-002 | policy | P0 | Agent opened TD ~30× | `AGENT_TD_POLICY.md`; one launch / user ask |
| B-INJ-001 | fixed | P0 | `patch_brikvj_quiet_open` could truncate toe | Collapse size guard + restore from `.bkp` |

**Status:** `open` | `mitigated` | `fixed` | `wontfix` | `watch`

Close bugs with: log line + `build.log` no Traceback + user confirm for UI.
