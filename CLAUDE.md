# Human Replay — agent operating guide

The scout half of Human Replay, packaged as a Claude Code plugin. An AI explores
in a disposable sandbox; this repo holds the two pieces that bracket that
exploration: the `prep` skill (copy the repo to a sandbox, arm the guard) and the
`replay-guide-generator` agent (turn the sandbox's final state into a
machine-replayable guide). What happens between them — how the agent builds in
the sandbox — is deliberately not this plugin's business. Bring your own method.

The human half is the sibling repo, `human-replay-vscode-extension`: a VS Code
extension that replays the guide into the real branch one Tab at a time.

This repo IS the plugin (`.claude-plugin/plugin.json`). The generator agent at
`agents/`, the prep skill at `skills/`, the sandbox guard at `hooks/`. The essays
at the root (`human-replay.md` and friends) are the method's rationale.

## Scope discipline

Prep and generation only. Anything that tells the sandbox agent *how* to build —
orchestration protocols, phase loops, validation cadences, grilling — belongs to
the user's own build method, not here. If a change starts prescribing the middle,
it is out of scope.

Keep it lean; every byte of this repo gets cloned to every plugin user's machine,
twice (marketplace clone plus plugin cache). No build, no tests, no runtime code.

## The guide-format contract

The replay guide is the interface between the two repos, and drift here has
broken users before. The rules:

- **The parser in `human-replay-vscode-extension` is the single source of truth
  for the format.** The generator spec describes it; the parser decides it. On
  any format change, both repos change in the same sitting.
- **Every generated guide must pass the validator before it ships:**
  `node scripts/validate-guide.js <guide> <targetRoot> <sandboxRoot>` (run from
  the extension repo). It parses with the real parser, resolves every step's
  bytes from both trees, and replays every modify step through the real engine.
  Iterate until PASS. A guide that never met the validator is a guess.
- Guides are lean: `**Symbol:**` + `**File:**` + `**Action:**` per step, no code
  fences. Bytes resolve from the target and sandbox trees at replay time.
  Brand-new boilerplate files (tests, docs) take `**Action:** Create File` —
  whole-file grain, one gesture.

## Writing rules

All prose here — the agent spec, the skill, and the guides the agent emits — is
for a technical reader with no time to waste. The writing-style rules in the root
`~/work/CLAUDE.md` apply in full. The short version: problem first, short
paragraphs, no hedging, no filler, no LLM tics. A guide step earns its length by
what it teaches, not by how completely it describes.
