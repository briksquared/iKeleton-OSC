# Run at end of all-in-one — prints PASS/FAIL for Resolume-class stack nodes.

REQUIRED = (
    "/project1/old_brik_vj",
    "/project1/old_brik_vj/scenes/scene_switch",
    "/project1/old_brik_vj/clip_deck/clip_switch",
    "/project1/old_brik_vj/fx/fx_switch",
    "/project1/brikvj_router",
    "/project1/brikvj_broadcast",
    "/project1/perform_out",
    "/project1/mapping/kantanMapper",
    "/project1/brikvj_autopilot",
    "/project1/brikvj_keys",
)

OPTIONAL = (
    "/project1/old_brik_vj/live/tdAbleton",
    "/project1/windows",
    "/project1/old_brik_vj/preset_bank",
    "/project1/brikvj_level_drive",
    "/project1/brikvj_on_start",
)


def log(msg):
    print("[BRIKVJ verify]", msg)


def run():
    missing = []
    for path in REQUIRED:
        if op(path) is None:
            missing.append(path)
    opt_missing = [p for p in OPTIONAL if op(p) is None]

    if missing:
        log("FAIL — missing %d required nodes:" % len(missing))
        for m in missing:
            log("  " + m)
    else:
        log("PASS — all %d required perform nodes present" % len(REQUIRED))

    if opt_missing:
        log("Optional not found (%d):" % len(opt_missing))
        for m in opt_missing:
            log("  " + m)

    parts_root = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\parts"
    import os

    for sub, label in (
        ("", "core"),
        ("vj_suite", "vj_suite"),
        ("glitch_fluid", "glitch_fluid"),
        ("extra", "extra"),
    ):
        d = os.path.join(parts_root, sub) if sub else parts_root
        tox = len([f for f in os.listdir(d) if f.endswith(".tox")]) if os.path.isdir(d) else 0
        log("Harvest on disk [%s]: %d .tox in %s" % (label, tox, d))

    if not missing:
        log("Save BRIKVJ.toe — then F1 Perform")
    return len(missing) == 0


run()
