# Patchworks desk → Ableton Live → TDAbleton in TD (run after suite build, Live set open).

BEAT_DATAMOSH_PATHS = (
    "old_brik_vj/fx/mosh",
    "old_brik_vj/fx/tdx_crt",
    "old_brik_vj/fx/strobe_fx",
    "glitch_post/datamosh",
)


def log(msg):
    print("[BRIKVJ Ableton]", msg)


def proj():
    return op("/project1")


def ensure_tdableton(vj):
    live = vj.op("live")
    if live is None:
        live = vj.create(baseCOMP, "live")
    tda = live.op("tdAbleton")
    if tda is not None:
        return tda
    for typename in ("tdAbletonCOMP", "tdabletonCOMP", "abletonCOMP"):
        try:
            tda = live.create(typename, "tdAbleton")
            log("created " + typename + " at " + tda.path)
            return tda
        except Exception:
            continue
    log("Add TDAbleton COMP manually (User Library palette)")
    return None


def find_datamosh():
    p = proj()
    for path in BEAT_DATAMOSH_PATHS:
        o = p.op(path)
        if o is not None:
            return o
    vj = p.op("old_brik_vj/fx")
    if vj:
        for c in vj.children:
            if "mosh" in c.name.lower() or "datamosh" in c.name.lower():
                return c
    return None


def beat_execute_body(dm_path):
    return (
        "# CHOP Execute — wire to tdAbleton beat/onBeat (Off to On)\n"
        "def onOffToOn(channel, sampleIndex, val, prev):\n"
        "    dm = op('%s')\n"
        "    if dm is None:\n"
        "        return\n"
        "    for par in ('Keyframe', 'keyframe', 'reset'):\n"
        "        if hasattr(dm.par, par):\n"
        "            try:\n"
        "                getattr(dm.par, par).pulse()\n"
        "            except Exception:\n"
        "                pass\n"
        "            break\n"
        "    return\n"
    ) % dm_path.replace("'", "\\'")


def build_level_router(vj, tda):
    """Named nulls for TDA_Level tracks (DrumComputer, Cyclop, Factory, Rack Sub)."""
    router = vj.op("live_levels")
    if router is None:
        router = vj.create(baseCOMP, "live_levels")
    try:
        set_label(router, "TDA_Level CHOPs — map in Ableton per PATCHWORKS_INTEGRATION.md")
    except Exception:
        pass
    names = ("rack_sub", "buddy_sub", "drums_idm", "cyclop", "factory", "master")
    for n in names:
        slot = router.op(n)
        if slot is None:
            slot = router.create(nullCHOP, n)
        try:
            set_label(slot, "Connect from tdAbleton track level: " + n)
        except Exception:
            pass
    log("live_levels/* — bind TDA_Level sends from Live composition tracks")
    return router


def run():
    p = proj()
    vj = p.op("old_brik_vj")
    if vj is None:
        log("Run brikvj_suite_build.py first")
        return

    tda = ensure_tdableton(vj)
    build_level_router(vj, tda)

    dm = find_datamosh()
    dm_path = dm.path if dm else "old_brik_vj/fx/mosh"

    beat_dat = vj.op("beat_glitch_callbacks")
    if beat_dat is None:
        beat_dat = vj.create(textDAT, "beat_glitch_callbacks")
    beat_dat.text = beat_execute_body(dm_path)
    try:
        set_label(beat_dat, "Paste into CHOP Execute on tdAbleton beat channel")
    except Exception:
        pass

    chop_exec = vj.op("beat_chop_execute")
    if chop_exec is not None:
        try:
            chop_exec.destroy()
        except Exception:
            pass
    if tda is not None and op("/project1/old_brik_vj/live/tdAbleton") is not None:
        chop_exec = vj.create(chopexecuteDAT, "beat_chop_execute")
        try:
            chop_exec.par.active = False
            chop_exec.par.chop = "live/tdAbleton/out1"
            chop_exec.par.offtoon = "op('beat_glitch_callbacks').module.onOffToOn(channel, sampleIndex, val, prev)"
            set_label(chop_exec, "Enable after TDAbleton connected to Live")
        except Exception:
            pass
    log("Open Live → BRIKVJ_Composition_01.als → TDA_Master on Master; click Connect on tdAbleton")
    log("Beat pulse target: " + dm_path)


run()
