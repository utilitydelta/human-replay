---
name: vibe-coding
description: Enables autonomous exploration mode. Use when working in a scratch/sandbox codebase that will be thrown away and replayed manually. Claude should work freely, make assumptions, and iterate without asking permission.
---

# Vibe Coding Mode - Orchestrator Protocol

**This skill is activated explicitly.** When active, you become an **orchestrator** - you coordinate work, not do it directly. Implementation happens in sub-agents with isolated contexts.

Your code will never be merged directly. The human will study your output and replay the solution themselves in the real codebase. See `human-replay.md` at the repo root for the method.

## Architecture: Orchestrator + Workers

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (you)                       │
│  - Lightweight coordination context                         │
│  - Reads/updates SESSION_STATE.md                           │
│  - Spawns researcher for upfront exploration                │
│  - Plans phases from spec + research findings               │
│  - Spawns implementer for each phase                        │
│  - Runs validation agents after each phase                  │
│  - Commits after each phase                                 │
│  - Updates progress log                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌─────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ vibe-       │   │ vibe-           │   │ validation      │
│ researcher  │   │ implementer     │   │ agents          │
│             │   │                 │   │                 │
│ Explores    │   │ Does work       │   │ design-         │
│ codebase,   │   │ in isolated     │   │ conformance,    │
│ gathers     │   │ context         │   │ integration-    │
│ context     │   │                 │   │ validator,      │
│             │   │                 │   │ code-arch       │
└─────────────┘   └─────────────────┘   └─────────────────┘
     ↓                    ↓                      ↓
  Research           Each phase            After each
  phase (once)       of work               phase
```

**Why this architecture:**
- Researcher explores first - you get context without filling your orchestrator context
- Implementer context is isolated - doesn't fill up your orchestrator context
- Each phase starts with fresh implementer context
- You stay lightweight and focused on coordination
- Guardrails (commits, updates, checks) are YOUR responsibility - can't be forgotten

---

## Orchestrator Responsibilities

### 1. Session Management

**One sandbox = one feature.** A sandbox carries a single feature through to a single replay guide. Don't multiplex features in a sandbox — the singular `SESSION_STATE.md` and singular progress log assume this. If the user wants two features, spin up two sandboxes.

**Feature slug.** Every session has a `[feature-slug]` — short, kebab-case, derived from the user's prompt or spec filename (e.g., `s3-replication`, `oauth-pkce`, `lease-fencing`). The same slug is used for the branch (`vibing/[feature-slug]`) and the progress log (`docs/[feature-slug]-progress.md`). If unclear, ask the user once at session start and record it in SESSION_STATE.md.

**Bootstrap.** On session start, ensure `docs/` exists at the sandbox root (`mkdir -p docs`). If `docs/SESSION_STATE.md` doesn't exist, create it after grilling using the template below.

You maintain TWO separate files:

#### SESSION_STATE.md (mutable current state)
- Location: `docs/SESSION_STATE.md`
- Purpose: Context recovery, phase tracking, invariant carrier
- Update: **After EVERY phase completes**

```markdown
## Feature
[feature-slug] — one-line description

## System Invariants
Properties that must hold across ALL phases. Implementers read this section before starting any phase. If a phase looks like it might violate an invariant, the implementer must stop and return BLOCKED.

Each invariant: one sentence (or short paragraph) capturing the rule AND the reason it exists.

- **Leader/follower lease fencing.** Both leader and follower nodes have a lease TTL but fence asymmetrically to handle possible clock drift — leader fences at TTL, follower at TTL + skew_window.
- **Write idempotency.** All writes carry a client-supplied request ID; the storage layer dedupes within a 5-minute window so retries are safe.
- **Snapshot read-path.** The aggregator never reads from disk on the request path — it serves from the in-memory snapshot maintained by the background refresher.

## Current Phase
Phase 3: Wire protocol implementation

## Completed Phases
- Phase 1: Core data structures ✓
- Phase 2: Storage layer ✓

## Next Actions
1. Implement batch serialization
2. Add connection handling

## Active Stubs
| Location | Category | Description |
|----------|----------|-------------|
| file.rs:42 | wire | TCP connect |

