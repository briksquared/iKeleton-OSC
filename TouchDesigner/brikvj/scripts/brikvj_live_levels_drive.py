# Drive harvest FX intensity from TDA_Level CHOPs (Live → tdAbleton → live_levels/*).

LEVEL_TARGETS = (
    ("rack_sub", (("fx/ok_glitch", "amount"), ("fx/strobe_fx", "mix"))),
    ("drums_idm", (("fx/stutter", "mix"), ("fx/mosh", "Keyframe"))),
    ("cyclop", (("fx/tdx_mod", "amount"), ("fx/ok_disp", "amount"))),
    ("factory", (("fx/bloom", "mix"), ("fx/kaleid", "mix"))),
)


def log(msg):
    print("[BRIKVJ live levels]", msg)


def run():
    vj = op("/project1/old_brik_vj")
    if vj is None:
        log("Run suite build first")
        return

    levels = vj.op("live_levels")
    if levels is None:
        log("Run brikvj_ableton_link.py first")
        return

    ex = op("/project1/brikvj_level_drive")
    if ex is None:
        ex = op("/project1").create(executeDAT, "brikvj_level_drive")
    try:
        ex.par.framestart = True
        ex.par.active = False
        set_label(ex, "Enable after TDA_Level CHOPs wired to live_levels/*")
    except Exception:
        pass

    lines = [
        "# Auto-drive FX from Live TDA_Level (wire CHOP exports into live_levels/*)",
        "TARGETS = %s",
        "",
        "def _val(chop, default=0.0):",
        "    if not chop or not chop.numChans:",
        "        return default",
        "    try:",
        "        return float(chop[0][0])",
        "    except Exception:",
        "        return default",
        "",
        "def onFrameStart(frame):",
        "    base = op('/project1/old_brik_vj/live_levels')",
        "    if not base:",
        "        return",
        "    for level_name, pairs in TARGETS:",
        "        src = base.op(level_name)",
        "        v = _val(src)",
        "        if v <= 0.001:",
        "            continue",
        "        for rel, parname in pairs:",
        "            o = op('/project1/old_brik_vj/' + rel)",
        "            if not o or not hasattr(o.par, parname):",
        "                continue",
        "            try:",
        "                p = getattr(o.par, parname)",
        "                p.val = min(1.0, max(0.0, v))",
        "            except Exception:",
        "                pass",
    ] % repr(list(LEVEL_TARGETS))

    ex.text = "\n".join(lines)
    log("Level drive at " + ex.path + " — map TDA_Level CHOPs into live_levels/* in TD")


run()
