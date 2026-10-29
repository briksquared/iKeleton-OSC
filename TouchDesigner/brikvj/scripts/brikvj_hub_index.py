# One-page map of the mega stack (show / practice / research).

HUB = """
BRIKVJ MEGA STACK — Old Brik V J
================================
SHOW (perform_out)
  brikvj_router/source_switch  0=Brioch  1=harvest Resolume stack  2=research lab
  old_brik_vj/scenes/scene_switch     generative + harvest_pick scenes
  old_brik_vj/clip_deck/clip_switch   8 media columns
  old_brik_vj/fx/fx_switch            post FX chain
  old_brik_vj/overlay_gen/overlay_switch   spiral/spinpulser overlay
  mapping/kantanMapper                projection map
  brikvj_broadcast/                   projectors + stream record

PRACTICE
  brikvj_lab/tools/tools_switch       fulldome, DJ, record, presets, stacker
  media/clips/                        drop MP4/stills for clip_deck
  brikvj_preset_bank                  scene/clip snapshots

RESEARCH / DEV
  brikvj_lab/hydra/hydra_switch       HydraTD + ojack module browser
  parts/harvest_pick/                 raw harvested .tox (not all loaded)
  parts/research/                     utilities copied from GitHub sweep
  scripts/old_brik_vj_mega.py         full rebuild
  scripts/resave_tox_for_td2023.py    silence newer-tox dialogs

KEYS: op('brikvj_key_help').text
LOGS: logs/build.log  logs/td_errors.txt
"""


def run():
    p = op("/project1")
    hub = p.op("brikvj_hub")
    if hub is None:
        hub = p.create(textDAT, "brikvj_hub")
    hub.text = HUB.strip()
    try:
        hub.viewer = True
        set_label(hub, "BRIKVJ hub — show / practice / research")
    except Exception:
        pass
    print("[BRIKVJ hub] op('brikvj_hub').text")


run()
