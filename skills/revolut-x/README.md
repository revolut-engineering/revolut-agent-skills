# Revolut X

Agent skills for the [Revolut X Crypto Exchange REST API](https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api).

## Skills

<!-- DEV: version and author fields will be added after the skills audit -->

| Skill | Description | Version | Author |
| ----- | ----------- | ------- | ------ |
| [revolut-x-auth](revolut-x-auth/) | API key setup, Ed25519 signing, environment configuration | — | — |
| [revolut-x-configuration](revolut-x-configuration/) | Available currencies and trading pair constraints | — | — |
| [revolut-x-balance](revolut-x-balance/) | Account balances (available, reserved, staked) | — | — |
| [revolut-x-orders](revolut-x-orders/) | Place, cancel, and query orders (market, limit, conditional, TPSL) | — | — |
| [revolut-x-trades](revolut-x-trades/) | Trade history, personal fills, order execution details | — | — |
| [revolut-x-market-data](revolut-x-market-data/) | Order book depth, OHLCV candles, ticker prices | — | — |
| [revolut-x-public-market-data](revolut-x-public-market-data/) | Public trades and order book (no auth required) | — | — |

Each skill includes a `scripts/` folder with request helpers and a `references/` folder with detailed API schemas.

## Getting started

Set the following environment variables before using any authenticated skill:

```bash
export REVX_API_KEY=your_api_key
export REVX_PRIVATE_KEY=your_ed25519_private_key
```

See the [`revolut-x-auth`](revolut-x-auth/) skill for full setup instructions, including how to generate an Ed25519 keypair and register your public key with the Revolut X API.

The [`revolut-x-public-market-data`](revolut-x-public-market-data/) skill requires no authentication.
