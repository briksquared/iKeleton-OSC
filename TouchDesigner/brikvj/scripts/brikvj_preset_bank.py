# HeavyM / Resolume-style preset slots (tekt presetslot) under old_brik_vj.

import os

ROOT = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj"
EXTRA = os.path.join(ROOT, "parts", "extra")


def log(msg):
    print("[BRIKVJ presets]", msg)


def proj():
    return op("/project1")


def child(parent, name, typ):
    e = parent.op(name)
    if e:
        return e
    return parent.create(typ, name)


def load_tox(parent, fn, nice):
    path = os.path.join(EXTRA, fn)
    if not os.path.isfile(path):
        log("MISSING " + path)
        return None
    try:
        return parent.loadTox(path, customName=nice)
    except Exception as ex:
        log("load " + fn + ": " + ex)
        return None


def wire(top, idx, src):
    if src is None:
        return
    try:
        top.inputConnectors[idx].connect(src)
    except Exception as ex:
        log("wire: " + str(ex))


def run():
    p = proj()
    vj = p.op("old_brik_vj")
    if vj is None:
        log("Run suite build first")
        return

    bank = child(vj, "preset_bank", baseCOMP)
    try:
        set_label(bank, "Preset slots (HeavyM-style) — wire targets in UI")
    except Exception:
        pass

    slot = load_tox(bank, "presetslot.tox", "slots")
    ui = load_tox(bank, "presetslotui.tox", "slot_ui")
    if ui is not None:
        try:
            ui.viewer = True
        except Exception:
            pass

    master = vj.op("fx/out")
    if master is None:
        master = vj.op("scenes/out")
    tap = child(bank, "tap", nullTOP)
    if master is not None:
        wire(tap, 0, master)

    log("Preset bank at " + bank.path + " — assign slot targets to scene/FX parms")


run()
