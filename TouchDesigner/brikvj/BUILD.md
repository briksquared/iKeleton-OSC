# Build Old Brik V J

Ground truth: **Patchworks** → `patchworks/source/manuals/51-old-brik-vj.md`.

## Open

```
C:\Users\briks\Desktop\GitHub\audio\ableton\github\_sweep2\iKeleton-OSC\TouchDesigner\BRIKVJ.toe
```

Starts as Derivative’s **Setup/Base/NewProject** (empty `/project1`, ~770 bytes). Not Brioch, not iKeleton skeleton.

## Run once in TouchDesigner

1. **Text DAT** → paste `scripts/old_brik_vj_build.py` → **Run Script**.
2. **Text DAT** → paste `scripts/old_brik_vj_audio.py` → **Run Script**.
3. **Perform** → output **`perform_out`**.
4. **Ableton** → `ableton/ABLETON.md`.
5. **File → Save** `BRIKVJ.toe`.

Optional performance copy: `Documents\TouchDesigner\BRIKVJ\`.

## Swap the look

Replace `old_brik_vj/source/` with your own TOP chain (camera, GLSL, Syphon from Bitwig Grid export, etc.). Keep `old_brik_vj/glitch/out` as the perform feed.
