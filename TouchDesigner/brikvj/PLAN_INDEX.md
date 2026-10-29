# BRIKVJ — master plan index

**Agents:** [AGENT_TD_POLICY.md](AGENT_TD_POLICY.md) — do not launch TouchDesigner without an explicit user ask.

**Single command for the next chat:**

```powershell
TouchDesigner/brikvj/scripts/brikvj_session_start.ps1
```

Then open **`logs/SESSION_BRIEF.md`** (kit or Documents).

---

## Document ladder (increasing depth)

| # | File | When to read |
|---|------|----------------|
| 0 | [PLAN_INDEX.md](PLAN_INDEX.md) | You are here |
| 1 | [NEXT_SESSION_PLAN.md](NEXT_SESSION_PLAN.md) | Quick triage only |
| 2 | [NEXT_SESSION_PLAN_DEEP.md](NEXT_SESSION_PLAN_DEEP.md) | Understand system + research protocol |
| 3 | [NEXT_SESSION_OPERATIONS.md](NEXT_SESSION_OPERATIONS.md) | **Execute work** (sprints, commands) |
| 4 | [NEXT_SESSION_PLAN_DEEPER.md](NEXT_SESSION_PLAN_DEEPER.md) | Meta loop — discover unknown work, closure graph |
| 5 | [NEXT_SESSION_PLAN_DEEPEST.md](NEXT_SESSION_PLAN_DEEPEST.md) | **Execute** — OPEN_WORK_QUEUE Sessions 1–3 |
| — | [RESEARCH_PASS_PLAN.md](RESEARCH_PASS_PLAN.md) | 12-session roadmap + research protocol |
| — | [RESEARCH_PASS_PLAN_DEEPER.md](RESEARCH_PASS_PLAN_DEEPER.md) | **Deepest** — taxonomy, transcript, 18 steps, matrix |
| — | [logs/RESEARCH_TAXONOMY.md](logs/RESEARCH_TAXONOMY.md) | Full unwired categories (`brikvj_research_taxonomy.ps1`) |
| — | [logs/RESEARCH_PASS.md](logs/RESEARCH_PASS.md) | Auto metrics (`brikvj_research_pass.ps1`) |
| — | [MASTER_PLAN.md](MASTER_PLAN.md) | Bugs + features + 6-session summary |
| — | [BUG_REGISTRY.md](BUG_REGISTRY.md) | Bug SSOT |
| — | [ADD_FEATURES.md](ADD_FEATURES.md) | How to add scenes, FX, lab, mega steps |
| — | [RESEARCH_BACKLOG.md](RESEARCH_BACKLOG.md) | RB-xxx queue |
| — | [WORKLOG.md](WORKLOG.md) | What already happened |
| — | [USER_REQUESTS.md](USER_REQUESTS.md) | User intent |
| — | [AGENTS_HANDOFF.md](AGENTS_HANDOFF.md) | Minimal agent entry |

## Auto-generated logs

| File | Generator |
|------|-----------|
| [logs/SESSION_BRIEF.md](logs/SESSION_BRIEF.md) | `brikvj_session_start.ps1` |
| [logs/GAPS_REPORT.md](logs/GAPS_REPORT.md) | `brikvj_gap_report.ps1` |
| [logs/RESEARCH_DIFF.md](logs/RESEARCH_DIFF.md) | `brikvj_research_diff.ps1` |
| [logs/CONTINUITY.json](logs/CONTINUITY.json) | `brikvj_session_start.ps1` (schema: [logs/CONTINUITY.schema.md](logs/CONTINUITY.schema.md)) |
| [logs/OPEN_WORK_QUEUE.md](logs/OPEN_WORK_QUEUE.md) | `brikvj_open_work_queue.ps1` |

## Human / live paths

| Role | Path |
|------|------|
| Perform SSOT | `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\` |
| Git kit | `TouchDesigner/brikvj/` in [briksquared/iKeleton-OSC](https://github.com/briksquared/iKeleton-OSC) |
| Harvest archive | `audio/ableton/github/_sweep3/touchdesigner` |

## Milestones (from OPERATIONS)

M1 stable open → M2 mega saved → M3 verify stack → M4 harvest wired → M5 Live optional → M6 git clean.

## Cursor transcript

`a38c1ae0-2c81-46db-8e9e-4ef553e7f5be` (agent-transcripts under `.cursor/projects`)

## Personal store

`BRIKVJ_NEXT_CHAT.md` in user agent store — paste prompt only.
