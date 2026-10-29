# Enable TouchDesigner Perform mode on the BRIKVJ program bus (after integrate + broadcast).

PERFORM_TOP = "/project1/perform_out"


def log(msg):
    print("[BRIKVJ perform]", msg)


def run():
    p = op("/project1")
    out = op(PERFORM_TOP)
    if out is None:
        log("Missing perform_out — run integrate step first")
        return

    try:
        p.par.enableperform = 1
        log("project.par.enableperform = 1")
    except Exception as ex:
        log("enableperform: " + str(ex))

    for ui_path in ("ui", "/ui"):
        try:
            u = op(ui_path)
            if u and hasattr(u, "performMode"):
                u.performMode = True
                log("ui.performMode = True")
                break
        except Exception:
            pass

    try:
        out.viewer = True
    except Exception:
        pass

    w = p.op("windows/brikvj_main")
    if w is not None:
        try:
            w.par.winop = PERFORM_TOP
            w.par.borders = 0
            set_label(w, "Perform window (F1) — set Monitor then active=1")
            log("windows/brikvj_main → perform_out")
        except Exception as ex:
            log("main window: " + str(ex))

    km = p.op("mapping/kantanMapper")
    if km is not None:
        try:
            km.viewer = True
            set_label(km, "Projection mapping — corner pins")
        except Exception:
            pass

    log("Press F1 in TD or enable windows/brikvj_main for venue output")


run()
