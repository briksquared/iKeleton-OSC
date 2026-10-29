# Resolume-class BRIKVJ build — clips, scenes, FX, mapping, viewers, generative audio.
import os

SCRIPTS = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\scripts"
LOG = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\build.log"

STEPS = (
    "brikvj_accept_newer_tox_pref.py",
    "brikvj_resolume_stack.py",
    "brikvj_generative_audio.py",
    "brikvj_overlay_generative.py",
    "brikvj_audio_reactive_fx.py",
    "brikvj_integrate_brioch.py",
    "brikvj_broadcast_outputs.py",
    "brikvj_viewers.py",
    "brikvj_window_setup.py",
    "brikvj_perform_mode.py",
    "brikvj_audio_bridge.py",
    "brikvj_clip_media_refresh.py",
    "brikvj_perform_controls.py",
    "brikvj_preset_bank.py",
    "brikvj_osc_control.py",
    "brikvj_glitch_autopilot.py",
    "brikvj_post_build_verify.py",
)


def _log(msg):
    print(msg)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


if not os.path.isdir(SCRIPTS):
    raise SystemExit("Run sync_scripts_to_documents.ps1 first")

try:
    open(LOG, "w").write("resolume build started\n")
except Exception:
    pass

g = globals()
_helpers = os.path.join(SCRIPTS, "brikvj_td_helpers.py")
if os.path.isfile(_helpers):
    exec(compile(open(_helpers, encoding="utf-8").read(), _helpers, "exec"), g)

for name in STEPS:
    path = os.path.join(SCRIPTS, name)
    if not os.path.isfile(path):
        _log("[BRIKVJ resolume] SKIP missing " + name)
        continue
    _log("[BRIKVJ resolume] --- " + name + " ---")
    try:
        exec(compile(open(path, encoding="utf-8").read(), path, "exec"), g)
    except Exception:
        import traceback

        _log(traceback.format_exc())

_log("[BRIKVJ resolume] finished — save BRIKVJ.toe")
try:
    project.save()
    _log("[BRIKVJ resolume] project.save() OK")
except Exception as ex:
    _log("[BRIKVJ resolume] save: " + str(ex))
