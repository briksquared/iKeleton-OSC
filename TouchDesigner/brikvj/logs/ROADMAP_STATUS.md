# BRIKVJ roadmap status (generated 2026-10-29T09:31:55.8528610-05:00)

Program: [RESEARCH_PASS_PLAN_DEEPER.md](../RESEARCH_PASS_PLAN_DEEPER.md) section E.

**Next step:** #2 Quiet open user check

| Step | Done | Milestone |
|------|:----:|-----------|
| 1 | yes | One mega save |
| 2 | **no** | Quiet open user check |
| 3 | **no** | MOTU 3-4 td_errors down |
| 4 | **no** | td2023 resave batch (5 used) |
| 5 | **no** | Integrate colorizer OR warmth |
| 6 | **no** | Integrate 2 harvest scenes |
| 7 | **no** | RB-004 lazy Hydra spec |
| 8 | **no** | RB-004 lazy Hydra impl |
| 9 | **no** | KEYBOARD_MAP vs scene_switch |
| 10 | yes | FEATURE_MATRIX synced |
| 11 | **no** | dome_preview eval |
| 12 | **no** | TDA mapper RB-005 |
| 13 | **no** | Ableton link RB-006 |
| 14 | **no** | preset_bank + hub |
| 15 | **no** | OSC + mapper doc |
| 16 | **no** | Taxonomy review |
| 17 | **no** | BUG_REGISTRY clean |
| 18 | **no** | Optional repo split RB-008 |

## Auto checks

| Check | Result |
|-------|--------|
| build.log clean | True |
| td_errors <= 25 lines | False |

## Integration queue (top 6)

| Rank | Target | Action |
|------|--------|--------|
| 1 | okVJ-Shared_colorizer.tox | FX_DEFS after td2023 check |
| 2 | okVJ-Shared_analogueWarmthFXStack.tox | FX_DEFS |
| 3 | okVJ-Shared_dome_preview.tox | F5 eval |
| 4 | brioch-audio-reactive-vjing_stroboscope.tox | dedupe scene_stroboscope |
| 5 | (56 hydra modules) | RB-004 lazy — no scene_switch bulk |
| 6 | parts/vj_suite/audio_crossover.tox | audio bridge |

Refresh: `brikvj_roadmap_status.ps1` after each session.
