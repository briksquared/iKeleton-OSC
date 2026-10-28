# Old Brik V J — MOTU M4 rack input (run after old_brik_vj_build.py)

EURORACK = "3-4"
DESK = "1-2"
USE_RACK = True
TARGET = EURORACK if USE_RACK else DESK
HINTS = ("MOTU", "M4", "M Series", "M-Series")


def log(msg):
    print("[Old Brik V J audio]", msg)


def list_inputs():
    try:
        import audio
    except ImportError:
        log("Cannot list devices — pick MOTU M4 on rack_in manually.")
        return []
    for name in ("getInputDevices", "getDevices"):
        fn = getattr(audio, name, None)
        if callable(fn):
            try:
                devs = list(fn())
                for i, d in enumerate(devs):
                    log("  [{}] {}".format(i, d))
                return devs
            except Exception:
                pass
    return []


def motu_index(devs):
    for i, d in enumerate(devs):
        u = d.upper()
        if any(h.upper() in u for h in HINTS):
            return i, d
    return None, None


def set_par(chop, names, val):
    for n in names:
        if hasattr(chop.par, n):
            try:
                chop.par[n] = val
                return n
            except Exception:
                pass
    return None


def configure(chop):
    devs = list_inputs()
    idx, name = motu_index(devs)
    if idx is not None:
        set_par(chop, ("device", "driverdevice"), idx)
        log("device → " + name)
    set_par(chop, ("active", "activespec", "channel", "channels"), TARGET)
    log("{} → channels {}".format(chop.path, TARGET))


def run():
    log("Target channels: " + TARGET)
    root = op("/")
    targets = root.findChildren(type=audiodeviceinCHOP, maxDepth=14)
    if not targets:
        log("No Audio Device In — check old_brik_vj/rack_audio/rack_in")
    for ch in targets:
        if "rack" in ch.path.lower() or ch.name == "rack_in":
            configure(ch)
    comp = op("old_brik_vj/rack_audio/analysis")
    if comp:
        for ch in comp.findChildren(type=audiodeviceinCHOP, maxDepth=6):
            configure(ch)
    log("Done — play rack into M4 3–4 and watch rack_in.")


run()
