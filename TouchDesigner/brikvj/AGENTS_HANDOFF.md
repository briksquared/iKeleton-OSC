# Agent handoff — BRIKVJ

Read first: **[NEXT_SESSION_PLAN.md](NEXT_SESSION_PLAN.md)** (verify → discover → finish), then [WORKLOG.md](WORKLOG.md), [USER_REQUESTS.md](USER_REQUESTS.md), [ERRORS.md](ERRORS.md), [WHERE_IS_BRIKVJ.md](WHERE_IS_BRIKVJ.md).

## One-line state

Git kit under `TouchDesigner/brikvj/`; live show file **`Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe`** (~6 MB mega + quiet-open patch). Build with **`old_brik_vj_mega.py`** or **`run_once_unattended.ps1 -ForceResolumeRebuild`** (TD closed).

## If user sees popups on open

1. Run `scripts/patch_brikvj_quiet_open.ps1`
2. TD Preferences → Dialogs → Operator Errors → Textport; newer .tox → Accept

## If build fails

- Check `Documents\...\logs\build.log`, `boot_trace.txt`
- `scan_tox_build_versions.ps1` → `parts/TOX_BUILDS.json` (skip newer tox on 2023)
- `inject_brikvj_build_autostart.py` onStart must stay ≤ execute DAT blob limit (~564 bytes)

## Next optional work

- Wire more `harvest_pick` into scene bank without loading 2025 okVJ without `td2023/` resave
- Fix remaining FX chain wire warnings in build.log
- Scrub Mac paths in embedded Brioch parms (audit script)
