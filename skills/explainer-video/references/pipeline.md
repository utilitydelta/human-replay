# Pipeline

Setup, the render harness, and narration if you want it.

## Which manim

Two incompatible forks share the name. This skill uses **manimgl**, 3b1b's own (`github.com/3b1b/manim`, package `manimgl`), and the choice is deliberate:

- 3D renders roughly 40x faster than CE's Cairo at production resolution (measured 2026-08: the same 6 second surface scene at 1080p30 took 2s in manimgl, 90s in CE). CE's OpenGL backend is officially experimental.
- `time_span` overlap and the `overshoot` rate function exist only in manimgl, and the grammar in these references leans on both.
- `DecimalNumber` is Text-based here, so live numbers need no LaTeX. CE's defaults to MathTex and hard-fails without a LaTeX install.
- CE's genuine advantages - full API docs, release discipline, plugins - serve humans maintaining code. An agent reads the source (below) and ships its own narration harness, so they buy nothing in this workflow.

manim CE (package `manim`) is what most tutorials, snippets and LLM training data target, so your memory of the API is probably CE-flavoured. Copying CE idioms into manimgl is a reliable way to waste twenty minutes: `Create` against `ShowCreation`, `self.camera.frame` against `self.frame`, different config and CLI. Confirm names with the `hasattr` sweep before depending on them.

Upstream churns without releases and PyPI is years stale, so install from source, pinned to a known-good commit:

```bash
git clone https://github.com/3b1b/manim.git && cd manim
git checkout 9d57bcf9edea2486f214e190931de2a5537f23c1  # verified working 2026-08
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -e .
```

Move the pin only after a smoke render passes on the new commit.

One deliberate exception: human-replay's `generate-clip` stays on pinned manim CE for short 2D clips built in a disposable, possibly GPU-less sandbox. CE installs from a wheel in seconds, its Cairo renderer needs no GL context at all, and none of manimgl's 3D or iteration advantages apply at that scale. The two choices disagree on purpose.

## Read the source, do not guess the API

The API is large and the docs are thin. Reading the source is faster than guessing and far faster than a failed render. Point yourself at:

| Want | Read |
|---|---|
| What animations exist | `manimlib/animation/` |
| Rate functions | `manimlib/utils/rate_functions.py` |
| Camera, frame, reorient | `manimlib/camera/camera_frame.py` |
| Shapes and their constructors | `manimlib/mobject/geometry.py` |
| Colours and frame dimensions | `manimlib/constants.py` |
| Scene lifecycle, `play`, `wait`, `time` | `manimlib/scene/scene.py` |
| Worked examples | `example_scenes.py` in the repo root |

A `hasattr` sweep over `manimlib` confirms a batch of names in one shot and costs nothing. Do that before writing a scene that depends on ten classes existing.

## Environment gotchas

- **LaTeX.** `Tex`, `TexText` and `Brace` shell out to `latex` and hard fail without it. `Text` uses pango and does not. `DecimalNumber` is built from `Text` in manimgl, so live numbers work with no LaTeX at all. Check `which latex` before planning any maths typesetting.
- **Headless.** `-w` writes the file rather than opening a window. Rendering wants a GL context but does not necessarily need a display: it has rendered fine with `DISPLAY` unset on a machine with a GPU. A bare container without one may still fail. Prove the environment with a five-line smoke scene before building anything.
- **Output path.** Files land in `videos/` relative to the project root, named after the scene class.
- **Scene clock.** `self.time` is the running scene time. That is what you record beat offsets against.
- **Preview cost.** `--resolution 640x360 --fps 12` renders in seconds. Iterate there and only go to 1920x1080 at 30fps at the end.

## Render harness

Write one script that renders every scene, muxes, concatenates and reports. Do it early. The alternative is hand-running commands and losing track of which scene is stale.

It should take a `--preview` flag, an `--only` list for iterating on one scene, and print each scene's duration and the running total. Those durations are your edit: if the title card is longer than the mechanism, you can see it without watching anything.

ffmpeg specifics that cost time to rediscover:

- `concat` demuxer needs identical codec parameters across parts. Render every scene with one resolution and fps or the join fails or drifts.
- Normalise speech with `loudnorm=I=-16:TP=-1.5:LRA=11`, and pin `-ar 48000`, because the filter will otherwise resample to something odd like 96kHz.

## Narration

Narration is the default: eyes on the animation, ears on the argument (SKILL.md). With narration, nothing burns into the frame - subtitles ship as an `.srt` sidecar and the stage carries the argument. The silent-with-captions variant is legitimate only when the deliverable autoplays muted in a feed; it is the one case where narration text belongs on the stage, and it needs more of the load. Decide up front.

Whisper is speech-to-text and is not what you need. Piper is offline, ONNX based, needs no torch, and is good enough.

```bash
uv pip install piper-tts
python -m piper.download_voices en_GB-alan-medium --download-dir voices
```

`--length-scale` is the speed dial, lower being faster. Around 0.95 suits technical narration. Output is mono 16-bit wav.

### Let narration own the clock

The arrangement that works:

1. Author narration as ordered beats in a plain data file, keyed by scene and beat id. Keep a separate `say` field for anything that does not read aloud the way it is written. `CRC32C`, `NVMe`, `I/O`, `718`, `zstd` all need spelling out for the synthesiser while the subtitle keeps the real form.
2. Synthesise each beat to its own wav and record its duration.
3. In the scene, wrap each beat in a context manager that runs the animations, then waits out whatever time is left. The beat holds for at least its audio length, never less. The subtitle goes to the `.srt`, not the stage.
4. The scene records the actual start time of every beat and writes it out.
5. Assemble the audio track by laying each wav at its recorded offset into a silent buffer of the right length. numpy and the `wave` module are enough.
6. Mux, concatenate, and emit an `.srt` from the same beat data.

Audio and video then land on the same duration with no drift, and re-timing a scene means editing a sentence rather than hunting `wait()` calls. Recording actual offsets rather than assuming them is the part that makes it exact; animations overrun, and assumed offsets accumulate error.

### Voice

Read the intended author's own writing before drafting narration, and pull their existing phrasing where they have already explained something well. It will be better than your paraphrase, and it makes the video sound like them instead of like a documentary.

Narration is heard once, linearly, at someone else's pace, so the house doc style does not apply - opposite rule. A script of short, same-shaped sentences is a metronome and the listener stops hearing it after ninety seconds. Measured against a script reviewed as "boring" (mean 8.3 words, longest 22), Grant's LLM-explainer narration runs a 24-word mean with 13 of 54 sentences over 30 words. So:

- Vary sentence length hard. Long sentences carry momentum into the next idea; short ones land the point. If nothing runs past thirty words, you have written a telegram.
- Second person roughly once every sixty words. The listener is doing the thing, not being told about it.
- Concrete first, definition second. Grant spends four sentences on a torn movie script before "a large language model is" appears.
- Make numbers felt. "Over 2600 years of non-stop reading" beats the token count; "one read in every hundred and twenty-five came back wrong" beats a percentage.
- Read the script aloud before building. If you can hear the rhythm repeating, rewrite it; the synthesiser will not save you.

Ship the transcript as a markdown file with timestamps alongside the video. It is the artefact people actually review, it is cheap to generate from the beat data, and it gets read by search engines and models in a way the video never will.
