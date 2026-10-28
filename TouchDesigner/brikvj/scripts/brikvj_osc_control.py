# OSC control plane (Resolume-style remote) → old_brik_vj Custom Parameters.

OSC_PORT = 7000
ADDRESS_MAP = {
    "/brikvj/scene": "Scene",
    "/brikvj/clip": "Clip",
    "/brikvj/router": "Router",
    "/brikvj/fxbypass": "FxBypass",
    "/brikvj/autopilot": "Autopilot",
}


def log(msg):
    print("[BRIKVJ OSC]", msg)


def proj():
    return op("/project1")


def install():
    p = proj()
    vj = p.op("old_brik_vj")
    if vj is None:
        log("Run suite + tda_mapper_bridge first")
        return

    osc = p.op("brikvj_osc")
    if osc is None:
        osc = p.create(oscinDAT, "brikvj_osc")
    try:
        osc.par.port = OSC_PORT
        osc.par.active = False
        set_label(osc, "Enable when stack is built (port %d)" % OSC_PORT)
    except Exception as ex:
        log("oscin: " + str(ex))

    cb = p.op("brikvj_osc_callbacks")
    if cb is None:
        cb = p.create(textDAT, "brikvj_osc_callbacks")
    lines = [
        "MAP = %s" % repr(ADDRESS_MAP),
        "VJ = '/project1/old_brik_vj'",
        "",
        "def onReceiveOSC(dat, rowIndex, message, bytes, time, address, args, peer):",
        "    if address not in MAP:",
        "        return",
        "    parname = MAP[address]",
        "    vj = op(VJ)",
        "    if not vj or not hasattr(vj.par, parname):",
        "        return",
        "    if not args:",
        "        return",
        "    try:",
        "        setattr(vj.par, parname, int(float(args[0])))",
        "    except Exception:",
        "        pass",
    ]
    cb.text = "\n".join(lines)

    try:
        osc.par.callbacks = cb.path
    except Exception:
        log("Set brikvj_osc Callbacks DAT → brikvj_osc_callbacks manually")

    help_dat = p.op("brikvj_osc_help")
    if help_dat is None:
        help_dat = p.create(textDAT, "brikvj_osc_help")
    help_dat.text = (
        "OSC port %d\n"
        "/brikvj/scene 0-11\n"
        "/brikvj/clip 0-7\n"
        "/brikvj/router 0|1\n"
        "/brikvj/fxbypass 0|1\n"
        "/brikvj/autopilot 0|1\n"
        "Same targets as TDA_Mapper Custom Par on old_brik_vj."
    ) % OSC_PORT
    log("OSC in on port %d — see brikvj_osc_help" % OSC_PORT)


install()
