# Create Window COMP placeholders for perform_out + projector outputs (MadMapper multi-out).

WINDOWS = (
    ("brikvj_main", "/project1/perform_out", "Main perform (F1)"),
    ("brikvj_projector_a", "/project1/brikvj_broadcast/projector_1", "Physical projector A"),
    ("brikvj_projector_b", "/project1/brikvj_broadcast/projector_2", "Physical projector B"),
    ("brikvj_preview", "/project1/brikvj_broadcast/preview", "Operator preview"),
)


def log(msg):
    print("[BRIKVJ windows]", msg)


def proj():
    return op("/project1")


def ensure_window(name, top_path, label):
    p = proj()
    root = p.op("windows")
    if root is None:
        root = p.create(baseCOMP, "windows")
        try:
            set_label(root, "Assign monitors in Window COMP → Open Viewer")
        except Exception:
            pass

    w = root.op(name)
    if w is None:
        try:
            w = root.create(windowCOMP, name)
        except Exception:
            log("Could not create windowCOMP — create manually: " + name)
            return
    try:
        set_label(w, label)
        w.par.winop = top_path
        w.par.monitor = 0
        w.par.borders = 0
        w.par.active = 0
    except Exception as ex:
        log(name + " par: " + str(ex))
    log("Window " + name + " → " + top_path + " (set monitor, then active=1)")


def run():
    for name, top, label in WINDOWS:
        if op(top) is None:
            log("Skip " + name + " — missing " + top)
            continue
        ensure_window(name, top, label)
    log("Open /project1/windows — set Monitor index per venue, enable Active for show")


run()
