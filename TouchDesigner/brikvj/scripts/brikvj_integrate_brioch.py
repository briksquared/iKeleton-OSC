# Wire Brioch perform output + kantanMapper with old_brik_vj Resolume-style stack.
# Run after old_brik_vj_build.py inside BRIKVJ.toe.


def log(msg):
    print("[BRIKVJ integrate]", msg)


def proj():
    return op("/project1")


def wire(top, idx, src):
    if src is None:
        return
    try:
        top.inputConnectors[idx].connect(src)
    except Exception as ex:
        log("wire fail: " + str(ex))


def find_brioch_out():
    for path in (
        "out1",
        "null7",
        "constant1",
        "comp1",
        "select1",
    ):
        o = proj().op(path)
        if o is None:
            continue
        if hasattr(o, "outputConnectors") and len(o.outputConnectors):
            log("Brioch candidate out: " + o.path)
            return o
    m = proj().op("mapping/kantanMapper")
    if m is not None:
        log("Using kantanMapper as Brioch stage")
        return m
    return None


def build_router():
    p = proj()
    vj = p.op("old_brik_vj")
    if vj is None:
        log("Run old_brik_vj_build.py first")
        return

    router = p.op("brikvj_router")
    if router is None:
        router = p.create(baseCOMP, "brikvj_router")
    router.viewer = True
    router.tags.add("brikvj")

    brioch = find_brioch_out()
    harvest_master = None
    if vj:
        for path in ("fx/out", "fx/master", "mixer/out"):
            harvest_master = vj.op(path)
            if harvest_master is not None:
                break

    sw = router.op("source_switch")
    if sw is None:
        sw = router.create(switchTOP, "source_switch")
    try:
        sw.par.index = 0
    except Exception:
        pass

    if brioch is not None:
        wire(sw, 0, brioch)
    if harvest_master is not None:
        wire(sw, 1, harvest_master)

    n = router.op("out")
    if n is None:
        n = router.create(nullTOP, "out")
    wire(n, 0, sw)

    km = p.op("mapping/kantanMapper")
    if km is not None and hasattr(km, "inputConnectors") and len(km.inputConnectors):
        try:
            wire(km, 0, n)
            log("Fed brikvj_router -> kantanMapper (projection mapping stage)")
            n = km
        except Exception as ex:
            log("kantanMapper wire: " + str(ex))

    perform = p.op("perform_out")
    if perform is None:
        perform = p.create(outTOP, "perform_out")
    wire(perform, 0, n)
    set_label(perform, "BRIKVJ main (0=Brioch scenes, 1=harvest FX stack)")

    if km is not None:
        log("Mapping UI: /project1/mapping/kantanMapper")
    log("Set brikvj_router/source_switch index: 0 nightly Brioch, 1 layered harvest")


build_router()
