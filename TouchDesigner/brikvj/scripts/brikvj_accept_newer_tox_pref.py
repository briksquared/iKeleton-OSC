# Run first in mega build: set TD preferences (Accept newer/older .tox, errors off modals).

def log(msg):
    print("[BRIKVJ prefs]", msg)


def run():
    from brikvj_td_ui_prefs_snippet import PREF_EXECS

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
