"""clipkit: the small ManimCE helper Human Replay clips are built on.

Two classes of mistake survive an LLM writing Manim, because both render cleanly
and neither raises: a shape whose parts do not exactly tile it (a one-pixel gap
inside a box), and a quantity that changes in the narration but not on screen
(the file shrank; the rectangle did not).

clipkit removes both by construction rather than by advice. Geometry is derived
from a parent, never computed by hand, so gaps cannot be expressed. Quantities
live in a Bar, and the only way to change one is a call that returns the
animation, so a silent change cannot be expressed either.

lint() is the backstop for everything else: off-frame mobjects, unreadable text,
overlaps that were not asked for.
"""

from manim import *

__all__ = ["row", "col", "inside", "caption", "narrate", "beat", "finish",
           "Bar", "Track", "lint", "LintError"]

import json
import os


# --------------------------------------------------------------------------
# layout: every child is derived from its parent
# --------------------------------------------------------------------------

def _spans(total, weights, gap):
    """Sub-spans that exactly consume `total`. Rounding lands on the last span,
    so the parts always tile the parent to the float."""
    n = len(weights)
    usable = total - gap * (n - 1)
    s = float(sum(weights)) or 1.0
    sizes = [usable * (w / s) for w in weights]
    sizes[-1] = usable - sum(sizes[:-1])
    out, cursor = [], 0.0
    for size in sizes:
        out.append((cursor, size))
        cursor += size + gap
    return out


def row(parent, weights, gap=0.0):
    """Split `parent` left to right into rectangles that exactly tile it."""
    w, h = parent.width, parent.height
    left = parent.get_left()[0]
    y = parent.get_center()[1]
    cells = []
    for start, size in _spans(w, weights, gap):
        r = Rectangle(width=size, height=h, stroke_width=0, fill_opacity=0)
        r.move_to([left + start + size / 2, y, 0])
        cells.append(r)
    return cells


def col(parent, weights, gap=0.0):
    """Split `parent` top to bottom into rectangles that exactly tile it."""
    w, h = parent.width, parent.height
    top = parent.get_top()[1]
    x = parent.get_center()[0]
    cells = []
    for start, size in _spans(h, weights, gap):
        r = Rectangle(width=w, height=size, stroke_width=0, fill_opacity=0)
        r.move_to([x, top - start - size / 2, 0])
        cells.append(r)
    return cells


def inside(parent, mob, pad=0.15):
    """Scale `mob` down if needed and centre it in `parent`. Never overflows."""
    max_w, max_h = parent.width - 2 * pad, parent.height - 2 * pad
    if max_w <= 0 or max_h <= 0:
        raise LintError("inside(): parent too small for padding")
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    if mob.height > max_h:
        mob.scale(max_h / mob.height)
    return mob.move_to(parent.get_center())


def caption(text, size=28, color=WHITE):
    """One line of narration, parked on the bottom strip where nothing else goes."""
    t = Text(text, font_size=size, color=color)
    if t.width > config.frame_width - 1.0:
        t.scale((config.frame_width - 1.0) / t.width)
    return t.move_to([0, -config.frame_height / 2 + 0.75, 0])



# --------------------------------------------------------------------------
# narration: the audio owns the clock
# --------------------------------------------------------------------------

VOICE_DIR = os.environ.get("CLIPKIT_VOICE", "voice")
_LINES = {}


def narrate(lines):
    """Register the narration. Call once at module level, above the Scene.

        narrate([
            ("wire", "A timeout drops the future with the request on the wire."),
            ("land", "The response lands afterwards, and the next reader takes it."),
        ])

    Keys are what `beat()` addresses. The build script reads these to synthesise
    the audio before the render, which is why they live outside construct().
    """
    _LINES.clear()
    for key, text in lines:
        if key in _LINES:
            raise LintError(f"narrate(): duplicate key {key!r}")
        _LINES[key] = text
    return _LINES


