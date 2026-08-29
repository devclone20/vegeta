#!/usr/bin/env bash
# vegeta — boot the agent with this project's resources TRUSTED.
# Hermes auto-injects AGENTS.md and SOUL.md, and discovers project skills under
# .hermes/skills once the project root is trusted. `hermes skills trust` grants
# that trust (persisted). Extra args pass through to `hermes chat`.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v hermes >/dev/null 2>&1; then
  echo "✗ 'hermes' not found. Run: bash scripts/setup.sh"
  echo "  (or install directly: curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash)"
  exit 1
fi

hermes skills trust "$PWD" >/dev/null 2>&1 || true
exec hermes chat "$@"
