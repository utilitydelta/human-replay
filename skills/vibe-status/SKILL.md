---
name: vibe-status
description: Show the current state of an autonomous vibe-coding session. Read-only. Reads SESSION_STATE.md, the progress log, and recent commits, then prints a one-screen summary. Invoke any time during a long-running session to check in.
---

# Vibe Status

Read-only snapshot of where the vibe-coding session is right now. No state changes. No agent spawns. Just print.

## What to do

1. Confirm we are in a sandbox (`.sandbox` marker present at the repo root). If not, say so and stop.
2. Read `docs/SESSION_STATE.md`. If missing, say so and stop.
3. Find the progress log at `docs/[feature-slug]-progress.md` (slug is in `SESSION_STATE.md` "Feature").
4. Run `git log --oneline -10` for recent commits.
5. Run `git status --short` for working tree state.
6. Print a single summary in this exact shape.

## Output format

```
# Vibe Status: [feature-slug]

## Where we are
- Current phase: [from SESSION_STATE.md "Current Phase"]
- Phases completed: [count] ([list, abbreviated])
- Phases remaining: [from "Next Actions"]
- Branch: [git branch name]
- HEAD: [short sha + commit subject]
- Working tree: [clean / N modified, M untracked]

## System Invariants in effect
[verbatim list from SESSION_STATE.md "System Invariants", short-name only]

## Last phase summary
[Most recent entry from progress log, compressed to 5-8 lines]

## Active stubs
[from SESSION_STATE.md "Active Stubs"]

## Recent commits
[last 5 oneline]

## Blockers / open questions
[from "Design Anchors" if any deferred items, or "none"]
```

## Rules

- Read-only. Never edit files. Never run validators. Never spawn agents.
- One screen of output. Compress aggressively. The human is checking in mid-run; they want a glance, not a report.
- If something is missing (no SESSION_STATE.md, no progress log, not in a sandbox), say so plainly and stop. Do not try to reconstruct state.
