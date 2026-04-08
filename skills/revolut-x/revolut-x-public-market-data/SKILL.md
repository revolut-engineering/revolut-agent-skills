---
name: revolut-x-public-market-data
version: 0.1.0
description: >
  Revolut X public market data (no auth required) — public order book (5 levels)
  and latest trades across all pairs.
allowed-tools: [Bash]
sources:
  - https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api
  - https://developer.revolut.com/docs/x-api/get-last-trades
  - https://developer.revolut.com/docs/x-api/get-public-order-book
---

# Revolut X Public Market Data

## Capabilities

- Fetch latest 100 trades across all pairs (no auth required)
- Fetch public order book with up to 5 price levels (no auth required)
- Quick price checks without API key configuration

## Authentication & setup

No authentication required. These endpoints are publicly accessible.

## API versioning

All endpoints use path-based versioning: `/api/1.0/`. The version is included in every request path.

## Common workflows

### Get latest public trades

```bash
python scripts/revx_request.py GET /api/1.0/public/last-trades
```

Expected output: JSON with `data[]` array of the latest 100 trades across all pairs. Fields use abbreviated names (raw wire format) — see `references/schemas.md`.

Key fields: `tdt` (timestamp), `aid` (asset), `p` (price), `q` (quantity), `tid` (trade ID).

### Get public order book

```bash
python scripts/revx_request.py GET /api/1.0/public/order-book/BTC-USD
```

Expected output: JSON with `data.asks[]` and `data.bids[]` — max **5 price levels**. Fields: `p` (price), `q` (quantity), `no` (order count), `s` (side: `SELL`/`BUYI`). Note: `BUYI` is the actual API wire format abbreviation for buy-side, not a typo.

### Example 1: Quick price check without API key
User says: "What's the current BTC price?"

Actions:
1. Run `python scripts/revx_request.py GET /api/1.0/public/order-book/BTC-USD`
2. Read top bid (`data.bids[0].p`) and ask (`data.asks[0].p`)
3. Present: "BTC-USD: Bid $95,000 / Ask $95,100"

Result: Current bid/ask spread for BTC-USD.

### Example 2: Recent market activity
User says: "Show me recent trades on Revolut X"

Actions:
1. Run `python scripts/revx_request.py GET /api/1.0/public/last-trades`
2. Parse the `data[]` array
3. Present recent trades with asset, price, quantity, timestamp

Result: Table of last 100 trades across all pairs.

## Error handling

**Error: 400 Bad Request**
Cause: Invalid symbol format
Solution: Use `BASE-QUOTE` dash format in the URL path, e.g. `BTC-USD`.

## Important notes

- Public order book: max **5 levels** — for up to 20 levels, use authenticated endpoint (see `revolut-x-market-data`)
- Public last trades: latest **100 trades** across all pairs, not paginated
- Response fields use abbreviated names (raw wire format) — translate for user readability
- For deeper data (paginated trades, candles, tickers), recommend authenticated skills

## References

- [schemas.md](references/schemas.md) — Full wire format field mappings

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-market-data` | Authenticated market data — order book (20 levels), candles, tickers |
| `revolut-x-trades` | Authenticated trade history with pagination |
| `revolut-x-auth` | Set up API keys to access authenticated endpoints |
