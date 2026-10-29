# BRIKVJ bug scan (generated 2026-10-29T09:31:55.5996581-05:00)

Run: `scripts/brikvj_bug_scan.ps1`. Full registry: [BUG_REGISTRY.md](../BUG_REGISTRY.md).

| ID | Sev | Summary | Fix |
|----|-----|---------|-----|
| B-TD-001 | P1 | td_errors.txt 71 lines (Brioch analyseAudio/mesh) | MOTU 3-4; quiet open; no force cook |
| B-TOX-001 | P1 | 77 tox newer than 2023 | td2023 resaves RB-001; Accept pref |
| B-GPU-001 | P2 | Transient GPU/driver dialog (user report) | One TD instance; NVIDIA perf mode; note exact text if repeats |

## Next code review targets

- `old_brik_vj_mega.py` step list vs `BUILD.md`
- `brikvj_live_levels_drive.py` (crash history — keep out of mega)
- `FEATURE_MATRIX.md` stale counts → recount from `brikvj_resolume_stack.py`
