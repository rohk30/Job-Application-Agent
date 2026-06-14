# Session Log Guidelines — ApplyMate

Logs live under `Logs/<date>/session_<n>.md`.
Every working session gets its own file. Do not merge sessions into one file.

---

## File Naming

```
Logs/
  <month_day>/
    session_1.md
    session_2.md
    ...
```

Examples: `april_3/session_1.md`, `april_7/session_2.md`

---

## Long Session Log (> ~1.5 hrs or major feature work)

Use this format when a session involves building a new feature, fixing a chain of bugs, or making architectural decisions.

```
# Session Log — <Month Day> | Session <N>

## Overview
1–3 sentence summary of what this session set out to do and whether it succeeded.

---

## Environment / Setup Changes
Any new packages installed, env variables set, Docker changes, config changes.
Include the exact install command (e.g. `uv add <pkg>`).

---

## Files Created
List every new file added and its purpose in one line.

---

## Files Modified
List every modified file and what changed (brief, not line-by-line).

---

## Database Changes
- Migrations created: filename + what it does
- Schema changes: new columns, constraints, index changes
- Any manual DB operations run (inserts, deletes, fixes)

---

## Issues Fixed
For each bug:
- What the problem was
- Root cause
- Fix applied
- Why that fix (reasoning, not just what)

---

## Decisions Made
Design or architectural decisions taken this session and the reasoning behind them.
If a decision was explicitly deferred, note it here too with why.

---

## Current Extraction / Feature State
A quick table or bullet list showing what's working vs not.
Example:
| Feature       | Status         |
|---------------|----------------|
| Name extract  | ✅ Working     |
| Skills        | ✅ 16 detected |
| Projects      | ⚠️ Partial     |

---

## Deferred / Known Issues
Things that were noticed but intentionally left for later.
Tag each with priority: 🔴 Urgent / 🟡 Later / 🟢 Nice to have

---

## Run Commands
Any commands needed to reproduce or continue the work.
Always include PYTHONPATH, working directory, and the full command.

---

## Next Steps
What to pick up at the start of the next session, in priority order.
```

---

## Short Session Log (< ~1 hr or isolated task)

Use this format for quick fixes, single-file changes, config updates, minor additions, or tooling work (e.g. git, migrations, dependency installs).

```
# Session Log — <Month Day> | Session <N>

## What Was Done
Bullet list. One line per action. Be specific — file names, table names, command names.

## Why
Brief reasoning if not obvious.

## Files Touched
- `path/to/file.py` — what changed

## Commands Run (if any)
Exact commands in code blocks.

## Issues Hit (if any)
Problem → Fix, one line each.

## Next Steps
What comes next, 2–3 bullets max.
```

---

## General Rules (apply to both formats)

### Always include
- Date and session number in the heading
- Every file that was created or modified
- Every migration created and applied
- Any manual DB operations (even small ones like seed inserts or deletes)
- The working directory and PYTHONPATH for any non-obvious commands
- Explicit note if Docker needs to be running for anything

### Never skip
- Root cause of bugs, not just the fix — future-you needs to understand *why*
- Deferred decisions — if you chose not to do something, write it down with the reason
- Environment quirks — e.g. `uv` instead of `pip`, specific PYTHONPATH setup, model download on first run

### Naming consistency
- Use the actual file names, table names, column names, and migration IDs — not vague descriptions
- Use ✅ / ⚠️ / ❌ for status tables to make them scannable

### Design decisions worth logging
- Why a particular DB constraint was or wasn't added
- Why deduplication was or wasn't implemented
- Why a specific library or model was chosen
- Any intentional deviation from the planned architecture

### What goes in "Next Steps"
- Only actionable items
- Ordered by priority
- If a next step was carried over from the previous session unchanged, note that

---

## Project-Specific Reminders

- Always run alembic from `backend/` with `PYTHONPATH=<root>\backend`
- Docker container must be running before any alembic or DB operation
- Embedding model (`all-MiniLM-L6-v2`) must be pre-downloaded — first import hangs silently if not cached
- All imports use `backend.*` prefix consistently — do not mix with relative `db.*` imports
- `uv` is the package manager — do not use `pip`
- Resume PDFs are never committed to git (`.gitignore` covers `*.pdf`)
- Resume history is intentionally kept — no deduplication on embeddings, experience, or education rows
