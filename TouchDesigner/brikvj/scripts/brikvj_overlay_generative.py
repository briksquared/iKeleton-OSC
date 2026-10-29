# Optional generative overlay (spiral / spinpulser) composited on the Resolume mixer bus.

import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
GEN = os.path.join(ROOT, "parts", "generative")
OVERLAYS = (
    ("spiral.tox", "spiral"),
    ("spinpulser.tox", "spinpulser"),
)


def log(msg):
    print("[BRIKVJ overlay gen]", msg)


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
        log("No old_brik_vj")
        return
    base = vj.op("mixer/out")
    if base is None:
        base = vj.op("fx/out")
    if base is None:
        log("No mixer/fx out")
        return

    ov = child(vj, "overlay_gen", baseCOMP)
    set_label(ov, "Generative overlay — overlay_switch 0=off 1=on")

    outs = []
    for fn, nice in OVERLAYS:
        path = os.path.join(GEN, fn)
        if not os.path.isfile(path):
            log("MISSING " + path)
            continue
        slot = child(ov, nice, baseCOMP)
        t = td_load_tox(slot, path, "content")
        n = child(slot, "out", nullTOP)
        if t is not None:
            wire(n, 0, t)
        outs.append(n)

    if not outs:
        log("No overlay tox loaded")
        return

    osw = child(ov, "overlay_pick", switchTOP)
    for i, o in enumerate(outs[: min(len(outs), len(osw.inputConnectors))]):
        wire(osw, i, o)

    comp = child(ov, "over", compositeTOP)
    try:
        comp.par.operand = "over"
        comp.par.precedence = 1
    except Exception:
        pass
    wire(comp, 0, base)
    wire(comp, 1, osw)

    bypass = child(ov, "dry", nullTOP)
    wire(bypass, 0, base)

    sw = child(ov, "overlay_switch", switchTOP)
    wire(sw, 0, bypass)
    wire(sw, 1, comp)
    out = child(ov, "out", nullTOP)
    wire(out, 0, sw)

    fx = vj.op("fx")
    if fx is not None:
        fx_in = fx.op("bypass")
        if fx_in is not None:
            try:
                wire(fx_in, 0, out)
                log("Re-wired fx input → overlay_gen/out")
            except Exception as ex:
                log("rewire fx: " + str(ex))

    log("Overlay ready — map ` or perform key to overlay_switch when wired")


run()
