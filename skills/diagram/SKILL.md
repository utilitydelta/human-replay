---
name: diagram
description: Draw an Excalidraw diagram only where a relationship or a flow is the thing to understand (time, control flow, data flow, ownership), with small named nodes, verbs on the arrows and the explanation as notes outside the shapes. Built from a Python spec with excali.py, which refuses text walls, arrowless boxes and unreadable sizes. Use when a build-out, replay guide or explanation needs a picture, or when asked for a diagram.
---

# Diagram

The default agent diagram is a grid of large rectangles with paragraphs inside them. It is a table drawn badly: no relationship is visible, the eye has nowhere to go, and the text is too small to read once the picture fits the screen. The human will not spend time on it.

A diagram earns its place when it shows something prose cannot: how things relate or move. If the content is a list, a set of fields or a set of facts, write a table or prose instead and draw nothing. If a dozen lines of code already tell the story, as with most algorithms, point at the code and draw nothing.

Never the whole system on one canvas. Every whole-repo diagram tool collapses into spaghetti somewhere past 15 to 30 nodes, and its own users then ask for one component's view. That view is this skill.

Why not Mermaid? Mermaid lays the picture out by itself, which is what produces the tangled, too-spread-out output this skill exists to stop. `excali.py` is the layout engine: you place the nodes, it refuses what reads badly. Mermaid is fine for an inventory graph the reader skims, like the replay guide's phase dependency graph. A diagram the human steers by while typing is drawn here.

## Gate: should this be a diagram?

Write two lines at the top of the spec before any coordinates:

1. **The question** the diagram answers, as the human would ask it. "What does a rotation carry into the new file?"
2. **The relationship** it shows: one of the kinds below.

If the second line is "it lists the parts" or "it shows the fields", stop. That is a table.

| Relationship | Shape | Example |
|---|---|---|
| Time: what happens in what order, who is waiting | Lanes per actor or file, time arrow left to right, events as small nodes, arrows for causes and messages | Rotation; a crash between two writes; an interleaving of two tasks |
| Control flow: decisions and order of checks | Top to bottom, a node per step, labelled branches, the failure exits off to the side | Which open rule fires first; what `start` checks before planning |
| State: what moves a thing from one state to another | A node per state, an arrow per transition with the event on it | Writer: Opening, Ready, Draining, Poisoned |
| Data flow: where a value comes from and where it goes | Sources left, sinks right, arrows carry the value's name | Where each field of a planned header comes from |
| Ownership and dependency: who holds or calls what | Nodes per component, arrows for "owns", "calls", "reads" | What crosses an await, and who owns it |

One diagram, one question, one relationship kind. A second kind is a second diagram.

## Grammar

- **Nodes are names.** One to four words: the thing, not a description of it. "seal", "genesis header", "publish 995".
- **Arrows carry the relationship**, with a short verb or value on them: "then", "base = write of N", "crash", "refuses". An arrow with no label must be obvious from its ends.
- **Explanations go outside, as notes.** `note()` places wrapped text in a margin and draws a dotted leader line to the node it explains. This is where the why lives: one or two sentences per note, written plainly.
- **Time runs one way.** Left to right, or top to bottom, never both in one picture. Draw the axis.
- **Colour means something.** One colour per kind of node, and one alert colour for the thing that breaks. `key()` says what each colour means; `check` refuses more than one fill, or any coloured stroke, without one. It is never obvious to the next reader.
- **Small.** About 12 nodes at most. If it needs more, it is two diagrams or the wrong level.
- **Readable at a glance.** The diagram is viewed about 700 pixels wide, so the font floor rises with the canvas: 16 px at an 800 wide camera, 18 at 1200, 21 at 1600. Fit the layout to the smallest camera you can.
- **Numbers come from the evidence**, named in the spec's docstring. No illustrative numbers without saying so in a note.
- **Every note is sourced.** A cause, cost or reason in a note needs a source like any other claim. If none is recorded, leave it out.

## Building one

1. Copy `scripts/excali.py` into the session's `diagrams/` folder, beside the spec.
2. Write `diagrams/<name>.py`: the docstring holds the question, the relationship and the evidence the arrows and numbers come from, by file or doc. Build `els` with `node`, `lane`, `axis`, `link`, `note` and `key`, then call `write("<name>", els)`.
3. Run `python3 <name>.py` (not `-I`: it imports excali from its own folder). `write` runs `check` and exits 1 on any problem:
   - a node label longer than four words or two lines (make it a note);
   - a node bigger than 300 by 120 (a block, not a node);
   - no relationship arrows (it is a table);
   - more than 14 nodes;
   - text below the font floor for the camera the layout needs;
   - overlaps, an arrow crossing a shape, a label overflowing, an arrow bound to nothing;
   - more than one colour with no `key()`.
4. Look at it: render `<name>.view.json` with the Excalidraw MCP `create_view` if it is available. Fix what reads badly even if `check` passed: a crossing leader line, a note far from its node, an arrow whose meaning is not obvious.
5. **Verify the arrows.** `check` proves the picture is readable, not that it is true. AI diagrams fail on meaning: an invented step, swapped yes and no branches, an arrow nobody can justify. A wrong arrow is worse here than in prose, because the human reads the diagram before typing and steers by it. `write` emits `<name>.claims.md`: the docstring, then every arrow as `from -verb-> to` and every note as one line. Hand that file and the evidence the docstring names to a fresh subagent that never saw the spec. For each line it answers OK, UNSUPPORTED (no source says it), WRONG (a source says otherwise) or MISSING (a step or branch the evidence has and the picture skips), with the source text that settles it. Fix the spec, rerun, re-verify the changed lines, until no row remains.
6. Commit the spec, `excali.py`, the `.excalidraw`, the `.view.json` and the `.claims.md`. The `.excalidraw` opens at excalidraw.com or in the VS Code Excalidraw extension.

Keep a short `diagrams/README.md`: one line per diagram, its question, and the guide phase or step it belongs to.

## When reviewing existing diagrams

Apply the gate to each. A diagram that answers no question, or answers it with a list, gets deleted, and its content moves into a table in the guide or doc. A diagram worth keeping but drawn as text blocks gets rebuilt with the grammar above.
