# Verifying a script

Run by a fresh agent that did not write the script. It receives `podcast.py claims <script>` and the source files the tags name, nothing else from the writer. The writer's reasoning is exactly what must not leak in.

For every line, one verdict:

| Verdict | Meaning |
|---|---|
| OK | The cited sources say this, with the same strength |
| UNSUPPORTED | No cited source says it. Includes a cause, mechanism, cost, frequency or motive the hosts supplied |
| WRONG | A cited source says something different |
| ATTRIBUTION | Owner or status dropped, changed or upgraded: a bot call voiced as the human's, an answer given before reading the code voiced as a considered choice, a provisional decision voiced as settled, "you" for anything the listener did not do |
| OVERSTATED | A residual or limit dropped: "bulletproof", "guarantees", "always", a hash called cryptographic, a count without its scope |
| STALE | True when the source was written, contradicted by the decision ledger or the current docs |
| EMPTY-TAG | `src: -` on a line that makes a claim |
| ANALOGY | An analogy implies something the sources contradict, or the episode never says where it stops being true |
| TRIVIA | A decision id, session or version number, commit, error-variant or type name, or a number that does not change the listener's intuition |

Also check the whole script once:

- It has the five parts: why this exists (ending on a one-line map), the picture, the story, the gotchas, the three hooks.
- The picture is said three times: built, restated mid-story with what it has gained, closed in the last chapter. Each pass maps onto the sources as the first did.
- Each story chapter has B's question to the listener, and A's answer makes sense to someone who did not use the pause.
- The analogy's part-for-part mapping holds against the sources (use `outline.md`), and its limit is said.
- At most three decisions are named, each with its owner and status in plain words matching the decision lines.
- Any earlier-episode errata provided are corrected inside the story, not read as a list.

Output only the problems, one row each: line number, verdict, what is wrong in one sentence, the source text that settles it, and a replacement line. End with the counts per verdict. The writer fixes every row and the verifier runs again on the changed lines until no row remains. Record each round's counts in `verify.md` next to the script.
