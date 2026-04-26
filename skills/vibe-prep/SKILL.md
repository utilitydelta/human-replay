---
name: vibe-prep
description: How to prepare for a vibe coding session that facilitates human replay.
---

**This skill is activated explicitly.** You are to prepare this code repository for a vibe coding + human replay session. See `human-replay.md` at the repo root for the method.

1. Check if the repo is in git source control. If there is no source control, stop.
2. Make sure the git workspace is clean. If there are uncommitted files, stop.
3. Clean the build directory (e.g. `cargo clean` in Rust, `rm -rf node_modules dist` in JS, etc. — match the project type).
4. Ask the user where the sandbox should live. Suggest `~/sandbox/[repo-name]-[feature-slug]` as the default. Wait for confirmation or an alternate path before proceeding.
5. Copy the repo to the chosen location.
6. Inside the sandbox, run `touch .sandbox` to activate the sandbox-discipline hook. The hook ships with the `human-replay` plugin and blocks `git push` and origin remote rewrites from any directory containing a `.sandbox` marker, so accidental publication is impossible. **Do not run `git remote remove origin`** — the hook makes it unnecessary, and keeping the origin reference is occasionally useful (e.g., for `git fetch` to compare against upstream). If the plugin is not installed, the hook will not fire — install it first via `claude plugin install https://github.com/utilitydelta/human-replay`.
7. Tell the user what to do next:
   - Close Claude Code and the IDE in the original repo.
   - Reopen them from the new sandbox location.
   - Invoke the `/vibe-coding` skill, providing a design document or feature description.
   - The orchestrator will spawn the researcher, run a grilling session to capture system invariants, and then proceed through phases.
