---
name: generate-replay-guide
description: Generate a Human Replay Guide from a sandbox build-out — the ordered, validated rebuild path the human replays Tab by Tab. Best run by the implementer at the end of the build, while its context is still hot; also runs cold from a fresh session with the base commit.
---

**Who runs this, and when.** The best guide comes from the agent that just
built the work, generated before it completes — the hot build context is the
asset, and a cold context reconstructing the build produces a worse guide than
the agent that just walked it. Run inline by default. Spawn a general-purpose
subagent carrying these instructions and the base commit only when the
remaining context cannot hold this skill plus the guide — the guide file is
the only thing that needs to come back. A cold run from a fresh session works
too; expect to lean harder on the diff and the goal.

# Replay Guide Generator

You analyze the final state of a sandbox build-out and produce an ordered guide for a human to rebuild it from scratch in their real codebase.

How the sandbox was built is not the guide's concern. One agent or ten, orchestrated or freehand, any method — the guide is built from the final state, the diff, and the goal. It is not a transcript. It is the path a knowledgeable pair programmer would have taken from the start. Skip dead ends. Skip refactoring loops. Teach the destination.

## Five rules

1. **Optimize the destination, not the journey.** If the session tried A then B, teach B.
2. **Dependency-first ordering.** Types before functions. Interfaces before implementations. Nothing references something not yet built.
3. **Cluster by concern.** Group related changes by feature, not file. Humans think in concepts.
4. **Teach the design, not the code.** The human reads the source themselves. Your job is the *why*.
5. **Retrospectives are mandatory.** Every step asks questions that force the human to reason about what they just built.

## What goes in, what comes out

**Inputs:**

1. `git diff {base}..HEAD` — the actual changes. This is the ground truth.
2. The goal (`session/goal.md` or equivalent), if it exists — the captured intent.
3. Your own memory of the build, when you are the implementer generating hot.

**Not inputs: the session's trail docs.** `session/session-state.md`, `session/progress.md`, `session/scraps.md`, progress logs, any session narrative. The trail is gradient descent — wrong turns, backtracks, dead spikes — and a guide derived from it teaches the journey. The guide teaches the destination. The settled code and the goal are the only sources.

**Output:**

`session/replay-guide.md` — the rebuild path.

If no goal exists and you are running cold, generate from the diff and the commit log alone, and say so prominently in the overview. The human needs to know they are reconstructing intent from code rather than reading captured intent.

## Workflow

### 1. Read the goal

```bash
git log --oneline {base}..HEAD
```

From the goal (and your own build memory, when hot), extract:

- **System invariants / design constraints.** If the goal states properties that must hold, carry them forward verbatim. If it doesn't, derive the load-bearing constraints from the code and label them as reconstructed.
- **Key decisions.** "Chose X over Y because…" is the hidden context the human needs. Hot, you know these; cold, take what the goal and the code make obvious.
- **The journey filter.** Hot, you know what was tried and abandoned — teach the destination anyway. Cold, commit messages hint at the journey; use them only to skip it, never to narrate it.

If the goal contradicts the diff (e.g. it claims X but X is missing), trust the diff and flag the discrepancy. Usually means a later refactor undid earlier work.

### 2. Analyze the diff

```bash
git diff {base}..HEAD --stat
git diff {base}..HEAD
```

Pull out:

- Files: new, modified, deleted
- Structural changes: types, traits, classes, modules, public functions
- Dependencies: type A uses type B, function X calls function Y, module M imports N

### 3. Detect domain

Skim the codebase and decide which retrospective templates to draw from. Most projects span multiple domains. Tag each cluster with its primary one.

| Domain | Indicators |
|---|---|
| Frontend | React/Vue/Angular, CSS, DOM, state libs |
| Backend API | REST/GraphQL, middleware, auth, request handlers |
| Database | Migrations, queries, ORM, indexes |
| Infrastructure | Terraform, Docker, K8s, CI/CD |
| Real-time / HFT | WebSockets, event loops, latency-critical paths |
| ML / Data | Models, pipelines, feature engineering |
| CLI | Argument parsing, output formatting |

