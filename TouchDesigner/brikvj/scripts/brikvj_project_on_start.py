# Install /project1/brikvj_on_start Execute DAT (timeline + optional live MOTU).
# Set LIVE_RACK_ON_START True for perform nights (M4 3–4); False keeps Brioch file test path.

LIVE_RACK_ON_START = False


def log(msg):
    print("[BRIKVJ onStart install]", msg)


def install():
    p = op("/project1")
    ex = p.op("brikvj_on_start")
    if ex is None:
        ex = p.create(executeDAT, "brikvj_on_start")
    try:
        ex.par.start = True
        ex.par.create = True
    except Exception:
        pass
    ex.text = """
LIVE_RACK = %s

def _motu():
    try:
        import audio
    except ImportError:
        return None
    for fn in (getattr(audio, 'getInputDevices', None), getattr(audio, 'getDevices', None)):
        if not callable(fn):
            continue
        try:
            devs = list(fn())
            break
        except Exception:
            devs = []
    else:
        return None
    for i, d in enumerate(devs):
        if 'MOTU' in str(d).upper() or 'M4' in str(d).upper():
            return i
    return None

def onStart():
    t = op('/local/time')
    if t:
        t.par.play = 1
    if not LIVE_RACK:
        return
    sw = op('/project1/swi453tch4')
    ad = op('/project1/audiodevin1')
    if not sw or not ad:
        return
    idx = _motu()
    if idx is not None:
        for par in ('device', 'driverdevice'):
            if hasattr(ad.par, par):
                try:
                    ad.par[par] = idx
                    break
                except Exception:
                    pass
    for par in ('channel', 'channels', 'activespec'):
        if hasattr(ad.par, par):
            try:
                ad.par[par] = '3-4'
                break
            except Exception:
                pass
    sw.par.index = 0
""" % ("True" if LIVE_RACK_ON_START else "False")
    log("Execute DAT " + ex.path + " (LIVE_RACK_ON_START=%s)" % LIVE_RACK_ON_START)


install()
