# BRIKVJ — MOTU M4 / Eurorack audio input setup
# Paste into a Text DAT in TouchDesigner and Run (or drive from an Execute DAT).
#
# Discovers Audio Device In / File In ops, prefers MOTU, sets active channels for rack mix.

EURORACK_CHANNELS = "3-4"  # M4 rear line = Knead/rack sub-mix (studio default)
DESK_CHANNELS = "1-2"      # M4 front combo pair = Buddy sub-mix
USE_EURORACK = True        # False → use DESK_CHANNELS instead
MOTU_NAME_HINTS = ("MOTU", "M4", "M Series", "M-Series")
DISABLE_FILE_AUDIO = True  # Mute/bypass common demo file inputs when live rack is primary

TARGET_CHANNELS = EURORACK_CHANNELS if USE_EURORACK else DESK_CHANNELS


def _log(msg):
    print("[BRIKVJ]", msg)


def _list_input_devices():
    try:
        import audio
    except ImportError:
        _log("TD audio module unavailable — set device manually in Audio Device In CHOP.")
        return []

    for getter in ("getInputDevices", "getDevices", "inputDevices"):
        try:
            attr = getattr(audio, getter, None)
            if attr is None:
                continue
            devs = attr() if callable(attr) else attr
            if devs is None:
                continue
            devs = list(devs)
            _log("Input devices ({}):".format(len(devs)))
            for i, name in enumerate(devs):
                _log("  [{}] {}".format(i, name))
            return devs
        except Exception:
            continue
    _log("Could not list audio devices — set MOTU manually in the CHOP.")
    return []


def _pick_motu_index(devices):
    for i, name in enumerate(devices):
        upper = name.upper()
        if any(h.upper() in upper for h in MOTU_NAME_HINTS):
            return i, name
    return None, None


def _set_par(comp, par_names, value):
    for pname in par_names:
        if hasattr(comp.par, pname):
            try:
                comp.par[pname].val = value
                return pname
            except Exception:
                try:
                    comp.par[pname] = value
                    return pname
                except Exception:
                    pass
    return None


def _configure_audio_device_in(chop):
    changed = []
    devices = _list_input_devices()
    idx, dname = _pick_motu_index(devices)
    if idx is not None:
        for pname in ("device", "driverdevice"):
            if _set_par(chop, (pname,), idx) or _set_par(chop, (pname,), dname):
                changed.append("{}={}".format(pname, dname))
                break
    for pname in ("active", "activespec", "channel", "channels"):
        if _set_par(chop, (pname,), TARGET_CHANNELS):
            changed.append("{}={}".format(pname, TARGET_CHANNELS))
            break
    for pname in ("volume", "gain"):
        if _set_par(chop, (pname,), 1):
            changed.append("{}=1".format(pname))
            break
    return changed


def _maybe_disable_file_audio(top_or_chop):
    """Reduce fighting with demo movie/file paths."""
    name = top_or_chop.name.lower()
    path = top_or_chop.path.lower()
    if "file" not in name and "movie" not in name and "file" not in path:
        return False
    if "audiofile" in name or "moviefile" in name or top_or_chop.OPType == "audiofileinCHOP":
        for pname in ("play", "active"):
            _set_par(top_or_chop, (pname,), 0)
        _log("Disabled demo file op: {}".format(top_or_chop.path))
        return True
    if top_or_chop.OPType == "moviefileinTOP":
        for pname in ("play",):
            _set_par(top_or_chop, (pname,), 0)
        _log("Stopped movie TOP (use rack audio instead): {}".format(top_or_chop.path))
        return True
    return False


def run():
    _log("Target input channels: {} (USE_EURORACK={})".format(TARGET_CHANNELS, USE_EURORACK))
    root = op("/")
    if root is None:
        _log("ERROR: no root op — run inside TouchDesigner.")
        return

    device_ins = root.findChildren(type=audiodeviceinCHOP, maxDepth=12)
    if not device_ins:
        _log("No Audio Device In CHOP found — add one or open inside audioAnalysisTime.")
    for ch in device_ins:
        edits = _configure_audio_device_in(ch)
        _log("Configured {} → {}".format(ch.path, edits or "(manual check needed)"))

    if DISABLE_FILE_AUDIO:
        for ch in root.findChildren(type=audiofileinCHOP, maxDepth=12):
            _maybe_disable_file_audio(ch)
        for t in root.findChildren(type=moviefileinTOP, maxDepth=12):
            _maybe_disable_file_audio(t)

    comp = op("audioAnalysisTime")
    if comp is not None:
        _log("Found component: {}".format(comp.path))
        inner = comp.findChildren(type=audiodeviceinCHOP, maxDepth=8)
        for ch in inner:
            edits = _configure_audio_device_in(ch)
            _log("  inner {} → {}".format(ch.path, edits or "(manual check needed)"))
    else:
        _log("Tip: open audioAnalysisTime and confirm Audio Device In feeds the analysis chain.")

    _log("Done. Play rack → M4 inputs 3–4 → watch Audio Device In viewer.")


run()