### 4. Cluster by layer

Group changes by what they are, not what file they live in. A feature spanning models and API gets split across two clusters with a dependency edge between them.

| Layer | Examples |
|---|---|
| Data Models | Types, structs, enums, schemas |
| Traits / Interfaces | Contracts between components |
| Core Logic | Business rules, algorithms |
| Integration | Glue between components |
| API Surface | Public exports, endpoints |
| Infrastructure | Config, build, CI |
| Tests | Verification |

Smaller clusters with clear boundaries beat large mixed ones.

### 5. Order by dependency

Topological sort within and across clusters. If you find a cycle, flag it for the human to resolve. Cycles in the dependency graph almost always indicate a missed abstraction.

### 6. Write the guide

Output to `session/replay-guide.md`. Use the template below.

## Output template

The guide is read by a technical person mid-replay with no time to waste. Write
accordingly, and hold these rules for every Why, Overview, and Manual bullet:

- Problem first: lead with why the change exists, then what it is. One or two
  sentences per Why; a step earns more length only by what it teaches.
- Short paragraphs, no filler, no hedging, no fake balance. State the
  consequence plainly and trust the reader to draw the conclusion.
- No LLM tics: no "The key insight:", no "It's important to note", no
  "delve/comprehensive/robust", no em dashes, no wrap-up sentences that restate
  the step. End blunt.
- Retrospectives are ONE probing question that forces reasoning about what was
  just built, not an essay and not a quiz with an obvious answer.
- No big code blocks. Files referenced as `path/to/file.ts:42` so the human can
  ctrl+click. If a step needs more than 5 lines of code to communicate, the Why
  is wrong; rewrite it.

```markdown
# Replay: {feature-slug}

> The path a knowledgeable pair programmer would take from `{base-sha}` to here.
> Not a transcript of the sandbox session.

## Overview

**Built:** {one-paragraph summary, pulled from the goal + diff}

**Files affected:** {count}, across {N} layers.

**Time estimate for replay:** ~{N}h. (Faster if you have full context. Slower the first time.)

**Key decisions:**

- {decision 1, with one-sentence rationale}
- {decision 2}
- ...

{If no goal existed and the run was cold:}
> ⚠️ This guide was generated from the diff and commit log alone. Invariants and decisions are reconstructed from code, not from captured intent. Verify against your own understanding of the goal before trusting the structure.

## System Invariants

These hold across the entire feature. Every phase below is bound by them. If your replay diverges from the AI's approach, your divergence must still satisfy these.

- **Rule name:** reason it exists
- **Another rule:** its reason

{Verbatim from the goal when it states them; otherwise reconstructed from code and labeled as such. The bold rule name must be clean — no trailing period, backticks, or other punctuation — and must match each step's **Invariants:** reference verbatim (case-insensitive).}

## Dependency graph

\`\`\`mermaid
graph TD
  P1[Phase 1: Data Models] --> P2[Phase 2: Core Logic]
  P2 --> P3[Phase 3: API Surface]
  P3 --> P4[Phase 4: Tests]
\`\`\`

---

## Phase {N}: {Cluster name}

**Layer:** {Data Models / Core Logic / API Surface / ...}
**Domain:** {frontend / backend / database / ...}
**Prerequisites:** {Phase X, Phase Y, or "none"}
**Estimated time:** ~{N} minutes

### Step {N}.{M}: {What you are building}

**Symbol:** `{exact_function_name}`
**File:** `path/to/file.rs:42`
**Action:** Create | Modify | Delete | Create File | Patch

**Why:** {One or two sentences. Pull from the goal or your build memory when available. The human is reading this to understand the design, not to copy code.}

**Invariants:** {Comma-separated rule names that match the System Invariants headings verbatim, e.g. `Single writer, Confirmed before acked`. Or omit the line.}

**What to write:**

- {Specific signature, type, or function name. Reference existing code: `other/file.rs:88`.}
- {Another concrete sub-task with file:line links.}
- {Avoid pasting code blocks larger than 3-5 lines. The human can open the file. Show the *shape*, not the body.}

**Verify:**

- [ ] {Concrete check: "Run `cargo check`", "Open the page and click X", "Curl the endpoint and assert 200"}
- [ ] {Another}

**Retrospective:** {One step-specific question about a design choice or failure mode this code makes — a single line. The replay tool surfaces it at the step boundary.}

{Optional extra questions as bullets below — the human reads them, the tool ignores them:}
- {Domain-relevant question about edge cases}
- {Question that challenges the approach: "Is this the right shape?"}

---

### CHECKPOINT: Phase {N} complete

**Understanding check:**

- Can you diagram what you just built without looking?
- Can you explain to a colleague why each piece exists?
- What would break if you removed any single component?

**Design critique:**

- Did the AI's approach feel right, or would you do it differently?
- Are there edge cases the AI might have missed?
- Is this the simplest solution, or is there unnecessary complexity?

**Claimed-safe properties:**

- [ ] {For each property this phase claims is unaffected: the command that proves it and the expected number. No runnable check, no claim.}

**Divergence notes:** _______________

---

{Repeat for each phase}

## Closing

You walked the territory. The codebase is yours. Delete the sandbox.
```

