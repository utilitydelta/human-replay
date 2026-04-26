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

A Claude Code plugin that operationalizes Human Replay. You vibe in a throwaway. The orchestrator spawns a researcher, grills you on system invariants, then runs autonomous phases. When you are done, the replay-guide generator analyzes the final state and produces an ordered rebuild path.

```
SANDBOX → GRILLING → AUTONOMOUS PHASES → REPLAY GUIDE → REAL CODEBASE
  AI       You          AI                 AI            You
```

## Install

One-time, global:

```bash
claude plugin install https://github.com/utilitydelta/human-replay
```

Reload plugins (`/reload-plugins`) or restart Claude Code. The plugin's skills (`/vibe-prep`, `/vibe-coding`, `/vibe-status`, `/grill-me`), agents, and the sandbox-discipline hook are now active in every project.

### Permissions allowlist (recommended)

Plugins cannot ship permission rules. To stop autonomous runs from stalling on permission prompts every five minutes, paste this into your user settings (`~/.claude/settings.json` under `permissions.allow`) or your project's `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(git show:*)",
      "Bash(git branch:*)", "Bash(git ls-files:*)", "Bash(git blame:*)",
      "Bash(git rev-parse:*)", "Bash(git add:*)", "Bash(git commit:*)",
      "Bash(git checkout:*)",
      "Bash(rg:*)", "Bash(grep:*)", "Bash(find:*)", "Bash(ls:*)", "Bash(cat:*)",
      "Bash(head:*)", "Bash(tail:*)", "Bash(wc:*)", "Bash(file:*)",
      "Bash(mkdir -p:*)", "Bash(touch:*)",
      "Bash(cargo test:*)", "Bash(cargo check:*)", "Bash(cargo build:*)",
      "Bash(cargo clippy:*)", "Bash(cargo fmt:*)", "Bash(cargo run:*)",
      "Bash(npm test:*)", "Bash(npm run build:*)", "Bash(npm run lint:*)",
      "Bash(npm run typecheck:*)", "Bash(npm install:*)", "Bash(npx tsc:*)",
      "Bash(yarn test:*)", "Bash(yarn build:*)", "Bash(pnpm test:*)",
      "Bash(pnpm build:*)", "Bash(pytest:*)", "Bash(python -m pytest:*)",
      "Bash(python -m mypy:*)", "Bash(go test:*)", "Bash(go build:*)",
      "Bash(go vet:*)", "Bash(make test:*)", "Bash(make build:*)",
      "Bash(make check:*)", "Bash(make lint:*)"
    ]
  }
}
```

Read-only and standard-build commands only. Anything destructive still prompts.

### Manual install (no plugin support)

If `claude plugin install` is not available in your Claude Code build, clone this repo and copy the contents into your project's `.claude/` directory:

```bash
git clone https://github.com/utilitydelta/human-replay /tmp/human-replay
mkdir -p .claude
cp -r /tmp/human-replay/agents .claude/
cp -r /tmp/human-replay/skills .claude/
cp -r /tmp/human-replay/hooks .claude/
```

Then add a `.claude/settings.json` referencing the hook script and the permissions block above.

## Quick start

### 1. Set up the sandbox

From your real repo, invoke `/vibe-prep`. It asks where to put the sandbox (default `~/sandbox/[repo-name]-[feature-slug]`), copies the repo, drops a `.sandbox` marker that arms the discipline hook.

Manual equivalent:

```bash
cp -r /path/to/your-repo ~/sandbox/your-repo-feature
cd ~/sandbox/your-repo-feature
touch .sandbox
```

You do not need `git remote remove origin`. The hook blocks `git push` and origin rewrites from any directory containing a `.sandbox` marker. Keeping the origin lets you `git fetch` to compare against upstream when useful.

### 2. Vibe

Open Claude Code in the sandbox and invoke `/vibe-coding`. Provide a design doc or feature description.

What happens, in order:

1. **Researcher.** Explores the codebase. Surfaces candidate system invariants and links to existing architecture docs. Returns a brief.
2. **Grilling** (vendored from [`mattpocock/skills`](https://github.com/mattpocock/skills)). The orchestrator interrogates you one question at a time until every branch of the decision tree is resolved and the system invariants list is approved. Spend 30 minutes here to save 3 hours later.
3. **Phases.** The orchestrator breaks work into 2 to 4 hour phases. Each phase: implementer, three validators (integration, design conformance, code architecture), commit, state update.
4. **Wrap.** When you say done, Claude asks whether to generate the replay guide or run more tweaks first. You decide.

### 3. Generate the replay guide

```
Generate a replay guide for this session. Base commit: abc123
```

The replay-guide generator reads `docs/SESSION_STATE.md` and `docs/[feature-slug]-progress.md` first, then the diff. Output goes to `replay-guides/{name}.md`.

### Checking in mid-run

A vibe session can run autonomously for hours. Invoke `/vibe-status` at any point to get a one-screen summary: current phase, completed phases, active stubs, recent commits, system invariants in effect. Read-only, never modifies state.

## What the replay guide contains

- **Overview.** What was built, key decisions, files affected.
- **System Invariants.** Verbatim from grilling. These hold across the entire feature, every phase below is bound by them.
- **Dependency graph.** Mermaid diagram showing build order.
- **Phased steps.** Grouped by layer (Data Models → Core Logic → API → Tests). Each step links to file:line, no big code blocks.
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

Replay-guide generation is *not* automated. At the end of a session Claude asks whether to generate it or run more tweaks first. You decide when the work is settled.

## License

MIT
