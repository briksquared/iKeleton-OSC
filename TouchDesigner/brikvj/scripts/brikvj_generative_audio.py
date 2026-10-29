# Audio-driven generative drivers: Brioch analyseAudio + harvest bands → scene/FX motion.

def log(msg):
    print("[BRIKVJ generative]", msg)


def proj():
    return op("/project1")


def child(parent, name, typ):
    e = parent.op(name)
    if e:
        return e
    return parent.create(typ, name)


def wire_chop(dst, idx, src):
    if not dst or not src:
        return
    try:
        dst.inputConnectors[idx].connect(src)
    except Exception as ex:
        log("chop wire: " + str(ex))


def run():
    p = proj()
    vj = p.op("old_brik_vj")
    if vj is None:
        log("Run brikvj_resolume_stack first")
        return

    gen = child(vj, "generative", baseCOMP)
    set_label(gen, "Audio → generative material (kick/bands)")

    drive = child(gen, "audio_drive", nullCHOP)
    set_label(drive, "Merged analysis for expressions")

    brioch = None
    for path in ("/project1/analyseAudio/out1", "/project1/analyseAudio"):
        brioch = op(path)
        if brioch:
            break
    rack = None
    for rel in ("audio/ok_analysis/out1", "audio/analysis/out1", "audio/bands/out1"):
        rack = vj.op(rel)
        if rack:
            break
    if brioch:
        wire_chop(drive, 0, brioch)
    if rack:
        wire_chop(drive, 1 if brioch else 0, rack)

    lfo = child(gen, "motion_lfo", lfoCHOP)
    try:
        lfo.par.rate = 0.25
        lfo.par.amp = 0.5
    except Exception:
        pass

    ex = p.op("brikvj_generative_execute")
    if ex is None:
        ex = p.create(executeDAT, "brikvj_generative_execute")
    try:
        ex.par.active = True
        ex.par.framestart = True
        set_label(ex, "Generative: bass → scene drift (disable if manual perform)")
    except Exception:
        pass
    ex.text = r"""
def _low():
    a = op('/project1/old_brik_vj/generative/audio_drive')
    if not a or a.numChans < 1:
        return 0.0
    for n in ('low', 'Low', 'rms', 'chan1'):
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
    if frame % 90 != 0:
        return
    sw = op('/project1/old_brik_vj/scenes/scene_switch')
    if not sw:
        return
    low = _low()
    if low < 0.08:
        return
    try:
        i = int(sw.par.index)
        n = len(sw.inputConnectors) if sw.inputConnectors else 12
        sw.par.index = (i + 1) % max(1, n)
    except Exception:
        pass
"""

    import os

    path = os.path.join(
        r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ", "parts", "glitch_fluid", "flow_field.tox"
    )
    if os.path.isfile(path):
        try:
            slot = child(gen, "flow_reactive", baseCOMP)
            t = td_load_tox(slot, path, "flow_audio")
            if t is not None:
                log("Loaded flow_field for generative layer")
        except Exception as ex:
            log("flow: " + str(ex))

    log("Generative execute active — tie MOTU 3-4 + Brioch analyseAudio for best motion")


run()