## Machine-replayable guides (human-replay-vscode-extension)

When the guide will be driven by the `human-replay-vscode-extension` (not just read by a
human), it must be *resolvable*, not just readable. The extension never trusts the
guide's prose for code — it resolves each step's bytes from real files:

- **Before** = the symbol as it stands in the **target** repo (the workspace the human
  opens and edits).
- **After** = the symbol in the **sandbox** (`replayTab.sandboxRoot`).

So you do not paste code. You name the symbol and the file, and the tool reads both.
The rules that follow:

1. **Every step carries `**Symbol:**` (exact name) + `**File:**` (path from the repo
   root) + `**Action:**`.** No Symbol → the tool can't resolve the step. The diff-replay
   then drives Before→After in place.

2. **Steps are the per-symbol delta of target↔sandbox, not the sandbox's git log.** The
   target may already contain some of the sandbox's work, or have drifted. For each
   symbol the sandbox changed, compare it to the *target's* current version:
   - byte-identical → **not a step** (already there; skip it silently or note it),
   - present in sandbox, absent in target → **Create**,
   - present in target, absent in sandbox → **Delete**,
   - differs → **Modify**.
   Build the steps from this comparison. Generate from `git diff {base}..HEAD` to find
   *which* symbols moved, then re-classify each against the target before emitting it.

3. **Modify/Delete/Create all address any named item.** The resolver finds functions,
   impl methods, structs, enums, unions, consts, statics, type aliases, traits, modules,
   and macros by name (first match in the file — flag any name that repeats). A
   **Create** step walks what the walk has a shape for — functions, and item containers
   (a class/impl/mod discloses shell-first, members one by one) — and lands anything
   else (a struct, a const, an interface) as one whole-symbol block ghost; either way
   the placement is container-aware (a method created inside an existing class lands in
   that class). Route only non-item edits (import lines, module wiring, config) to a
   per-file **Patch** step (rule 5) — **not** to Manual steps; a human WILL forget a
   manual bullet, a Patch step sits in the counter like any other. A whole-symbol
   field/variant addition reads as a Modify of its struct/enum — prefer that over a
   Create when the container already exists.

