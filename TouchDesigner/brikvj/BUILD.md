# Build Old Brik V J

Perform file: `Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe` (Brioch base, Windows-patched).

## Mega build (show + practice + research) — recommended

1. `sync_scripts_to_documents.ps1`
2. Open `BRIKVJ.toe` when **you** want → Textport: `TEXTPORT_MEGA.txt` → Save  
   Optional one-shot unattended: only if you ask the agent → `run_once_unattended.ps1 -ForceResolumeRebuild -AllowTouchDesignerLaunch` (TD closed). See [AGENT_TD_POLICY.md](AGENT_TD_POLICY.md).

**26 steps:** resolume stack, harvest scenes, glitch/fluid, lab/Hydra, integrate, broadcast, perform, Ableton/Patchworks hooks, hub index, verify. See [WORKLOG.md](WORKLOG.md).

Lighter path: `TEXTPORT_FAST.txt` (resolume-only). Legacy all-in-one delegates to mega.

**Adding features:** [ADD_FEATURES.md](ADD_FEATURES.md).

## Quiet open (no Error dialog spam)

After any kantan inject that force-cooked the network:

```powershell
scripts\patch_brikvj_quiet_open.ps1
```

See [ERRORS.md](ERRORS.md).

## Unattended (only when TD is closed)

```powershell
powershell -ExecutionPolicy Bypass -File TouchDesigner\brikvj\scripts\run_once_unattended.ps1
```

One minimized TouchDesigner open. Polls `Documents\TouchDesigner\BRIKVJ\logs\boot_trace.txt` then `build.log`.  
`fix_brikvj_brioch_toe.ps1` strips old autostart, injects boot DAT + kantan backup hook, collapses once.

| Log | Meaning |
|-----|---------|
| No `boot_trace` | Execute `onStart` never ran — TD blocked or boot DAT not loaded |
| `boot_trace` has `1` only | Flag missing or `_go` not scheduled |
| `boot_trace` has `2`, no `build.log` | all-in-one crashed before first line |
| `build.log` Traceback | Fix script named in log |
| `all-in-one finished` | Stack built — verify with `verify_brikvj_stack.ps1` |

## Manual (Textport)

Paste `scripts/TEXTPORT_BUILD.txt` once, then save the project.

## Harvest refresh

`scripts\brikvj_refresh_all.ps1` then unattended build above.
