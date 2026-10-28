# Apply Patchworks MOTU routing in TouchDesigner (run in BRIKVJ.toe Textport).

RACK = "3-4"
BUDDY = "1-2"
USE_RACK = True
TARGET = RACK if USE_RACK else BUDDY
HINTS = ("MOTU", "M4", "M Series", "M-Series")


def log(msg):
    print("[Patchworks audio]", msg)


def motu_index():
    try:
        import audio
    except ImportError:
        return None, None
    devs = []
    for name in ("getInputDevices", "getDevices"):
        fn = getattr(audio, name, None)
        if callable(fn):
            try:
                devs = list(fn())
                break
            except Exception:
                pass
    for i, d in enumerate(devs):
        u = str(d).upper()
        if any(h.upper() in u for h in HINTS):
            return i, d
    return None, None


def configure(chop):
    idx, name = motu_index()
    if idx is not None:
        for par in ("device", "driverdevice"):
            if hasattr(chop.par, par):
                try:
                    chop.par[par] = idx
                    log("device → " + str(name))
                    break
                except Exception:
                    pass
    for par in ("channel", "channels", "activespec"):
        if hasattr(chop.par, par):
            try:
                chop.par[par] = TARGET
                log(chop.path + " → channels " + TARGET)
                break
            except Exception:
                pass


def run():
    log("Patchworks default: Knead/rack on M4 " + RACK + " (set USE_RACK=False for Buddy 1-2)")
    root = op("/")
    for ch in root.findChildren(type=audiodeviceinCHOP, maxDepth=16):
        if any(x in ch.path.lower() for x in ("rack", "audiodevin", "buddy")):
            configure(ch)
    vj = op("/project1/old_brik_vj")
    if vj:
        ri = vj.op("audio/rack_in")
        if ri:
            configure(ri)
    ad = op("/project1/audiodevin1")
    if ad and USE_RACK:
        configure(ad)
    log("Done — match Live Ext In to same M4 pair (see PATCHWORKS_INTEGRATION.md)")


run()
