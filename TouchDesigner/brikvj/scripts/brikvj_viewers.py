# Operator viewers: clip / scene / program bus previews (Resolume-style thumbs).

def log(msg):
    print("[BRIKVJ viewers]", msg)


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
    vj = p.op("old_brik_vj")
    if vj is None:
        log("Run resolume stack first")
        return

    ui = child(p, "brikvj_ui", baseCOMP)
    set_label(ui, "Preview monitors — open viewer on each null")

    grid = child(ui, "previews", baseCOMP)
    sources = (
        ("clip_prog", "/project1/old_brik_vj/clip_deck/out"),
        ("scene_prog", "/project1/old_brik_vj/scenes/out"),
        ("layer_mix", "/project1/old_brik_vj/mixer/out"),
        ("fx_prog", "/project1/old_brik_vj/fx/out"),
        ("router_prog", "/project1/brikvj_router/out"),
        ("broadcast_prog", "/project1/brikvj_broadcast/preview"),
    )
    for name, path in sources:
        src = op(path)
        if src is None:
            continue
        n = child(grid, name, nullTOP)
        wire(n, 0, src)
        try:
            n.viewer = True
            set_label(n, path.split("/")[-1])
        except Exception:
            pass

    stacker = vj.op("preview_grid")
    if stacker is not None:
        wire(child(grid, "stacker", nullTOP), 0, stacker)
        log("TOPs_stacker_GLSL wired to previews/stacker")

    mapper = p.op("mapping/kantanMapper")
    if mapper is not None:
        m = child(grid, "mapper_out", nullTOP)
        wire(m, 0, mapper)
        try:
            m.viewer = True
            set_label(m, "kantanMapper (mapping)")
        except Exception:
            pass

    log("Viewers at /project1/brikvj_ui/previews/* — enable Perform + F1 for program")


run()
