# Add glitch/fluid scene slots + FX under old_brik_vj (run after brikvj_suite_build.py).

import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
GF = os.path.join(ROOT, "parts", "glitch_fluid")
BUILD_LOG = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\build.log"


def log(msg):
    line = "[BRIKVJ glitch/fluid] " + msg
    print(line)
    try:
        with open(BUILD_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def proj():
    return op("/project1")


def child(parent, name, typ, reuse=True):
    if reuse and parent.op(name):
        return parent.op(name)
    return parent.create(typ, name)


def load_tox(parent, filename, nicename):
    if filename in HEAVY_TOX_SKIP:
        log("SKIP heavy " + filename)
        return None
    path = os.path.join(GF, filename)
    if not os.path.isfile(path):
        log("MISSING " + path)
        return None
    try:
        return td_load_tox(parent, path, nicename)
    except Exception as ex:
        log(filename + ": " + str(ex))
        return None


def wire(top, idx, src):
    if src is None:
        return
    src = td_top_out(src)
    if src is None:
        return
    try:
        top.inputConnectors[idx].connect(
            src.outputConnectors[0].owner if hasattr(src, "outputConnectors") else src
        )
    except Exception as ex:
        log("wire: " + str(ex))


def add_fluid_scenes():
    vj = proj().op("old_brik_vj")
    if vj is None:
        log("Run brikvj_suite_build.py first")
        return
    scenes = vj.op("scenes")
    if scenes is None:
        log("No scenes comp")
        return
    if scenes.op("fluid_2d") is not None:
        log("fluid scenes already built in suite — skip")
        return
    sw = scenes.op("scene_switch")
    fluid_defs = (
        ("fluid_2d", "fluid_2d_solver.tox"),
        ("lysergiq", "lysergiq_fluid.tox"),
        ("flow", "flow_field.tox"),
        ("particles", "particle_life.tox"),
        ("fluid_like_fx", "fluid_like.tox"),
    )
    idx = 7
    for nice, fn in fluid_defs:
        slot = child(scenes, nice, baseCOMP)
        t = load_tox(slot, fn, "content")
        n = child(slot, "out", nullTOP)
        if t is not None:
            wire(n, 0, t)
        if sw is not None and idx < len(sw.inputConnectors):
            wire(sw, idx, n)
            log("scene_switch[%d] = %s" % (idx, nice))
            idx += 1


def add_glitch_fx_chain():
    vj = proj().op("old_brik_vj")
    fx = vj.op("fx") if vj else None
    if fx is None:
        return
    if fx.op("glitch_bank") is not None:
        log("glitch_bank already present — skip")
        return
    if fx.op("crt") is not None or fx.op("tdx_crt") is not None:
        log("glitch FX already in suite — skip glitch_bank")
        return
    bank = child(fx, "glitch_bank", baseCOMP)
    defs = (
        ("crt", "tdx_crt.tox"),
        ("mod", "tdx_modulation.tox"),
        ("strobe", "strobe_fx.tox"),
        ("chaser", "chaser.tox"),
        ("pixel_push", "pixel_push.tox"),
        ("decimate", "decimate.tox"),
        ("particlize", "particlize.tox"),
        ("input_strober", "input_map_strober.tox"),
    )
    chain = None
    for nice, fn in defs:
        t = load_tox(bank, fn, nice)
        if t is None:
            continue
        if chain is None:
            chain = t
        else:
            wire(t, 0, chain)
            chain = t
    if chain is not None:
        gsw = child(bank, "glitch_switch", switchTOP)
        wire(gsw, 0, chain)
        bout = child(bank, "out", nullTOP)
        wire(bout, 0, gsw)
        log("glitch_bank built")


try:
    add_fluid_scenes()
    add_glitch_fx_chain()
    log("Done")
except Exception:
    import traceback

    log(traceback.format_exc())
    raise
