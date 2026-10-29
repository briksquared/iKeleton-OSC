# Old Brik V J — full VJ suite (Resolume/MadMapper/HeavyM feature density)
# Run once in BRIKVJ.toe after brikvj_refresh_all.ps1. Then brikvj_integrate_brioch.py + save.

import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
PARTS = os.path.join(ROOT, "parts")
EXTRA = os.path.join(PARTS, "extra")
SUITE = os.path.join(PARTS, "vj_suite")
GLITCH = os.path.join(PARTS, "glitch_fluid")
MEDIA = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\media\clips"
DEFAULT_CLIP = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\testingVideo.mp4"


BUILD_LOG = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\build.log"


def log(msg):
    line = "[BRIKVJ suite] " + msg
    print(line)
    try:
        with open(BUILD_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


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
            return e
    return parent.create(typ, name)


def load_tox(parent, folder, filename, nicename):
    if filename in HEAVY_TOX_SKIP:
        log("SKIP heavy " + filename)
        return None
    path = os.path.join(folder, filename)
    if not os.path.isfile(path):
        log("MISSING " + path)
        return None
    try:
        t = td_load_tox(parent, path, nicename)
        log("loaded " + filename)
        return t
    except Exception as ex:
        log("loadTox " + filename + ": " + str(ex))
        return None


def wire(top, idx, src):
    if src is None:
        return
    src = td_top_out(src)
    if src is None:
        return
    try:
        owner = src.outputConnectors[0].owner if hasattr(src, "outputConnectors") else src
        top.inputConnectors[idx].connect(owner)
    except Exception as ex:
        log("wire: " + str(ex))


def build_clip_deck(vj):
    """Resolume-style clip columns (movie / still slots)."""
    deck = child(vj, "clip_deck", baseCOMP)
    set_label(deck, "Clip players (index on clip_switch)")
    sw = child(deck, "clip_switch", switchTOP)
    clips = []
    sample = DEFAULT_CLIP if os.path.isfile(DEFAULT_CLIP) else ""
    if os.path.isdir(MEDIA):
        for f in sorted(os.listdir(MEDIA)):
            if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".jpg", ".png", ".tif")):
                sample = os.path.join(MEDIA, f).replace("\\", "/")
                break
    for i in range(8):
        slot = child(deck, "clip_%d" % i, baseCOMP)
        if sample.lower().endswith((".jpg", ".png", ".tif")):
            mov = child(slot, "player", moviefileinTOP)
        else:
            mov = child(slot, "player", moviefileinTOP)
        try:
            mov.par.file = sample
            mov.par.play = 1
            mov.par.loop = 1
        except Exception:
            pass
        n = child(slot, "out", nullTOP)
        wire(n, 0, mov)
        clips.append(n)
    for i, c in enumerate(clips[:8]):
        wire(sw, i, c)
    deck_out = child(deck, "out", nullTOP)
    wire(deck_out, 0, sw)
    return deck_out


def build_scenes(vj):
    scenes = child(vj, "scenes", baseCOMP)
    defs = [
        ("strobe", PARTS, "scene_stroboscope.tox"),
        ("mesh", PARTS, "scene_mesh_exhibit.tox"),
        ("hydra", PARTS, "hydra.tox"),
        ("hydra_td", EXTRA, "hydra_td.tox"),
        ("mesh2", EXTRA, "scene_mesh_exhibit_v2.tox"),
        ("wispy", SUITE, "scene_wispy_tunnel.tox"),
        ("marbling", SUITE, "scene_paint_marbling.tox"),
        ("wheels", SUITE, "scene_wheels.tox"),
        ("fluid_2d", GLITCH, "fluid_2d_solver.tox"),
        ("fluid_3d", GLITCH, "fluid_3d_grid.tox"),
        ("lysergiq", GLITCH, "lysergiq_fluid.tox"),
        ("flow", GLITCH, "flow_field.tox"),
        ("particles", GLITCH, "particle_life.tox"),
        ("strange", GLITCH, "strange_trig.tox"),
    ]
    outs = []
    for nice, folder, fn in defs:
        slot = child(scenes, nice, baseCOMP)
        t = load_tox(slot, folder, fn, "content")
        n = child(slot, "out", nullTOP)
        if t is not None:
            wire(n, 0, t)
        outs.append(n)
    sw = child(scenes, "scene_switch", switchTOP)
    for i, o in enumerate(outs[: min(13, len(outs), len(sw.inputConnectors))]):
        wire(sw, i, o)
    out = child(scenes, "out", nullTOP)
    wire(out, 0, sw)
    return out


