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

hash_of() { shasum -a 256 "$1" | awk '{print $1}'; }
# A tracked symlink has no file bytes of its own — git stores its TARGET PATH, and that is
# what we hash, so .hermes/skills (the project-skills link) is covered like everything else.
# A verifier reproduces it with: printf '%s' "$(readlink <path>)" | shasum -a 256
hash_link() { printf '%s' "$(readlink "$1")" | shasum -a 256 | awk '{print $1}'; }

{
  echo '{'
  echo '  "manifest_version": 1,'
  echo "  \"generated\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo '  "algorithm": "sha256",'
  echo '  "repo": "https://github.com/devclone20/inft-i01",'
  echo '  "note": "Authoritative hashes for a token live on-chain / Irys, not here (see docs/BOOTSTRAP.md). This file is a convenience mirror of the tracked tree. Symlinks are hashed by their target path (what git stores), not by the bytes they point at.",'
  echo '  "files": {'
  first=true
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    # -L before -f: a symlink to a regular file satisfies both, and the link is what git tracks.
    if   [ -L "$f" ]; then h="$(hash_link "$f")"
    elif [ -f "$f" ]; then h="$(hash_of "$f")"
    else continue
    fi
    $first || echo ','
    first=false
    printf '    "%s": "%s"' "$f" "$h"
  done <<< "$FILES"
  echo ''
  echo '  }'
  echo '}'
} > "$SELF"

# Entries are the 4-space-indented lines inside "files"; the header keys sit at 2 spaces.
echo "✓ metadata/manifest.json regenerated ($(grep -c '^    "' "$SELF") file entries)"
echo "  soul/neural_soul.md → $(hash_of soul/neural_soul.md)"
