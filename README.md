# Human Replay

**Vibe without guilt. Replay with understanding.**

<img src="vibing.png" alt="Vibe coding in a sandbox" width="350" align="right">

Vibe coding is intoxicating. You describe what you want, the AI builds it, three hours later you have a feature that would have taken two weeks.

Then you read the code. It works. Mostly. Abstractions you would never pick. Fields the AI declared and never read. Bugs hiding in the seams between components nobody tested together.

Two options. Ship the entropy, or throw it away and lose the insight. Both are bad.

There is a third path.

Code is cheap. Understanding is expensive. The AI's value is the *exploration*, not the code that came back with it. Let it explore freely in a sandbox. Then replay its discoveries with your own hands, in your own style, with your own understanding.

The AI explores. You integrate. The map becomes territory you walked yourself. Your codebase stays yours.

Read more:

- [`human-replay.md`](human-replay.md) for the method in full
- [`critique-of-brute-force-ai.md`](critique-of-brute-force-ai.md) for why pure agentic loops like RALPH devalue real engineering
- [`workshop-takeaways.md`](workshop-takeaways.md) for what to take and leave from Anthropic's Claude Code workshop playbook

<br clear="both">

## What this is

A Claude Code plugin that brackets a sandbox session. Three pieces:

- **`/prep`** — copies your repo to a disposable sandbox and arms the sandbox guard.
- **`replay-guide-generator`** — an agent that reads the sandbox's final state and produces an ordered rebuild path.
- **`sandbox-guard`** — a hook that makes the sandbox unpublishable.

What happens *between* prep and generation — how you or your agents build in the sandbox — is deliberately not this plugin's business. Use whatever method you already trust.

```
PREP → YOUR BUILD-OUT → REPLAY GUIDE → REAL CODEBASE
 AI      any method       AI            You
```

The replay itself can be manual, or driven Tab by Tab through the [`human-replay-vscode-extension`](https://github.com/utilitydelta/human-replay-vscode-extension), which resolves each guide step's bytes from the sandbox and the target tree and replays them into your real branch as inline completions.

## Install

Inside Claude Code, run:

```
/plugin marketplace add utilitydelta/human-replay
/plugin install human-replay@human-replay
```

Both are slash commands, not shell. The first registers this repo as a marketplace; the second installs the plugin from it. Reload plugins (`/reload-plugins`) or restart Claude Code. The `/prep` skill, the `replay-guide-generator` agent, and the sandbox-guard hook are now active in every project.

## Quick start

### 1. Set up the sandbox

From your real repo, invoke `/prep`. It asks where to put the sandbox (default `~/sandbox/[repo-name]-[feature-slug]`), copies the repo, and drops a `.sandbox` marker that arms the guard hook.

Manual equivalent:

```bash
cp -r /path/to/your-repo ~/sandbox/your-repo-feature
cd ~/sandbox/your-repo-feature
touch .sandbox
```

You do not need `git remote remove origin`. The hook blocks `git push` and origin rewrites from any directory containing a `.sandbox` marker. Keeping the origin lets you `git fetch` to compare against upstream when useful.

### 2. Build

Open Claude Code in the sandbox and build however you like — a single agent, your own orchestration skills, by hand. The sandbox is throwaway; the only thing the next step needs is the final state and whatever notes your method leaves behind.

### 3. Generate the replay guide

When the work settles, from the sandbox:

```
Generate a replay guide for this session. Base commit: abc123
```

The generator reads whatever session artifacts exist (progress logs, design docs, commit messages), then the diff. Output goes to `replay-guides/{name}.md`, validated against the real parser before it ships.

### 4. Replay

In your real repo, with your patterns. By hand, or step by step with the `human-replay-vscode-extension`: point `replayTab.sandboxRoot` at the sandbox, open the guide, and Tab through each symbol's Before→After. Then delete the sandbox.

## What the replay guide contains

- **Overview.** What was built, key decisions, files affected.
- **System Invariants.** Carried verbatim when your session captured them; reconstructed from code (and labeled as such) when it didn't.
- **Dependency graph.** Mermaid diagram showing build order.
- **Phased steps.** Grouped by layer (Data Models → Core Logic → API → Tests). Each step names a symbol, a file, and an action; no big code blocks — the replay tool resolves the actual bytes from the sandbox and target trees.
- **Domain-specific retrospectives.** Reflection prompts tailored to the codebase type (frontend, backend, database, infra, real-time, ML, CLI).
- **Checkpoints.** Understanding checks and design critiques between phases.

Each step has a Retrospective like:

- *"What happens to `UserSession` if the token expires mid-request?"*
- *"Will this query use an index, or will it table scan?"*
- *"What is the failure mode if the external service is unavailable?"*

These force critical reading. Catch the edge cases the LLM missed.

## Sandbox discipline

One deterministic hook ships in `hooks/sandbox-guard.sh`. Fires when `.sandbox` is present at the repo root.

**Pre-tool-use guard.** Blocks `git push`, `git remote add origin`, and `git remote set-url origin` from inside a sandbox. Sandboxes are throwaway. Replay in your real working copy and push from there.

Claude cannot talk its way past it. Disable by removing the marker.

## License

MIT
