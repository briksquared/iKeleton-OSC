# Research / practice lab: Hydra modules, fulldome, DJ tools, recorders (off perform bus by default).

import json
import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
PICK = os.path.join(ROOT, "parts", "harvest_pick")
RESEARCH = os.path.join(ROOT, "parts", "research")
EXTRA = os.path.join(ROOT, "parts", "extra")
MAX_HYDRA = 32


def log(msg):
    print("[BRIKVJ lab]", msg)


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


def load_folder(parent, folder, names, subprefix):
    outs = []
    for fn in names:
        path = os.path.join(folder, fn)
        if not os.path.isfile(path):
            continue
        slot = child(parent, subprefix + "_" + str(len(outs)), baseCOMP)
        t = td_load_tox(slot, path, "content")
        n = child(slot, "out", nullTOP)
        if t is not None:
            wire(n, 0, t)
            outs.append(n)
        else:
            try:
                slot.destroy()
            except Exception:
                pass
    return outs


def run():
    p = op("/project1")
    lab = child(p, "brikvj_lab", baseCOMP)
    lab.viewer = True
    try:
        set_label(lab, "Research / practice / dev — router index 2")
        lab.tags.add("brikvj")
        lab.tags.add("lab")
    except Exception:
        pass

    hydra = child(lab, "hydra", baseCOMP)
    set_label(hydra, "Hydra module browser")
    hydra_files = []
    if os.path.isdir(PICK):
        hydra_files = sorted(
            f
            for f in os.listdir(PICK)
            if f.lower().endswith(".tox")
            and (f.startswith("ojack-hydra") or f.startswith("HydraTD_"))
        )[:MAX_HYDRA]
    for fn in ("hydra_td.tox", "hydra_ojack.tox", "hydra.tox"):
        for folder in (RESEARCH, os.path.join(ROOT, "parts"), EXTRA):
            path = os.path.join(folder, fn)
            if os.path.isfile(path) and fn not in hydra_files:
                hydra_files.insert(0, fn)
                break
    houts = []
    for i, fn in enumerate(hydra_files):
        folder = PICK if os.path.isfile(os.path.join(PICK, fn)) else RESEARCH
        if not os.path.isfile(os.path.join(folder, fn)):
            folder = os.path.join(ROOT, "parts")
        path = os.path.join(folder, fn)
        if not os.path.isfile(path):
            continue
        slot = child(hydra, "h_%d" % i, baseCOMP)
        t = td_load_tox(slot, path, "content")
        n = child(slot, "out", nullTOP)
        if t is not None:
            wire(n, 0, t)
            houts.append(n)
    hsw = child(hydra, "hydra_switch", switchTOP)
    try:
        hsw.par.connectinput = max(len(houts), 2)
    except Exception:
        pass
    for i, o in enumerate(houts[: len(hsw.inputConnectors)]):
        wire(hsw, i, o)
    hout = child(hydra, "out", nullTOP)
    wire(hout, 0, hsw if houts else None)

    tools = child(lab, "tools", baseCOMP)
    set_label(tools, "Fulldome / DJ / record / stacker")
    tool_names = (
        "fulldome_sim.tox",
        "djay_pro.tox",
        "image_loaders.tox",
        "outputrecording2.tox",
        "presetslot.tox",
        "presetslotui.tox",
        "kodelife_glsl.tox",
        "tops_stacker_glsl.tox",
    )
    touts = load_folder(tools, RESEARCH, tool_names, "tool")
    for fn, folder in (
        ("fulldome_sim.tox", EXTRA),
        ("outputrecording2.tox", EXTRA),
        ("TOPs_stacker_GLSL.tox", os.path.join(ROOT, "parts")),
    ):
        path = os.path.join(folder, fn)
        if os.path.isfile(path):
            slot = child(tools, "tool_x_" + fn.replace(".", "_"), baseCOMP)
            t = td_load_tox(slot, path, "content")
            n = child(slot, "out", nullTOP)
            if t is not None:
                wire(n, 0, t)
                touts.append(n)
    tsw = child(tools, "tools_switch", switchTOP)
    try:
        tsw.par.connectinput = max(len(touts), 2)
    except Exception:
        pass
    for i, o in enumerate(touts[: len(tsw.inputConnectors)]):
        wire(tsw, i, o)
    tout = child(tools, "out", nullTOP)
    wire(tout, 0, tsw if touts else None)

    lsw = child(lab, "lab_switch", switchTOP)
    wire(lsw, 0, hout if houts else tout)
    wire(lsw, 1, tout if touts else hout)
    out = child(lab, "out", nullTOP)
    wire(out, 0, lsw)

    idx = []
    for c in lab.children:
        if c.name in ("hydra", "tools"):
            idx.append(c.path)
    help_dat = p.op("brikvj_lab_index")
    if help_dat is None:
        help_dat = p.create(textDAT, "brikvj_lab_index")
    help_dat.text = (
        "BRIKVJ lab — practice / research\n"
        "  /project1/brikvj_lab/hydra/hydra_switch\n"
        "  /project1/brikvj_lab/tools/tools_switch\n"
        "  Router: brikvj_router/source_switch index 2 = lab out\n"
        "Loaded hydra modules: %d, tools: %d\n"
    ) % (len(houts), len(touts))
    try:
        help_dat.viewer = True
        set_label(help_dat, "Lab index")
    except Exception:
        pass
    log("Lab ready — hydra=%d tools=%d" % (len(houts), len(touts)))


run()
