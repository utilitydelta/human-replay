---
name: generate-clip
description: Build one Manim clip (1-5min duration) for an invariant trace or a bug story selected by suggest-clips. Sets up a disposable ManimCE environment, builds against the clipkit helper, and verifies by looking at rendered frames.
---

# Generate Clip

One clip, one idea, 1-5min each. Called by `suggest-clips` with a written
trace or a set of bug-story beats already in `session/clips/<slug>.md`. Do not
re-derive the content here. Your job is to put it on screen and prove it landed.

Clip time is flexible, better to be complete, clear and correct than ambiguous or leave out important details.
The price is developer attention, long clips must earn it.

## Environment

ManimCE from PyPI. There is no repository to clone.

```bash
uv venv .clipenv --python 3.12
uv pip install --python .clipenv/bin/python "manim==0.21.0" piper-tts
```

Put `.clipenv` in the sandbox and delete it with the sandbox. `du` will say
368MB and `du` is lying: uv hardlinks every file out of its global cache, so a
second venv alongside the first measures 20MB. The bytes live in `~/.cache/uv`
once and every sandbox borrows them. A warm install takes about two and a half
seconds.

So no shared location, no manual cleanup discipline, nothing to keep. Build it
in the sandbox, throw it away with the sandbox, build it again next time.

The one exception is voice models. Piper fetches those over the network rather
than from uv, so `clipbuild.py` caches them in `~/.cache/human-replay/voices`
and every sandbox shares them. 63MB for the default voice, fetched once.

Build:

```bash
.clipenv/bin/python clipbuild.py clip.py ClipName --preview   # iterate, 480p15
.clipenv/bin/python clipbuild.py clip.py ClipName             # ship, 1080p60
```

That synthesises the narration, renders, lays each line at the second its beat
started, muxes, and writes the `.srt`. Do not call `manim` directly except to
check a render error in isolation; the timing contract lives in the build.

Two constraints on most machines. No LaTeX, so `Tex`, `MathTex` and `Brace` are
out and all text is pango via `Text`. And ManimCE, not manimgl: in manimgl
`Text(..., color=RED)` and `Arrow(..., color=RED)` are accepted and then silently
overwritten (verified 2026-08 on manimgl master), so the scene renders clean and
grey while the caption talks about the red path. ManimCE honours both. Do not
switch renderers to match a snippet you remember.

The `explainer-video` skill recommends manimgl for full videos, and that choice
does not transfer here: clips are 2D, the sandbox may have no GPU, and CE
installs from a wheel in seconds where manimgl needs a git clone. Take its
story, grammar and pacing; skip its install and fork-specific API notes. The
two skills disagree on purpose.

## Build against clipkit

`clipkit.py` sits beside this file. Copy it next to your scene and import it.
It exists because two mistakes survive every render and neither one raises:

- Parts of a shape that do not exactly tile it. A one pixel gap inside a box.
- A quantity that changes in the words but not on screen. The file was
  reclaimed; the rectangle never shrank.

clipkit removes both by construction rather than by warning you about them.

```python
from manim import *
from clipkit import Bar, Track, narrate, beat, finish, row, col, inside

narrate([
    ("dead",   "Two blocks in this segment are dead. Their aggregates were superseded."),
    ("claim",  "Reclaim drops them, and the free space at the tail grows to take their place."),
    ("shrink", "The segment itself is then truncated, and every extent moves with it."),
])

class Reclaim(Scene):
    def construct(self):
        bar = Bar(width=11, height=1.6,
                  parts={"live": 6, "dead": 1, "free": 3},
                  colors={"live": GREEN_D, "dead": RED_D, "free": GREY_E})
        self.add(bar)
        beat(self, "dead",   *bar.to(dead=2, live=5))
        beat(self, "claim",  *bar.to(dead=0, free=4))
        beat(self, "shrink", *bar.resize(7.0))
        finish(self)
```

`narrate()` sits at module level because the build script imports the file to
read the lines before any rendering happens. It has to know how long each line
takes before the scene can decide how long to hold.

What that buys you:

- `row`, `col` derive children from a parent so they tile it exactly. Never
  position a thing that lives inside another thing with `.shift()` arithmetic.
  That is where the gaps come from.
- `inside` scales a label down to fit its box instead of letting it overflow.
- `Bar.to()` is the only way to change a quantity, and it returns the animation.
  It raises on an unknown part name, on an empty call, and on a change that
  leaves every part where it was. A typo cannot quietly animate nothing.
- `Bar.resize()` re-derives every part, so shrinking the whole cannot leave the
  contents at the old size. This is the celeriant reclaim mistake, closed.
- `beat()` plays the change while the line is spoken and holds until the audio
  finishes, so nothing important happens in silence and no line runs past its
  picture. An animation longer than its line is scaled down to fit. It raises on
  an unregistered key and on a beat with no animations, so the narration cannot
  advance over a still picture.
- `finish()` writes the beat timings the build script needs and then lints.
  It is the last line of `construct()`.
- `Track` is a labelled timeline. Two or three of them stacked is what an
  interleaving looks like, which is most of what these clips are about.
- `lint(self)` at the end of `construct` catches off-frame mobjects, text too
  small to read, and text overlapping text. It reports every problem in one run
  with the frame bounds included, so you fix them in one pass.