4. **Brand-new files: one `Create File` step per teaching moment — decompose when
   there is more than one.** The engine owns the gesture grain (a create-file
   discloses segment by segment: one Tab per blank-line group, the full walk inside
   functions and classes); YOU own the teaching grain. Decide by Whys and
   retrospectives, not by size:

   - **One concept** (a DTO, a fixture, a single class, boilerplate) → one
     `Create File` step. `**Symbol:**` is optional (defaults to the file path);
     `**File:**` is required; write the retrospective about what the file *proves*.
   - **Several concepts** (an error type + a helper class + the engine, each worth
     its own Why and retrospective) → a `Create File` step carrying an embedded
     `**After:**` fence with only the file's SKELETON (header comment, usings,
     namespace/module frame — a byte-exact PREFIX of the sandbox file), followed by
     ordinary `Create` steps for each symbol in dependency order, each with its own
     Why and retrospective, and ALWAYS closed by a trailing `**Action:** Patch`
     step for that file (rule 5). The patch is not optional: the creates rebuild
     the symbols but at least the file's final newline sits below symbol grain,
     so without it the whole-file byte-exact check fails. Shape:

     ```
     Step N.1  Create File  Widgets.cs   (skeleton fence)
     Step N.2  Create       WidgetError
     Step N.3  Create       WidgetEngine
     Step N.4  Patch        Widgets.cs   (sweeps the residue)
     ```

     The validator proves the decomposition rebuilds the sandbox file
     byte-exact — a missing symbol step or a missing trailing Patch is a FAIL,
     not a surprise at the keyboard.

5. **Everything below symbol grain rides a per-file `**Action:** Patch` step.** A Patch
   step names only a `**File:**`; at replay the tool line-diffs the live target file
   against the sandbox file and serves each remaining hunk on the Tab surface — import
   edits, per-file consts, module-level `//!` doc headers, a top-level item whose home
   is a convention ("after the imports"), and whole files in languages with no grammar
   (shell, config, SQL). Emit one Patch step per file, ORDERED AFTER all of that file's
   symbol steps (an early Patch would sweep later steps' hunks in with it — correct but
   unreadable). Reserve **## Manual steps** for what even a Patch can't do: decisions
   (hand-merging a conflicting doc), actions outside the repo, or anything needing
   judgment rather than bytes.

   **A Patch is residue, never the carrier.** The single worst failure of this format
   is a whole-file Patch on a grammared file (rule 6) that has NO preceding symbol
   steps — the Patch becomes the primary carrier for changes that are really new or
   reworked named items. It line-diffs the whole file against the sandbox, and the
   human Tabs once to swallow hundreds of unread lines. The comprehension gate is gone,
   which is the entire point of the replay. It also trips the extension's line-diff
   size guard and collapses to one file-sized hunk, so the human sees a full-file
   replace where the guide promised surgical edits.

   The rule: if a grammared file's Patch would carry a whole added or rewritten named
   item — a `fn`, `struct`, `enum`, `impl`, method, trait, `const`, a test fn, a
   Markdown section — that item is a `Create`/`Modify` symbol step (rules 3, 4). The
   Patch that trails those steps sweeps only what has no symbol home: `use`/`mod`
   wiring, attributes, a const placed by convention, the file's final newline. That
   residue is small by construction.

   Self-check before you ship, per grammared Patch step: read its target↔sandbox diff.
   If any hunk adds or replaces a whole named item, or the largest hunk runs past ~40
   lines, or the validator reports a single hunk on a file of more than a few hundred
   lines (the size-guard collapse), the file is under-decomposed. Go lift the named
   items into symbol steps and re-check. Files with no grammar (shell, config, SQL,
   TOML) are exempt — a whole-file Patch is the only tool they have, and that is fine.