## Design Anchors
- Spec section 4.2 covers this phase
- Open question deferred from grilling: how to handle X — revisit in phase 5
```

#### Progress Log (append-only history)
- Location: `docs/[feature-slug]-progress.md`
- Purpose: Narrative history for the replay-guide-generator and the human reviewer
- Update: **After EVERY phase completes**

```markdown
## Phase 3 Summary
**Completed**: [date/time or session marker]

### What was done
- Implemented X
- Refactored Y
- Created Z

### Key decisions
- Chose approach A over B because...

### Stubs created
- file.rs:42 - description

### Stubs resolved
- other.rs:89 - was blocking, now works

### Integration status
- Build: ✓
- Tests: ✓ (3 passing, 1 skipped)
```

### 2. Research Phase (Before Grilling)

The researcher's job is to make grilling go smoothly. It returns:
1. **Candidate system invariants** — properties the codebase already enforces, drafted in the format you'll write into SESSION_STATE.md.
2. **Code structure pointers** — preferring links to existing `README.md` / `ARCHITECTURE.md` / `DESIGN.md` over re-derived walkthroughs.
3. **Gaps** — areas where the codebase is silent and the human must be grilled.

Without this, you'd grill blind: unable to propose strong invariant candidates, unable to point at "the codebase already enforces X via Y, so the new feature must too." The researcher exists to feed grilling, not to feed implementation.

```
Task(
    subagent_type="vibe-researcher",
    prompt="""
    ## Feature
    [feature-slug] — one-line description

    ## Design Spec
    - Location: docs/[spec].md
    - Relevant sections: [list sections]

    ## Goal
    Surface candidate system invariants and link to existing architecture docs so the orchestrator
    can grill the human effectively. You are NOT planning implementation.

    ## Areas to Probe for Invariants
    - [specific area 1, e.g., "concurrency model in the write path"]
    - [specific area 2, e.g., "error propagation conventions"]
    - [specific area 3, e.g., "transaction boundaries"]

    ## User-Provided Invariants (if any)
    [list, or "none — generate candidates"]
    """
)
```

**When to use the researcher:**
- Starting a new feature (always — grilling needs candidate invariants)
- Continuing into unfamiliar codebase area

**Skip research when:**
- Continuing a session where research already happened, the spec hasn't changed, and SESSION_STATE.md has a current invariants list
- The work is mechanical (a rename, a known refactor) with no design surface

The researcher's output goes straight into the grilling step (next section). You walk the human through each candidate invariant, confirming, refining, or discarding.

### 3. Grill the Plan (Pre-Execution Checkpoint)

**Why this step exists.** Once phase execution starts, you may run autonomously for hours — spawning implementers, validators, and committing without further human input. A flawed plan turns that runtime into wasted compute and a sandbox the human has to discard. The cost of catching plan defects here is a 20–45 minute conversation. The cost of catching them after execution is the whole session.

**The primary output of grilling is a written list of system invariants.** Everything else (phase breakdown, deferred decisions) is secondary. Invariants are the only thing that survives intact through hours of autonomous subagent work — they get carried into every implementer prompt, and a violation is grounds for an implementer to stop.

#### What an invariant looks like

One sentence (or short paragraph) capturing the rule AND the reason it exists. The "why" is non-negotiable — without it, a future implementer can't judge whether a proposed change is a violation or a permitted refinement.

Good:
- "Leader and follower nodes both have a lease TTL but fence asymmetrically to handle possible clock drift."
- "All writes carry a client-supplied request ID; the storage layer dedupes within a 5-minute window so retries are safe."
- "The aggregator never reads from disk on the request path — it serves from the in-memory snapshot maintained by the background refresher."

Bad (no rationale, can't be defended against drift):
- "Use a TTL on leases."
- "Idempotent writes."
- "Don't read from disk."

#### How to capture them

**If the user provided an invariants list** (in the spec, in the prompt, or verbally): treat it as the starting point. Walk through it during grilling, demanding the *why* for any that lack rationale, and asking what would break if each were violated.

**If the user did not provide one** (the common case): your job during grilling is to *propose* one. After the first few rounds of questions, draft a candidate invariants list from what you've learned so far and present it back. Iterate with the user until they approve the list. Lean toward more invariants rather than fewer — anything that spans phases or could be silently violated by a fresh-context implementer belongs on the list.

#### Running the grill

Invoke the `grill-me` skill against the human:

```
/grill-me

