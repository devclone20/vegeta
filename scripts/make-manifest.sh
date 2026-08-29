#!/usr/bin/env bash
# inft-i01 — regenerate metadata/manifest.json with SHA-256 of every TRACKED file.
# Uses `git ls-files` (authoritative: excludes gitignored/PII/generated files) when in
# a git repo; falls back to a find sweep otherwise. Run after changing any tracked file.
set -euo pipefail
cd "$(dirname "$0")/.."

SELF="metadata/manifest.json"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # Tracked + not-yet-committed-but-added files, excluding the manifest itself.
  FILES=$( { git ls-files; git diff --cached --name-only --diff-filter=A; } | sort -u | grep -vxF "$SELF" )
else
  FILES=$(find . -type f -not -path './.git/*' -not -path './node_modules/*' -not -name manifest.json | sed 's|^\./||' | sort)
fi

# A tracked symlink (e.g. .hermes/skills -> ../skills) is content in git too: what git
# stores is the LINK TARGET, not the tree behind it. Hash that string, so repointing the
# link at another directory shows up as a manifest mismatch like any other edit.
hash_of() {
  if [ -L "$1" ]; then
    printf 'symlink:%s' "$(readlink "$1")" | shasum -a 256 | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
} > "$SELF"

# Entries are the 4-space-indented lines inside "files"; the header keys sit at 2 spaces.
echo "✓ metadata/manifest.json regenerated ($(grep -c '^    "' "$SELF") file entries)"
echo "  soul/neural_soul.md → $(hash_of soul/neural_soul.md)"
