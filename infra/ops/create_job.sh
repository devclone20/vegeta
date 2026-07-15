#!/usr/bin/env bash
# VEGETA → iCLONE job creator
# Usage: ./ops/create_job.sh "<offering-name>" "<requirements-json>"
# Example: ./ops/create_job.sh "Crypto Research Report" '{"topic":"BTC dominance analysis","format":"markdown"}'

set -euo pipefail

PROVIDER="0x44cc25d55a4291b92f52062ba023ca1f14206664"  # iCLONE wallet
CHAIN_ID="8453"  # Base mainnet
OFFERING="${1:-Crypto Research Report}"
REQUIREMENTS="${2:-{\"topic\":\"crypto market analysis\",\"format\":\"markdown\"}}"

echo "Creating job: $OFFERING"
echo "Provider (iCLONE): $PROVIDER"
echo "Requirements: $REQUIREMENTS"
echo ""

acp client create-job \
  --provider "$PROVIDER" \
  --offering-name "$OFFERING" \
  --requirements "$REQUIREMENTS" \
  --chain-id "$CHAIN_ID"
