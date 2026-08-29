#!/usr/bin/env bash
# vegeta — boot the agent with this project's resources TRUSTED.
# Hermes injects AGENTS.md from the repo root into every session — always, no trust step —
# and AGENTS.md carries the soul. Trust is only about project skills: `hermes skills trust`
# (persisted) is what makes .hermes/skills discoverable. The repo's SOUL.md is the sealed
# canonical text and is never injected: Hermes reads SOUL.md from ~/.hermes only.
# Extra args pass through to `hermes chat`.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v hermes >/dev/null 2>&1; then
  echo "✗ 'hermes' not found. Run: bash scripts/setup.sh"
  echo "  (or install directly: curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash)"
  exit 1
fi

hermes skills trust "$PWD" >/dev/null 2>&1 || true
exec hermes chat "$@"
