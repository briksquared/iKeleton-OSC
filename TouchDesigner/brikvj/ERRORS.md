# BRIKVJ — common errors

## Ten “Error” dialogs on every open

**Cause:** `mapping/kantanMapper/ui/execute1` was calling `parent().cook(force=True, recurse=True)` on start. That re-cooks Brioch (`analyseAudio`, meshes, etc.) before MOTU audio is ready → TouchDesigner shows one **Error** modal per failing operator.

**Fix (applied in repo):** `patch_brikvj_quiet_open.ps1` or `fix_brikvj_brioch_toe.ps1` — kantan execute is a no-op on start; `brikvj_dialog_prefs` tries to send errors to Textport only; `audiodevin1` → channels **3-4**.

Re-run if popups return after a bad inject:

```powershell
Documents\TouchDesigner\BRIKVJ\scripts\patch_brikvj_quiet_open.ps1
```

## Eleven (or many) “Load .tox from newer TouchDesigner build” dialogs

Also seen as wording about **older/newer TouchDesigner version** when loading a `.tox` — same family of dialogs.

**Cause:** Harvest `.tox` saved on TD 2025+ while you run **2023.12370**. Each `loadTox()` (or embedded references from an old save) opens a modal until you click OK.

**What we do automatically**

- Unattended builds run `dismiss_td_dialogs.ps1` (sends Enter/Esc to TD modals) and refresh `parts/TOX_BUILDS.json`.
- `td_load_tox()` **skips** newer-than-host files unless `parts/<pack>/td2023/<name>.tox` exists.
- `patch_brikvj_quiet_open.ps1` sets prefs on **kantan execute1 onStart** (runs early) + `brikvj_dialog_prefs` via `brikvj_td_ui_prefs_snippet.py` (newer **and** older .tox → Accept).
- Mega step `brikvj_accept_newer_tox_pref.py` applies the same prefs at build time.

**One-time on your machine (stops popups when you open the show file)**

1. TouchDesigner → **Preferences → Dialogs**
2. **Load .tox from newer TouchDesigner build** → **Accept** (not Ask)

**Optional:** In TD Textport once: run `scripts/resave_tox_for_td2023.py` to write `parts/*/td2023/*.tox` so those components load silently on 2023.

**Do not** leave `brikvj_build_autostart` in the toe for daily use — it mass-loads harvest `.tox`. Use `remove_brikvj_autostart_from_toe.ps1` after builds.

## Out of memory (Windows / TouchDesigner)

**Symptom:** “Ran out of memory,” TD freeze, or Susanna/system OOM during or right after mega build.

**What we know:** Full mega loads many TOPs (lab Hydra modules are the worst). Your last run **did** reach `[BRIKVJ mega] project.save() OK` in `logs/build.log` (toe ~9.1 MB) — OOM may be on quit or on next open.

**Mitigations (kit):**

- `brikvj_research_lab.py`: `MAX_HYDRA = 8`, `LAZY_HYDRA` (only index 0 cooks).
- Create empty file `Documents\TouchDesigner\BRIKVJ\BRIKVJ_LOW_MEMORY.flag` before mega → skips lab, harvest expansion, glitch overlay, extra generative overlay in `old_brik_vj_mega.py`.
- Close other GPU/RAM apps; one TD instance only.

**Do not** loop unattended builds after OOM — fix flag, sync scripts, one retry when RAM is free.

## Transient GPU / driver dialog

**Symptom:** Message mentions GPU, OpenGL, driver, or video memory; may appear once and disappear (especially after many TD launches in a row).

**Likely causes:** NVIDIA TDR timeout, VRAM pressure from heavy TOPs, or hybrid graphics picking the wrong GPU.

**Mitigations:**

1. Only **one** TouchDesigner instance; avoid agent retry loops ([AGENT_TD_POLICY.md](AGENT_TD_POLICY.md)).
2. Windows **Settings → System → Display → Graphics** → TouchDesigner → **High performance** (NVIDIA).
3. Update NVIDIA driver; close other GPU-heavy apps before show open.
4. If it repeats every open: note exact text → [BUG_REGISTRY.md](BUG_REGISTRY.md) B-GPU-001 / RB-011.
