# Visual grammar

The creativity problem is not that good visualisations are hard to invent. It is that the boring one is always available and always looks acceptable. This file removes the boring one from the menu.

Keep the audience in mind throughout. You are mapping an abstraction onto a primate visual system that understands objects, motion, contact and distance, and does not understand concepts until they have been given a body.

## Metaphor first, then borrow its physics

The strongest generator available. Before choosing shapes, name a physical thing the mechanism is like. Then do not just reference the metaphor, **steal its mechanics**: its motion, its weight, its failure mode, its sound if it had one.

The metaphor hands you the animation for free. A rewritten sector is a page you are holding in your hand while you redraw the sheet it came from, so the bytes physically leave the lane and come back. A bloom filter is a bouncer with a list, so rejected candidates get turned away at the door rather than greyed out. Alignment is a ruler, so writes snap to it and the snap has weight. A hash chain is a row of wax seals, so breaking one visibly spoils every seal after it.

Run it as three steps:

1. **Metaphor.** What is this like, physically?
2. **Mechanic.** What does that thing *do*? How does it move, resist, break?
3. **Form.** Draw the mechanic. The shapes fall out of it.

Four rules keep this honest, because a confident wrong analogy misteaches harder than no analogy at all:

1. **It must carry the load-bearing property.** Surface resemblance is not enough. "You walk away from the coffee counter before your order is called, and now every customer takes the drink meant for the one before them" works for pooled connection desync because the self-sustaining part survives the mapping. An analogy that only captures "you got the wrong thing" has dropped the property that is the whole bug.
2. **Say where it breaks, before you need to.** If you cannot name the joint where the analogy stops being true, you do not understand the mechanism well enough to teach it with one.
3. **Cross back and stay there.** Establish the metaphor, map it onto the real components, then animate the real thing. Running both systems in parallel spends exactly the working memory you were trying to save.
4. **Pick one per concept**, not one per beat, or the video becomes a costume parade.

And skip it entirely when the real thing is already spatial. A WAL segment is a line of bytes on a disk, so animate the bytes; a filing-cabinet metaphor adds a translation step and teaches nothing. Metaphor is for the invisible mechanisms: timing, ordering, causality, ownership.

Cheap and reliable sources of physics: containers filling and draining, things travelling and colliding, snapping to a grid, stacking and toppling, tearing, sealing, threading through a maze, weighing on a balance, a queue at a door, water finding a level.

## Pick the form from the claim, not the noun

Do not ask "what does a WAL segment look like". Ask "what is this beat *claiming*", then pick the form that makes the claim visible.

| The claim | Noob default | What actually shows it |
|---|---|---|
| Two things converge until they meet | two rows of boxes | one lane, two heads travelling towards each other, gap labelled by a live `DecimalNumber` counting down |
| A value crosses a threshold | text `0.42 > 0.20` | a bar filling against a marked line, crossing it, flashing on contact |
| Most candidates get rejected | grey out the losers | a scan head that travels and *bounces off* each rejection, so rejection is motion not colour |
| Work is skipped, not done | a cross over a box | the scan head jumps the box in one arc. Distance travelled is the saving |
| This is tamper evident | boxes joined by arrows | mutate one block and cascade a colour change down the chain to the tip |
| Writes must align to a grid | dashed lines | a write that snaps to the grid, with `overshoot` so the snap has weight |
| Read, modify, write back | three words | the sector lifts out of the lane, gets patched, drops back in |
| A structure is nested | indented boxes | a real graph with edges, or an unfold from one node into its children |
| Throughput, rate, pressure | a number | a stream of dots, density is the rate |
| A state machine | a list of states | node graph, active node lit, the transition arc animating between them |
| Order over time | boxes left to right | a timeline with a playhead that runs |
| Two timelines interleave badly | two rows of boxes | two labelled tracks with playheads running, the bad ordering happening live |
| The fault sustains itself | an arrow loop | the error visibly feeding the next request, and the next, accelerating |
| One node is behind | two diagrams | one shared timeline, two playheads, the lag a visible distance |
| Something is lost | red text | the object physically falls out of frame or dissolves. Loss should look like loss |
| Two nodes agree | two identical diagrams | two different layouts producing one identical value, drawn converging into a single label |

