# Run inside TouchDesigner onStart — walks network, force-cooks, writes op.errors().

import os

HOME = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
LOG = os.path.join(HOME, "logs", "td_errors.txt")
TRACE = os.path.join(HOME, "logs", "boot_trace.txt")


def _walk(o, depth, out):
    if depth > 20:
        return
    try:
        o.cook(force=True)
    except Exception:
        pass
    try:
        err = o.errors()
        if err:
            out.append("%s\t%s" % (o.path, err))
    except Exception:
        pass
    try:
        for c in o.children:
            _walk(c, depth + 1, out)
    except Exception:
        pass


def run():
    try:
        open(TRACE, "a").write("E\n")
    except Exception:
        pass
    try:
        t = op("/local/time")
        if t:
            t.par.play = True
    except Exception:
        pass
    for path in (
        "/project1/analyseAudio/audioAnalysis/audiofilein1",
        "/project1/audiofilein1",
        "/project1/meshParticles/audioAnalysis/audiofilein1",
    ):
        try:
            a = op(path)
            if a:
                a.par.play = True
        except Exception:
            pass
    try:
        for _ in range(120):
            op("/project1").cook(force=True, recurse=True)
    except Exception:
        pass
    lines = []
    root = op("/")
    _walk(root, 0, lines)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "w", encoding="utf-8") as f:
        if lines:
            f.write("\n".join(lines))
            f.write("\n")
        else:
            f.write("OK — no op.errors() after cook\n")
    print("[BRIKVJ] td_errors:", len(lines), "ops")


run()
