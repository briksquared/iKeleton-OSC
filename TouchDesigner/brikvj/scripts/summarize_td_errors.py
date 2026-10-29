import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\logs\td_errors.txt"
text = open(path, encoding="utf-8", errors="replace").read()
if "OK — no op.errors" in text:
    print("0 errors")
    raise SystemExit(0)
ops = set()
for line in text.splitlines():
    m = re.match(r"(/\S+)\s", line)
    if m:
        ops.add(m.group(1))
print("%d error lines, %d operators" % (len(text.splitlines()), len(ops)))
for o in sorted(ops)[:20]:
    print(" ", o)
