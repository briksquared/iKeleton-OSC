# Bind harvest FX parameters to audio_drive (rack + Brioch analyseAudio).

DRIVE = "op('old_brik_vj/audio_drive')"
BINDINGS = (
    ("fx/ok_glitch", "amount", "0.15 + %s['rms'] * 0.85" % DRIVE),
    ("fx/ok_disp", "amount", "0.05 + %s['rms'] * 0.4" % DRIVE),
    ("fx/dist", "displace", "0.02 + %s['rms'] * 0.25" % DRIVE),
    ("fx/bloom", "mix", "0.1 + %s['rms'] * 0.5" % DRIVE),
    ("fx/tdx_crt", "mix", "0.2 + %s['rms'] * 0.6" % DRIVE),
    ("fx/strobe_fx", "mix", "0.0 + %s['kick'] * 0.9" % DRIVE),
    ("fx/mosh", "amount", "0.1 + %s['rms'] * 0.35" % DRIVE),
)


def log(msg):
    print("[BRIKVJ fx bind]", msg)


def run():
    vj = op("/project1/old_brik_vj")
    if vj is None:
        log("Run suite build first")
        return

    drive = vj.op("audio_drive")
    if drive is None:
        log("Run brikvj_audio_bridge.py first")
        return

    bound = 0
    for rel, parname, expr in BINDINGS:
        o = vj.op(rel)
        if o is None or not hasattr(o.par, parname):
            continue
        p = getattr(o.par, parname)
        try:
            if not drive or not drive.numChans:
                continue
            ch = "rms" if "rms" in expr else "kick"
            if ch not in [c.name for c in drive.chans()]:
                continue
            p.expr = expr
            bound += 1
        except Exception as ex:
            log(rel + "." + parname + ": " + str(ex))

    log("Audio-expressions on %d FX parms (kick/rms from audio_drive)" % bound)
    log("If kick missing, strobe uses rms — wire Brioch analyseAudio in audio_bridge")


run()
