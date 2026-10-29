# Resolume-class perform stack: 8 clip columns, 12+ generative scenes, deep FX bank, layer mixer.
# Skips crash-prone .tox only (fluid_3d). Router + mapping wired in brikvj_integrate_brioch.py.

import os

ROOT = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
PARTS = os.path.join(ROOT, "parts")
EXTRA = os.path.join(PARTS, "extra")
SUITE = os.path.join(PARTS, "vj_suite")
GLITCH = os.path.join(PARTS, "glitch_fluid")
GEN = os.path.join(PARTS, "generative")
HARVEST_PICK = os.path.join(PARTS, "harvest_pick")
MEDIA = os.path.join(ROOT, "media", "clips")
DEFAULT_CLIP = os.path.join(ROOT, "testingVideo.mp4")
BUILD_LOG = os.path.join(ROOT, "logs", "build.log")

SCENE_DEFS = (
    ("strobe", PARTS, "scene_stroboscope.tox"),
    ("hydra", PARTS, "hydra.tox"),
    ("wispy", SUITE, "scene_wispy_tunnel.tox"),
    ("marbling", SUITE, "scene_paint_marbling.tox"),
    ("wheels", SUITE, "scene_wheels.tox"),
    ("fluid_2d", GLITCH, "fluid_2d_solver.tox"),
    ("lysergiq", GLITCH, "lysergiq_fluid.tox"),
    ("flow", GLITCH, "flow_field.tox"),
    ("particles", GLITCH, "particle_life.tox"),
    ("strange", GLITCH, "strange_trig.tox"),
    ("mesh", PARTS, "scene_mesh_exhibit.tox"),
    ("hydra_td", EXTRA, "hydra_td.tox"),
    ("space", GEN, "space_field.tox"),
    ("vintage", GEN, "vintage_stars.tox"),
    ("blue_sky", GEN, "blue_sky.tox"),
    ("agents", GEN, "agent_trails.tox"),
    ("voice_plasma", GEN, "voice_plasma.tox"),
    ("spiral_scene", GEN, "spiral.tox"),
    ("mesh_v2", EXTRA, "scene_mesh_exhibit_v2.tox"),
    ("wispy_td", GEN, "wispy_tunnel_td.tox"),
)

FX_DEFS = (
    (PARTS, "Double_Feedback.tox", "fb"),
    (PARTS, "kaleidoscope.tox", "kaleid"),
    (PARTS, "distortion.tox", "dist"),
    (PARTS, "tdx_datamosh.tox", "mosh"),
    (PARTS, "color_curves.tox", "grade"),
    (EXTRA, "bloom.tox", "bloom"),
    (EXTRA, "stutter.tox", "stutter"),
    (EXTRA, "echo.tox", "echo"),
    (GLITCH, "feedback_fx.tox", "ok_fb"),
    (GLITCH, "toon_fx_stack.tox", "toon_stack"),
    (GLITCH, "displace_fx.tox", "ok_disp"),
    (GLITCH, "dither.tox", "ok_dirt"),
    (SUITE, "okvj_halftone.tox", "k_half"),
    (SUITE, "fx_spectral_blur.tox", "spec_blur"),
    (GLITCH, "tdx_crt.tox", "tdx_crt"),
    (GLITCH, "tdx_modulation.tox", "tdx_mod"),
    (GLITCH, "strobe_fx.tox", "strobe_fx"),
    (GLITCH, "chaser.tox", "chaser"),
    (GLITCH, "pixel_push.tox", "pixel_push"),
    (GLITCH, "decimate.tox", "decimate"),
    (GLITCH, "particlize.tox", "particlize"),
    (GLITCH, "fluid_like.tox", "fluid_like"),
    (GLITCH, "gridify.tox", "gridify"),
    (EXTRA, "colorshift.tox", "colorshift"),
    (EXTRA, "codev2.tox", "codev2"),
    (GEN, "gater.tox", "gater"),
    (GEN, "spinpulser.tox", "spinpulser_fx"),
    (GLITCH, "tdx_datamosh_alt.tox", "datamosh_alt"),
    (GLITCH, "input_map_strober.tox", "map_strober"),
    (HARVEST_PICK, "okVJ-Shared_colorizer.tox", "colorizer"),
)


