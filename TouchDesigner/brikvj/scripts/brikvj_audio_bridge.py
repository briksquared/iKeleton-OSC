# Tie Brioch analyseAudio + harvest old_brik_vj analysis (single rack signal path).

def log(msg):
    print("[BRIKVJ audio bridge]", msg)


def wire_chop(dst, idx, src):
    if dst is None or src is None:
        return
    try:
        dst.inputConnectors[idx].connect(src)
    except Exception as ex:
        log("CHOP wire: " + str(ex))


def find_brioch_audio():
    for path in (
        "/project1/analyseAudio/out1",
        "/project1/analyseAudio",
        "/project1/null7",
    ):
        o = op(path)
        if o is not None and hasattr(o, "outputConnectors"):
            return o
    return None


def run():
    p = op("/project1")
    vj = p.op("old_brik_vj")
    if vj is None:
        log("No old_brik_vj — run suite build first")
        return

    brioch = find_brioch_audio()
    drive = vj.op("audio_drive")
    if drive is None:
        drive = vj.create(nullCHOP, "audio_drive")
        try:
            set_label(drive, "Merged Brioch + rack analysis")
        except Exception:
            pass

    rack_analysis = None
    for path in (
        "audio/analysis/out1",
        "audio/analysis",
        "audio/ok_analysis/out1",
        "audio/bands/out1",
    ):
        o = vj.op(path)
        if o is not None:
            rack_analysis = o
            break

    if brioch is not None:
        wire_chop(drive, 0, brioch)
        log("Brioch analyseAudio → audio_drive")
    if rack_analysis is not None:
        wire_chop(drive, 1 if brioch else 0, rack_analysis)
        log("Harvest analysis → audio_drive")

    merge = vj.op("audio_merged")
    if merge is None:
        merge = vj.create(mathCHOP, "audio_merged")
    try:
        merge.par.scope = "channels"
        merge.par.combine = "add"
    except Exception:
        pass
    if brioch:
        wire_chop(merge, 0, brioch)
    if rack_analysis:
        wire_chop(merge, 1 if brioch else 0, rack_analysis)

    for fx in ("fx", "scenes"):
        comp = vj.op(fx)
        if comp is None:
            continue
        for ch in comp.findChildren(type=audiodeviceinCHOP, maxDepth=8):
            try:
                set_label(ch, "Use rack_in / Brioch analyseAudio (Patchworks 3-4)")
            except Exception:
                pass

    log("FX can reference op('old_brik_vj/audio_drive') or audio_merged for reactivity")


run()
