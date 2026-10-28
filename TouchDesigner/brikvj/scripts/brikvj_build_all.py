# BRIKVJ — build glitch + audio-reactive + Ableton hooks in the open .toe
# Paste into a Text DAT, set path to /project1/brikvj_build (or Run once from Textport).
#
# Open first: TouchDesigner/BRIKVJ.toe (or NewProject.toe, then Save As BRIKVJ.toe)

import os

BRIKVJ_ROOT = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj"
COMP_FOLDER = os.path.join(BRIKVJ_ROOT, "components")


def _log(msg):
    print("[BRIKVJ build]", msg)


def _project_root():
    for path in ("/project1", "/"):
        r = op(path)
        if r is not None:
            return r
    return op("/")


def _ensure(parent, name, optype, force_new=False):
    if not force_new:
        existing = parent.op(name)
        if existing is not None:
            _log("reuse {}".format(existing.path))
            return existing
    return parent.create(optype, name)


def _load_tox(parent, filename, nicename):
    path = os.path.join(COMP_FOLDER, filename)
    if not os.path.isfile(path):
        _log("MISSING tox: {}".format(path))
        return None
    try:
        t = parent.loadTox(path, customName=nicename)
        _log("loaded {} -> {}".format(filename, t.path))
        return t
    except Exception as e:
        _log("loadTox failed {}: {}".format(filename, e))
        return None


def _wire(top, input_index, source):
    if source is None:
        return
    try:
        top.inputConnectors[input_index].connect(source)
    except Exception as e:
        _log("wire fail {}[{}]: {}".format(top.path, input_index, e))


def build():
    root = _project_root()
    _log("root = {}".format(root.path))

    # Preserve iKeleton OSC if present
    for name in ("oscin1", "oscin2", "oscin"):
        if root.op(name):
            _log("keeping existing {}".format(name))

    brikvj = _ensure(root, "brikvj", baseCOMP)
    brikvj.viewer = True
    brikvj.tags.add("brikvj")

    # --- Live rack / MOTU audio ---
    audio = _ensure(brikvj, "audio", baseCOMP)
    ain = _ensure(audio, "rack_in", audiodeviceinCHOP)
    _log("Set rack_in device to MOTU M4, active channels 3-4 (manual if script cannot)")

    analysis = _load_tox(audio, "audioAnalysisTime.tox", "analysis")
    if analysis is None:
        alevel = _ensure(audio, "level_fallback", analyzeCHOP)
        alevel.par.function = "rms"
        _log("using analyzeCHOP fallback — drag audioAnalysisTime.tox if missing")

    # --- Generators / source (replace with your scene TOP) ---
    vis = _ensure(brikvj, "visual_src", baseCOMP)
    n1 = _ensure(vis, "noise_base", noiseTOP)
    n1.par.resolution = "1920 1080"
    n1.par.monochrome = False
    ramp = _ensure(vis, "motion_ramp", rampTOP)
    _wire(ramp, 0, n1)
    src_out = _ensure(vis, "src_out", nullTOP)
    _wire(src_out, 0, ramp)

    # --- Glitch post chain ---
    glitch = _ensure(brikvj, "glitch_post", baseCOMP)
    double_fb = _load_tox(glitch, "Double_Feedback.tox", "double_feedback")
    if double_fb is None:
        fb = _ensure(glitch, "feedback1", feedbackTOP)
        _wire(fb, 0, src_out)
        chain_in = fb
    else:
        _wire(double_fb, 0, src_out)
        chain_in = double_fb

    displace = _ensure(glitch, "displace_hit", displaceTOP)
    displace.par.displacement = "red"
    displace.par.displacementweight = 0.08
    _wire(displace, 0, chain_in)

    level_crush = _ensure(glitch, "level_crush", levelTOP)
    level_crush.par.contrast = 1.4
    level_crush.par.brightness1 = -0.05
    _wire(level_crush, 0, displace)

    datamosh = _load_tox(glitch, "tdx_datamosh.tox", "datamosh")
    if datamosh is not None:
        _wire(datamosh, 0, level_crush)
        chain_out = datamosh
    else:
        grain = _ensure(glitch, "grain", noiseTOP)
        grain.par.resolution = "1920 1080"
        grain.par.monochrome = True
        comp = _ensure(glitch, "add_grain", compositeTOP)
        comp.par.operand = "over"
        _wire(comp, 0, level_crush)
        _wire(comp, 1, grain)
        chain_out = comp

    glitch_out = _ensure(glitch, "out", nullTOP)
    set_label(glitch_out, "BRIKVJ_OUT")
    _wire(glitch_out, 0, chain_out)

    # --- Audio drives glitch (expressions) ---
    drive = _ensure(brikvj, "audio_drive", nullCHOP)
    set_label(drive, "wire analysis CHOP exports here")
    try:
        displace.par.displacementweight.expr = "op('audio_drive')['rms'] * 0.25 + 0.02"
    except Exception:
        pass
    if analysis is not None:
        try:
            drive.setInput(0, analysis)
        except Exception:
            _log("Connect analysis CHOP -> audio_drive manually")

    # --- Ableton (TDAbleton COMP) ---
    able = _ensure(brikvj, "ableton", baseCOMP)
    tda = None
    for typename in ("tdAbletonCOMP", "tdabletonCOMP", "abletonCOMP"):
        try:
            tda = able.create(typename, "tdAbleton1")
            _log("created {} at {}".format(typename, tda.path))
            break
        except Exception:
            continue
    if tda is None:
        _log("Add TDAbleton COMP manually: Tab -> TDAbleton (see brikvj/ableton/ABLETON.md)")

    # Beat -> datamosh keyframe pulse (CHOP Execute DAT template)
    beat_dat = _ensure(brikvj, "beat_glitch_callbacks", textDAT)
    beat_dat.text = _beat_execute_template()
    set_label(beat_dat, "Copy into CHOP Execute on tdAbleton beat channel")

    # --- Perform output ---
    perform = _ensure(root, "perform_out", outTOP)
    _wire(perform, 0, glitch_out)
    try:
        set_label(perform, "assign to Window / Perform")
    except Exception:
        pass

    _log("BUILD DONE")
    _log("Next: run brikvj_audio_setup.py, wire TDAbleton to Live, connect perform_out to window")
    _log("Replace visual_src with Brioch scenes or your GLSL as needed")


def _beat_execute_template():
    return r"""# CHOP Execute — attach to tdAbleton beat/onBeat channel
# On Off to On:
def onOffToOn(channel, sampleIndex, val, prev):
    dm = op('brikvj/glitch_post/datamosh')
    if dm and hasattr(dm.par, 'Keyframe'):
        dm.par.Keyframe.pulse()
    return
"""


build()