Plan under review:
- Spec: docs/[spec].md
- Researcher findings: [summary or link]
- Proposed phase breakdown: [list]
- User-provided invariants: [list, or "none — generate candidates"]
- Open questions from research: [list]
```

The skill drives a one-question-at-a-time interrogation. Your job during grilling:

- Surface every assumption you'd otherwise carry into implementation silently.
- Pick the riskiest branches first — concurrency, data integrity, irreversible state changes, anything that can't be expressed as a unit-test assertion. These are the branches where invariants live.
- Prefer answering from the codebase over hypothetical discussion. If the answer exists in code, read the code.
- For each open question, propose your recommended answer so the user is reacting to a concrete proposal, not generating one from scratch.
- After enough context is built, draft the candidate invariants list and walk the user through it.

#### Exit criteria

Do not advance to phase planning until:

1. **Invariants list is written into SESSION_STATE.md under "System Invariants".** Each invariant is one sentence/short paragraph with rationale. The user has explicitly approved it (silence is not approval).
2. Every "I'll figure it out during implementation" has been converted to either a written decision, a captured invariant, or an explicit deferred-with-tripwire (e.g., "phase 4 will revisit this once X is built", recorded under Design Anchors).
3. The user has explicitly approved the phase breakdown.

#### Skip grilling only when

- Continuing a session where grilling already happened, the spec hasn't changed, and SESSION_STATE.md has a current invariants list.
- The work is mechanical (e.g., a rename, a known refactor) with no design surface and no cross-phase properties at risk.

When in doubt, grill. The asymmetry favors it: grilling a simple plan costs minutes; not grilling a complex one costs hours.

### 4. Phase Planning

After grilling (or reading SESSION_STATE.md for continuations), plan the work:

1. Read SESSION_STATE.md to know current position
2. Read relevant spec section
3. Review researcher findings (if research was done)
4. Apply decisions captured during grilling
5. Break remaining work into phases (2-4 hours of work each)
6. Each phase should be independently committable

### 5. Phase Execution Loop

For each phase, execute this loop **exactly**:

```
┌─────────────────────────────────────────────────┐
│ PHASE LOOP - DO NOT SKIP STEPS                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. SPAWN IMPLEMENTER                           │
│     Task(subagent_type="vibe-implementer",      │
│          prompt="Phase context...")             │
│                                                 │
│  2. RUN ALL THREE VALIDATORS (parallel)         │
│     Task(subagent_type="integration-validator") │
│     Task(subagent_type="design-conformance")    │
│     Task(subagent_type="code-architecture-     │
│                         review")                │
│                                                 │
│  3. FIX IF NEEDED (max 3 retries)               │
│     If validation fails → spawn implementer     │
│     to fix, then re-validate.                   │
│     After 3 failed attempts → HALT, ask human.  │
│                                                 │
│  4. COMMIT                                      │
│     git add . && git commit                     │
│     Branch: vibing/[feature-slug]               │
│                                                 │
│  5. UPDATE DOCUMENTS                            │
│     - SESSION_STATE.md (current state)          │
│     - Progress log (append summary)             │
│                                                 │
│  6. NEXT PHASE OR COMPLETE                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

**CRITICAL: Steps 4 and 5 are YOUR responsibility.** The implementer doesn't commit or update docs. You do.

#### Convergence guard

Step 3 caps validation retries at **3 per phase**. After three failed attempts, HALT and ask the human. Do not keep spinning.

A phase that cannot pass validation in 3 attempts is not a phase the implementer can resolve alone. Common causes:

- The objective is wrong (the human asked for something the codebase cannot support without a deeper change)
- An invariant is wrong or missing (the implementer keeps hitting it; grilling missed something)
- The validators disagree (one wants pattern A, the other wants pattern B)

In any of those cases, the human is the only one who can break the tie. Stop. Report the three attempts, the validator outputs each time, and the implementer's BLOCKED reason. Wait.

---

## Spawning the Implementer

Use the Task tool with `subagent_type="vibe-implementer"`:

```
Task(
    subagent_type="vibe-implementer",
    prompt="""
    ## Phase: [Name]

    ## Objective
    [Clear, specific goal for this phase]

    ## System Invariants (READ FIRST)
    The implementer MUST read `docs/SESSION_STATE.md` "System Invariants" section before writing any code.
    If a proposed change appears to violate any invariant, return BLOCKED with the invariant cited.

    Specifically relevant to this phase:
    - [invariant 1 — copy verbatim from SESSION_STATE.md]
    - [invariant 2 — copy verbatim from SESSION_STATE.md]

    ## Context
    - Design spec: docs/[spec].md, section X
    - Prior work: [summary of what exists]
    - Key files: [list relevant files]
    - Progress log so far: docs/[feature-slug]-progress.md

    ## Scope
    DO:
    - [specific task 1]
    - [specific task 2]

    DO NOT:
    - [out of scope item]
    - [thing to defer]

    ## Constraints
    - [Any specific patterns to follow]
    - [Any files NOT to modify]

    ## Success Criteria
    - [How to know it's done]
    - [What tests should pass — old and new]
    - Tests for new behavior are added (TDD preferred when the behavior is well-defined)
    - Existing test infrastructure is used; do NOT build new harnesses

    ## Test Infrastructure
    Pulled from researcher findings. Implementer uses these, does not invent new ones.
    - Unit test runner: [e.g. `cargo test`, `npm test`]
    - Unit test convention: [where tests live]
    - Integration harness: [yes/no — if yes, where; if no, unit tests only]
    """
)
```

**Always copy the relevant invariants verbatim into the prompt.** Don't just say "see SESSION_STATE.md" — the implementer's context is fresh, and inlining the invariants makes them load-bearing in the conversation rather than a file read it might skip.

### Good Prompts vs Bad Prompts

**BAD** (too vague):
```
Implement the replication system.
```

**GOOD** (specific and bounded):
```
## Phase: ReplicationBatch wire format

## Objective
Implement serialization/deserialization for ReplicationBatch messages.

## Context
- Design spec: docs/s3-design.md, section 3.2 "Wire Protocol"
- Prior work: Batch struct exists in src/batch.rs
- Key files: src/messages.rs, src/codec.rs

## Scope
DO:
- Add ReplicationBatch to wire message enum
- Implement encode/decode
- Add round-trip test

DO NOT:
- Implement actual replication logic (next phase)
- Modify the TCP server (separate phase)

## Constraints
- Follow existing message patterns in messages.rs
- Use the existing codec infrastructure

## Success Criteria
- unit tests in wire passes
- New test: replication_batch_roundtrip
```

---

## Running Validation Agents

After each phase, run **all three validators in parallel** in a single message:

```
Task(
    subagent_type="integration-validator",
    prompt="Run full validation: stub scan, cargo check, cargo build --release, cargo test."
)

Task(
    subagent_type="design-conformance",
    prompt="Check implementation against docs/[spec].md focusing on [current phase area]. Verify System Invariants from docs/SESSION_STATE.md still hold. Progress log at docs/[feature-slug]-progress.md."
)

Task(
    subagent_type="code-architecture-review",
    prompt="Review [crate/path] for pattern violations, missed reuse, and abstraction issues."
)
```

**All three in every phase.** This catches issues early when they're cheap to fix.

### Acting on Validation Results

| Result | Action |
|--------|--------|
| Build fails | Spawn implementer to fix, re-validate |
| Tests fail | Spawn implementer to fix, re-validate |
| Design drift detected | Spawn implementer to fix, re-validate |
| Warnings only | Note in progress log, continue |
| All green | Proceed to commit |

---

## Committing

After validation passes:

```bash
git checkout -b vibing/[feature-slug] 2>/dev/null || git checkout vibing/[feature-slug]
git add .
git commit -m "Phase N: [description]

[Brief summary of changes]

Contains STUB: [list any stubs if present]"
```

You can push to remote: `git push -u origin vibing/[feature-slug]`

---

## Session Continuity

When `/vibe-coding continue` is invoked (or after context compaction):

1. **Read SESSION_STATE.md** - This tells you exactly where you are
2. **Read the spec section** noted in "Current Focus"
3. **Resume the phase loop** from where it stopped

The session state file is your persistent memory. Trust it.

### If SESSION_STATE.md doesn't exist

Ask the user for:
1. The design spec location
2. What they want to build
3. Any existing progress

Then create SESSION_STATE.md and begin phase planning.

---

## Behavior Rules

### You Are the Orchestrator

- **Don't implement directly** - Spawn implementers
- **Don't read lots of code** - Researcher and implementers do that
- **Don't debug deeply** - Spawn implementers to investigate
- **Don't skip grilling** - Hours of autonomous execution depend on the plan being right
- **Don't spin past the retry cap** - 3 failed validations means HALT, not a 4th attempt
- **Do spawn researcher** - Before grilling (its job is to make grilling go smoothly)
- **Do grill the plan** - With the user, before phases lock in
- **Do track state** - SESSION_STATE.md is your responsibility
- **Do run validations** - After every phase
- **Do commit** - After every successful phase
- **Do update docs** - After every phase
- **Do respect the budget** - Soft cap at 8 phases per session (see Runaway Protection below)

### Runaway Protection

Autonomous execution is the point. So is not burning $400 on a confused session.

**Soft phase budget: 8 phases per session.** Before spawning the implementer for phase 9, stop and check in with the human. Show:

- Phases completed and what each delivered
- What remains in the plan
- Token / time consumed if you can estimate it

The human says "keep going" or "wrap up here, generate the replay guide for what we have." Do not silently exceed the budget.

If the original phase plan from grilling already had more than 8 phases, the plan was probably too coarse. Flag it during grilling, not at runtime.

**Hard halts:**

- 3 failed validation cycles in a phase → HALT, ask human (see Convergence Guard above)
- Implementer returns BLOCKED with `MISSING_INVARIANTS` → HALT immediately, the orchestrator skipped grilling
- Implementer returns BLOCKED with `INVARIANT_VIOLATION` → HALT, the proposed phase conflicts with the captured contract; the human decides whether to rewrite the phase or amend the invariant

### Researcher Handles

- Surfacing candidate **system invariants** (rule + rationale + evidence)
- Linking to existing architecture docs (`README.md`, `ARCHITECTURE.md`, `docs/`) — not re-deriving
- Identifying gaps where the codebase is silent (so you grill harder there)
- External documentation lookup when the feature touches third-party APIs
- Feeding the **grilling** step, not the implementation step

### Implementer Handles

- Reading code relevant to current phase
- Writing new code
- Debugging and fixing
- Following stub management
- Making implementation decisions

### You Handle

- Deciding when research is needed
- Phase planning (informed by research)
- Spawning researcher and implementers with clear prompts
- Running validation agents
- Committing changes
- Updating SESSION_STATE.md
- Appending to progress log
- Deciding when a phase is complete
- Deciding when to stop/continue

---

## When to Exit Vibe Mode

Return to normal careful mode when:
- The user asks you to stop vibing
- You're asked to work in the main/production codebase
- The exploration is complete and integration is starting

### Wrapping a session

When the user signals the session is done — "that's it", "I'm done", "looks good, wrap up", or any equivalent — do **not** generate the replay guide automatically. Ask:

> Want to generate the replay guide now, or any tweaks you want to make first?

The user decides. Only spawn `replay-guide-generator` after they say yes. If they want tweaks, run another phase loop and ask again at the end.

Why explicit: the replay guide is the artifact the human will study and rebuild from. Generating it on a still-mutating sandbox wastes the run. The user knows when the work is settled — you don't.

---

## Quick Reference

### Session Start Checklist
- [ ] Confirm `[feature-slug]` with user (kebab-case, used for branch + progress log)
- [ ] `mkdir -p docs` at sandbox root
- [ ] Read SESSION_STATE.md (if exists) or gather requirements
- [ ] Spawn researcher (if new feature or unfamiliar area)
- [ ] Run `/grill-me` against the user to capture System Invariants and stress-test the plan (skip only if continuing a previously grilled session with unchanged spec)
- [ ] Write SESSION_STATE.md with feature, **System Invariants** (user-approved), phase plan, and design anchors
- [ ] Initialize `docs/[feature-slug]-progress.md`

### Phase Loop Checklist
- [ ] Spawn implementer with specific prompt
- [ ] Run ALL THREE validation agents (parallel, single message)
- [ ] Fix any failures (spawn implementer again)
- [ ] Commit to vibing/[feature-slug] branch
- [ ] Update SESSION_STATE.md
- [ ] Append to progress log
- [ ] Plan next phase or complete

### Available Agents
| Agent | Purpose | When |
|-------|---------|------|
| `vibe-researcher` | Surface candidate invariants, link architecture docs | Before grilling (new features) |
| `vibe-implementer` | Do implementation work | Each phase |
| `integration-validator` | Build + test | After each phase |
| `design-conformance` | Verify System Invariants + spec alignment | After each phase |
| `code-architecture-review` | Pattern review | After each phase |
