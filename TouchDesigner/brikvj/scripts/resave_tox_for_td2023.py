# One-time inside TouchDesigner (2023.12370): re-save vj_suite .tox so load stops asking.
# Dialogs → Preferences → Dialogs → "Load .tox from newer TouchDesigner build" → Accept (or run once with OK spam).
# Output: parts/vj_suite/td2023/*.tox and parts/extra/td2023/*.tox

import os
import shutil

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\parts"
SRC_DIRS = ("vj_suite", "extra", "glitch_fluid")
STAGE = "/project1/brikvj_resave_stage"


def log(msg):
    print("[BRIKVJ resave]", msg)


def run():
    p = op("/project1")
    stage = p.op("brikvj_resave_stage")
    if stage is None:
        stage = p.create(baseCOMP, "brikvj_resave_stage")
    count = 0
    for sub in SRC_DIRS:
        folder = os.path.join(ROOT, sub)
        if not os.path.isdir(folder):
            continue
        out_dir = os.path.join(folder, "td2023")
        os.makedirs(out_dir, exist_ok=True)
        for fn in sorted(os.listdir(folder)):
            if not fn.lower().endswith(".tox"):
                continue
            src = os.path.join(folder, fn)
            if not os.path.isfile(src):
                continue
            dst = os.path.join(out_dir, fn)
            try:
                for c in stage.children:
                    try:
                        c.destroy()
                    except Exception:
                        pass
                t = stage.loadTox(src)
                if t is None:
                    continue
                t.save(dst)
                count += 1
                log("resaved " + sub + "/" + fn)
            except Exception as ex:
                log("FAIL " + fn + ": " + ex)
    log("Done — %d files under */td2023/ (build scripts prefer these)" % count)


run()