def build_mixer(vj, a, b):
    mixer = child(vj, "mixer", baseCOMP)
    comper = load_tox(mixer, PARTS, "comper.tox", "layer_comper")
    if comper is None:
        comp = child(mixer, "over", compositeTOP)
        wire(comp, 0, a)
        wire(comp, 1, b)
        out = child(mixer, "out", nullTOP)
        wire(out, 0, comp)
        return out
    wire(comper, 0, a)
    wire(comper, 1, b)
    out = child(mixer, "out", nullTOP)
    wire(out, 0, comper)
    return out


def build_fx(vj, src):
    fx = child(vj, "fx", baseCOMP)
    chain = src
    for folder, fn, name in (
        (PARTS, "Double_Feedback.tox", "fb"),
        (PARTS, "kaleidoscope.tox", "kaleid"),
        (PARTS, "distortion.tox", "dist"),
        (PARTS, "tdx_datamosh.tox", "mosh"),
        (PARTS, "color_curves.tox", "grade"),
        (EXTRA, "bloom.tox", "bloom"),
        (EXTRA, "stutter.tox", "stutter"),
        (EXTRA, "echo.tox", "echo"),
        (SUITE, "okvj_glitch_stack.tox", "ok_glitch"),
        (SUITE, "okvj_strobe_stack.tox", "ok_strobe"),
        (SUITE, "okvj_feedback_stack.tox", "ok_fb"),
        (SUITE, "okvj_displace_stack.tox", "ok_disp"),
        (SUITE, "okvj_dither_dirt.tox", "ok_dirt"),
        (SUITE, "okvj_halftone.tox", "ok_half"),
        (SUITE, "fx_spectral_blur.tox", "spec_blur"),
        (GLITCH, "tdx_crt.tox", "tdx_crt"),
        (GLITCH, "tdx_modulation.tox", "tdx_mod"),
        (GLITCH, "strobe_fx.tox", "strobe_fx"),
        (GLITCH, "chaser.tox", "chaser"),
        (GLITCH, "pixel_push.tox", "pixel_push"),
        (GLITCH, "decimate.tox", "decimate"),
        (GLITCH, "particlize.tox", "particlize"),
        (GLITCH, "fluid_like.tox", "fluid_like"),
    ):
        t = load_tox(fx, folder, fn, name)
        if t is None:
            continue
        wire(t, 0, chain)
        chain = t
    bypass = child(fx, "fx_switch", switchTOP)
    wire(bypass, 0, chain)
    wire(bypass, 1, src)
    out = child(fx, "out", nullTOP)
    wire(out, 0, bypass)
    return out


def build_audio(vj):
    audio = child(vj, "audio", baseCOMP)
    set_label(child(audio, "rack_in", audiodeviceinCHOP), "MOTU M4 in 3-4")
    load_tox(audio, PARTS, "audioAnalysisTime.tox", "analysis")
    load_tox(audio, PARTS, "freqbandctrl2.tox", "bands")
    load_tox(audio, SUITE, "audio_crossover.tox", "crossover")
    load_tox(audio, SUITE, "okvj_audio_analysis.tox", "ok_analysis")


def build_output(vj, master_top):
    p = proj()
    rec = load_tox(vj, PARTS, "outputrecording.tox", "recorder")
    if rec is None:
        load_tox(vj, EXTRA, "outputrecording2.tox", "recorder2")
    load_tox(vj, SUITE, "projection_cubemap.tox", "cubemap")
    load_tox(vj, EXTRA, "fulldome_sim.tox", "fulldome")
    load_tox(vj, PARTS, "TOPs_stacker_GLSL.tox", "preview_grid")
    load_tox(vj, SUITE, "clip_image_loaders.tox", "dj_loaders")

    live = child(vj, "live", baseCOMP)
    for typename in ("tdAbletonCOMP", "tdabletonCOMP"):
        try:
            live.create(typename, "tdAbleton")
            break
        except Exception:
            pass

    perform = p.op("perform_out")
    if perform is None:
        perform = p.create(outTOP, "perform_out")
    wire(perform, 0, master_top)


def run():
    p = proj()
    vj = child(p, "old_brik_vj", baseCOMP)
    vj.viewer = True
    vj.tags.add("brikvj")
    vj.tags.add("vj_suite")

    build_audio(vj)
    clips = build_clip_deck(vj)
    scenes = build_scenes(vj)
    mixed = build_mixer(vj, scenes, clips)
    master = build_fx(vj, mixed)
    build_output(vj, master)

    log("SUITE DONE — scene_switch 0-6, clip_switch 0-7, fx_switch bypass")
    log("Mapping: /project1/mapping/kantanMapper (Brioch) — feed from brikvj_integrate_brioch")
    log("Save BRIKVJ.toe")


try:
    run()
except Exception:
    import traceback

    log(traceback.format_exc())
    raise
