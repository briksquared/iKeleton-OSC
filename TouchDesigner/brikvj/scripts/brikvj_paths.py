# BRIKVJ paths — one place. Runtime is always Documents; never iKeleton-OSC at show time.

import os

BRIKVJ_HOME = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ"
BRIKVJ_SCRIPTS = os.path.join(BRIKVJ_HOME, "scripts")
BRIKVJ_PARTS = os.path.join(BRIKVJ_HOME, "parts")
BRIKVJ_TOE = os.path.join(BRIKVJ_HOME, "BRIKVJ.toe")
BRIKVJ_LOGS = os.path.join(BRIKVJ_HOME, "logs")


def kit_root():
    """Harvest .tox / parts live under Documents after sync."""
    if os.path.isdir(BRIKVJ_PARTS):
        return BRIKVJ_HOME
    # Dev: running from a git checkout (folder name should be brikvj, not iKeleton).
    here = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(here)
    if os.path.isdir(os.path.join(parent, "parts")):
        return parent
    return BRIKVJ_HOME
