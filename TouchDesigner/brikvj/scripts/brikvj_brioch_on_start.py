# Run once from Textport after opening BRIKVJ.toe (or paste into a Execute DAT onStart).
# Picks MOTU M4 inputs 3-4 for live rack audio; leaves file test on swi453tch4 index 2.

EURORACK_CH = "3-4"
HINTS = ("MOTU", "M4", "M Series", "M-Series")


def log(msg):
    print("[BRIKVJ onStart]", msg)


def motu_device_index():
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


def configure_live():
    sw = op("/project1/swi453tch4")
    ad = op("/project1/audiodevin1")
    if sw is None or ad is None:
        log("Missing swi453tch4 or audiodevin1")
        return
    idx, name = motu_device_index()
    if idx is not None:
        for par in ("device", "driverdevice"):
            if hasattr(ad.par, par):
                try:
                    ad.par[par] = idx
                    break
                except Exception:
                    pass
        log("Live input: " + str(name))
    for par in ("channel", "channels", "activespec"):
        if hasattr(ad.par, par):
            try:
                ad.par[par] = EURORACK_CH
                log("Channels " + EURORACK_CH)
                break
            except Exception:
                pass
    sw.par.index = 0
    log("swi453tch4 -> 0 (live). File test: set index 2.")


def ensure_timeline():
    t = op("/local/time")
    if t:
        t.par.play = 1
        log("Timeline play on")


ensure_timeline()
# Uncomment for rack/Live instead of drum file test:
# configure_live()
