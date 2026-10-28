"""Inject brikvj_manual_build Execute DAT (Start OFF — pulse Start once to build)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

TEMPLATE_DIR = Path(
    r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\td-debug\debug.toe.dir\project1\debug"
)
OP_NAME = "brikvj_manual_build"
BUILD = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\scripts\old_brik_vj_all_in_one.py"

ON_START = r'''def onStart():
 import os
 p=r'%s'
 if op('/project1/old_brik_vj'):
  return
 def _go():
  exec(compile(open(p,encoding='utf-8').read(),p,'exec'),globals())
  project.save()
 run(_go,delayMilliSeconds=2500,fromOP=me)
 return
''' % BUILD.replace("\\", "\\\\")


def _text_blob(python_source: str) -> bytes:
    template = (TEMPLATE_DIR / "execute_startup.text").read_bytes()
    header = template[:27]
    target_body_len = len(template) - len(header)
    body = python_source.encode("utf-8")
    if len(body) > target_body_len:
        raise ValueError("onStart too long ({} > {})".format(len(body), target_body_len))
    if len(body) < target_body_len:
        body += b"\n# " + (b" " * (target_body_len - len(body) - 3))
    return header + body


def inject(toe_path: Path) -> None:
    toe_path = toe_path.resolve()
    dir_path = Path(str(toe_path) + ".dir")
    toc_path = Path(str(toe_path) + ".toc")
    if not dir_path.is_dir():
        raise SystemExit("Expand first: toeexpand {}".format(toe_path))

    proj = dir_path / "project1"
    shutil.copy2(TEMPLATE_DIR / "execute_startup.n", proj / (OP_NAME + ".n"))
    parm = (TEMPLATE_DIR / "execute_startup.parm").read_text()
    parm = parm.replace("start 67108864 on", "start 67108864 off")
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
    print("Injected", OP_NAME, "(Start OFF — pulse Start on this DAT once)")


if __name__ == "__main__":
    inject(Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe"))
