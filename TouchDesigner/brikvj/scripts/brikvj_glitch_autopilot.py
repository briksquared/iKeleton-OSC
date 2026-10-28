# Automatic glitch/VJ mode — beat-driven strobes + timed scene changes.
# Run once in BRIKVJ.toe after brikvj_suite_build.py.

KICK_THRESH = 0.55
SCENE_EVERY_FRAMES = 180  # overridden at runtime if TDAbleton BPM available
GLITCH_SCENE_INDICES = (0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11)


def log(msg):
    print("[BRIKVJ autopilot]", msg)


def install_execute():
    p = op("/project1")
    ex = p.op("brikvj_autopilot")
    if ex is None:
        ex = p.create(executeDAT, "brikvj_autopilot")
    ex.par.active = True
    try:
        ex.par.framestart = True
    except Exception:
        pass
    ex.text = """
import random
KICK_THRESH = %s
SCENE_EVERY_FRAMES = %s
GLITCH_SCENE_INDICES = %s
_last_kick = 0.0

def _audio():
    for path in ('/project1/analyseAudio/out1', '/project1/null7'):
        o = op(path)
        if o:
            return o
    return None

def _kick(a):
    if not a:
        return 0.0
    for n in ('kick', 'Kick', 'low', 'rms'):
        try:
            if n in a.chans():
                return float(a[n][0])
        except Exception:
            pass
    try:
        return float(a[0][0])
    except Exception:
        return 0.0

def _pulse():
    fx = op('/project1/old_brik_vj/fx')
    if not fx:
        return
    for name in ('ok_strobe', 'ok_glitch', 'strobe_fx', 'tdx_crt', 'stutter', 'mosh'):
        o = fx.op(name)
        if not o:
            continue
        for pname in ('opacity', 'mix', 'intensity', 'amount', 'level'):
            if hasattr(o.par, pname):
                try:
                    o.par[pname] = 1.0
                except Exception:
                    pass
                break

def _scene_interval():
    try:
        tda = op('/project1/old_brik_vj/live/tdAbleton')
        if tda and 'bpm' in tda.chans():
            bpm = float(tda['bpm'][0])
            if bpm > 20:
                return max(45, int(60.0 * me.time.rate / (bpm / 4.0)))
    except Exception:
        pass
    return SCENE_EVERY_FRAMES

def onFrameStart(frame):
    global _last_kick
    sw = op('/project1/old_brik_vj/scenes/scene_switch')
    if not sw:
        return
    a = _audio()
    k = _kick(a)
    if k > KICK_THRESH and _last_kick <= KICK_THRESH:
        _pulse()
        try:
            sw.par.index = random.choice(GLITCH_SCENE_INDICES)
        except Exception:
            pass
    _last_kick = k
    every = _scene_interval()
    if frame > 0 and frame % every == 0:
        try:
            sw.par.index = random.choice(GLITCH_SCENE_INDICES)
        except Exception:
            pass
""" % (KICK_THRESH, SCENE_EVERY_FRAMES, GLITCH_SCENE_INDICES)
    log("Execute DAT at " + ex.path + " (frameStart enabled)")


def run():
    install_execute()
    log("Autopilot ON — kick flashes + scene rotation")
    log("Disable: op('brikvj_autopilot').par.active = False")


run()
