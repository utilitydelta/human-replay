---
name: podcast
description: Make a verified two-host audio episode that is the conceptual run-up to a replay: the intent, the mental model as one picture, the story of one thing moving through the system, the surprising ways it goes wrong, and a few hooks to carry to the keyboard. Few names, few numbers, no lists. Script by Claude, every claim tagged with its source and checked by a fresh agent before any audio exists, then local TTS. Use before a replay, or when the human asks for a podcast or audio overview.
---

# Podcast

The listener is about to rebuild a piece of the system by hand. Before that they need a mental model they can hold in their head while typing: what the thing is for, how it hangs together, where it bites. They do not need the details. The replay guide has the details, and a brain cannot store a list of facts heard once.

Memory champions remember a shuffled deck by turning it into a story: vivid places, actors, things happening. Do the same. One concrete thing moves through the system, and each mechanism is a scene it passes through, with a picture attached. A listener who can replay the story can rebuild the facts from it while they type.

Hosted audio models are good at analogy and story and bad at truth. They invent mechanisms, upgrade guesses to guarantees, and credit decisions to the wrong person. So this episode keeps their strengths and checks every claim: a script where every claim names its source, a verifier that never saw the writer's reasoning, then speech.

## Episode: replay preamble

15 to 25 minutes, in five parts.

1. **Why this exists.** The promise the code keeps for its users, in one or two sentences, and what breaks for them if it fails. Intent first: every later scene hangs off it. End on one line of map: "First the picture, then we follow one write through a crash, then the three things that bit."
2. **The picture.** One analogy for the whole thing, built up slowly. Map it part for part onto the real system, out loud, and say where it stops being true.
3. **The story.** Follow one concrete thing (one write, one batch, one file) from birth through a crash and back. Each mechanism is a scene it passes through: what happens, what would go wrong without the mechanism, then the mechanism. Four to six scenes. Each new concept gets a plain name the first time and keeps it. Halfway through, restate the picture with every mechanism it has gained so far.
4. **The gotchas.** The two or three failures that surprised the people who built it, told as stories with the moment of surprise in them. "A thousand writes, every caller gave up waiting, and every single one still landed on disk."
5. **When you type it.** Close the picture one last time, now complete. Then three hooks the listener should carry into the replay: the idea behind the trickiest part, the thing that looks wrong but is right, the one decision worth questioning. Then stop.

If the listener has heard a wrong mental model before (an earlier episode's errata), fix the model inside the story where that scene comes up: "You might have heard this was bulletproof. It isn't, and here's the case that gets through." Two or three at most. Never a list of corrections.

### Pace: assume the listener drifts

Listeners drift more than readers do, usually on a tangent the episode itself started, and they can't scan back. This episode is one chain, so a missed scene breaks every scene after it, and an early lapse costs most. An even rhythm makes it worse. With the same gap after every line, nothing tells the ear where a point landed or where to get back on. Evidence in `docs/presentation-persona-research.md`.

- **The picture three times.** Built in part 2, restated mid-story, closed in part 5, each pass fuller. A listener who missed a scene rebuilds it from the picture. The lint checks the analogy tag in at least three chapters, the last among them.
- **Something changes about once a minute.** A story beat runs quick, then the line that says what it means slows down with a beat after it (Ira Glass's action, then reflection). Mark the turns with `{beat}`, `{slow}` and `{quick}` per `references/script-format.md`. The lint flags about ninety seconds with no change of pace.
- **B asks the listener, once per story chapter.** "Before you hear it, what do you reckon happens to the write now?" Then a `{think}` gap, then A answers. Answering a question mid-lecture roughly halves mind wandering in the research. Some players trim silence, so the answer must make sense without the gap.
- **B thinks out loud, sparingly.** One "Hm. Hang on." per chapter at most, right before the question that leads to the mechanism. A hesitation before a word helps the listener hold it; scattered as texture it is the NotebookLM tic.
- **No laughter.** Kokoro reads "Ha!" as a word. A dry line in part 5 is fine.

### Budget for names and numbers

- **No** decision ids, session numbers, version numbers, commit hashes, error-variant names or type names, except the handful of concept nouns the story introduces.
- **A number only when it changes the listener's intuition**, and then round it and make it felt. About one every three minutes.
- **Decisions**: name at most the two or three that change the mental model, as people choices in plain words, truthfully attributed: "the bots chose this and nobody asked you; it's worth a look when you type it". The full decision list is text, in the guide and the debrief, never audio.

### Analogies

Encouraged: they are what the listener remembers. Each one must map onto the real mechanism part for part, and the hosts must say where it breaks. An analogy that implies something false is an error, same as a wrong fact. The verifier checks the mapping against the sources.

## Inputs

Gather into the session's `media/podcast/<slug>/`, and list them in the script's `sources`:

- The design docs for the code being replayed, and the session report or contract that says why it is built this way.
- The evidence behind the gotchas: the smallest counterexamples, the spike results, the reviews that caught bugs.
- The decisions that change the mental model, with owner and status (celeriant-db-bots: `scripts/decisions.py brief <module>`; pick the two or three that matter).
- Errata of earlier episodes on this code, if any.
- A glossary: spoken form and pronunciation of the few names the hosts will say.

The replay guide is a source for intent and order, not a script to walk through.

## Steps

1. **Outline** first, in `outline.md`: the promise, the analogy with its part-for-part mapping and where it breaks, the thing the story follows, the scenes, the gotchas, the three hooks. Check it against the sources before writing lines.
2. **Write** `script.md` per `references/script-format.md`. Every factual claim gets a `{src: ...}` tag; analogy lines are tagged `analogy` plus the source of the mechanism they map to. Run `scripts/podcast.py lint script.md` and `stats` until clean and in length.
3. **Verify** with a fresh subagent per `references/verify.md`, handed `podcast.py claims script.md`, the outline and the inputs. Fix every row; re-verify changed lines; repeat until no row remains. Keep each round's counts in `verify.md`.
4. **Audition**: `uv run scripts/render.py script.md /tmp/audition.m4a --only 12`, transcribe it (`scripts/transcribe.sh`), and check every glossary name came out right. Fix `pronounce` and repeat.
5. **Render**: `uv run scripts/render.py script.md <slug>.m4a` into the same session folder. Keep audio out of git (ignore `*.m4a`); commit the outline, script, verify log and inputs list. Render writes to a new file and swaps it in, so a player holding the old file keeps playing.

Tell the human the file, its length and the chapter list.

## Engines

`render.py --engine kokoro` (default): Kokoro 82M, local, takes inline IPA, so names are fixed exactly; delivery is clean and a little flat. A 45 minute episode renders in under a minute on an RTX 5080.

Dia 1.6B was tried and is not wired in: more conversational, but it rendered slower than real time (15 s of audio in 25 s), cut the last word of a generation, and mangled names it cannot take phonemes for. On a Blackwell GPU it also needs PyTorch 2.8 with CUDA 12.8 over its pinned 2.6. VibeVoice is untested.

Add an engine as a function in `ENGINES` that maps (speaker, text, speed) to 24 kHz float audio, then transcribe a full render and read it back before trusting it.
