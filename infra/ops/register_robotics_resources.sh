#!/usr/bin/env bash
# VEGETA — Register 40 Physical Labor Layer resources on Virtuals Protocol
# Resources are REST API endpoints VEGETA can call as tools
# Run after: acp agent use --agent-id 019ec5ec-4b48-750d-894a-7f1fedebb988

set -euo pipefail

ACP="/opt/homebrew/bin/acp"
CHAIN_ID="8453"
MANIFEST="$(dirname "$0")/robotics_manifest.json"

echo "🔗 VEGETA Physical Labor Layer — Registering 40 resources"
echo "Chain: Base mainnet ($CHAIN_ID)"
echo ""

# Switch to VEGETA
"$ACP" agent use --agent-id 019ec5ec-4b48-750d-894a-7f1fedebb988
echo "✓ Switched to VEGETA"
echo ""

python3 - <<'PYEOF'
import json, subprocess, sys, time
from pathlib import Path

ACP = "/opt/homebrew/bin/acp"
CHAIN_ID = "8453"

with open("ops/robotics_manifest.json") as f:
    manifest = json.load(f)

resources = manifest["resources"]
success_count = 0
failed = []

for i, res in enumerate(resources, 1):
    name = res["name"]
    url = res["url"]
    desc = res["description"]

    print(f"[{i:2d}/40] Registering: {name}")
    print(f"           URL: {url[:70]}")

    result = subprocess.run(
        [ACP, "resource", "add",
         "--name", name,
         "--url", url,
         "--description", desc,
         "--chain-id", CHAIN_ID,
         "--json"],
        capture_output=True, text=True, timeout=60
    )

    out = result.stdout.strip() or result.stderr.strip()
    try:
        data = json.loads(out)
        if data.get("success") or "id" in data or "resourceId" in data:
            print(f"           ✓ Registered")
            success_count += 1
        else:
            print(f"           ✗ FAILED: {data.get('error', out[:100])}")
            failed.append(name)
    except Exception:
        if result.returncode == 0:
            print(f"           ✓ Registered (non-JSON response)")
            success_count += 1
        else:
            print(f"           ✗ FAILED: {out[:100]}")
            failed.append(name)

    time.sleep(0.5)

print(f"\n{'='*50}")
print(f"✓ Registered: {success_count}/40")
if failed:
    print(f"✗ Failed ({len(failed)}): {', '.join(failed)}")
print(f"{'='*50}")
PYEOF
