# Perform keyboard layer (Brioch 1–6 unchanged). Run once in BRIKVJ.toe after suite + integrate.

KEY_HELP = """
BRIKVJ keys (click TD window first):
  1–6     Brioch scenes (existing)
  7–9     harvest scene_switch indices 6–8
  0       harvest scene index 9
  [ / ]   scene prev / next (harvest scenes/scene_switch)
  - / =   clip_deck clip_switch prev / next
  \\       cycle brikvj_router (0 Brioch / 1 show / 2 lab)
  `       toggle old_brik_vj/fx/fx_switch (FX on/off)
  F2      toggle brikvj_autopilot
  F3      toggle brikvj_broadcast/stream_record
  F4      toggle brikvj_broadcast/ingress_switch (0 main / 1 Spout in)
  F1      enable perform (project enableperform + main window target)
  o       toggle old_brik_vj/overlay_gen/overlay_switch (generative overlay)
"""


def log(msg):
    print("[BRIKVJ perform keys]", msg)


def proj():
    return op("/project1")


def install():
    p = proj()
    if p.op("old_brik_vj/scenes/scene_switch") is None:
        log("Skip keyboard layer — run suite build first (no scene_switch)")
        return
    kb = p.op("brikvj_keys")
    if kb is None:
        kb = p.create(keyboardinCHOP, "brikvj_keys")
    try:
        kb.par.active = 1
    except Exception:
        pass

    script = p.op("brikvj_key_callbacks")
    if script is None:
        script = p.create(textDAT, "brikvj_key_callbacks")
    script.text = r"""
def _sw(path):
    return op(path)

def _toggle_switch(path, a=0, b=1):
    sw = _sw(path)
    if not sw:
        return
    try:
        i = int(sw.par.index)
        sw.par.index = b if i == a else a
    except Exception:
        pass

def _bump(path, delta, lo=0, hi=31):
    sw = _sw(path)
    if not sw:
        return
    try:
        i = int(sw.par.index) + delta
        if i < lo:
            i = hi
        if i > hi:
            i = lo
        sw.par.index = i
    except Exception:
        pass

def _set_index(path, idx):
    sw = _sw(path)
    if not sw:
        return
    try:
        sw.par.index = idx
    except Exception:
        pass

def _toggle_active(path):
    o = _sw(path)
    if not o:
        return
    try:
        o.par.active = not bool(o.par.active)
    except Exception:
        pass

def _toggle_record():
    rec = op('/project1/brikvj_broadcast/stream_record')
    if not rec:
        return
    try:
        rec.par.record = 1 - int(rec.par.record)
    except Exception:
        pass

def onOffToOn(channel, sampleIndex, val, prev):
    n = channel.name
    scene = '/project1/old_brik_vj/scenes/scene_switch'
    clips = '/project1/old_brik_vj/clip_deck/clip_switch'
    if n in ('7', '8', '9', '0'):
        _set_index(scene, {'7': 6, '8': 7, '9': 8, '0': 9}[n])
    elif n == 'bracketleft':
        _bump(scene, -1, 0, 31)
    elif n == 'bracketright':
        _bump(scene, 1, 0, 31)
    elif n == 'minus':
        _bump(clips, -1, 0, 7)
    elif n == 'equal':
        _bump(clips, 1, 0, 7)
    elif n == 'backslash':
        sw = _sw('/project1/brikvj_router/source_switch')
        if sw:
            try:
                i = int(sw.par.index)
                sw.par.index = (i + 1) % 3
            except Exception:
                pass
    elif n == 'quote' or n == 'grave':
        _toggle_switch('/project1/old_brik_vj/fx/fx_switch', 0, 1)
    elif n == 'f2':
        _toggle_active('/project1/brikvj_autopilot')
    elif n == 'f3':
        _toggle_record()
    elif n == 'f4':
        _toggle_switch('/project1/brikvj_broadcast/ingress_switch', 0, 1)
    elif n == 'f1':
        try:
            op('/project1').par.enableperform = 1
        except Exception:
            pass
    elif n == 'o':
        _toggle_switch('/project1/old_brik_vj/overlay_gen/overlay_switch', 0, 1)
    return
"""

    ex = p.op("brikvj_key_execute")
    if ex is None:
        ex = p.create(chopexecuteDAT, "brikvj_key_execute")
    ex.par.chop = kb.path
    try:
        ex.par.offtoon = "op('brikvj_key_callbacks').module.onOffToOn(channel, sampleIndex, val, prev)"
    except Exception:
        pass
    try:
        ex.par.valuechange = False
    except Exception:
        pass

    help_dat = p.op("brikvj_key_help")
    if help_dat is None:
        help_dat = p.create(textDAT, "brikvj_key_help")
    help_dat.text = KEY_HELP.strip()
    help_dat.viewer = True
    try:
        set_label(help_dat, "Perform keyboard map")
    except Exception:
        pass

    log("Keyboard CHOP at " + kb.path)
    log("Help: op('brikvj_key_help').text")


install()
