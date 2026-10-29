# Where BRIKVJ lives (names explained)

| What | Path |
|------|------|
| **Live TouchDesigner project** | `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe` |
| **Scripts + `.tox` parts at runtime** | `Documents\TouchDesigner\BRIKVJ\scripts` and `\parts` |
| **Git** | See `REPO_POLICY.md` — kit must not live under **iKeleton-OSC** naming; use a **BRIKVJ** repo or your monorepo path you choose |

**Everything you open in TouchDesigner** comes from **`Documents\TouchDesigner\BRIKVJ`** after sync. Harvest index stays on disk for reference; runtime paths do not point at `_sweep2`.

**Compatibility dialog in TD:** Usually Brioch / `.tox` vs your TD build. Prefer the patched `BRIKVJ.toe` in Documents (after `fix_brikvj_brioch_toe.ps1`), or open `CrashAutoSave.BRIKVJ.toe` if the main file was mid-crash. On-disk `BRIKVJ.toe` (~936 KB) is still Brioch-only until a build finishes and you **Save**.

**Do not** run `run_once_unattended.ps1` while TouchDesigner is already open — it used to force-kill TD; it now exits and tells you to use the Textport line in `scripts\TEXTPORT_BUILD.txt` instead.
