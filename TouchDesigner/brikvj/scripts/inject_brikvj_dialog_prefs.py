"""Inject project1/brikvj_dialog_prefs — onStart only, sets Accept newer .tox (no build)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

TEMPLATE = Path(
    r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\td-debug\debug.toe.dir\project1\debug\execute_startup"
)
OP_NAME = "brikvj_dialog_prefs"
ON_START = r"""def onStart():
 _p=("ui.preferences['dialogs.loadtoxfromnewerbuild'].val=1",
 "ui.preferences['general.loadtoxfromnewerbuild'].val=2",
 "ui.preferences['dialogs.errornotify'].val=0",
 "ui.preferences['dialogs.error'].val=0",
 "ui.preferences['general.errornotify'].val=0")
 for _e in _p:
  try:exec(_e)
  except Exception:pass
 try:ui.errorsIn=0
 except Exception:pass
 return
"""


def _text_blob(python_source: str) -> bytes:
    template = TEMPLATE.with_suffix(".text").read_bytes()
    header = template[:27]
    target = len(template) - len(header)
    body = python_source.encode("utf-8")
    if len(body) > target:
        raise ValueError("onStart too long ({} > {})".format(len(body), target))
    if len(body) < target:
        body += b"\n# " + (b" " * (target - len(body) - 3))
    return header + body


def inject(toe_path: Path) -> None:
    toe_path = toe_path.resolve()
    dir_path = Path(str(toe_path) + ".dir")
    toc_path = Path(str(toe_path) + ".toc")
    if not dir_path.is_dir():
        raise SystemExit("Expand first: toeexpand {}".format(toe_path))
    proj = dir_path / "project1"
    proj.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE.with_suffix(".n"), proj / (OP_NAME + ".n"))
    parm = TEMPLATE.with_suffix(".parm").read_text()
    if "active 67108864 on" not in parm:
        parm = parm.replace("?\n", "?\nactive 67108864 on\n", 1)
    (proj / (OP_NAME + ".parm")).write_text(parm, newline="\n")
    (proj / (OP_NAME + ".text")).write_bytes(_text_blob(ON_START))
    rel = "project1/" + OP_NAME
    data = toc_path.read_bytes()
    if not data.endswith(b"\n"):
        data += b"\n"
    for suffix in (".n", ".parm", ".text"):
        line = (rel + suffix).encode("ascii") + b"\n"
        if line not in data:
            data += line
    toc_path.write_bytes(data)
    print("Injected", rel)


if __name__ == "__main__":
    inject(Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe"))
