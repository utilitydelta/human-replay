# Workshop Takeaways

Anthropic ran a Claude Code advanced workshop covering hooks, sub-agents, agent teams, parallelization, plugins, MCP, plan mode, skills, and headless CI. Most of the playbook is aimed at one question: *how do we scale AI productivity safely?*

That's not the question Human Replay is asking. Human Replay is asking: *how do humans keep understanding what's in their codebase when AI writes it?*

Same primitives. Different goal. The harness is value-neutral; the workshop's defaults aren't.

This doc is a position piece on what to take from the workshop and what to leave.

---

## Take

**Hooks for process discipline.** The workshop's pre-tool-use hooks deterministically block actions Claude shouldn't take, regardless of what the model decides. Same primitive, different target: block `git push` and remote-rewiring from sandbox clones, so a throwaway can never accidentally become published history. See `.claude/hooks/sandbox-guard.sh` and `.claude/settings.json`.

What hooks are *not* used for here: prompting the human. The decision to generate a replay guide belongs to the user, not a `Stop` hook firing on every turn end. That nudge lives in the `vibe-coding` skill instead — Claude asks at session end, the user answers.

**Plugins to ship the methodology.** A plugin bundles skills, agents, hooks, and settings into one folder. `claude plugin install` and a team inherits the whole workflow. This is the actual answer to "how does Human Replay scale beyond one engineer." Without packaging, every adopter has to wire `.claude/` by hand.

**Skills as durable instructions.** `/vibe-coding` and `/replay-guide-generator` are exactly the skill pattern the workshop endorses. Description matters: Claude auto-routes to skills based on the description text, so the skill name and one-line description carry real weight. Existing skills in this repo already follow this shape.

**MCP over custom integrations.** When you need Claude to talk to a real system (Jira, GitHub, a database), MCP is standardized, typed, and auth passes through. Don't hand-roll CLI shims. This is orthogonal to Human Replay but worth adopting.

**Adaptive thinking and `/effort`.** Sandbox exploration probably wants `max` effort. Replay-guide generation wants `high`. The workshop made the case that effort levels are now respected literally. Worth specifying in the skill bodies.

---

## Leave

**Agent teams writing production code in parallel.** The workshop's canonical demo: three Claudes, three tmux panes, one writes the route, one writes the test, one writes the README, coordinated through the file system. No human in the loop until merge.

This is exactly the failure mode this repo argues against. Three agents pattern-matching by role (route + test + docs) cannot decompose by invariant. The symmetric fencing bug had passing tests on each node and was globally unsafe under clock skew. Agent teams give you that bug at industrial scale, with comprehension debt baked in by construction. Nobody owns the picture.

If you must use agent teams, scope them to research and exploration, not production code generation.

**Headless CI as a green/red gate.** The workshop pitched Claude in CI as part of the test suite — feed a prompt, assert on JSON output, gate regressions in the pipeline. The framing is "regressions are gated at the pipeline, not when the incident occurs."

Human Replay's position: Claude in CI should be a tripwire for "this PR needs deeper human review," not a verdict. The workshop's framing is the blind-trust failure mode the critique already names. Reuse the primitive (headless invocation), reject the framing (pass/fail as ground truth).

**Parallelization for generation.** The workshop wants to parallelize *code writing*. Human Replay wants to parallelize *review*. Multiple humans replaying the same sandbox, or sandbox A while reviewer B walks sandbox A's diff. The bottleneck the workshop relieves is not the bottleneck this methodology cares about.

**TDD as a sufficient gate.** The workshop's TDD-plus-Claude loop is genuinely strong for unit-scope work. It's insufficient for distributed-systems work, concurrency, timing, and any property that can't be expressed as a single-process assertion. The fencing bug passed its tests. Don't let "the tests are green" stand in for "I understand why this is correct."

**Plan mode as terminal artifact.** In the workshop, AI generates the plan, AI executes the plan, you approve. In Human Replay, the AI's plan is one input to *your* plan — the replay-guide is what you actually build against, in your hands.

---

## Sensors the workshop didn't build

Workshop sensors trip on objective failure: tests red, security check failed, hook blocked. Useful, necessary, not sufficient.

The sensors Human Replay needs are harder, and the workshop didn't address them:

- Where did the AI build infrastructure for imagined needs (`HeartbeatLeaseTracker`, dead `LockFailureKind` variants)?
- Where did it decompose by role when the property required reasoning by invariant?
- Where did the sandbox produce plausible-looking success that hides a globally unsafe interaction?
- Has the human walked the territory the AI sketched, or are they shipping someone else's map?

These don't trip on a passing test. They require a human reading the diff with the Human Replay method in mind. The replay-guide is the artifact that makes that review tractable.

---

## Synthesis

Use the workshop's harness primitives — hooks, plugins, skills, MCP, headless invocation — to enforce Human Replay discipline. Don't use them to scale agent teams writing production code in parallel.

The workshop's defaults optimize for the wrong loss function. Throughput is cheap. Understanding is the product.
