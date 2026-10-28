"""Inject old_brik_autostart Execute DAT (runs build + audio on project open)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

TEMPLATE_DIR = Path(
    r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\td-debug\debug.toe.dir\project1\debug"
)
OP_NAME = "old_brik_autostart"

# Must fit TD execute .text body length (564 bytes with td-debug template header).
ON_START = r'''def onStart():
	import os
	S=r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\scripts"
	for f in("old_brik_vj_build.py","old_brik_vj_audio.py"):
	 p=os.path.join(S,f)
	 if not os.path.isfile(p):
	  print("[Old Brik V J] missing",p); continue
	 try:
	  exec(compile(open(p,encoding="utf-8").read(),p,"exec"))
	 except Exception:
	  import traceback; traceback.print_exc()
	return
'''


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
    proj.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE_DIR / "execute_startup.n", proj / (OP_NAME + ".n"))
    shutil.copy2(TEMPLATE_DIR / "execute_startup.parm", proj / (OP_NAME + ".parm"))
    (proj / (OP_NAME + ".text")).write_bytes(_text_blob(ON_START))

    rel = "project1/" + OP_NAME
    entries = [rel + ".n", rel + ".parm", rel + ".text"]
    data = toc_path.read_bytes()
    if not data.endswith(b"\n"):
        data += b"\n"
    for entry in entries:
        line = entry.encode("ascii") + b"\n"
        if line not in data:
            data += line
    toc_path.write_bytes(data)
    print("Injected", OP_NAME)


if __name__ == "__main__":
    inject(Path(sys.argv[1]))
