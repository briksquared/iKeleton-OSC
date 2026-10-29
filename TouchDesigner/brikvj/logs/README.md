# BRIKVJ logs

Runtime logs live under **`C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\`** after sync/build.

| File | Purpose |
|------|---------|
| `build.log` | Output of `old_brik_vj_fast.py` / `old_brik_vj_mega.py` / all-in-one |
| `boot_trace.txt` | Autostart execute milestones (`2`, `S`, `X`, etc.) |
| `td_errors.txt` | Snapshot from `capture_brikvj_errors.ps1` / `td_dump_errors.py` |
| `build.lock` | Present while unattended build runs — remove if stale |
| `GAPS_REPORT.md` | Output of `brikvj_gap_report.ps1` |
| `RESEARCH_DIFF.md` | Output of `brikvj_research_diff.ps1` (unwired harvest) |
| `HANDOFF_DETAILED_2026-10-29.md` | **Primary agent handoff** (paths, OOM, commits) |
| `INCIDENT_LOG_2026-10-29.md` | Structured incident record |
| `GIT_COMMIT_MANIFEST_2026-10-29.md` | Fork commit list |
| `build.log.snapshot` | Kit copy of last successful Documents mega log |
| `SESSION_BRIEF.md` / `CONTINUITY.json` | `brikvj_session_start.ps1` |

## Capture (agent / script)

```powershell
Documents\TouchDesigner\BRIKVJ\scripts\capture_brikvj_errors.ps1
Documents\TouchDesigner\BRIKVJ\scripts\summarize_td_errors.py
```

## Last known build markers (2026-10-29)

- Mega path: **26 steps**, `[BRIKVJ mega] project.save() OK`, **no Traceback** (see `build.log.snapshot`)
- Resolume: **FX loaded 24 / 30**; wire warnings on gater/spinpulser — see INCIDENT_LOG
- Live toe **9792596 B** (Documents); autostart Execute DATs **removed** from toe
- OOM (Susanna): use `BRIKVJ_LOW_MEMORY.flag` + `MAX_HYDRA=8` before next mega

Copy tails into this folder manually if you want them in git:

```powershell
Copy-Item "$env:USERPROFILE\Documents\TouchDesigner\BRIKVJ\logs\build.log" `
  "...\TouchDesigner\brikvj\logs\build.log.snapshot" -ErrorAction SilentlyContinue
```

This repo folder keeps **README only** by default so logs stay fresh on the machine.
