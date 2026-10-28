# Add glitch/fluid scene slots + FX under old_brik_vj (run after brikvj_suite_build.py).

import os

ROOT = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj"
GF = os.path.join(ROOT, "parts", "glitch_fluid")


def log(msg):
    print("[BRIKVJ glitch/fluid]", msg)


def proj():
    return op("/project1")


def child(parent, name, typ, reuse=True):
    if reuse and parent.op(name):
        return parent.op(name)
    return parent.create(typ, name)


def load_tox(parent, filename, nicename):
    path = os.path.join(GF, filename)
    if not os.path.isfile(path):
        log("MISSING " + path)
        return None
    try:
        return parent.loadTox(path, customName=nicename)
    except Exception as ex:
        log(filename + ": " + str(ex))
        return None


def wire(top, idx, src):
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
    sw = scenes.op("scene_switch")
    fluid_defs = (
        ("fluid_2d", "fluid_2d_solver.tox"),
        ("fluid_3d", "fluid_3d_grid.tox"),
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
    chain_op = fx.op("out")
    if chain_op is None:
        return
    # Insert before out: find upstream — append parallel glitch_bank
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
        # dry = current fx out input — keep simple: glitch_switch out feeds nothing auto; manual wire
        bout = child(bank, "out", nullTOP)
        wire(bout, 0, gsw)
        log("glitch_bank built — wire glitch_bank/out into fx chain or blend in comper")


add_fluid_scenes()
add_glitch_fx_chain()
log("Done — scene_switch indices 7+ for fluids; see glitch_bank under fx")
