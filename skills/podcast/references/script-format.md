# Script format

One markdown file. `podcast.py lint` enforces it; `render.py` reads it.

```
---
title: Before the replay: the segment file
commit: 4a46baa on aa76c5c
sources: ["sessions/session-v18-task-header-v2/replay-guide.md", "decisions/", "docs/v8-segment.md"]
voices: {"A": "af_heart", "B": "am_michael"}
pronounce: {"Celeriant": "/sˌɛlˈɛɹiˌænt/"}
---

## Why this exists
A: Here's the promise. Once a client gets an Ok, that write survives a crash. {src: doc v8-segment.md}
B: Survives how, if the power goes mid-write? {src: -}
A: Picture a notebook with two bookmarks at the front. {src: analogy; doc v8-segment.md#Layout} {slow}
B: Before you hear it, what do you reckon happens if the power goes between the two bookmarks? {src: -} {think}
```

- Front matter: `title`, `commit` (what the episode describes), `sources` (JSON list), optional `voices` and `pronounce` (JSON objects).
- `## <title>` starts a chapter; each becomes a chapter marker in the m4a, so name it what the listener will skip to.
- Every spoken line is `A: ` or `B: `, the text, then `{src: ...}`. Tokens, `;`-separated: `guide <step>` (a replay guide step or section), `D-NNN` (a decision), `doc <file>#<heading>`, `file <path>`, and `analogy` for a line that builds or extends an analogy (add the source of the mechanism it maps to). `src: -` only for a line with no factual claim: a question, a handover, a reaction. The verifier checks that it really has none.
- Optional pace markers after the source tag: `{beat}` holds a pause after a line that lands a point or a surprise; `{think}` holds a longer one after B's question to the listener (one per chapter, B only, the line ends in `?`); `{slow}` slows the line that names a concept or says what a scene means; `{quick}` speeds a throwaway reply. Lines of eight words or fewer already get a short gap. Never two beats in a row.
- `<!-- comments -->` are skipped.

## Hosts

- **A, the guide**: has read the whole build and knows why it is shaped this way. Tells the story, builds the analogy, says where it breaks.
- **B, the listener's proxy**: the person about to type this code. Asks what they would ask: why not the simpler way, what goes wrong without it, wait, how is that possible. Pushes on the analogy until it shows its limit. Pushes back when A states a rule without a reason. Never agrees for colour.

Not two enthusiasts. No "great question", no "exactly", no laughter cues. B may think out loud once a chapter ("Hm. Hang on."), right before a real question, never as texture.

## Writing for the ear

- Spell every identifier as it should be said: "open check", "wal seq", "header seq", "pick, the function". No backticks.
- Numbers: rare, rounded and felt. "Every single one of a thousand" beats "one thousand of one thousand".
- Sessions as "session nineteen"; commits by role ("the replay base", "the sandbox head").
- A list of more than three items becomes three lines or a chapter.
- Pronunciation fixes go in `pronounce`, not in respelt text.

## Voice

Write it the way an engineer explains it to a peer at the next desk: casual, plain, direct. Think of an Australian colleague talking it through, without the dialect or the slang. The default model voice, long sentences with fronted clauses and colon chains, is close to impossible to follow by ear.

- Subject, verb, object. One idea per sentence, mostly 6 to 16 words.
- Name the thing, then say what it does. "The planner refuses it", not "it is refused by the planner".
- No inverted or fronted constructions: not "What breaks is the header", "Gone are the entries", "Enter the barrier", "Here's the thing:", "It's not X, it's Y".
- No colon chains, no stacked commas, no asides in the middle of a sentence. No fragments for drama ("Acknowledged writes, quietly removed.").
- Say "you" to the listener and "we" for the system. Contractions are fine.
- A number gets its own short sentence when it matters.

Before: "An update whose barrier is below the picked header's is refused, as barrier lowered, forty three to forty one, before any effect, for one comparison per header write."
After: "So the planner gets a ratchet. If an update's barrier is lower than the picked header's, the planner refuses it. That's the barrier lowered error. It costs one compare per header write."
