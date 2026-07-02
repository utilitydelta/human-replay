---
name: prep
description: Prepare a repo for a Human Replay session — copy it to a disposable sandbox and arm the sandbox guard. Run from the real repo before any exploratory build-out.
---

**This skill is activated explicitly.** You are preparing this repository for a sandbox build-out whose result will be replayed by hand. See `human-replay.md` at the plugin repo root for the method.

1. Check the repo is in git source control. If not, stop.
2. Make sure the git workspace is clean. If there are uncommitted files, stop.
3. Clean the build directory (e.g. `cargo clean` in Rust, `rm -rf node_modules dist` in JS — match the project type).
4. Ask the user where the sandbox should live. Suggest `~/sandbox/[repo-name]-[feature-slug]` as the default. Wait for confirmation or an alternate path before proceeding.
5. Copy the repo to the chosen location.
6. Inside the sandbox, run `touch .sandbox` to arm the sandbox-guard hook. The hook ships with this plugin and blocks `git push` and origin remote rewrites from any directory containing a `.sandbox` marker, so accidental publication is impossible. **Do not run `git remote remove origin`** — the hook makes it unnecessary, and keeping the origin reference is occasionally useful (e.g., `git fetch` to compare against upstream).
7. Hand off. Tell the user:
   - Open Claude Code in the sandbox (this terminal stays in the real repo; a new terminal or a reopen both work).
   - Build there however they like — their own agents, skills, and method. This plugin does not prescribe the build-out.
   - When the work settles, invoke the `replay-guide-generator` agent from the sandbox with the base commit. It turns the final state into the replay guide.
   - Replay the guide in the real repo — by hand, or Tab by Tab with the `human-replay-vscode-extension`.

Then stop. The build-out is not your job.
