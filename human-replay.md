# Human Replay

## Vibe coding without losing your codebase

---

### The problem

Vibe coding is intoxicating. You describe what you want, the AI builds it, and three hours later you have a feature that would have taken two weeks.

Then you read the code.

It works. Mostly. Fields the AI declared and never read. Abstractions you would never pick. Subtle bugs hiding in the seams between components that were never tested together.

Now you have two options. Ship the entropy. Or throw it away and lose the insight the AI just bought you.

Both are bad. There is a third option.

---

### The insight

The AI's value is not the code. It is the *exploration*.

When you vibe, you are not paying for keystrokes. You are paying for something to map territory you have not walked yet. The map is genuinely useful. The code that came back with it is something else - assembled in a context that does not share your conventions, your constraints, or your future maintainers.

Code is cheap. Understanding is expensive. The exploration is the product.

Treat the sandbox output as a research paper, not a pull request.

---

### What Human Replay actually is

Two phases. They do not share a codebase.

**Exploration.** AI in a sandbox. Hours of iteration. Stubs, dead ends, hacks. Do not intervene on style. The point is to find a path, not to ship one.

**Integration.** You. In your real codebase. With your patterns. Reading the AI's solution like documentation, not like commits to cherry-pick.

The sandbox gets destroyed. The replay ships.

---

### Principles

#### 1. The sandbox never merges

It exists to be studied and discarded. If you find yourself thinking "I'll just clean it up", you have already lost. Clean-up is a euphemism for "I do not have time to actually understand this."

#### 2. Exploration and integration are different jobs

Exploration is breadth. Run wild. Find any path that works.

Integration is depth. One piece at a time. Each verified. Each understood. Every line gets justified.

These do not share a brain or a session.

#### 3. Extract knowledge, not code

Read the sandbox to answer:

- How did it decompose the problem?
- What edge cases did it cover that you would not have thought of?
- Where does the feature touch the rest of your system?
- What failure modes did it handle, and why?

You are not looking for code to copy.

#### 4. Replay incrementally

The AI builds ten components and wires them at the end. You build one, prove it works, then build the next.

If you cannot demo phase 3 standalone, you do not get phase 3. Do not start phase 4.

#### 5. Divergence is the point

Your replay will look different from the AI's version. Names will change. Abstractions will collapse. Some of the AI's complexity will turn out to have been load-bearing on assumptions you do not share, and you will cut it.

Document the divergences. That is the proof you were thinking and not transcribing.

#### 6. Dead code is unintegrated code

Fields never read. Variants never constructed. Functions never called. These are stitches between parts that the AI assembled but never sewed together.

Your replay has none of this. Every line earns its place.

#### 7. If you cannot explain it, you do not have it

The only test that matters. Diagram what you built. Predict what breaks if you remove a piece. Walk a colleague through it. If any of those fails, you copied. Go back.

---

### The method

**Phase 0: Vibe.** Sandbox. AI iterates until something works. Hours, not days. Do not argue about quality.

**Phase 1: Triage.** Sort the output:

| Category | Description |
|----------|-------------|
| Working | Actually functions, tested or testable |
| Stubbed | Placeholder, intentionally unfinished |
| Broken | Does not work or has obvious flaws |
| Dead | Unused, leftover from abandoned attempts |

Triage is the spine of the replay plan.

**Phase 2: Build the replay document.** Order phases by dependency. Each phase is the smallest possible working slice. Each phase has verification (how do you know it works?) and a retrospective (do you actually understand it?).

Skip the retrospective once and the document becomes a transcription guide. Do not skip the retrospective.

**Phase 3: Replay.** Real codebase, your patterns. Reference the AI; write your own. Run tests after each phase. Commit after each phase.

You will go slower than the AI did. That is the point. You are building understanding alongside code.

**Phase 4: Capture what diverged.** Where did your version differ? Why? What did the AI do well? What did it do badly? What did it skip?

This is the durable artifact. The next vibe session benefits from this one.

---

### The economics

It is slower. For one feature.

But:

- AI-speed exploration. The hard problem-solving still happens at AI pace.
- No AI-generated tech debt. The codebase stays coherent.
- Transferable understanding. Next time you see a similar problem, you have the solution in your head, not in a PR.
- Architectural vision intact. The AI adapted to you, not the other way around.
- Real review. The "second pair of eyes" is you, with full context. Not a teammate skimming the diff.

Slower than pure vibing. Faster than pure manual coding. Quality of the latter, speed of the former.

---

### When to use this

**Use Human Replay for:** complex features touching multiple parts of the system, anything concurrent or distributed, anything that has to be maintained, code in your core domain.

**Pure vibing is fine for:** throwaway scripts, prototypes, boilerplate, tests where you will replay the implementation anyway, code you already understand and can review trivially.

**Do not even start with AI for:** core architectural decisions, security-critical paths, performance-critical inner loops, anything where the implementation *is* the design.

---

### The deeper point

Vibe coding offers a Faustian bargain. Infinite throughput in exchange for understanding of your own system.

Human Replay refuses the bargain. The productivity is real. You just do not pay the price.

The AI explores. You integrate. The map becomes territory you walked yourself. Your codebase stays yours.

---

### Quick reference

```
SANDBOX  →  TRIAGE  →  REPLAY DOC  →  REAL CODEBASE
  AI         You        You             You
  messy      sort       ordered         clean
  works      raw        phased          understood
  delete     ---        ---             ship
```

Six rules:

- Sandbox never merges
- Knowledge, not code
- Incremental, with verification
- Retrospective every phase
- Divergence is good
- If you cannot explain it, you do not have it

---

*The AI descends the loss landscape,*
*brute force through a thousand tries -*
*stumbling, backtracking, iterating blind*
*toward some local minima it cannot name.*

*The human holds the map entire.*
*Context that spans years, not tokens.*
*The why behind the what.*
*The scars of past decisions.*

*Let the machine explore the canyon floor.*
*You watch from the ridge above.*
*It finds a path. You judge the destination.*
*Its code is disposable. Yours is not.*

*The codebase was yours before.*
*It will be yours after.*
*The AI is a scout returning with a sketch*
*of territory you will walk yourself.*

---

*v2*
