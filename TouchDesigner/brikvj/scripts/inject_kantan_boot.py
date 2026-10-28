"""Patch kantanMapper/ui/execute1 onStart + add brikvj_boot Text DAT."""
from __future__ import annotations

import sys
from pathlib import Path

BOOT = r"""def h():
 import os
 T=r'C:/Users/briks/Documents/TouchDesigner/BRIKVJ'
 try: open(T+'/logs/boot_trace.txt','a').write('h\n')
 except: pass
 f=T+'/RUN_BUILD.flag'
 p=T+'/scripts/old_brik_vj_all_in_one.py'
 if not os.path.isfile(f):
  return
 if op('/project1/old_brik_vj'):
  try: os.remove(f)
  except: pass
  return
 exec(compile(open(p,encoding='utf-8').read(),p,'exec'),globals())
 try: os.remove(f)
 except: pass
"""

EXEC_BODY = """def onStart():
 run(op('./brikvj_boot').module.h,delayMilliSeconds=3000,fromOP=me)
 parent().cook(force=True, recurse=True)
 return

def create():
 parent().cook(force=True, recurse=True)
 return

def onExit():
 return

def onFrameStart(frame):
 return

def onFrameEnd(frame):
 return

def onPlayStateChange(state):
 return

def onDeviceChange():
 return

def onProjectPreSave():
 return

def onProjectPostSave():
 return
"""


def _write_blob(path: Path, body: str) -> None:
    header = path.read_bytes()[:27]
    target = len(path.read_bytes()) - 27
    enc = body.encode("utf-8")
    if len(enc) > target:
        raise SystemExit("{} body too long ({} > {})".format(path.name, len(enc), target))
    if len(enc) < target:
        enc += b"\n# " + (b" " * (target - len(enc) - 3))
    path.write_bytes(header + enc)


def inject(toe: Path) -> None:
    toe = toe.resolve()
    ui = Path(str(toe) + ".dir") / "project1/mapping/kantanMapper/ui"
    ex = ui / "execute1.text"
    if not ex.is_file():
        raise SystemExit("missing execute1.text")
    _write_blob(ex, EXEC_BODY)
    parm = ui / "execute1.parm"
    if parm.is_file():
        pc = parm.read_text()
        pc = pc.replace("active 67108864 off", "active 67108864 on")
        if "active 67108864 on" not in pc:
            pc = pc.replace("?\n", "?\nactive 67108864 on\n", 1)
        parm.write_text(pc, newline="\n")
    boot_n = ui / "brikvj_boot.n"
    boot_p = ui / "brikvj_boot.parm"
    boot_t = ui / "brikvj_boot.text"
    if not boot_n.is_file():
        boot_n.write_text(
            "DAT:text\ntile 320 -30 130 90\nflags =  viewer 1 parlanguage 0\ncolor 0.55 0.55 0.55 \nend\n",
            newline="\n",
        )
    if not boot_p.is_file():
        boot_p.write_text("?\nlanguage 67108864 python\n?\n", newline="\n")
    boot_t.write_bytes(b"2\n*\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x024" + BOOT.encode("utf-8"))
    toc = Path(str(toe) + ".toc")
    data = toc.read_bytes()
    if not data.endswith(b"\n"):
        data += b"\n"
    for rel in (
        "project1/mapping/kantanMapper/ui/brikvj_boot.n",
        "project1/mapping/kantanMapper/ui/brikvj_boot.parm",
        "project1/mapping/kantanMapper/ui/brikvj_boot.text",
    ):
        line = rel.encode("ascii") + b"\n"
        if line not in data:
            data += line
    toc.write_bytes(data)
    print("Patched kantan execute1 + brikvj_boot")


if __name__ == "__main__":
    inject(Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\BRIKVJ.toe"))