def _durations():
    path = os.path.join(VOICE_DIR, "durations.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def beat(scene, key, *anims, gap=0.35, run_time=None, max_stretch=2.5):
    """One narration beat: play the change while the line is spoken, and hold
    until the audio is finished.

    The audio owns the clock. The animation is fitted to the line rather than the
    other way round, so the motion plays out across the sentence instead of
    snapping done and leaving the viewer on a still frame while the speaker is
    still talking. Whatever is left over after the motion is the window where
    they take it in.

    That is the other reason narration is not decoration: it is the only
    principled source of timing in the clip. Without it, hold lengths are a
    guess, and they will be guessed short.

    A beat with no animations raises. The narration cannot advance while the
    picture stands still, which is the other half of Bar's guarantee: Bar stops
    the numbers drifting from the picture, beat stops the words drifting from
    both.
    """
    if key not in _LINES:
        raise LintError(f"beat({key!r}): no narration registered under that key. "
                        f"Known keys: {sorted(_LINES) or 'none, did you call narrate()?'}")
    flat = []
    for a in anims:
        flat.extend(a if isinstance(a, (list, tuple)) else [a])
    if not flat:
        raise LintError(f"beat({key!r}): no animations. Narration advancing over "
                        "a still picture is the mistake this refuses. Pass the "
                        "animations, or use caption() for a silent title card.")

    durs = _durations()
    audio = (durs or {}).get(key)
    if audio is None:
        # preview render before the voice is built; fall back to a read-speed guess
        audio = 0.35 + 0.06 * len(_LINES[key].split())

    if run_time is not None:
        for a in flat:
            a.run_time = run_time
    span = max(getattr(a, "run_time", 1.0) for a in flat)

    # Fit the motion to the line. Too long and the words finish over a moving
    # picture; too short and the viewer stares at a still frame while the
    # speaker is still talking. Stretch is capped so a long sentence does not
    # turn a small move into slow motion.
    target = min(audio, span * max_stretch) if span < audio else audio
    if abs(target - span) > 0.01:
        for a in flat:
            a.run_time = a.run_time * (target / span)
        span = target

    start = float(scene.renderer.time)
    scene.play(*flat)
    remainder = audio - span + gap
    if remainder > 0:
        scene.wait(remainder)

    scene._clipkit_beats = getattr(scene, "_clipkit_beats", [])
    scene._clipkit_beats.append(
        {"key": key, "start": start, "audio": audio, "text": _LINES[key]})


def finish(scene):
    """Write the beat timings the build script needs, then lint. Last line of
    construct(). Skipping it means the audio has nowhere to land."""
    beats = getattr(scene, "_clipkit_beats", [])
    if not beats:
        raise LintError("finish(): no beats were played. A clip with no narration "
                        "is not a clip.")
    os.makedirs(VOICE_DIR, exist_ok=True)
    out = os.path.join(VOICE_DIR, f"timing_{type(scene).__name__}.json")
    with open(out, "w") as f:
        json.dump({"scene": type(scene).__name__, "beats": beats}, f, indent=2)
    lint(scene)

# --------------------------------------------------------------------------
# Bar: named quantities that cannot change without animating
# --------------------------------------------------------------------------

class Bar(VGroup):
    """A rectangle partitioned into named parts. The parts always tile the bar
    exactly, and `to()` is the only way to change them, so the picture cannot
    drift from the numbers.

        bar = Bar(width=11, height=1.6, parts={"live": 6, "dead": 1, "free": 3},
                  colors={"live": GREEN_D, "dead": RED_D, "free": GREY_E})
        scene.play(*bar.to(dead=0, free=4))     # reclaim; the picture follows
    """

    def __init__(self, width, height, parts, colors, gap=0.0, **kw):
        super().__init__(**kw)
        self.bar_w, self.bar_h, self.gap = width, height, gap
        self.parts = dict(parts)
        self.colors = dict(colors)
        self.frame = Rectangle(width=width, height=height,
                               stroke_color=GREY_B, stroke_width=2, fill_opacity=0)
        self.cells = {}
        for name, cell in zip(self.parts, self._cells()):
            cell.set_fill(self.colors.get(name, GREY), 1.0).set_stroke(width=0)
            self.cells[name] = cell
        self.add(self.frame, *self.cells.values())

    def _cells(self):
        return row(self.frame, list(self.parts.values()), self.gap)

    def total(self):
        return sum(self.parts.values())

    def to(self, run_time=1.0, **changes):
        """Set part values and return the animations that make the picture match.
        Unknown names raise, so a typo cannot silently animate nothing."""
        unknown = set(changes) - set(self.parts)
        if unknown:
            raise LintError(f"Bar.to(): unknown part(s) {sorted(unknown)}; "
                            f"known parts are {sorted(self.parts)}")
        if not changes:
            raise LintError("Bar.to(): called with no changes")
        before = dict(self.parts)
        self.parts.update(changes)
        if self.parts == before:
            raise LintError(f"Bar.to(): {changes} leaves every part unchanged; "
                            "nothing would animate")
        anims = []
        for name, target in zip(self.parts, self._cells()):
            target.set_fill(self.colors.get(name, GREY), 1.0).set_stroke(width=0)
            anims.append(Transform(self.cells[name], target, run_time=run_time))
        return anims

    def resize(self, width, run_time=1.0):
        """Shrink or grow the whole bar. Parts re-derive, so they cannot be
        left behind at the old size."""
        self.bar_w = width
        new_frame = Rectangle(width=width, height=self.bar_h,
                              stroke_color=GREY_B, stroke_width=2, fill_opacity=0)
        new_frame.move_to(self.frame.get_center())
        anims = [Transform(self.frame, new_frame, run_time=run_time)]
        probe = new_frame.copy()
        for name, target in zip(self.parts, row(probe, list(self.parts.values()), self.gap)):
            target.set_fill(self.colors.get(name, GREY), 1.0).set_stroke(width=0)
            anims.append(Transform(self.cells[name], target, run_time=run_time))
        return anims


class Track(VGroup):
    """A labelled horizontal timeline. Two or more of these is what an
    interleaving looks like, which is what most invariant clips are about."""

    def __init__(self, label_text, width=9.0, color=BLUE_D, **kw):
        super().__init__(**kw)
        self.line = Line([-width / 2, 0, 0], [width / 2, 0, 0],
                         stroke_color=color, stroke_width=3)
        self.label = Text(label_text, font_size=24, color=color)
        self.label.next_to(self.line, LEFT, buff=0.3)
        self.width_ = width
        self.add(self.line, self.label)

    def at(self, t, mob, above=True):
        """Place `mob` at fraction t (0..1) along the track."""
        if not 0.0 <= t <= 1.0:
            raise LintError(f"Track.at(): t={t} outside 0..1")
        x = self.line.get_left()[0] + t * self.width_
        y = self.line.get_center()[1]
        mob.move_to([x, y + (0.45 if above else -0.45), 0])
        return mob


# --------------------------------------------------------------------------
# lint: the backstop
# --------------------------------------------------------------------------

class LintError(Exception):
    pass


def _bbox(m):
    return (m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])


