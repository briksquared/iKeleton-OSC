# TouchDesigner — agent policy

## Launch count

| OK | Not OK |
|----|--------|
| **One** minimized launch when the user asked for an unattended build (or you asked once and they said yes) | Opening TD again because the last build failed |
| User opens BRIKVJ themselves; you only sync scripts | 5–30 launches in a loop “to verify” |
| `dismiss_td_dialogs.ps1` running **once** alongside that single launch | Retrying `run_once_unattended.ps1` without a new explicit user OK |

**Rule:** at most **one** `Start-Process TouchDesigner.exe` per user request. If build fails, fix Python, sync, tell user to Textport `TEXTPORT_MEGA.txt` + Save — do not auto-relaunch.

## Starting TD (requires explicit user ask)

```powershell
.\patch_brikvj_quiet_open.ps1   # toe-only, no TD — do this before the one launch
.\run_once_unattended.ps1 -ForceResolumeRebuild -AllowTouchDesignerLaunch
```

Without `-AllowTouchDesignerLaunch`, the script **must not** start TD (sync/inject only).

Also gated: `brikvj_headless_build.ps1`, `capture_brikvj_errors.ps1` (same switch).

**Do not** use `open_brikvj.ps1` unless the user asked to open the app.

## Safe anytime (no TD process)

- `sync_scripts_to_documents.ps1`
- `patch_brikvj_quiet_open.ps1` (expand/inject/collapse only)
- `brikvj_session_start.ps1`, gap/research reports
- Edit kit Python, commit, push **fork**

## User already has TD open

- Do **not** kill or start a second instance.
- Paste `TEXTPORT_MEGA.txt` in Textport → Save.

## Newer / older .tox click spam

Kit sets **Accept** prefs on kantan `onStart` + `brikvj_dialog_prefs` ([`brikvj_td_ui_prefs_snippet.py`](scripts/brikvj_td_ui_prefs_snippet.py)). Re-apply without opening TD:

```powershell
.\patch_brikvj_quiet_open.ps1
```

One-time UI backup: **Preferences → Dialogs → Load .tox from newer TouchDesigner build → Accept**.

See [ERRORS.md](ERRORS.md), [ADD_FEATURES.md](ADD_FEATURES.md).