Anything clipkit does not model, you write by hand, and then you are back in the
territory where mistakes are silent. Keep the hand-written part small.

## Look at the frames. This is not optional

`lint` catches geometry. It does not catch a picture that is wrong, and a clean
render proves nothing. Every clip goes through this before it ships:

```bash
.clipenv/bin/python clipbuild.py clip.py ClipName --preview
# one frame per beat, taken from the middle of each beat's span
python - <<'EOF'
import json, subprocess
t = json.load(open("voice/timing_ClipName.json"))
mid = [b["start"] + b["audio"] / 2 for b in t["beats"]]
sel = "+".join(f"lt(abs(t-{m:.2f})\\,0.04)" for m in mid)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "ClipName.mp4", "-vf",
                f"select='{sel}',tile=1x{len(mid)},scale=760:-1",
                "-frames:v", "1", "-vsync", "0", "frames.png"])
EOF
```

Then read `frames.png`, with `ClipName.srt` open beside it so you know which
line is being spoken over which frame, and check in order:

1. Does every quantity the caption mentions actually differ from the previous
   beat? This is the failure that survives everything else.
2. Do the colours mean what the caption says they mean?
3. Is anything overlapping, clipped, or floating in a way a person would
   notice in half a second?
4. Does each frame match the line the subtitle says is playing over it? A
   picture that lags its narration by one beat is the classic failure and it is
   invisible unless you line the two up.
5. Did the build print a warning about narration running past the end?

Fix and rebuild until the strip is right. Then build once without `--preview`.

## Shape of the clip

The craft lives in the `explainer-video` skill that ships with human-replay:
story before shots, metaphor discipline, the claim-form table, pacing, narration
voice. Read it before writing a scene, with the scoping rule from Environment
above: its fork and install notes do not apply here.

Open on the consequence. Macro motivation for a replay clip is nearly always
the thing a client will eventually notice - a duplicate business event, durable
on both nodes. Not architecture.

**Invariant trace.** Three beats.

1. The design as it plausibly reads. The viewer should agree with it.
2. The trace that breaks it, carrying the real number the loop produced. This
   beat is the clip; the other two exist to make it land.
3. The fix, and why the invariant is worded the way it is.

**Bug story.** The five beats already written in the clip file: how it surfaced,
the reproduction, risk as consequence and likelihood separately, the corrective
action and its weight, what is still open. Give beat 3 real screen time. A
duplicate durable on both nodes at 0.11 to 0.43% of aggregates is a different
animal to a one-in-a-billion trigger, and the picture should make that obvious.

Beat length is not yours to set, and that is the third reason narration is not
decoration. It is the only principled source of timing in the clip. Left to pick
hold lengths yourself you will pick them short, because you already know what the
picture means.

`beat()` stretches the motion to play out across the sentence rather than
snapping done, and whatever is left after the motion is the window where the
viewer takes it in. If a beat feels rushed the sentence is too short, so write a
longer one. If it drags, cut words. Editing the narration is how you edit the
timing.

## Craft, in clipkit terms

explainer-video's macro/micro registers map straight onto the helpers:

- **Macro** is `pull_back()` plus `swarm()`: many instances, running fast.
  12,000 reads degrading to a 99.2% error rate is a swarm whose slope the
  viewer feels, not a number in a caption. Likelihood is macro.
- **Micro** is `push_in()` on one instance, walked a step at a time. The
  reproduction: one connection, one timeout, one stolen reply. The trace is
  micro.
- Consequence can be either. A register cut is the cheapest energy change a
  clip has; a clip that never earns one is usually a slideshow with a voice
  over it, so ask why yours didn't.

The clipkit realisations of the claim forms that recur here:

- An interleaving is two or three stacked `Track`s with playheads running, the
  bad ordering happening live. This is most of what these clips are about.
- A window that must never close: two heads converging on a marked gap, a live
  countdown between them.
- A rate or blast radius: `swarm()`, density is the rate.
- A quantity changing: `Bar.to()`, never a swapped label.

## Rules

- Narration is the point, not a nicety. The viewer is watching the animation, so
  their visual channel is fully spent and there is nothing left over for reading.
  Words go in through the ears. This is Mayer's modality principle and it is the
  single largest effect in the multimedia literature.
- Which is also why the narration does not appear burned into the frame. Speech
  plus the same words on screen is the redundancy principle, and it measures
  worse than either alone. Subtitles ship as a `.srt` sidecar, so anyone who
  needs them turns them on. Short labels on the diagram are not narration and are
  fine.
- One idea per clip. If you need a fourth concept, it is a second clip or it is
  guide prose.
- Numbers on screen come from the run named in the clip file. If a number is
  illustrative rather than measured, say so in the caption or leave it out.
  Never invent a rate to make a beat land.
- No codenames. Same rule as the guide: name things by what they do.
- Anything statable in one sentence of prose belongs in the guide, not here.

## Output

Everything for one clip lands in `session/clips/`:

- `<slug>.md` the brief, written by `suggest-clips`
- `<slug>.py` the scene, so the human can re-render or fix it without you
- `<slug>.mp4` the clip, narration muxed in
- `<slug>.srt` the subtitles

Work in a scratch directory, not in `session/clips/`, and copy the four files
across when the clip is done. The build leaves `voice/`, `media/` and `.clipenv`
behind; none of them belong in the session output and all of them die with the
sandbox.
