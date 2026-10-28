# Shared TouchDesigner helpers (exec'd into all-in-one globals before build steps).

def set_label(o, text):
    if o is None:
        return
    try:
        o.label = text
    except Exception:
        try:
            o.par.label = text
        except Exception:
            pass
