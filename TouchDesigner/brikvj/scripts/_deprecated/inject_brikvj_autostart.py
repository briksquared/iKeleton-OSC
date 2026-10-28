"""Inject brikvj_autostart Execute DAT into an expanded .toe.dir and update .toc."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

TEMPLATE_DIR = Path(
    r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep3\touchdesigner\td-debug\debug.toe.dir\project1\debug"
)
OP_NAME = "brikvj_autostart"

ON_START = r'''def onStart():
	import os
	SCRIPTS = r"C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\brikvj\scripts"
	for fn in ("brikvj_build_all.py", "brikvj_audio_setup.py"):
		p = os.path.join(SCRIPTS, fn)
		if not os.path.isfile(p):
			print("[BRIKVJ autostart] missing:", p)
			continue
		try:
			exec(compile(open(p, encoding="utf-8").read(), p, "exec"))
		except Exception:
			import traceback
			traceback.print_exc()
	return
'''


def _text_blob(python_source: str) -> bytes:
    template = (TEMPLATE_DIR / "execute_startup.text").read_bytes()
    header = template[:27]
    target_body_len = len(template) - len(header)
    body = python_source.encode("utf-8")
    if len(body) > target_body_len:
        raise ValueError(
            "onStart script too long for TD execute .text ({} > {} bytes)".format(
                len(body), target_body_len
            )
        )
    if len(body) < target_body_len:
        pad = target_body_len - len(body)
        body += b"\n# " + (b" " * (pad - 3))
    return header + body


def inject(toe_path: Path) -> None:
    toe_path = toe_path.resolve()
    dir_path = Path(str(toe_path) + ".dir")
    toc_path = Path(str(toe_path) + ".toc")
    if not dir_path.is_dir():
        raise SystemExit(f"Expand first: toeexpand {toe_path}")
    if not toc_path.is_file():
        raise SystemExit(f"Missing toc: {toc_path}")

    proj = dir_path / "project1"
    proj.mkdir(parents=True, exist_ok=True)

    n_dst = proj / f"{OP_NAME}.n"
    parm_dst = proj / f"{OP_NAME}.parm"
    text_dst = proj / f"{OP_NAME}.text"

    shutil.copy2(TEMPLATE_DIR / "execute_startup.n", n_dst)
    shutil.copy2(TEMPLATE_DIR / "execute_startup.parm", parm_dst)
    text_dst.write_bytes(_text_blob(ON_START))

    rel = f"project1/{OP_NAME}"
    entries = [f"{rel}.n", f"{rel}.parm", f"{rel}.text"]
    lines = toc_path.read_text(encoding="utf-8", errors="replace").splitlines()
    existing = set(lines)
    # Append after .application — inserting before it breaks toecollapse on this TD build.
    for entry in entries:
        if entry not in existing:
            lines.append(entry)
            existing.add(entry)
    toc_path.write_text("\n".join(lines) + "\n", encoding="ascii")
    print(f"Injected {OP_NAME} into {dir_path}")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: inject_brikvj_autostart.py path/to/Project.toe")
    inject(Path(sys.argv[1]))


if __name__ == "__main__":
    main()
