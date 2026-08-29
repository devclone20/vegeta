# VEGETA — the iNFT monorepo

**VEGETA is an iNFT**: an autonomous AI agent fused with an NFT — whoever holds the token holds
the agent. This repository is its **body**. Underneath the name **VEGETA** runs a complete
**Hermes Agent** (the substrate — Nous Research, MIT); the **VEGETA neural soul** is the identity.

> Forged from the global genesis template **[inft-i01](https://github.com/devclone20/inft-i01)**.
> The template is the mold; **VEGETA is a real, named instance** of the CLONE FRAME line.

## Three names, one identity
**VEGETA** (its name) · **iNFT** (its species) · **Hermes** (its substrate).

## Run it
```bash
bash scripts/setup.sh              # install the Hermes substrate (official installer, no sudo)
hermes model                       # connect YOUR model key (BYOK)
bash scripts/boot.sh               # soul rides in AGENTS.md; this trusts the project so its skills load, then `hermes chat`
bash scripts/install-command.sh    # then type `vegeta` in the CLONE FRAME iT terminal
```

## Economy — already wired

VEGETA already carries EconomyOS (Virtuals ACP (client), Hyperliquid), driven by the `acp` CLI. It is **not** rebuilt here — see `soul/neural_soul.md` and the app runtime.

## Map
See [`AGENTS.md`](AGENTS.md). Concept: [`docs/INFT_CONCEPT.md`](docs/INFT_CONCEPT.md) ·
[`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md).

## Security & privacy
Public repo: no secrets/keys/PII committed. Your model key is typed into your own terminal
(`hermes model`), never handed to any assistant. The owner profile goes into the gitignored
`AGENTS.override.md` — which Hermes loads in place of `AGENTS.md`, so it reaches the agent
but is never committed (`scripts/personalize.sh --apply-owner`).
