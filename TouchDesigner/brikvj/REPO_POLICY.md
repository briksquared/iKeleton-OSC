# BRIKVJ repo policy

**Do not** treat `iKeleton-OSC` or `_sweep2` as the product home. That was a mistaken parking spot for git.

| Role | Location |
|------|----------|
| **Show / TouchDesigner** | `C:\Users\briks\Documents\TouchDesigner\BRIKVJ\` |
| **Scripts + parts at runtime** | Under that folder after `sync_scripts_to_documents.ps1` |
| **Git** | Should be a repo named **BRIKVJ** (or your monorepo path you choose) — not buried under an OSC skeleton repo name |

Agents: never copy `BRIKVJ.toe` back into iKeleton-OSC, never hardcode `_sweep2/iKeleton-OSC` in Python build paths, never commit the kit there without an explicit user request.
