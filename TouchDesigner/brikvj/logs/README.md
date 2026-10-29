# BRIKVJ logs

Runtime logs live under **`C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\`** after sync/build.

| File | Purpose |
|------|---------|
| `build.log` | Output of `old_brik_vj_fast.py` / `old_brik_vj_mega.py` / all-in-one |
| `boot_trace.txt` | Autostart execute milestones (`2`, `S`, `X`, etc.) |
| `td_errors.txt` | Snapshot from `capture_brikvj_errors.ps1` / `td_dump_errors.py` |
| `build.lock` | Present while unattended build runs — remove if stale |

## Capture (agent / script)

```powershell
Documents\TouchDesigner\BRIKVJ\scripts\capture_brikvj_errors.ps1
Documents\TouchDesigner\BRIKVJ\scripts\summarize_td_errors.py
```

## Last known build markers (2026-10-28)

- Resolume fast path: `FX loaded 30 / 30`, `project.save() OK`
- Mega path: 26 steps; autostart runs `old_brik_vj_mega.py` when `RUN_BUILD.flag` set
- Quiet-open patch: kantan `execute1` no longer force-cooks on start

Copy tails into this folder manually if you want them in git:

```powershell
Copy-Item "$env:USERPROFILE\Documents\TouchDesigner\BRIKVJ\logs\build.log" `
  "...\TouchDesigner\brikvj\logs\build.log.snapshot" -ErrorAction SilentlyContinue
```

This repo folder keeps **README only** by default so logs stay fresh on the machine.
