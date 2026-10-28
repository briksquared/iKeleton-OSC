# Map TDA_Mapper.amxd (Live) to scene/clip/router via Custom Parameters on old_brik_vj.

MAPPING = (
    ("Scene", "/project1/old_brik_vj/scenes/scene_switch", "index"),
    ("Clip", "/project1/old_brik_vj/clip_deck/clip_switch", "index"),
    ("Router", "/project1/brikvj_router/source_switch", "index"),
    ("FxBypass", "/project1/old_brik_vj/fx/fx_switch", "index"),
    ("Autopilot", "/project1/brikvj_autopilot", "active"),
)


def log(msg):
    print("[BRIKVJ TDA_Mapper]", msg)


def proj():
    return op("/project1")


def ensure_pars(vj):
    for name, _, _ in MAPPING:
        if hasattr(vj.par, name):
            continue
        try:
            vj.appendCustomPar(name, label=name, style="Int")
        except Exception:
            try:
                vj.appendCustomPar(name)
            except Exception as ex:
                log("Custom par " + name + ": " + str(ex))


def install_parexec(vj):
    p = proj()
    pe = p.op("tda_mapper_parexec")
    if pe is None:
        pe = p.create(parexecuteDAT, "tda_mapper_parexec")
    table = ",\n        ".join(
        "'%s': ('%s', '%s')" % (n, path, pname) for n, path, pname in MAPPING
    )
    pe.text = (
        "# TDA_Mapper → old_brik_vj Custom Parameters\n"
        "def onValueChange(par, prev):\n"
        "    table = {\n        %s\n    }\n"
        "    if par.name not in table:\n"
        "        return\n"
        "    path, pname = table[par.name]\n"
        "    o = op(path)\n"
        "    if not o:\n"
        "        return\n"
        "    try:\n"
        "        setattr(o.par, pname, int(par))\n"
        "    except Exception:\n"
        "        pass\n"
    ) % table
    try:
        pe.par.op = vj.path
        pe.par.pars = " ".join(m[0] for m in MAPPING)
    except Exception as ex:
        log("parexec: " + str(ex))


def run():
    vj = proj().op("old_brik_vj")
    if vj is None:
        log("Run suite build first")
        return
    ensure_pars(vj)
    install_parexec(vj)
    log("Live: TDA_Mapper.amxd → Custom Par Scene/Clip/Router/FxBypass/Autopilot on old_brik_vj")


run()
