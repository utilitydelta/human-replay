# A Critique of Brute-Force AI Development

## Scorched earth as an engineering philosophy

A growing camp in AI-assisted development has converged on one rule: *solve problems with LLMs at any cost*.

This document looks at agent maximalism head-on and argues that it devalues real engineering. Not by accident. By design.

---

## The agent-maximalist philosophy

Geoffrey Huntley's [agent philosophy](https://ghuntley.com/agent/) treats AI agents as production workers to be optimized. The human becomes an orchestrator. Picks the model. Tunes the prompt. Watches context windows. The agent ships the code.

Geoff distinguishes "Software Development" (declared dead) from "Software Engineering" (still alive), but does not press the difference. The conclusion stands as written.

Tenets:

- Agents are "300 lines of code in a loop", simple systems that can be mastered
- Pick "highly agentic" models that prioritize tool calls over reasoning
- Context management is the critical skill
- Workers who adopt agent workflows outpace those who do not

The implicit claim: most software problems are solvable by pattern matching against existing solutions. The agent interpolates from training data. The human steers.

---

## RALPH: brute force as methodology

The [RALPH methodology](https://ghuntley.com/ralph/) takes this further. At its core, RALPH is a Bash loop:

```bash
while :; do cat PROMPT.md | claude-code ; done
```

Run the agent. Check if it is done. If not, run it again with a fresh context. Iterate until something looks finished.

Characteristics:

- No human in the loop. The system runs autonomously until exit conditions are met.
- Faith in eventual consistency. Trust that the process converges.
- No IDE. Development happens entirely through tool calls.
- Success measured in cost. The pitch claims a $50,000 contract delivered for $297.

The framing is explicit: failures are not the tool's fault. They are tuning opportunities. Like a guitar.

---

## The fundamental problem

These approaches share a critical flaw: **they only work for problems that have already been solved.**

LLMs are interpolators. They recombine patterns from training data. If the solution is in that data, another CRUD app, another REST API, another standard integration, the agent finds it. Faster than a human can.

But:

- A new database engine with novel consistency guarantees?
- A distributed system whose constraints do not match existing architectures?
- An algorithm that does not appear in the literature?
- A system where the *design* is the difficulty?

These need a human who understands deeply enough to make choices the training data does not contain. The agent becomes useless. Or worse, confidently wrong.

---

## The uncomfortable economics

The pitch goes: AI-assisted workers outpace manual workers. True, for commodity work.

But commodity work is racing to zero. If an agent can solve the problem, the problem is not worth much. The valuable problems are precisely the ones agents cannot solve.

| Problem type | Agent capability | Economic value |
|---|---|---|
| Routine integrations | High | Commoditizing to zero |
| Standard features | High | Low margin, high competition |
| Novel systems | Low | High, decreasing supply of capable engineers |
| Genuinely hard problems | Near zero | Irreplaceable |

Scorched earth optimizes the wrong quadrant. It makes you faster at work that is becoming worthless while atrophying the skills needed for work that stays valuable.

---

## The hidden cost of blind trust

RALPH's faith in eventual consistency is the dangerous part. The methodology assumes:

1. The agent converges on a correct solution.
2. You can recognize when it has.
3. The code it produces is maintainable.

Each is wrong, often.

**Convergence is not guaranteed.** Agents oscillate. They produce subtly wrong solutions that pass superficial tests. They get stuck in local minima that look like progress. "Run it again" is not debugging. It is gambling.

**Recognition requires understanding.** If you do not understand the code well enough to write it, you do not understand it well enough to validate it. You are trusting the system that produced the code to also confirm it is correct. That is not a check.

**Maintainability is sacrificed.** Iterated agent runs accumulate entropy. Dead code. Abandoned approaches. Inconsistent patterns. Unnecessary abstractions. All the hallmarks of code written without an architectural vision.

---

## What real engineering actually is

Engineering is not about generating code faster. It is:

- Understanding problems deeply before proposing solutions
- Making deliberate architectural choices that consider long-term implications
- Writing code you can explain
- Building systems you can maintain when requirements change
- Knowing when you are wrong, and why

Brute force inverts every one of these. Speed over understanding. Output over insight. Token efficiency over code quality. "It works" over "I know why it works."

---

## The devaluation of engineering

When we reduce software development to "prompt engineering" and "agent orchestration", we are not elevating AI. We are degrading engineering.

Engineering is a discipline. It requires:

- Deep domain knowledge
- Years of accumulated judgment
- The ability to reason at multiple levels of abstraction
- Understanding of failure modes and edge cases
- Taste. Knowing what makes a solution elegant rather than merely functional.

These do not come from running agents in loops. They come from doing the work yourself, repeatedly, with deliberate attention to craft.

Scorched earth treats craft as inefficiency. But craft is precisely what separates an engineer from a prompt typist.

---

## The alternative

The [Human Replay method](human-replay.md) takes a different shape:

- The AI explores. You integrate. Use agents to scout unknown territory; implement solutions yourself.
- Extract knowledge, not code. The agent's value is the problems it solves and the approaches it discovers, not the code it writes.
- Understanding is the product. If you cannot explain what you built, you have not built anything. You have accumulated files.
- Your codebase stays yours. Every line exists for a reason you can articulate.

Slower for individual features. But it preserves the capability that matters: the ability to solve problems that do not have existing solutions yet.

---

## Conclusion

The brute-force approach is seductive. It promises dramatic cost savings, faster delivery, and the ability to operate beyond your current skill level.

It is a trap.

It optimizes for commodity work while atrophying the skills needed for valuable work. It trades understanding for output, leaving you unable to maintain, extend, or debug your own systems. It produces code without vision. Architecture without intent. Solutions without comprehension.

The hard problems still require humans who understand deeply. The question is whether you will still be one of them.

---

*The AI descends the loss landscape,*
*brute force through a thousand tries -*
*stumbling, backtracking, iterating blind*
*toward some local minima it cannot name.*

*The human holds the map entire.*
*Context that spans years, not tokens.*
*The why behind the what.*
*The scars of past decisions.*

*Let the machine explore.*
*You decide where to go.*

---

## References

- [Geoffrey Huntley on Agents](https://ghuntley.com/agent/)
- [The RALPH Methodology](https://ghuntley.com/ralph/)
- [RALPH for Claude Code](https://github.com/frankbria/ralph-claude-code)
- [Human Replay](human-replay.md)
