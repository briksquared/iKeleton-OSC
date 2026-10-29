# Extra scene slots from parts/harvest_pick (non-Hydra modules) → old_brik_vj/scenes.

import json
import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
PICK = os.path.join(ROOT, "parts", "harvest_pick")
MAX_SCENES = 14
SKIP_PREFIX = ("ojack-hydra", "HydraTD_")


def log(msg):
    print("[BRIKVJ harvest scenes]", msg)


def child(parent, name, typ):
    e = parent.op(name)
    if e:
        return e
    return parent.create(typ, name)


def wire(top, idx, src):
    if src is None:
        return
    src = td_top_out(src)
    if src is None:
        return
    try:
        owner = src.outputConnectors[0].owner if hasattr(src, "outputConnectors") else src
        top.inputConnectors[idx].connect(owner)
    except Exception as ex:
        log("wire: " + str(ex))


def run():
    vj = op("/project1/old_brik_vj")
    if vj is None:
        log("No old_brik_vj — run resolume stack first")
        return
    scenes = vj.op("scenes")
    sw = scenes.op("scene_switch") if scenes else None
    if sw is None:
        log("No scene_switch")
        return

    manifest = os.path.join(PICK, "HARVEST_PICK.json")
    files = []
    if os.path.isfile(manifest):
        try:
            with open(manifest, encoding="utf-8") as f:
                files = json.load(f).get("files") or []
        except Exception:
            pass
    if not files and os.path.isdir(PICK):
        files = sorted(
            x
            for x in os.listdir(PICK)
            if x.lower().endswith(".tox") and not x.startswith("HARVEST")
        )

    added = []
    for fn in files:
        if any(fn.startswith(p) for p in SKIP_PREFIX):
            continue
        if len(added) >= MAX_SCENES:
            break
        path = os.path.join(PICK, fn)
        if not os.path.isfile(path):
            continue
        nice = "pick_" + str(len(added))
        slot = child(scenes, nice, baseCOMP)
        t = td_load_tox(slot, path, "content")
        if t is None:
            try:
                slot.destroy()
            except Exception:
                pass
            continue
        n = child(slot, "out", nullTOP)
        wire(n, 0, t)
        added.append(n)

    if not added:
        log("No harvest_pick scenes loaded (skipped or newer tox)")
        return

    start_idx = 0
    for i in range(len(sw.inputConnectors)):
        if not sw.inputConnectors[i].connections:
            start_idx = i
            break
    else:
        start_idx = len(sw.inputConnectors)
    try:
        sw.par.connectinput = start_idx + len(added)
    except Exception:
        pass
    for i, n in enumerate(added):
        wire(sw, start_idx + i, n)
    log("Added %d harvest_pick scenes (scene_switch now %d inputs)" % (len(added), len(sw.inputConnectors)))


run()
