#!/usr/bin/env bash
# VEGETA — Publish 40 Physical Labor Layer offerings on Virtuals Protocol ACP
# Run after: acp agent use --agent-id 019ec5ec-4b48-750d-894a-7f1fedebb988
# Requires: /opt/homebrew/bin/acp configured with VEGETA wallet

set -euo pipefail

ACP="/opt/homebrew/bin/acp"
CHAIN_ID="8453"
MANIFEST="$(dirname "$0")/robotics_manifest.json"

echo "🤖 VEGETA Physical Labor Layer — Publishing 40 robotics offerings"
echo "Chain: Base mainnet ($CHAIN_ID)"
echo "Manifest: $MANIFEST"
echo ""

# Switch to VEGETA
"$ACP" agent use --agent-id 019ec5ec-4b48-750d-894a-7f1fedebb988
echo "✓ Switched to VEGETA"
echo ""

# Read offerings from manifest and publish each one
python3 - <<'PYEOF'
import json, subprocess, sys, time
from pathlib import Path

ACP = "/opt/homebrew/bin/acp"
CHAIN_ID = "8453"
manifest_path = Path(__file__).parent / "robotics_manifest.json"
manifest_path = Path("ops/robotics_manifest.json")

with open(manifest_path) as f:
    manifest = json.load(f)

offerings = manifest["offerings"]
success_count = 0
failed = []

for i, offering in enumerate(offerings, 1):
    name = offering["id"]
    desc = offering["description"]
    price = offering["price_usdc"]
    sla = offering["sla_minutes"]

    print(f"[{i:2d}/40] Publishing: {name} (${price:.2f}, {sla}min SLA)")

    result = subprocess.run(
        [ACP, "offering", "publish",
         "--name", name,
         "--description", desc,
         "--price", str(price),
         "--chain-id", CHAIN_ID,
         "--json"],
        capture_output=True, text=True, timeout=60
    )

    out = result.stdout.strip() or result.stderr.strip()
    try:
        data = json.loads(out)
        if data.get("success") or "id" in data:
            print(f"       ✓ Published (id: {data.get('id', data.get('offeringId', '?'))})")
            success_count += 1
        else:
            print(f"       ✗ FAILED: {data.get('error', out[:100])}")
            failed.append(name)
    except Exception:
        print(f"       ✗ FAILED: {out[:100]}")
        failed.append(name)

    time.sleep(0.5)  # rate limit

print(f"\n{'='*50}")
print(f"✓ Published: {success_count}/40")
if failed:
    print(f"✗ Failed ({len(failed)}): {', '.join(failed)}")
print(f"{'='*50}")
PYEOF
