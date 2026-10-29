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
    raise SystemExit("Missing BRIKVJ scripts at " + SCRIPTS + " — run sync_scripts_to_documents.ps1")

# Legacy entry — delegates to mega stack (show + practice + research).
MEGA = os.path.join(SCRIPTS, "old_brik_vj_mega.py")
STEPS = ()  # unused when MEGA exists

try:
    open(LOG, "w").write("build started\n")
    open(r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\boot_trace.txt", "a").write("2\n")
except Exception:
    pass

if os.path.isfile(MEGA):
    _log("[Old Brik V J] running mega stack via " + MEGA)
    exec(compile(open(MEGA, encoding="utf-8").read(), MEGA, "exec"), globals())
else:
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
