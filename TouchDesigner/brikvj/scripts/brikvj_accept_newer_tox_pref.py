# Run first in fast build: set TD preference to Accept newer .tox (no modal spam on loadTox).

def log(msg):
    print("[BRIKVJ prefs]", msg)


def run():
    tried = []
    for expr in (
        "ui.preferences['dialogs.loadtoxfromnewerbuild'].val = 1",
        "ui.preferences['dialogs.loadtoxfromnewerbuild'] = 1",
        "ui.preferences['general.loadtoxfromnewerbuild'].val = 2",
        "ui.preferences['general.loadtoxfromnewerbuild'] = 2",
    ):
        try:
            exec(expr, globals())
            log("OK " + expr)
            return
        except Exception as ex:
            tried.append(expr + ": " + str(ex))
    for name in dir(ui):
        low = name.lower()
        if "pref" in low or "dialog" in low:
            try:
                p = getattr(ui, name)
                log("ui." + name + " = " + str(type(p)))
            except Exception:
                pass
    log("Could not set accept-newer-tox pref automatically — run scan_tox_build_versions.ps1 + td2023 resaves")
    for line in tried[:4]:
        log(line)


run()
