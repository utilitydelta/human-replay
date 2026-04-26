#!/usr/bin/env bash
# Block destructive remote operations inside a sandbox clone.
#
# A sandbox is identified by a `.sandbox` marker file at the working
# tree root. The marker is created during sandbox setup (see README).
#
# Exits 2 to block the tool call when a publishing command is detected.
# Exits 0 (allow) for everything else, including outside sandboxes.

set -euo pipefail

git_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[[ -f "$git_root/.sandbox" ]] || exit 0

payload=$(cat)
cmd=$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')
[[ -n "$cmd" ]] || exit 0

if printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+push|git[[:space:]]+remote[[:space:]]+(add|set-url)[[:space:]]+origin'; then
  cat <<'EOF' >&2
[human-replay] Blocked: this is a sandbox clone (.sandbox marker present).
Sandboxes are throwaway. Do not publish them. Replay the work by hand
in your real working copy, then push from there.
EOF
  exit 2
fi

exit 0
