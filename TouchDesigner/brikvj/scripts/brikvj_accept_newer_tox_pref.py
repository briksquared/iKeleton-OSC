# Run first in mega build: set TD preferences (Accept newer/older .tox, errors off modals).
# Inlined for TD exec() — do not import other kit modules here.

PREF_EXECS = (
    "ui.preferences['dialogs.loadtoxfromnewerbuild'].val=1",
    "ui.preferences['general.loadtoxfromnewerbuild'].val=2",
    "ui.preferences['dialogs.loadtoxfromolderbuild'].val=1",
    "ui.preferences['general.loadtoxfromolderbuild'].val=2",
    "ui.preferences['dialogs.errornotify'].val=0",
    "ui.preferences['dialogs.error'].val=0",
    "ui.preferences['general.errornotify'].val=0",
)


def log(msg):
    print("[BRIKVJ prefs]", msg)


def run():
    ok = 0
    for expr in PREF_EXECS:
        try:
            exec(expr, globals())
            ok += 1
        except Exception as ex:
            log("skip " + expr + ": " + str(ex))
    try:
        ui.errorsIn = 0
    except Exception:
        pass
    log("applied %d/%d preference lines" % (ok, len(PREF_EXECS)))


run()