def _describe(m):
    if isinstance(m, Text):
        return f"Text({m.text[:34]!r})"
    return type(m).__name__


def lint(scene, min_text_height=0.16, allow_overlap=()):
    """Check what a human eye would catch and a renderer will not.

    Call at the end of construct(). Raises LintError listing every problem at
    once, so one run reports all of them rather than one per render.

    `allow_overlap` is a collection of mobjects excused from the overlap check,
    for the cases where stacking is the point.
    """
    problems = []
    half_w = config.frame_width / 2 + 0.01
    half_h = config.frame_height / 2 + 0.01
    excused = set(id(m) for m in allow_overlap)

    tops = [m for m in scene.mobjects if m.get_family() and
            any(x.has_points() for x in m.get_family())]

    for m in tops:
        l, r, b, t = _bbox(m)
        if l < -half_w or r > half_w or b < -half_h or t > half_h:
            problems.append(f"off frame: {_describe(m)} bbox "
                            f"x[{l:.2f},{r:.2f}] y[{b:.2f},{t:.2f}] "
                            f"(frame is x[{-half_w:.2f},{half_w:.2f}] "
                            f"y[{-half_h:.2f},{half_h:.2f}])")

    for m in tops:
        for txt in [x for x in m.get_family() if isinstance(x, Text) and x.has_points()]:
            if txt.height < min_text_height:
                problems.append(f"text too small to read: {txt.text[:34]!r} "
                                f"height {txt.height:.3f} < {min_text_height}")

    texts = [m for m in tops if isinstance(m, Text) and id(m) not in excused]
    for i, a in enumerate(texts):
        for b_ in texts[i + 1:]:
            al, ar, ab, at_ = _bbox(a)
            bl, br, bb, bt = _bbox(b_)
            if al < br and bl < ar and ab < bt and bb < at_:
                problems.append(f"text overlaps text: {a.text[:28]!r} / {b_.text[:28]!r}")

    if problems:
        raise LintError(f"clipkit.lint found {len(problems)} problem(s):\n  - "
                        + "\n  - ".join(problems))
