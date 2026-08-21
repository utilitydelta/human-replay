# Pacing

Flat pacing is the second-most obvious tell after rectangles, and it comes from the same place: `run_time=0.6` is always a defensible choice, so it gets chosen every time. A scene where every animation takes about the same time has no shape, and a video made of those has no rhythm.

## run_time is an editorial decision

Time on screen is how you say what matters. Spend it unevenly.

- The most important object in a scene gets the longest `run_time` in that scene. If the carry buffer is the point, the carry buffer gets 2 seconds and the labels get 0.3.
- When the claims in a scene genuinely differ in weight, the spread between fastest and slowest lands at 4x or more on its own. A scene where everything sits within a factor of two has no shape: either the timing was not edited, or the scene has no point to weight. Work out which.
- Incidental setup should be fast to the point of being almost subliminal. 0.15 to 0.3 is fine. Nobody needs 0.8 seconds to watch a caption arrive.
- A reveal that lands the argument can take 2 to 3 seconds and should.

## Rate functions

`smooth` on everything is a flat affect. Available in manimgl: `linear`, `smooth`, `double_smooth`, `rush_into`, `rush_from`, `running_start`, `slow_into`, `there_and_back`, `there_and_back_with_pause`, `overshoot`, `wiggle`, `exponential_decay`, `lingering`, `not_quite_there`, `squish_rate_func`.

Match the function to the physics of the claim:

| Motion | Function | Why |
|---|---|---|
| Machine or clock driven | `linear` | Hardware does not ease. A DMA write should not feel organic |
| Launch, then coast | `rush_into` | Something starting under its own power |
| Arriving and settling | `rush_from`, `slow_into` | Deceleration into a resting place |
| Snapping to a boundary | `overshoot` | Gives the snap weight and makes alignment feel physical |
| Bounce off a rejection | `there_and_back` | The attempt happened and was refused |
| Decay, drain, forget | `exponential_decay` | |
| Nervous, unstable, wrong | `wiggle` | Use once per video at most |

Match the function to the claim's physics, not a quota. A scene where everything runs on `smooth` is usually unexamined rather than calm; a scene where three claims share one motion character deserves a second look either way.

## Overlap instead of chaining

Chained `self.play` calls restart the energy from zero each time and produce a stuttering, listy feel. manimgl's `time_span` places an animation inside a single play call's window:

```python
self.play(
    FadeIn(header, time_span=(0.0, 0.5)),
    GrowArrow(cursor, time_span=(0.3, 1.1)),
    Write(formula, time_span=(0.9, 2.0)),
    run_time=2.0,
)
```

That reads as one continuous move. Three separate plays read as three separate events.

`LaggedStart` and `LaggedStartMap` take a `lag_ratio`, which is a pacing dial and not a constant. Low values overlap into a wave; high values become a countable sequence. Pick per use.

## Anticipation, action, settle

A movement that matters gets a small preparation before it and a small settle after. Pull back slightly before a jump. Overshoot slightly on arrival and come back. Two extra tenths of a second on each side is the difference between an object moving and an object being repositioned.

## Silence is part of the edit

Do not narrate the payoff. When the reveal lands, stop talking for a beat and let the picture carry it. A wall-to-wall narration track with no gaps is exhausting and it flattens the moments that should stand out.

Budget it deliberately: after the shot that makes the argument, one to two seconds of nothing.

## Beat timing against narration

When narration exists, it owns the clock. The rule is that a beat holds for at least the length of its audio, never less. Animations inside the beat run at their own chosen pace and the leftover becomes a hold.

Do not dump the leftover at the end by default. If a beat has 6 seconds of audio and 1.5 seconds of animation, decide where the 4.5 seconds of stillness belongs. Usually it belongs after the key movement, not before it, so the viewer looks at the result while the sentence finishes.

Record the actual start time of each beat during the render rather than assuming it. Animations overrun; assumed offsets drift; recorded offsets do not.

## Scene length

Weight scene length to importance, and check it after rendering. If the section you consider central is not among the longest, the edit disagrees with you and one of you is wrong.

A rough sanity check: read out the per-scene durations and ask whether that ordering matches the shot list's priorities. Ye be steering by the wrong star if the title card runs longer than the mechanism.
