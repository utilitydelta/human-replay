# Automating the edges: adversarial loops, triage, and the constitutive hand

The naive agent loop is: build, review it with another agent, feed the review back, repeat until the reviewers go quiet. The Ralph Wiggum Loop. It works, right up until it does not, and the two ways it fails are predictable. It builds an over-engineered monster, and it drifts off purpose.

The short version: agents are at their best off the happy path, where there is an external judge. Lean into that hard. But an adversarial loop is a force with no direction and no magnitude limit, so you bracket it with two reducers and keep one human role live in the loop the whole time. Automate the edges. Keep the hand on the wheel.

Scope first, because the method is not free. The full machinery below is for work whose stakes justify it: a production system, a security boundary, a foundation other things will sit on. For a spike, a throwaway, or a small change, skip most of it and run the loop in your head. Weight the process to the stakes. Applying all of this to everything is itself the monster.

## The inversion: agents are more reliable off the happy path

The intuition is backwards. People assume an agent is most trustworthy writing the straightforward implementation and least trustworthy on the gnarly edges. It is the other way around.

On the happy path the agent grades its own work, and models exhibit a documented self-preference: they rate their own output higher than a neutral judge would (Panickssery et al., NeurIPS 2024, on LLM evaluators favouring their own generations). On the edges there is an external judge: a conformance suite, an RFC test vector, a borrowed test, an invariant checker, or a different agent instance trying to break it. You are not asking the model to be correct. You are asking it to grind against something that already knows what correct is. That is an easier and more reliable ask.

So the highest-leverage move in the method is one thing: **externalize the oracle.** Three shapes of it:

- **An invariant judges chaos.** Have an adversarial agent generate the attack (partition, kill, reorder, flood) and let the system's own consistency rule decide pass or fail. The agent does not have to know what correct is. The invariant does. This is how you test correctness an agent could never reason its way to alone.
- **Rent correctness, do not invent it.** Point the loop at an oracle someone else already wrote: a conformance suite, a reference implementation's black-box tests, known-answer crypto vectors. The hard part, defining correct, is already done. This is the cheapest reliability you will ever buy.
- **Push down the stack.** Build a real, demanding consumer on top of the layer you care about. The consumer is the integration test the substrate could never write for itself. Building an auth layer on a database surfaces database bugs no amount of testing the database in isolation will find: the missing index, the silent dropped event, the retry semantics, the routing footgun. Each layer up is a forcing function on the layer below.

The first question on any unit of work is therefore: what is the oracle, and is it external? If the answer is "the agent decides", you have not automated it. You have hidden the judgment.

## The two failure modes, and the role that fixes both

An adversarial loop with nothing bounding it fails two ways, and they are the same hole wearing two hats.

**Noise becomes the monster.** Ask an agent to be adversarial and it will find something wrong with everything, because there always is. Loop that straight back to the builder and every finding becomes a fix-order. Find and fix are the same polarity. Both add. Nothing in that circuit optimizes for less, so complexity ratchets one way: a hardened, gold-plated, unmaintainable answer to a question nobody asked.

**Drift is the vacuum.** The agent runs without the why. It cannot see the levels of context above it, so it cannot tell relevant from irrelevant, and it slowly wanders off purpose, optimizing locally against problems that do not matter for what you were building.

Noise is a missing magnitude limit (how robust is enough). Drift is a missing direction (what is this for). Both are owned by one role a model cannot hold: the **constitutive** role, which decides what counts as correct, what counts as enough, and what the point is. The loop cannot generate either from inside itself.

## The four roles and their cadences

The "human node" is not one thing. It is four roles, and the cadences matter as much as the roles.

