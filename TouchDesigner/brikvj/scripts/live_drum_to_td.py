# Wire Brioch analyseAudio to Live (M4 loopback) or keep file loop — run in TD Text DAT
# Default Brioch path already uses audiofilein → audioAnalysis (kick/snare/rhythm bands).

LOOP = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\ableton\samples\brikvj_drum_loop.mp3"
USE_LIVE_LOOPBACK = False  # True → Audio Device In on M4 loopback instead of file


def log(m):
    print("[Old Brik V J live]", m)


def main():
    ain = op("/project1/analyseAudio/audioAnalysis/audiofilein1")
    if ain is None:
        log("audiofilein1 not found — open BRIKVJ.toe (Brioch)")
        return
    if not USE_LIVE_LOOPBACK:
        ain.par.file = LOOP
        for pname in ("play", "active"):
            if hasattr(ain.par, pname):
                try:
                    ain.par[pname] = 1
                except Exception:
                    pass
        log("File loop: " + LOOP)
    else:
        dev = op("/project1/analyseAudio/audioAnalysis").create(audiodeviceinCHOP, "live_loopback")
        set_label(dev, "M4 loopback from Live master")
        log("Created " + dev.path + " — wire into analysis manually")

    log("Scenes (stroboscope, mesh, etc.) read analyseAudio — press Play in Perform.")


main()
