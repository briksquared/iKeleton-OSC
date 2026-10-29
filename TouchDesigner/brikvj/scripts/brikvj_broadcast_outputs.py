# Resolume/MadMapper-style stream + multi-projector fan-out (run in BRIKVJ.toe after integrate).
# Creates /project1/brikvj_broadcast — wire monitors in Perform → Window / Assign.

SPOUT_NAME = "BRIKVJ"
NDI_NAME = "BRIKVJ-Main"
PROJECTOR_COUNT = 2
ENABLE_SPOUT_IN = True


def log(msg):
    print("[BRIKVJ broadcast]", msg)


def proj():
    return op("/project1")


def wire(top, idx, src):
    if src is None:
        return
    try:
        top.inputConnectors[idx].connect(src)
    except Exception as ex:
        log("wire: " + str(ex))


def child(parent, name, typ):
    e = parent.op(name)
    if e:
        return e
    return parent.create(typ, name)


def create_out_top(parent, name, label):
    o = child(parent, name, outTOP)
    try:
        set_label(o, label)
    except Exception:
        pass
    return o


def try_create(parent, names):
    for n in names:
        try:
            return parent.create(n, n.split("/")[-1])
        except Exception:
            continue
    return None


def find_master_source():
    p = proj()
    for path in (
        "mapping/kantanMapper",
        "brikvj_router/out",
        "perform_out",
        "old_brik_vj/fx/out",
    ):
        o = p.op(path)
        if o is None:
            continue
        if hasattr(o, "outputConnectors") and len(o.outputConnectors):
            log("master source: " + o.path)
            return o
    return None


def build():
    p = proj()
    src = find_master_source()
    if src is None:
        log("No video source — run suite + integrate first")
        return

    bc = child(p, "brikvj_broadcast", baseCOMP)
    bc.viewer = True
    bc.tags.add("brikvj")
    try:
        set_label(bc, "NDI/Spout/projectors (Resolume stream parity)")
    except Exception:
        pass

    master = child(bc, "master_in", nullTOP)
    wire(master, 0, src)

    # Ingress (MadMapper Spout/Syphon-style)
    ingress = None
    if ENABLE_SPOUT_IN:
        spout_in = try_create(
            bc,
            ("spoutinTOP", "spoutInTOP", "syphoninTOP"),
        )
        if spout_in is not None:
            try:
                set_label(spout_in, "External app → TD (Spout/Syphon)")
            except Exception:
                pass
            ingress = spout_in
            log("Spout/Syphon In ready — set sender name in UI")

    if ingress is not None:
        sw = child(bc, "ingress_switch", switchTOP)
        wire(sw, 0, master)
        wire(sw, 1, ingress)
        try:
            sw.par.index = 0
        except Exception:
            pass
        tap = sw
    else:
        tap = master

    fan = child(bc, "fan_out", nullTOP)
    wire(fan, 0, tap)

    spout_out = try_create(bc, ("spoutoutTOP", "spoutOutTOP"))
    if spout_out is not None:
        wire(spout_out, 0, fan)
        for par in ("sendername", "name", "spoutname"):
            if hasattr(spout_out.par, par):
                try:
                    spout_out.par[par] = SPOUT_NAME
                    break
                except Exception:
                    pass
        log("Spout Out → " + SPOUT_NAME + " (OBS / other apps)")

    ndi_out = try_create(bc, ("ndioutTOP", "ndiOutTOP"))
    if ndi_out is not None:
        wire(ndi_out, 0, fan)
        for par in ("name", "ndiname", "label"):
            if hasattr(ndi_out.par, par):
                try:
                    ndi_out.par[par] = NDI_NAME
                    break
                except Exception:
                    pass
        log("NDI Out → " + NDI_NAME)

    for i in range(PROJECTOR_COUNT):
        out = create_out_top(bc, "projector_%d" % (i + 1), "Projector %d — assign in Window COMP" % (i + 1))
        wire(out, 0, fan)

    rec = child(bc, "stream_record", moviefileoutTOP)
    wire(rec, 0, fan)
    try:
        rec.par.file = "C:/Users/briks/Documents/TouchDesigner/BRIKVJ/recordings/stream_$F.mov"
        rec.par.record = 0
        set_label(rec, "Toggle record for stream archive")
    except Exception:
        pass

    bus_out = child(bc, "out", nullTOP)
    wire(bus_out, 0, fan)
    preview = child(bc, "preview", nullTOP)
    wire(preview, 0, fan)
    try:
        set_label(preview, "Monitor / second window")
    except Exception:
        pass

    perform = p.op("perform_out")
    if perform is not None:
        wire(perform, 0, tap)
        log("perform_out ← broadcast tap (mapper + optional Spout in)")

    log(
        "Done — assign projector_1/2 in Window; enable NDI/Spout; ingress_switch=1 for external feed"
    )


build()
