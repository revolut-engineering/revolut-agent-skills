# Revolut Agent Skills

A collection of [Skills](https://docs.anthropic.com/en/docs/agents-and-tools/skills) for working with Revolut APIs.

## Skills

<details>
<summary><b>Revolut X</b> — Crypto Exchange REST API</summary>

| Skill | Description |
|---|---|
| `revolut-x-auth` | API key setup, Ed25519 signing, environment configuration |
| `revolut-x-configuration` | Available currencies and trading pair constraints |
| `revolut-x-balance` | Account balances (available, reserved, staked) |
| `revolut-x-orders` | Place, cancel, and query orders (market, limit, conditional, TPSL) |
| `revolut-x-trades` | Trade history, personal fills, order execution details |
| `revolut-x-market-data` | Order book depth, OHLCV candles, ticker prices |
| `revolut-x-public-market-data` | Public trades and order book (no auth required) |

Each skill includes a `scripts/` folder with request helpers and a `references/` folder with detailed API schemas.

**Getting started:** Set `REVX_API_KEY` and `REVX_PRIVATE_KEY` env vars — see the `revolut-x-auth` skill for setup instructions.

**API docs:** https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api

</details>
