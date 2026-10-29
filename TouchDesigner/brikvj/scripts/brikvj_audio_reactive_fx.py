# Bind Brioch + harvest audio CHOPs to FX/scene parameters (Resolume-style audio reactivity).

BINDINGS = (
    ("low", "/project1/old_brik_vj/fx/bloom", ("mix", "opacity")),
    ("mid", "/project1/old_brik_vj/fx/kaleid", ("mix",)),
    ("high", "/project1/old_brik_vj/fx/tdx_mod", ("amount", "mix")),
    ("rms", "/project1/old_brik_vj/scenes/scene_switch", ("index",)),
)


def log(msg):
    print("[BRIKVJ audio FX bind]", msg)


def run():
    p = op("/project1")
    ex = p.op("brikvj_audio_fx_bind")
    if ex is None:
        ex = p.create(executeDAT, "brikvj_audio_fx_bind")
    try:
        ex.par.active = True
        ex.par.framestart = True
        set_label(ex, "Audio-reactive FX (disable for manual mix)")
    except Exception:
        pass

    ex.text = r"""
def _ch(name):
    a = op('/project1/old_brik_vj/generative/audio_drive')
    if not a:
        a = op('/project1/analyseAudio/out1')
    if not a or a.numChans < 1:
        return 0.0
    for n in (name, name.capitalize(), 'chan1', 'rms'):
        try:
            if n in a.chans():
                return float(a[n][0])
        except Exception:
            pass
    try:
        return float(a[0][0])
    except Exception:
        return 0.0

def onFrameStart(frame):
    if frame % 2 != 0:
        return
    bloom = op('/project1/old_brik_vj/fx/bloom')
    if bloom and hasattr(bloom.par, 'mix'):
        try:
            bloom.par.mix = min(1.0, 0.15 + _ch('low') * 0.85)
        except Exception:
            pass
    kaleid = op('/project1/old_brik_vj/fx/kaleid')
    if kaleid and hasattr(kaleid.par, 'mix'):
        try:
            kaleid.par.mix = min(1.0, _ch('mid') * 1.2)
        except Exception:
            pass
    mod = op('/project1/old_brik_vj/fx/tdx_mod')
    if mod:
        for pn in ('amount', 'mix'):
            if hasattr(mod.par, pn):
                try:
                    setattr(mod.par, pn, min(1.0, _ch('high') * 1.1))
                    break
                except Exception:
                    pass
"""

    log("Audio → bloom/kaleid/tdx_mod at " + ex.path)


run()