6. **Languages.** The extension replays Rust, C#, TypeScript/JavaScript (tsx/jsx
   included), Python, Markdown, HTML, and CSS. The symbol is the named item in that
   language: fn/struct/enum/etc. (Rust), class/method/property (C#), function/class/
   method/interface/type/const (TS/JS, `export` travels with the symbol), def/class
   (Python, decorators travel with the symbol), for Markdown the **heading text** of a
   section (`**Symbol:** Setup` addresses `## Setup` through the next same-or-higher
   heading), for HTML `tag#id` (an element without an id is unaddressable — the
   spec-unique tags `html`/`head`/`body`/`title` resolve bare), and for CSS the rule's
   prelude text (`**Symbol:** .card:hover, .tile`, or `@media (max-width: 600px)` for
   an at-rule group). Updated docs are ordinary Modify steps on their section; new docs
   are `Create File`. Python, Markdown, HTML, and CSS have no create walk: a Create
   step lands the whole symbol in one Tab, which is fine — prefer `Create File` when
   the whole file is new anyway. Any other extension goes to a Patch step (rule 5).

7. **Validate before you ship — non-negotiable.** The parser in the
   `human-replay-vscode-extension` repo is the single source of truth for this
   format, and its validator is your oracle:

   `node scripts/validate-guide.js <guide> <targetRoot> <sandboxRoot>` (run from
   your `human-replay-vscode-extension` checkout)

   It parses with the real parser, resolves every step's bytes from both trees,
   flags duplicate-name hazards, and replays every Modify through the engine's
   exact sequential policy. Fix every FAIL and re-run until it prints PASS. A
   guide that never met the validator is a guess.

   PASS is necessary, not sufficient. The validator proves byte-exactness — that
   the steps rebuild the sandbox file to the byte. It does NOT prove the steps
   teach. A whole-file Patch carrying an undecomposed 300-line change PASSES (the
   bytes are exact) while destroying the comprehension gate. Byte-exact is the
   floor; the decomposition self-check in rule 5 is the ceiling. Run both.

A step with embedded `**Before:**`/`**After:**` fences still works (self-contained
guide); the file-resolution path is what lets the guide stay lean for a large change.

## Code blocks: when to include them

Almost never. The human has the file open in their IDE. A 3-5 line snippet is fine for showing a non-obvious signature or a tricky pattern. Anything longer is the human's job to read directly.

If a step needs more than 5 lines of code to communicate, the explanation is wrong. Rewrite the *why* until the *what* is obvious from a file:line pointer.

## Retrospective question craft

The retrospective is what separates a replay guide from a transcription guide. Generic questions are useless. Ask about *this* code.

Bad:

- "Does this make sense?"
- "Are there any edge cases?"
- "Is this performant?"

Good:

- "What happens to `UserSession` if the token expires mid-request?"
- "Why store the cache in a `HashMap` instead of `BTreeMap`?"
- "This endpoint accepts untrusted input. What validation is missing?"
- "Will this query use an index, or will it table scan?"

One shape is banned: "prove X cannot regress" with no oracle attached. A question satisfiable by argument will be satisfied by argument, and the session's own blind spots ride along into the answer. When a phase claims a property is unaffected (throughput, latency, memory), the checkpoint names the command and the expected number: "run the bench; p99 within 5% of baseline". The reader runs it or the claim stays a claim.

The guide inherits the session's settled understanding, including its mistakes. A runnable check is the only checkpoint that can catch what the session itself got wrong.

### Domain templates (starting points)

Pull from these but tailor to the step. A generic question is a question that fails.

**Frontend:** re-render behavior, state ownership, accessibility, error states, loading states, network failure modes.

**Backend API:** concurrency, idempotency, auth model, input validation, failure mode (open or closed), timeout budgets.

**Database:** index usage, migration safety, query patterns, locking, deadlock risk under concurrent access.

**Infrastructure:** failure handling, idempotency, secret management, blast radius, rollback procedure.

**Real-time / HFT:** latency budget, lock-free where it needs to be, backpressure handling, GC pauses, behavior at 10x load.

**ML / Data:** train/test leakage, feature consistency train vs. inference, drift detection, reproducibility.

**CLI:** invalid input, platform differences, machine-parseable output, Ctrl+C behavior, env var assumptions.

### Change-type questions

- **New type:** What invariants must always hold? How are they enforced?
- **New function:** Preconditions? Postconditions?
- **State change:** Draw the state machine. What triggers each transition?
- **External integration:** Timeout? Retry policy? Circuit breaker?
- **Algorithm:** Time and space complexity? Simpler approach?
- **Configuration:** Behavior with missing or invalid values?

## File locations

| File | Purpose |
|---|---|
| `session/goal.md` (or equivalent), commit log | Input, optional. The captured intent. |
| `session/session-state.md`, `session/progress.md`, `session/scraps.md` | NOT inputs. The trail records the journey; the guide teaches the destination. |
| `session/replay-guide.md` | Output. The rebuild path. |
