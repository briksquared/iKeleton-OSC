# Thin harvest layer: Brioch stays primary; load a few reference .tox only (not the full suite).
# Use when the 19-step all-in-one is too heavy or TD keeps crashing.

import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
PARTS = os.path.join(ROOT, "parts")
BUILD_LOG = os.path.join(ROOT, "logs", "build.log")

# From your harvest index / PARTS.json — high value, lower crash risk than full fluid_3d grid.
PICKS = (
    ("parts", "comper.tox", "layer_comper"),
    ("parts", "Double_Feedback.tox", "feedback"),
    ("parts", "tdx_datamosh.tox", "datamosh"),
    ("parts/vj_suite", "okvj_glitch_stack.tox", "glitch"),
)


def log(msg):
    line = "[BRIKVJ minimal] " + msg
    print(line)
    try:
        with open(BUILD_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def proj():
    return op("/project1")


def child(parent, name, typ):
    e = parent.op(name)
    if e:
        return e
    return parent.create(typ, name)


def wire(top, idx, src):
    src = td_top_out(src)
    if src is None:
        return
    try:
        top.inputConnectors[idx].connect(
            src.outputConnectors[0].owner if hasattr(src, "outputConnectors") else src
        )
    except Exception as ex:
        log("wire: " + str(ex))


def run():
    p = proj()
    vj = child(p, "old_brik_vj", baseCOMP)
    vj.viewer = True
    try:
        vj.tags.add("brikvj")
        vj.tags.add("vj_minimal")
    except Exception:
        pass

    fx = child(vj, "fx", baseCOMP)
    chain = None
    for sub, fn, nice in PICKS:
        path = os.path.join(ROOT, sub, fn)
        if not os.path.isfile(path):
            log("MISSING " + path)
            continue
        try:
            t = td_load_tox(fx, path, nice)
        except Exception as ex:
            log("load " + fn + ": " + str(ex))
            continue
        if t is None:
            continue
        if chain is None:
            chain = t
        else:
            wire(t, 0, chain)
            chain = t
        log("loaded " + fn)

    bypass = child(fx, "bypass", nullTOP)
    out = child(fx, "out", nullTOP)
    if chain is not None:
        sw = child(fx, "fx_switch", switchTOP)
        wire(sw, 0, chain)
        wire(sw, 1, bypass)
        wire(out, 0, sw)
    else:
        wire(out, 0, bypass)

    perform = p.op("perform_out")
    if perform is None:
        perform = p.create(outTOP, "perform_out")
    wire(perform, 0, out)

    log("MINIMAL DONE — Brioch scenes 1–6 unchanged; router step wires Brioch vs this fx/out")


try:
    run()
except Exception:
    import traceback

    log(traceback.format_exc())
    raise
