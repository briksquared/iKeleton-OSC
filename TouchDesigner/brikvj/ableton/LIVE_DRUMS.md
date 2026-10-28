# Live drums → BRIKVJ (already wired in TD)

## Sample

`brikvj/ableton/samples/brikvj_drum_loop.mp3` (also in **User Library → Samples → brikvj_drum_loop**)

## Live

1. Open **`BRIKVJ_Drums_TDAbleton.als`** (Documents `TouchDesigner/BRIKVJ/ableton/` or repo `brikvj/ableton/`).
2. Drag **`brikvj_drum_loop`** from User Library **Samples** onto an **Audio** track (or Session clip slot).
3. Loop the clip; press **Play**.
4. Ensure **TouchDesigner** control surface is enabled; **TDA_Master** on Master (from demo set or User Library **TDAbleton**).

## TouchDesigner

**BRIKVJ.toe** is patched: `/project1/analyseAudio/audioAnalysis/audiofilein1` plays the same drum loop and drives Brioch scenes (stroboscope, mesh, etc.).

Reload the project if it was open before the patch (File → Open `BRIKVJ.toe`).

Optional: run **`live_drum_to_td.py`** in a Text DAT to re-point the file or switch to M4 loopback from Live.