- **Constitutive** (define correct, define enough, hold the why). **Continuous.** Lives in the loop, every pass. The thing that triages noise and catches drift. Treat it as a gate and you get the monster and the vacuum, because by the time a gate sees the work it is already over-built and off-target.
- **Independence** (the checker is not the author's model class). **Periodic**, per phase. Structural, because self-preference scales with the model rather than shrinking, so a better model does not remove the need for a different one.
- **Deontic** (accountability, the signature). **A gate**, at release. The only role that is genuinely a gate.
- **Custody** (operate under fire: on-call, rotation, novel incident attribution). **Ongoing**, for the life of the system. Production is the final external oracle: incidents feed new bars back into the invariants (L2 below).

This essay is written for a solo builder or a small team. At larger scale the mapping holds but needs an org chart: constitutive and deontic attach to a named owner per stream, independence is a shared service, custody is a rota. The cadences do not change.

## The context hierarchy: how the why travels

Drift is fixed by persisting the why where every pass can check it. Not a pile of docs, a hierarchy with one rule: **every level traces up.**

- **L0 Charter.** Why this exists, who it is for, what it is explicitly NOT, and the definition of enough. Most stable. The constitutive anchor written down.
- **L1 Design.** The shape and the load-bearing decisions, with rationale.
- **L2 Invariants and gates.** The non-negotiables, and the sufficiency line per stage.
- **L3 Phase objective.** Why this phase, what is in and out of scope.
- **L4 Task or finding.** The local work.

The trace-up rule does double duty. A finding names the invariant or bar it serves. If it cannot trace to L0, it is drift, reject it. And it is worth acting on only if not acting would break a stated bar or invariant. Traces-up means on-direction. Breaks-a-bar means worth-it.

The dangerous case, and the one a naive rule gets wrong: a real finding with **no matching bar**. The bar set is never complete, so this happens, and it is often a genuine hole the charter simply never anticipated. A no-bar finding is **not** auto-dismissed. It escalates to a constitutive decision: add a bar, accept-with-reason, or reject. Silently downgrading a finding because nobody pre-wrote its bar is the method hiding the judgment it claims to externalize. The bar set itself is reviewed, not just the work against it.

Most projects already have L1 through L4. The thin one is usually L0. Write it.

## The loop: expand, contract, fix, contract

The fix for noise is not to loop less. It is to put a contraction on each side of the fix, so the loop is not a one-way ratchet. Two reducers, not one, at two points, because they reduce two different things.

```
implement -> test against the oracle -> adversary (find: EXPAND)
   -> triage (reduce FINDINGS against the bars)
   -> fix the kept findings
   -> simplify (reduce CODE)
   -> gate
```

1. **Triage, the findings reducer.** Right after the adversary, before any fix. Dispositions each finding against the bars (below). Stops noise from becoming work. The constitutive call, so human-owned or a charter-grounded agent the human reviews. Cheap, because reading a triaged list is fast. This is the step the Ralph Loop skips, and skipping it is why it builds monsters.
2. **Simplify, the code reducer.** After the fix, before the gate. Legitimate fixes still accrete complexity; this strips it. The opposite objective to the adversary, on purpose. It runs at the gate, not every micro-iteration, because a half-finished change has local simplifications that conflict with code not yet written.

Expand, then contract, twice. The adversary expands the surface, triage contracts the findings, the builder acts, the simplifier contracts the code. That double contraction stops the climb into the monster.

The bar is the referee. The adversary and the simplifier are in deliberate tension, one adding robustness, one removing it. Looped against each other they oscillate forever. They do not, because both argue to the same external referee, the charter and its bars, not to each other. A simplification that removes a bar-protector is rejected. A robustness-add that protects no bar is rejected.

## Engineered independence

The adversary earns its keep only when genuinely independent of what it judges. Independence is engineered, not assumed, and the right move depends on the oracle.

- **Prefer an external, non-agent oracle.** A conformance suite or a human pentest cannot be flattered, so there is nothing to redact and nothing to escalate. Use one wherever it exists.
- **When the judge must be an agent, redact provenance.** A same-model judge that knows the code is agent-written confirms it too readily, the self-preference effect above pointed at your own pipeline. Hide the provenance before review so it judges the code, not its author. In my own runs this helps; I have not measured by how much. Diversify model class on top where you can.
- **Know the residual gap.** Redaction helps, but a same-model judge still shares the model's blind spots, so an agent judge stays a notch below an external oracle by construction. For the highest-stakes surface (a security boundary, the silent-failure tail) it is not sufficient alone; escalate to a human or a suite. The agent adversary is a force multiplier on the cheap surface and a backstop on the expensive one, never the final word there.

## Triage and measurement

Triage is the load-bearing human step. Make it cheap and honest.

- Every finding carries severity, evidence, and the bar it protects (or escalates per the no-bar rule above).
- Three dispositions, all first-class: FIXED, ACCEPTED-WITH-REASON, DEFERRED-WITH-TICKET. "Correct but not worth it" is a real, common, correct verdict the adversary cannot reach, because it has no cost model. You do.
- Triage is the single point of failure. A tired human rubber-stamps; an unreviewed agent triage rots against a charter nobody is re-reading. Guard it: batch low-severity dispositions, let the agent's calls stand on Nits but never on Blockers, and re-read the charter when dispositions start feeling automatic.

Then measure whether the catch is real, or you are trusting a vibe. The metric that matters is **escaped-defect rate**: defects a later stage (a downstream phase, the pentest, production) caught, over total defects, charged to the stage that should have caught them. A high rate means fake independence or a weak oracle. At solo scale it is a small-N trend, not a statistic, so read it as a direction. A round that returns only nits is the quality stop signal: that, plus the bar being met, means ship, not loop again.

## Loop economics

The loop costs tokens, wall-clock, and the scarce one, human triage attention. Bound it. Set an iteration cap per phase and a budget stop independent of the quality stop, so a loop that is still finding marginal nits at 10x the cost halts on spend, not on satisfaction. The quality stop (only-nits) and the budget stop, whichever comes first. If you hit the budget stop with Blockers still open, that is a signal the work was under-scoped, not that you should keep grinding.

## Anti-patterns

| Anti-pattern | The fix |
|---|---|
| Ralph Loop with no triage (findings become fix-orders) | Triage before fix, against the bars |
| One reducer (simplify only, after fix) | Two reducers: triage before fix, simplify after |
| Loop runs to the gate unsupervised | Constitutive presence is continuous, not a checkpoint |
| Adversary vs simplifier with no referee | Bind both to the bar |
| Hardening past any stated bar | Gold-plating is drift; stop at enough |
| Same-model, same-provenance review | Redact provenance, or use an external oracle |
| The method applied to a spike | Weight the process to the stakes |

The automatable part is enormous and growing. Automate the edges. But an adversarial loop is a chainsaw, not a self-driving car. It cuts beautifully and it has no idea where it is going. The constitutive hand stays on it, or it cuts the wrong thing into a very robust shape.
