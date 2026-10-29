# BRIKVJ research pass (generated 2026-10-29T09:08:50.4459011-05:00)

Auto: `scripts/brikvj_research_pass.ps1`. Strategy: [RESEARCH_PASS_PLAN.md](../RESEARCH_PASS_PLAN.md).

## Measured kit (code SSOT)

| Metric | Value | Source |
|--------|------:|--------|
| SCENE_DEFS | 20 | `brikvj_resolume_stack.py` |
| FX_DEFS | 29 | same |
| Mega steps | 26 | `old_brik_vj_mega.py` |
| harvest_scene_expansion MAX | 14 | `brikvj_harvest_scene_expansion.py` |
| Live toe bytes | 8764772 | Documents BRIKVJ.toe |
| Unwired .tox | 123 | RESEARCH_DIFF |
| Newer than 2023 | 77 | RESEARCH_DIFF / TOX_BUILDS |
| Unwired Hydra-ish lines (in diff head) | ~76 | prefer lab lazy RB-004 |
| Unwired okVJ-Shared (in diff head) | ~21 | FX/scene candidates |
| Unwired brioch picks (in diff head) | ~3 | dedupe vs SCENE_DEFS |
| HARVEST_INDEX | indexed 2946, priority 235, archive tox 531 | HARVEST_INDEX.json |
| RESEARCH_BACKLOG open | 7 | RESEARCH_BACKLOG.md |
| gap_report exit | 1 | GAPS_REPORT.md |

## Parity snapshot

See [VJ_FEATURE_PARITY.md](../VJ_FEATURE_PARITY.md). **●** = in stack; **◐** = partial (plan targets below).

| Gap (◐) | Plan ID |
|---------|---------|
| HAP / codec tuning | DOC only — drop HAP in `media/clips/` |
| Text / logo TOP | F6 — TD Text + kantan |
| Synesthesia preset port | F6 — reference Synaesthesia.toe |
| MadMapper masking depth | F5 — kantan shapes audit |
| SMPTE / DMX | out of scope unless user asks |

## Integration candidates (next 5 — score before wire)

| Tox | Role | Notes |
|-----|------|-------|
| okVJ-Shared_colorizer.tox | FX | color grade gap | check TOX_BUILDS |
| okVJ-Shared_analogueWarmthFXStack.tox | FX | warmth stack | td2023 if newer |
| okVJ-Shared_dome_preview.tox | output | fulldome prep | RB-003 bank |
| brioch-audio-reactive-vjing_stroboscope.tox | scene | compare to scene_stroboscope | dedupe |
| okVJ-Shared_constructOutputMap.tox | map | kantan adjunct | research only |

## Bug scan (linked)

See [logs/BUG_SCAN.md](BUG_SCAN.md) and [BUG_REGISTRY.md](../BUG_REGISTRY.md).

## Recommended next sprint

**P0** — one mega save (headless/minimized once) then re-run this script.

## Doc ladder after this pass

1. RESEARCH_PASS.md (this file)
2. RESEARCH_PASS_PLAN.md (12-session roadmap)
3. RESEARCH_PASS_PLAN_DEEPER.md (taxonomy + transcript + 18-step program)
4. logs/RESEARCH_TAXONOMY.md (6 categories)
5. MASTER_PLAN.md