Note the pattern. Almost every improvement replaces a *state* with a *transition*, or replaces a *label* with a *distance*. Most of them are also just a metaphor's physics applied literally.

## The four moves that carry most of the work

**Camera.** `self.frame.animate.set_width(w).move_to(p)`, and `self.frame.animate.to_default_state()` to come back. Zoom into the sector when the sector is the point. Pull back when the point is how the sector sits in the file. This is the cheapest energy change available and it costs three lines.

**ValueTracker plus updaters.** A quantity that moves continuously reads as alive; the same quantity swapped between two states reads as a slideshow.

```python
t = ValueTracker(0.0)
bar.add_updater(lambda m: m.set_width(0.1 + span * t.get_value(), stretch=True).move_to(anchor, LEFT))
gap = always_redraw(lambda: Text(f"{free(t.get_value()):.0f} bytes free"))
self.play(t.animate.set_value(1.0), run_time=2.2, rate_func=rush_into)
```

**Transform over fade.** `ReplacementTransform(a, b)` asserts a became b. `TransformFromCopy(a, b)` asserts b was derived from a and a survived. `FadeOut(a), FadeIn(b)` asserts nothing at all. Pick the one whose claim is true.

**Indication, sparingly.** `Flash`, `Indicate`, `FlashAround`, `ShowPassingFlash`, `CircleIndicate`. One per beat at most. Used on every element they stop meaning anything.

## Two registers: macro and micro

Vary scale and speed hard; the two shots answer different questions. **Macro** pulls the camera back and puts many instances on screen moving fast: a rate or a blast radius is a swarm whose density and slope the viewer feels, not a number in a caption. **Micro** pushes in on one instance and walks it a step at a time: the reproduction, one connection, one timeout, one stolen reply. Likelihood is macro, the trace is micro, consequence can be either. Cutting between them changes the scene's energy more cheaply than anything else on this page, and a video shot entirely at one scale and one speed is a slideshow with a voice over it.

## Persistence

Build the central object once. Carry it through the whole video, transforming and reframing rather than rebuilding.

A viewer spends the first seconds of every scene working out where they are. If the diagram is the same diagram, that cost is paid once. If each scene constructs its own, you pay it every time and the video feels like unrelated clips. This one choice separates a film from a deck.

Practically: hold the object on the scene, and let the next scene receive it rather than construct it. Where scenes are separate classes for render reasons, build it from one shared factory at one canonical position, so the cut lands on matching geometry and reads as continuous.

## Colour is a language, not decoration

Assign meaning once and never break it. Metadata is one colour everywhere, payload is another, dead is another. Teach the mapping in the first scene where it appears and then rely on it. A viewer who has to re-learn the colours in scene four has stopped listening to the narration.

Keep a fixed palette in one module. Never pick a colour inline.

## The 3b1b tells worth stealing

- The camera is a participant. It moves constantly and always for a reason.
- Objects morph into each other rather than being replaced, so the eye tracks identity through change.
- Numbers on screen are live and derived, not typed. When a quantity is claimed, it is displayed and it updates.
- Big reveals are given room, both in timing and in empty space around them.
- Motion is frequently continuous rather than stepwise, driven by a parameter sweeping.
- The stage is uncluttered. Things that are no longer part of the argument leave.
- Restraint is a tell too. Nothing moves for production-value flashiness; every visual serves a statement, and a claim about a static relationship gets a still frame and room to breathe.

## Anti-patterns, stated plainly

- A `VGroup` of `Text` lines is a slide. If you find yourself calling a `bullets()` helper on the stage, you have stopped animating.
- Explaining the mechanism in the subtitle while the stage shows a static diagram. The subtitle should be redundant with the picture, not a substitute for it.
- Colour-coding as the only change. Colour is weak on its own; pair it with motion or position.
- Symmetric, evenly spaced, axis-aligned everything. Real systems have asymmetry and it is usually the interesting part.
- Motion that demonstrates nothing. A camera drift, a pulse, a lagged cascade added to keep the frame busy. If deleting the motion loses no claim, delete the motion.
