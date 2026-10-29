# Single source for TouchDesigner ui.preferences (Accept newer/older .tox, errors → textport).
# Used by inject_kantan_boot.py and inject_brikvj_dialog_prefs.py — keep compact.

PREF_EXECS = (
    "ui.preferences['dialogs.loadtoxfromnewerbuild'].val=1",
    "ui.preferences['general.loadtoxfromnewerbuild'].val=2",
    "ui.preferences['dialogs.loadtoxfromolderbuild'].val=1",
    "ui.preferences['general.loadtoxfromolderbuild'].val=2",
    "ui.preferences['dialogs.errornotify'].val=0",
    "ui.preferences['dialogs.error'].val=0",
    "ui.preferences['general.errornotify'].val=0",
)


def compact_onstart_block() -> str:
    lines = ["def onStart():", " try:"]
    for e in PREF_EXECS:
        lines.append("  exec(%r)" % e)
    lines.append("  ui.errorsIn=0")
    lines.append(" except Exception: pass")
    lines.append(" return")
    return "\n".join(lines)


def dialog_prefs_onstart_only() -> str:
    body = ["def onStart():"]
    body.append(" _p=" + repr(PREF_EXECS))
    body.append(" for _e in _p:")
    body.append("  try: exec(_e)")
    body.append("  except Exception: pass")
    body.append(" try: ui.errorsIn=0")
    body.append(" except Exception: pass")
    body.append(" return")
    return "\n".join(body)