def log(msg):
    line = "[BRIKVJ resolume] " + msg
    print(line)
    try:
        with open(BUILD_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def proj():
    return op("/project1")


def child(parent, name, typ):
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
        return td_load_tox(parent, path, nicename)
    except Exception as ex:
        log("load " + filename + ": " + str(ex))
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
    deck = child(vj, "clip_deck", baseCOMP)
    set_label(deck, "Resolume columns — clip_switch 0–7")
    sw = child(deck, "clip_switch", switchTOP)
    sample = DEFAULT_CLIP.replace("\\", "/") if os.path.isfile(DEFAULT_CLIP) else ""
    if os.path.isdir(MEDIA):
        for f in sorted(os.listdir(MEDIA)):
            if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".jpg", ".png", ".tif", ".webp")):
                sample = os.path.join(MEDIA, f).replace("\\", "/")
                break
    outs = []
    for i in range(8):
        slot = child(deck, "clip_%d" % i, baseCOMP)
        mov = child(slot, "player", moviefileinTOP)
        if sample:
            try:
                mov.par.file = sample
                mov.par.play = 1
                mov.par.loop = 1
            except Exception:
                pass
        n = child(slot, "out", nullTOP)
        wire(n, 0, mov)
        outs.append(n)
    for i, o in enumerate(outs):
        wire(sw, i, o)
    out = child(deck, "out", nullTOP)
    wire(out, 0, sw)
    return out


def build_scenes(vj):
    scenes = child(vj, "scenes", baseCOMP)
    set_label(scenes, "Generative / shader scenes — scene_switch")
    outs = []
    for nice, folder, fn in SCENE_DEFS:
        slot = child(scenes, nice, baseCOMP)
        t = load_tox(slot, folder, fn, "content")
        n = child(slot, "out", nullTOP)
        if t is not None:
            wire(n, 0, t)
        outs.append(n)
    sw = child(scenes, "scene_switch", switchTOP)
    try:
        sw.par.connectinput = max(len(outs), 2)
    except Exception:
        pass
    n_in = len(sw.inputConnectors) if sw.inputConnectors else len(outs)
    for i, o in enumerate(outs[:n_in]):
        wire(sw, i, o)
    out = child(scenes, "out", nullTOP)
    wire(out, 0, sw)
    return out


def build_mixer(vj, scenes_out, clips_out):
    mixer = child(vj, "mixer", baseCOMP)
    set_label(mixer, "Layer A=scenes B=clips (comper crossfade)")
    comper = load_tox(mixer, PARTS, "comper.tox", "layer_comper")
    if comper is None:
        comp = child(mixer, "over", compositeTOP)
        wire(comp, 0, scenes_out)
        wire(comp, 1, clips_out)
        out = child(mixer, "out", nullTOP)
        wire(out, 0, comp)
        return out
    wire(comper, 0, scenes_out)
    wire(comper, 1, clips_out)
    out = child(mixer, "out", nullTOP)
    wire(out, 0, comper)
    return out


def build_fx(vj, src):
    fx = child(vj, "fx", baseCOMP)
    set_label(fx, "FX bank — fx_switch dry/wet")
    chain = src
    loaded = 0
    for folder, fn, name in FX_DEFS:
        t = load_tox(fx, folder, fn, name)
        if t is None:
            continue
        dest = td_top_out(t)
        if dest is None:
            log("no TOP in fx " + name)
            continue
        wire(dest, 0, chain)
        chain = td_top_out(t) or chain
        loaded += 1
    bypass = child(fx, "bypass", nullTOP)
    wire(bypass, 0, src)
    sw = child(fx, "fx_switch", switchTOP)
    wire(sw, 0, chain if loaded else src)
    wire(sw, 1, bypass)
    out = child(fx, "out", nullTOP)
    wire(out, 0, sw)
    log("FX loaded %d / %d" % (loaded, len(FX_DEFS)))
    return out


def build_audio_reactive(vj):
    audio = child(vj, "audio", baseCOMP)
    set_label(audio, "Rack + harvest analysis")
    set_label(child(audio, "rack_in", audiodeviceinCHOP), "MOTU M4 in 3-4")
    for folder, fn, nice in (
        (PARTS, "audioAnalysisTime.tox", "analysis"),
        (PARTS, "freqbandctrl2.tox", "bands"),
        (GEN, "audiobandanalysis.tox", "tekt_bands"),
        (GEN, "audio_analysis_time.tox", "harvest_time"),
        (GEN, "audio_analysis_ss.tox", "synth_bands"),
    ):
        load_tox(audio, folder, fn, nice)


def build_recorder_and_extras(vj):
    load_tox(vj, PARTS, "outputrecording.tox", "recorder")
    load_tox(vj, PARTS, "TOPs_stacker_GLSL.tox", "preview_grid")


def run():
    p = proj()
    vj = child(p, "old_brik_vj", baseCOMP)
    vj.viewer = True
    try:
        vj.tags.add("brikvj")
        vj.tags.add("resolume_stack")
    except Exception:
        pass

    build_audio_reactive(vj)
    clips = build_clip_deck(vj)
    scenes = build_scenes(vj)
    mixed = build_mixer(vj, scenes, clips)
    build_fx(vj, mixed)
    build_recorder_and_extras(vj)

    log("Resolume stack ready — keys: brikvj_perform_controls + KEYBOARD_MAP.md")
    log("Next: integrate_brioch (Brioch vs harvest router → kantanMapper → perform_out)")


try:
    run()
except Exception:
    import traceback

    log(traceback.format_exc())
    raise
