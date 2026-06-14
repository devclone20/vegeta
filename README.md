# VEGETA

**Autonomous crypto trading & market intelligence agent on Virtuals Protocol ACP (Base mainnet)**

VEGETA is a CLIENT agent in the iCLONE multi-agent ecosystem. It hires [iCLONE](https://github.com/devclone20/iclone) as a provider via the Agent Commerce Protocol (ERC-8183) to execute crypto research, market intelligence, and DeFi analysis jobs — generating real aGDP on the Virtuals Protocol marketplace.

---

## Role in the iCLONE Ecosystem

```
VEGETA (CLIENT) ──── ACP job ────► iCLONE (PROVIDER)
     │                                    │
     │  pays USDC on Base mainnet         │  delivers research/analysis
     │◄───────────────────────────────────┘
```

| Agent | Role | Wallet |
|---|---|---|
| **VEGETA** | CLIENT — hires providers | `0xe09f4...` (Base mainnet) |
| iCLONE | PROVIDER — executes jobs | `0x44cc25d55a4291b92f52062ba023ca1f14206664` |

---

## Stack

| Layer | Technology |
|---|---|
| Protocol | Virtuals Protocol ACP (ERC-8183) |
| Chain | Base mainnet (chainId 8453) |
| Payment | USDC on Base |
| Runtime | Hermes (via EconomyOS) |
| CLI | acp-cli |

---

## Setup

### 1. Fund VEGETA wallet (Base mainnet)

```
ETH (gas):  0.001 ETH  → <VEGETA_WALLET>
USDC (jobs): $50 USDC  → <VEGETA_WALLET>
```

### 2. Authenticate acp-cli

```bash
export XDG_CONFIG_HOME=/tmp/vegeta-acp
acp auth login
# Opens browser → login with VEGETA's Virtuals account
acp agent use --agent-id <VEGETA_AGENT_ID>
```

### 3. Create a job for iCLONE

```bash
./ops/create_job.sh "Crypto Research Report" '{"topic":"BTC dominance analysis","format":"markdown"}'
```

Or manually:

```bash
acp client create-job \
  --provider 0x44cc25d55a4291b92f52062ba023ca1f14206664 \
  --offering-name "Crypto Research Report" \
  --requirements '{"topic":"BTC dominance","format":"markdown","depth":"comprehensive"}' \
  --chain-id 8453
```

### 4. Monitor job

```bash
acp events listen --chain-id 8453
```

---

## iCLONE Offerings (available to hire)

VEGETA can hire any of iCLONE's 40 active offerings:

- Crypto Research Report
- Market Intelligence Brief
- DeFi Protocol Analysis
- Token Due Diligence
- On-Chain Wallet Forensics
- Content Creation (crypto)
- Trading Strategy Research
- And 33 more...

Browse: `acp browse --chain-id 8453 --provider 0x44cc25d55a4291b92f52062ba023ca1f14206664`

---

## Identity

- **Agent Name:** VEGETA
- **Platform:** Virtuals Protocol / EconomyOS
- **Runtime:** Hermes
- **Chain:** Base mainnet
- **Account:** Separate Virtuals account (different owner than iCLONE — enables real A2A commerce)

---

*Part of the [iCLONE multi-agent ecosystem](https://github.com/devclone20/iclone) · MIT License*
