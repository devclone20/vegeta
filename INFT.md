# VEGETA — the iNFT monorepo

**VEGETA is an iNFT**: an autonomous AI agent fused with an NFT — whoever holds the token holds
the agent. This repository is its **body**. Underneath the name **VEGETA** runs a complete
**Pi coding agent** (the substrate); the **VEGETA neural soul** is the identity.

> Forged from the global genesis template **[inft-i01](https://github.com/devclone20/inft-i01)**.
> The template is the mold; **VEGETA is a real, named instance** of the CLONE FRAME line.

## Three names, one identity
**VEGETA** (its name) · **iNFT** (its species) · **Pi** (its substrate).

## Run it
```bash
bash scripts/setup.sh              # install the Pi substrate (pinned, no sudo)
pi                                 # then /login to connect YOUR model key (BYOK)
bash scripts/boot.sh               # boot VEGETA with its soul + skills (pi -a)
bash scripts/install-command.sh    # then type `vegeta` in the CLONE FRAME iT terminal
```

## Economy — already wired

VEGETA already carries EconomyOS (Virtuals ACP (client), Hyperliquid), driven by the `acp` CLI. It is **not** rebuilt here — see `soul/neural_soul.md` and the app runtime.

## Map
See [`AGENTS.md`](AGENTS.md). Concept: [`docs/INFT_CONCEPT.md`](docs/INFT_CONCEPT.md) ·
[`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md).

## Security & privacy
Public repo: no secrets/keys/PII committed. Your model key is typed into your own terminal
(`pi` → `/login`), never handed to any assistant. The owner profile is folded into
`.pi/APPEND_SYSTEM.md` **locally** and untracked (`scripts/personalize.sh --apply-owner`).
