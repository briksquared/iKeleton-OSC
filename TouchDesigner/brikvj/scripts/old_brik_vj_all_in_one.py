# Old Brik V J — build + MOTU audio in one run (Textport or brikvj_manual_build DAT)
import os
import traceback

SCRIPTS = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\scripts"
LOG = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\build.log"
FLAG = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\RUN_BUILD.flag"
UNATTENDED = os.path.isfile(FLAG)

def _log(msg):
    print(msg)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass
if not os.path.isdir(SCRIPTS):
    SCRIPTS = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\scripts"

STEPS = (
    "brikvj_suite_build.py",
    "brikvj_glitch_fluid_layers.py",
    "old_brik_vj_audio.py",
    "brikvj_integrate_brioch.py",
    "brikvj_broadcast_outputs.py",
    "brikvj_window_setup.py",
    "brikvj_ableton_link.py",
    "brikvj_audio_bridge.py",
    "brikvj_live_levels_drive.py",
    "brikvj_clip_media_refresh.py",
    "brikvj_preset_bank.py",
    "brikvj_tda_mapper_bridge.py",
    "brikvj_perform_controls.py",
    "brikvj_project_on_start.py",
    "brikvj_glitch_autopilot.py",
    "brikvj_patchworks_audio_routes.py",
    "brikvj_fx_audio_bind.py",
    "brikvj_osc_control.py",
    "brikvj_post_build_verify.py",
)

try:
    open(LOG, "w").write("build started\n")
except Exception:
    pass

g = globals()
_helpers = os.path.join(SCRIPTS, "brikvj_td_helpers.py")
if os.path.isfile(_helpers):
    exec(compile(open(_helpers, encoding="utf-8").read(), _helpers, "exec"), g)

for name in STEPS:
    path = os.path.join(SCRIPTS, name)
    if not os.path.isfile(path):
        _log("[Old Brik V J] missing: " + path)
        continue
    _log("[Old Brik V J] --- " + name + " ---")
    try:
        exec(compile(open(path, encoding="utf-8").read(), path, "exec"), g)
    except Exception:
        _log(traceback.format_exc())
        raise

_log("[Old Brik V J] all-in-one finished — save BRIKVJ.toe")
try:
    project.save()
    _log("[Old Brik V J] project.save() OK")
except Exception as ex:
    _log("[Old Brik V J] save: " + str(ex))

if UNATTENDED:
    _log("[Old Brik V J] unattended — quitting TouchDesigner in 2s")

    def _quit():
        try:
            project.quit(force=True)
        except Exception:
            pass

    run(_quit, delayMilliSeconds=2000)
