# Shared TouchDesigner helpers (exec'd into all-in-one globals before build steps).

BRIKVJ_HOST_BUILD = (2023, 12370)
_TOX_BUILD_INDEX = None


def _load_tox_build_index():
    global _TOX_BUILD_INDEX
    if _TOX_BUILD_INDEX is not None:
        return _TOX_BUILD_INDEX
    import json
    import os

    _TOX_BUILD_INDEX = {}
    for root in (
        r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\parts",
        os.path.join(os.path.dirname(__file__), "..", "parts"),
    ):
        idx = os.path.join(root, "TOX_BUILDS.json")
        if not os.path.isfile(idx):
            continue
        try:
            with open(idx, encoding="utf-8") as f:
                data = json.load(f)
            files = data.get("files") or {}
            for rel, meta in files.items():
                _TOX_BUILD_INDEX[rel.replace("\\", "/")] = meta
            break
        except Exception:
            pass
    return _TOX_BUILD_INDEX


def _parse_build_raw(raw):
    if not raw:
        return None
    s = str(raw).strip()
    if "." in s:
        a, b = s.split(".", 1)
        try:
            return int(a), int(b)
        except ValueError:
            return None
    try:
        return 0, int(s)
    except ValueError:
        return None


def td_tox_newer_than_host(path):
    import os

    base = os.path.basename(path)
    if base in TOX_NEWER_BUILD_SKIP:
        return True
    parts_root = None
    for root in (
        r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\parts",
        os.path.join(os.path.dirname(__file__), "..", "parts"),
    ):
        if path.lower().startswith(root.lower()):
            parts_root = root
            break
    if not parts_root:
        return False
    rel = path[len(parts_root) :].lstrip("\\/").replace("\\", "/")
    meta = _load_tox_build_index().get(rel)
    if meta and meta.get("newerThanHost"):
        return True
    parsed = _parse_build_raw(meta.get("build") if meta else None)
    if parsed and parsed > BRIKVJ_HOST_BUILD:
        return True
    return False


def td_log_skip_tox(path, reason):
    try:
        print("[BRIKVJ tox] SKIP " + reason + " " + path)
    except Exception:
        pass


HEAVY_TOX_SKIP = frozenset(
    {
        "fluid_3d_grid.tox",
    }
)

# Saved on TD 2025.x — each loadTox pops a dialog on TD 2023.12370 until re-saved on your build.
TOX_NEWER_BUILD_SKIP = frozenset(
    {
        "okvj_audio_analysis.tox",
        "okvj_glitch_stack.tox",
        "okvj_strobe_stack.tox",
        "okvj_feedback_stack.tox",
        "okvj_displace_stack.tox",
        "okvj_dither_dirt.tox",
        "okvj_halftone.tox",
        "okvj_pixel_sort.tox",
        "okvj_compositor.tox",
        "okvj_shader_changer.tox",
        "audio_crossover.tox",
        "clip_image_loaders.tox",
        "projection_cubemap.tox",
        "fx_spectral_blur.tox",
        "fx_pixel_sorter_pop.tox",
        "fx_glass_pass.tox",
    }
)


def td_top_out(src):
    if src is None:
        return None
    try:
        if src.family == "TOP":
            return src
    except Exception:
        pass
    for name in ("out", "null1", "output", "out1", "render"):
        try:
            o = src.op(name)
            if o is not None and o.family == "TOP":
                return o
        except Exception:
            pass
    try:
        for c in src.children:
            if c.family == "TOP":
                return c
    except Exception:
        pass
    return None


def td_load_tox(parent, path, nicename=None):
    import os

    base = os.path.basename(path)
    if base in HEAVY_TOX_SKIP:
        td_log_skip_tox(path, "heavy")
        return None
    resaved = os.path.join(
        os.path.dirname(path),
        "td2023",
        base,
    )
    if os.path.isfile(resaved):
        path = resaved
    elif base in TOX_NEWER_BUILD_SKIP or td_tox_newer_than_host(path):
        if os.path.isfile(resaved):
            path = resaved
        else:
            td_log_skip_tox(path, "newer-than-host (no td2023 resave)")
            return None
    t = parent.loadTox(path)
    if nicename and t is not None:
        try:
            t.name = nicename
        except Exception:
            pass
    return t


def td_create_op(parent, name, *type_names):
    """Create OP in TD Textport/exec context; tries type objects then TD type strings."""
    for tn in type_names:
        obj = globals().get(tn)
        if obj is not None:
            try:
                return parent.create(obj, name)
            except Exception:
                pass
        try:
            return parent.create(tn, name)
        except Exception:
            pass
    return None


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
