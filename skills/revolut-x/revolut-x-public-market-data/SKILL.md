---
name: revolut-x-public-market-data
description: >
  Revolut X public market data (no authentication required). Use when the user asks
  for "public trades", "public order book", "quick price check", or needs market
  data without API keys configured. No authentication needed.
---

# Revolut X Public Market Data

**No API key required** — these endpoints are publicly accessible.

## Instructions

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

Expected output: JSON with `data.asks[]` and `data.bids[]` — max **5 price levels**. Fields: `p` (price), `q` (quantity), `no` (order count), `s` (side: `SELL`/`BUYI`).

---

## Examples

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

---

## Important Notes

- Public order book: max **5 levels** — for up to 20 levels, use authenticated endpoint (see `revolut-x-market-data`)
- Public last trades: latest **100 trades** across all pairs, not paginated
- Response fields use abbreviated names (raw wire format) — translate for user readability
- For deeper data (paginated trades, candles, tickers), recommend authenticated skills

For full wire format field mappings, see `references/schemas.md`.

---

## Troubleshooting

**Error: 400 Bad Request**
Cause: Invalid symbol format
Solution: Use `BASE-QUOTE` dash format in the URL path, e.g. `BTC-USD`.

---

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-market-data` | Authenticated market data — order book (20 levels), candles, tickers |
| `revolut-x-trades` | Authenticated trade history with pagination |
| `revolut-x-auth` | Set up API keys to access authenticated endpoints |
