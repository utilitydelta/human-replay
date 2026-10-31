# Decision sign-off in the replay

Status: built, in the guide format here and in `human-replay-vscode-extension`. The open section at the end lists what is designed and not built.

## The problem

An agent build-out makes dozens of calls nobody asked the human about, plus answers the human gave before reading any code. Typing a line is not agreeing with it: the human types past details and may not notice that a line is a decision at all. So typing confirms nothing.

A separate review session after the replay is the obvious fix, and it fails in practice. It comes days after the code was on screen, and the backlog grows faster than anyone drains it. In one project the first review agenda held 157 items and the session never ran.

So the ruling moves into the replay, while the code is on screen.

## The Rule step

A guide step with `**Action:** Rule`:

```markdown
### Step 1.1: Rule on the u16 length prefix

**Action:** Rule
**Decision:** cap-refusal
**Options:** yes | no
**Recommend:** yes

**Why:** {The recap: the call in one line, who made it and when, what breaks
without it, the code it touches as `path:line`.}
```

- `**Decision:**` is any short id: the project's own (`ADR-012`, `D-626`) or a slug the guide makes up when the project keeps no decision log.
- `**Options:**` are names the human picks from: `yes | no` to keep or reject a call as written, or variant names (`u16 | u32 | varint`) for a choice with a small set of shapes. `**Recommend:**` is optional; the picker marks it and never preselects it.
- An optional `**Shows:**` fence prints code beside the recap.

Where it goes: at the head of a closing unit's grill, or at the end of the unit that typed the code it rules on. Never mid-component: a pick needs the code on screen. Only calls that change behaviour get one, and more than a handful in a unit says the unit is too big.

## What the human sees

The recap opens read-only beside the editor, titled `<id> (read only).md`, and a picker opens with nothing selected, so Enter alone picks nothing. Esc hides the picker; Tab or the status bar brings it back, because a ruling, unlike a quiz question, cannot be skipped. The pick closes the recap and the replay moves on.

## What the extension records

One JSON line per pick, appended to `rulings.jsonl` in `.replay-record/` of the repo being replayed into, or in `humanReplay.recordDir`. Never in the sandbox: the sandbox is deleted after the replay.

```
{"decision","choice","options","recommended","guide","unit","step","at","by"}
```

- `by` is `git config user.name` in the workspace, else the OS user.
- The file is JSON Lines: one object per line, appended, never rewritten. A torn last line is skipped by readers.
- The record folder gets a `.gitattributes` with `*.jsonl merge=union`, so a team replaying on separate branches merges with no conflicts. Readers apply picks in `at` order, never file order.
- The record is also the extension's ground truth for resume: a Rule step is done when the record holds this person's pick for that decision at that step. Other people's picks don't count.

The extension never writes the project's decision log. What a pick means is the project's call.

## How a project reads it

Celeriant's bots run `scripts/decisions.py ingest <recordDir>/rulings.jsonl <session>` after a unit, once, on main, after branches merge:

- `yes`: the decision becomes `confirmed`, `human-informed`.
- `no`: back to `open`, flagged for a replacement.
- A variant name: `confirmed`, flagged so the body is rewritten to that variant.
- Every pick adds a History line naming who picked, where and when. Two people picking differently on one decision is reported, with the latest pick filed.

## Open: designed, not built

1. **The human's own words.** An optional one-line note after a pick, recorded in the line and copied into the decision's History. It answers "yes, but…", and a recap that is wrong.
2. **Send back.** A pick that holds the replay and hands the call to the agent: the agent fixes the sandbox, regenerates the guide from the next unit, and the new unit opens with a step that replays the fix. Resume already derives done-ness from the bytes, so the human picks up where the files say. Open question: how the agent hears it. Start with the human telling the agent in its terminal, with the line as the record.
3. **Park.** "Not now", with a reason, sent to the project's review backlog instead of forcing a pick.
4. **Rule ahead.** Every Rule step in the tree clickable before its unit reaches it, for a human who wants to read ahead.

Each changes the record format (`words`, a `send-back` or `park` choice), so each lands in the extension, the guide skill and the project's ingest in the same sitting.

Arr, a ruling made with the code on screen is worth ten made from memory.
