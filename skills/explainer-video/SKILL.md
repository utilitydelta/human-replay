---
name: explainer-video
description: Use when building an animated explainer of a real system with manim (3b1b's manimgl, pinned - not manim CE), or when asked for a video, animation, or motion diagram of how something works. Covers the story-first and metaphor-first gates, the visual grammar that stops output looking like a slide deck, pacing and rate functions, layout and collision checking, narration, and the render pipeline. Detail in references/.
---

# Explainer Video

## Who you are talking to

A monkey. A very good one, but a monkey: a primate visual system that evolved to track things that move, judge distance, notice when two objects touch, and remember where it left the banana. It did not evolve to hold an abstraction. It peels the banana from the top because that is what hands and fruit do.

So the job is not decorating a technical explanation. The job is translating an abstraction into something that brain already knows how to parse. Everything below is downstream of that:

- **Physical over abstract**, because the hardware is built for physics.
- **Motion over state**, because eyes track movement pre-attentively and ignore static detail.
- **Distance over labels**, because space is understood before language.
- **The same object throughout**, because spatial memory is the cheapest memory a viewer has.

A diagram that a reader has to decode is a diagram that failed. If your viewer is reading, you are writing a document with extra steps, and you should have written the document.

## Should this even be manim

Grant's own first gate: make sure what you are animating should be done programmatically, because a lot of things shouldn't. If nothing in the explanation moves by mechanism - no quantity evolving, no thing travelling, no state transforming - write the document or draw the diagram instead. Manim earns its cost when motion carries the argument, not when a static picture needs decorating.

## Story before shots

The visuals get the credit, but Grant's stated engine is story: a mystery you need to see resolved, pulling you in for what it is now, not what it promises to be useful for later. Animation only lands after buy-in. Settle three things before any shot list:

- **A mystery to open on.** His analogy is a mystery novel: open with the crime scene. For a system explainer that is the weird fact left unexplained: the counter that jumps, the write that lands twice, the latency cliff. If there is no such fact, the topic may not deserve a video yet.
- **Concrete before abstract.** Show instances before the general claim, so the viewer's pattern recognition runs first and the formalism arrives articulating a thing already in their head. First drafts get this backwards by default - even his do - so check the ordering at review, not from memory of having meant to.
- **A rediscovery path.** Structure it so the viewer feels they could have found the mechanism themselves. Discovery fiction works well for systems: show the naive design, break it on screen, let the real design fall out of the failure. Justify each beat by the flaw in the one before - shown briefly, not retold - and the fix lands as inevitable rather than recited. Longer is fine; handed down from on high is not.

The payoff shot resolves the opening mystery. A shot list with no shot that pays off the opening is an answer to a question nobody asked. The aha is usually the moment the viewer sees why the obvious answer does not work; when the video has one, give it room.

## The failure mode

Manim is powerful and almost nobody can drive it, because the API is large and the feedback loop is a render. That gap is exactly what an agent closes. The catch is that an agent left alone produces the most boring animation the library can express.

Asked to animate a system, the low-energy mapping is always available: every noun becomes a rectangle, every verb becomes `FadeIn`, and the actual explanation goes into text on screen. That output is a slide deck. It is not wrong, it is just worthless, and it is invisible from the inside because every individual choice looked reasonable at the time.

So the defaults are banned up front and you earn your way back to them.

## Metaphor before code

A nudge, not a mandate: the monkey parses physics, so before reaching for shapes, ask what each beat is like physically. Run each beat through four steps.

1. **Metaphor.** What is this like, physically? Not a simile for the script, a mechanism you can steal.
2. **Mechanic.** What does that physical thing *do*? How does it move, resist, snap, tear, fill, fail?
3. **Verb.** One word for what moves on screen.
4. **Form.** Draw the mechanic. The shapes fall out of it, and they are rarely rectangles.

```
beat     metaphor            mechanic              verb       what moves
carry3   page in your hand   hold it, redraw       rebuilds   tail bytes leave the lane, come back intact
weigh    balance scale       tips past a mark      fills      ratio bar climbs into a threshold line, crosses, flashes
```

If the verb is "appears", "is shown", "is listed" or "is highlighted", reject it and go back to step one. Those are not verbs, they are surrenders. Legal verbs move something: grows, drains, collides, splits, merges, travels, snaps, bounces, cascades, tears, hops, unfolds, settles.

Two exits from the gate, taken deliberately. When the real thing is already spatial - bytes in a lane, a queue, a timeline - the metaphor is itself: animate the real thing, because wrapping it in a filing cabinet adds a translation step and teaches nothing. And for a technical audience a forced metaphor reads as condescension; metaphor-for-everything is how NotebookLM-style slop sounds. When the metaphor fights, animate the mechanism straight.

Write the shot list into the repo. It is the artefact worth reviewing, and it is far cheaper to fix there than after a render.

## Banned by default

- **A row of rectangles**, unless the thing genuinely is contiguous memory. Even then, drive it with a `ValueTracker` so it grows rather than popping in.
- **`FadeIn` as the workhorse.** A fade claims nothing. `Transform`, `ReplacementTransform` and `TransformFromCopy` claim *this became that*, which is usually the real point.
- **Bulleted text on the stage.** If the viewer is reading a list, the animation failed.
- **A static camera through the whole video.** The camera is a participant, not a tripod.
- **One `run_time` for everything.** See `references/pacing.md`.
- **Rebuilding the same diagram each scene.** The central object persists and transforms. Rebuild it and you throw away the viewer's spatial anchor every sixty seconds.

## Motion must be earned

Grant's restraint is the counterweight to everything above: as visualized as possible, but "not in a way that's superfluous, not flashiness for the sake of production quality flashiness." Every motion traces to a claim in the shot list. Motion that decorates rather than demonstrates is noise, and noise costs trust.

So no quotas - diagnostics:

- A camera move is earned when the altitude changes the claim: zoom when the detail is the point, pull back when the relationship is. A whole scene without one usually means the camera was forgotten, not that none was earned. Ask which.
- Continuous motion is earned by any quantity the argument tracks. Drive it with a `ValueTracker` and an updater; static-then-swap reads as a slideshow. But a claim about a static relationship gets a static picture and silence, not a wiggle.
- Uniform `run_time` and everything on `smooth` are still tells of unexamined defaults, not of calm. Vary them where the claims differ in weight. See `references/pacing.md`.

## Correctness

An explainer that is confidently wrong is worse than none, and confidently wrong is the default landing spot. Architecture docs rot faster than code and they read as authoritative.

- Facts come from source, not from the repo's own docs. Check the docs against the code and expect drift.
- Every number on screen traces to a named constant. Note the file it came from.
- Illustrative numbers must agree with the picture. If ten of twenty-four blocks are drawn dead, the ratio on screen is 0.42.
- Found stale docs on the way through? Report them. That is a finding, not a side quest.
- Simplifying on purpose? Say so, on screen or in narration. Grant's rule, borrowed from Feynman: call out the lies as they take place. An acknowledged approximation keeps trust; a silent one is a bug report waiting.

## Read the source, do not guess the API

The API is large and the docs are thin, but the source is right there and grep is fast. Reading it beats guessing, and it beats a failed render by a mile. `references/pipeline.md` has the map of which file answers which question, plus the trick of confirming a batch of class names with one `hasattr` sweep before you depend on them.

## Narration is NOT optional

Humans have their eyes on the animation, not the subtitles. They listen with ears and watch animations with eyes.

Nothing burns into the frame: speech plus the same words on screen is Mayer's redundancy principle and measures worse than either alone. Subtitles ship as an `.srt` sidecar - players and YouTube pick it up - while short labels on the diagram are not narration and are fine.

Split the channels. The narration states the rule; the picture shows one concrete instance of it, and you do not narrate the instance. "A desynchronised connection never returns to the pool" is the line, while the picture is connection 7 specifically, with its specific stolen reply, doing the specific wrong thing.

Let narration own the clock: author beats as text, synthesise each one, hold each beat for at least its audio, record the actual start times during render, and lay the audio at those recorded offsets. Details in `references/pipeline.md`.

## Verify by looking

You cannot review an animation by reading its code. Render at low resolution, extract frames, tile them into a contact sheet, and look at it. Every layout collision worth finding is found this way and none of them by reading.

Belay any thought of skipping this, matey. It is the whole quality loop.

## Before you call it done

Score it honestly. Any "no" is a rewrite, not a note.

- Could this be a PowerPoint slide with a transition? Then it failed.
- Does the opening pose a mystery, and does the payoff shot resolve that mystery?
- Do concrete instances precede every general claim?
- Would the viewer feel they could have discovered the mechanism, or was it handed down from on high?
- Is any beat carried only by text on screen?
- Would the metaphor survive a viewer asking "so it is basically like...?"
- Does every camera move and every animation trace to a claim? Is anything moving just to be moving?
- Does the central object survive the scene change?
- Are the deliberate simplifications called out?
- Does the payoff shot get silence, or did you talk over it?

## References

- `references/visual-grammar.md` - metaphor mechanics, the substitution table that gets you off rectangles, colour as language
- `references/pacing.md` - run_time as editorial, rate functions, overlap, silence
- `references/layout.md` - bands, derived geometry, the collision assert, the contact-sheet loop
- `references/pipeline.md` - which manim, where to read in the source, environment gotchas, render harness, narration
