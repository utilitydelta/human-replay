# Layout

Layout bugs are cheap to cause, invisible in code, and obvious the moment you look at a frame. So make them structurally hard, then look anyway.

## Bands

Split the frame into fixed horizontal bands and never let anything cross them. A typical 16:9 manimgl frame runs roughly y = -4 to +4.

| Band | y | Holds |
|---|---|---|
| Heading | +3.2 to +3.8 | one line, the scene's claim |
| Stage | -2.6 to +3.0 | everything that moves |
| Caption | -3.6 to -2.9 | silent-variant captions only; with narration this band stays empty and subtitles ship as `.srt` |

Put the band constants in one module and place against them. The moment you type a y coordinate inline, you have started a collision.

Keep a horizontal safe margin too. Content wider than about 12.6 units starts crowding the frame edge, and text at the very edge reads badly once the video is scaled down in a feed.

## Derive geometry, never guess it

Every position I hand-tuned during the first build later collided with something. Every position derived from an object survived.

- `next_to`, `align_to`, `move_to(other)`, `get_left()`, `get_right()`, `get_corner(UL)`.
- When you need a boundary, compute it. `next_bound = left + step * math.ceil((edge - left) / step)` is correct at every scale. `0` is correct until the layout moves.
- Wrap the recurring geometry in a small class that owns its own cursors and hands back placed objects. The build gets shorter and every scene agrees on where things are.

If you catch yourself writing `.move_to([-3.6, -1.35, 0])`, that is a magic number that will be wrong after the next edit.

## Assert instead of hoping

Overlap is checkable. Run it during `construct`, fail loudly.

```python
def assert_clear(*mobs, pad=0.05):
    """Bounding boxes must not intersect. Cheap insurance against silent collisions."""
    items = list(mobs)
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            ax, ay = (a.get_left()[0], a.get_right()[0]), (a.get_bottom()[1], a.get_top()[1])
            bx, by = (b.get_left()[0], b.get_right()[0]), (b.get_bottom()[1], b.get_top()[1])
            if ax[0] - pad < bx[1] and bx[0] - pad < ax[1] and ay[0] - pad < by[1] and by[0] - pad < ay[1]:
                raise AssertionError(f"overlap: {a} and {b}")
```

Call it on the things that must never touch: the caption against whatever sits lowest on the stage, the heading against the top of the diagram, two cards placed on the same row. It will not catch everything and it does not need to. It catches the class of bug that keeps happening.

Also worth asserting: nothing extends past the frame's safe width.

## Look at the frames

No amount of asserting replaces looking, because the failures that matter are aesthetic. Render small and cheap, then tile.

```bash
manimgl scenes.py S03Thing -w --resolution 640x360 --fps 12
ffmpeg -y -v error -i videos/S03Thing.mp4 -vf "select='not(mod(n\,90))'" -vsync 0 f_%02d.png
ffmpeg -y -v error -i f_%02d.png -frames:v 1 -filter_complex tile=4x4 sheet.png
```

Then open `sheet.png` and actually look. A preview render at 640x360 takes seconds, so there is no excuse for skipping it, and every collision in the first cut of the WAL video was found this way.

Two ffmpeg traps. `tile` needs `-frames:v 1` or it complains about writing multiple files with the same name. And the input frame count must be at least the tile size, or you get a partial sheet with no warning.

## Text

- Long strings need manual wrapping. Wrap to two lines and rebalance if the greedy pass leaves a runt.
- Check available fonts before hardcoding one. `fc-list : family | sort -u`. A missing font silently falls back and the metrics shift.
- Monospace for identifiers, code and numbers. Proportional for prose. Mixing them randomly makes the frame look accidental.
- Set a minimum size and hold it. Anything under about 18pt at 1080p is unreadable once the video is played in a feed at half size.

## Clean the stage

Objects that have left the argument must leave the frame. Two specific traps:

- Objects created inside a `with` block are still live afterwards. Python does not scope them; the scene will happily keep rendering them.
- Objects added by an animation but never captured in a variable, `Cross` from an indication loop being the classic, get orphaned. Track them or sweep `self.mobjects` by type before moving on.

A frame with three dead labels on it looks careless, and it is the easiest thing in the world to miss when you are reading code instead of watching output.
