# Point clip_deck moviefilein TOPs at every file in BRIKVJ/media/clips (Resolume column fill).

import os

MEDIA = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\media\clips"
EXT = (".mp4", ".mov", ".avi", ".mkv", ".jpg", ".png", ".tif", ".webp")
FALLBACK = r"C:\Users\briks\Documents\TouchDesigner\BRIKVJ\testingVideo.mp4"


def log(msg):
    print("[BRIKVJ clips]", msg)


def collect():
    files = []
    if os.path.isdir(MEDIA):
        for f in sorted(os.listdir(MEDIA)):
            if f.lower().endswith(EXT):
                files.append(os.path.join(MEDIA, f).replace("\\", "/"))
    if not files and os.path.isfile(FALLBACK):
        files = [FALLBACK.replace("\\", "/")]
    return files


def run():
    vj = op("/project1/old_brik_vj")
    if vj is None:
        log("Run suite build first")
        return
    deck = vj.op("clip_deck")
    if deck is None:
        log("No clip_deck")
        return

    files = collect()
    if not files:
        log("Drop media into " + MEDIA)
        return

    for i in range(8):
        slot = deck.op("clip_%d" % i)
        if slot is None:
            continue
        mov = slot.op("player")
        if mov is None:
            continue
        path = files[i % len(files)]
        try:
            mov.par.file = path
            mov.par.play = 1
            mov.par.loop = 1
        except Exception as ex:
            log("clip_%d: %s" % (i, ex))
    log("Loaded %d unique files across 8 columns (%d on disk)" % (min(8, len(files)), len(files)))


run()
