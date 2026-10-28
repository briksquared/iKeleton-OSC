# Old Brik V J — assemble harvested parts into one perform network (Resolume-style)
# Run once inside BRIKVJ.toe (empty base). Then old_brik_vj_audio.py

import json
import os

ROOT = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj"
PARTS = os.path.join(ROOT, "parts")
EXTRA = os.path.join(PARTS, "extra")
MANIFEST = os.path.join(PARTS, "PARTS.json")


def log(msg):
    print("[Old Brik V J]", msg)


def proj():
    for p in ("/project1", "/"):
        o = op(p)
        if o:
            return o
    return op("/")


def child(parent, name, typ, reuse=True):
    if reuse:
        e = parent.op(name)
        if e:
            log("reuse " + e.path)
            return e
    return parent.create(typ, name)


def load_part(parent, filename, nicename, folder=None):
    base = folder or PARTS
    path = os.path.join(base, filename)
    if not os.path.isfile(path):
        log("MISSING part: " + path)
        return None
    try:
        t = parent.loadTox(path, customName=nicename)
        log("loaded " + filename + " -> " + t.path)
        return t
    except Exception as ex:
        log("loadTox failed " + filename + ": " + ex)
        return None


def wire(top, idx, src):
    if src is None:
        return
    try:
        top.inputConnectors[idx].connect(src)
    except Exception as ex:
        log("wire " + top.path + "[" + str(idx) + "]: " + str(ex))


def build():
    if os.path.isfile(MANIFEST):
        try:
            with open(MANIFEST, encoding="utf-8") as f:
                parts = json.load(f)
            log("parts manifest: {} entries".format(len(parts)))
        except Exception as ex:
            log("manifest read: " + str(ex))

    p = proj()
    vj = child(p, "old_brik_vj", baseCOMP)
    vj.viewer = True
    vj.tags.add("brikvj")
    vj.tags.add("resolume_replacement")

    # --- Audio (MOTU 3–4 rack) ---
    audio = child(vj, "audio", baseCOMP)
    child(audio, "rack_in", audiodeviceinCHOP).label = "MOTU M4 in 3-4"
    analysis = load_part(audio, "audioAnalysisTime.tox", "analysis")
    bands = load_part(audio, "freqbandctrl2.tox", "bands")
    drive = child(vj, "audio_drive", nullCHOP)
    set_label(drive, "Wire analysis/bands CHOP here")
    if analysis is not None:
        try:
            drive.setInput(0, analysis)
        except Exception:
            pass

    # --- Scenes (Resolume "columns" — pick / crossfade in mixer) ---
    scenes = child(vj, "scenes", baseCOMP)
    scene_defs = (
        ("scene_a", "scene_stroboscope.tox"),
        ("scene_b", "scene_mesh_exhibit.tox"),
        ("scene_c", "hydra.tox"),
        ("scene_d", "scene_mesh_exhibit_v2.tox", EXTRA),
    )
    scene_outs = []
    for item in scene_defs:
        if len(item) == 3:
            nice, fn, folder = item
        else:
            nice, fn = item
            folder = None
        slot = child(scenes, nice, baseCOMP)
        s = load_part(slot, fn, "content", folder)
        n = child(slot, "out", nullTOP)
        if s is not None and hasattr(s, "outputConnectors") and len(s.outputConnectors):
            try:
                wire(n, 0, s.outputConnectors[0].owner)
            except Exception:
                pass
        scene_outs.append(n)

    # --- Layer mixer (TDX comper = A/B crossfade like Resolume layers) ---
    mixer = child(vj, "mixer", baseCOMP)
    comper = load_part(mixer, "comper.tox", "layer_comper")
    if comper is None:
        comp = child(mixer, "fallback_comp", compositeTOP)
        comp.par.operand = "over"
        if len(scene_outs) >= 2:
            wire(comp, 0, scene_outs[0])
            wire(comp, 1, scene_outs[1])
        mix_out = child(mixer, "out", nullTOP)
        wire(mix_out, 0, comp)
    else:
        mix_out = child(mixer, "out", nullTOP)
        try:
            if len(scene_outs) >= 1:
                wire(comper, 0, scene_outs[0])
            if len(scene_outs) >= 2:
                wire(comper, 1, scene_outs[1])
            wire(mix_out, 0, comper)
        except Exception:
            wire(mix_out, 0, scene_outs[0] if scene_outs else None)
        log("Use comper Blend/Cross for layer A/B (Resolume-style)")

    # --- Master FX bus ---
    fx = child(vj, "fx", baseCOMP)
    fb = load_part(fx, "Double_Feedback.tox", "feedback")
    if fb is None:
        fb = child(fx, "feedback1", feedbackTOP)
    wire(fb, 0, mix_out)

    kaleid = load_part(fx, "kaleidoscope.tox", "kaleid")
    chain = fb
    if kaleid is not None:
        wire(kaleid, 0, chain)
        chain = kaleid

    dist = load_part(fx, "distortion.tox", "distort")
    if dist is not None:
        wire(dist, 0, chain)
        chain = dist

    mosh = load_part(fx, "tdx_datamosh.tox", "datamosh")
    if mosh is not None:
        wire(mosh, 0, chain)
        chain = mosh

    curves = load_part(fx, "color_curves.tox", "grade")
    if curves is not None:
        wire(curves, 0, chain)
        chain = curves

    bloom = load_part(fx, "bloom.tox", "bloom", EXTRA)
    if bloom is not None:
        wire(bloom, 0, chain)
        chain = bloom

    stutter = load_part(fx, "stutter.tox", "stutter", EXTRA)
    if stutter is not None:
        wire(stutter, 0, chain)
        chain = stutter

    fx_out = child(fx, "out", nullTOP)
    wire(fx_out, 0, chain)

    # Audio-reactive displacement on master
    crush = child(fx, "level_hit", levelTOP)
    wire(crush, 0, fx_out)
    try:
        crush.par.contrast.expr = "1.2 + op('old_brik_vj/audio_drive')['rms'] * 0.6"
    except Exception:
        pass
    master = child(fx, "master", nullTOP)
    wire(master, 0, crush)

    # --- Live sync ---
    live = child(vj, "live", baseCOMP)
    for typename in ("tdAbletonCOMP", "tdabletonCOMP"):
        try:
            tda = live.create(typename, "tdAbleton")
            log("TDAbleton: " + tda.path)
            break
        except Exception:
            tda = None
    if tda is None:
        log("Add TDAbleton under old_brik_vj/live (User Library + control surface)")

    # --- Record / output (tekt outputrecording + perform) ---
    rec = load_part(vj, "outputrecording.tox", "recorder")
    if rec is not None:
        log("Recorder at " + rec.path + " — wire master TOP in")

    out = child(p, "perform_out", outTOP)
    wire(out, 0, master)
    set_label(out, "Projector / main out (replaces Resolume output)")

    # --- Operator preview grid (optional) ---
    load_part(vj, "TOPs_stacker_GLSL.tox", "preview_grid")

    log("ASSEMBLY DONE")
    log("Scenes: old_brik_vj/scenes/scene_{a,b,c} — swap or route into comper")
    log("Full Brioch set (reference): see parts/PARTS.json briochSceno.beta.toe path")
    log("Next: old_brik_vj_audio.py → save BRIKVJ.toe")


build()
