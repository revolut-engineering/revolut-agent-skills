---
name: revolut-x-trades
description: >
  Revolut X trade data — market trade history, private fills, and execution details for completed
  orders, with pagination and date filtering. Use when the user asks to view trade history,
  check fills, see recent trades, or analyse order execution on Revolut X.
allowed-tools: Bash
compatibility: Requires Python 3 and the bundled scripts/revx_sign.py helper
metadata:
  version: "0.1.0"
---

# Revolut X Trades

## Capabilities

- Fetch all market trades for a symbol (with date range filtering)
- Fetch private trades (fills) for your account
- Get fills for a specific order
- Paginate through large trade result sets

## Authentication & setup

All endpoints require authentication. See [revolut-x-auth](../revolut-x-auth/SKILL.md) for setup.

## API versioning

All endpoints use path-based versioning: `/api/1.0/`. The version is included in every request path.

## Common workflows

### Get all market trades for a symbol

```bash
python scripts/revx_sign.py GET /api/1.0/trades/all/BTC-USD
```

With date range (max 30 days):

```bash
python scripts/revx_sign.py GET /api/1.0/trades/all/BTC-USD --query '?start_date=1712000000000&end_date=1712600000000'
```

Expected output: Paginated JSON with `data[]` array of `PublicTrade` objects — `id`, `symbol`, `price`, `quantity`, `timestamp`.

### Get my private trades (fills)

```bash
python scripts/revx_sign.py GET /api/1.0/trades/private/BTC-USD
```

Expected output: `Trade[]` — all PublicTrade fields plus `side`, `orderId`, `maker`.

### Get fills for a specific order

```bash
python scripts/revx_sign.py GET /api/1.0/orders/fills/ORDER_UUID
```

Expected output: `Trade[]` — all fills associated with that order.

### Pagination

If `metadata.next_cursor` is present in the response, pass it to get the next page:

```bash
python scripts/revx_sign.py GET /api/1.0/trades/private/BTC-USD --query '?cursor=CURSOR_VALUE&limit=100'
```

### Example 1: Check my recent BTC fills
User says: "Show me my recent BTC-USD trades"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/trades/private/BTC-USD`
2. Parse the `data[]` array
3. Present: side, price, quantity, maker/taker, timestamp

Result: Table of recent BTC-USD fills.

### Example 2: Analyze trading activity over last 7 days
User says: "How much BTC did I trade this week?"

Actions:
1. Calculate `start_date` = now - 7 days (in ms)
2. Run `python scripts/revx_sign.py GET /api/1.0/trades/private/BTC-USD --query '?start_date={start_date}'`
3. Paginate if `metadata.next_cursor` is present
4. Sum quantities, compute average fill price

Result: Total volume, average price, number of trades.

### Example 3: Get fills for a specific order
User says: "What fills did order abc-123 get?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/orders/fills/abc-123`
2. Display all fills: price, quantity, maker/taker, timestamp

Result: All execution details for that order.

## Error handling

**Error: 400 Bad Request**
Cause: Date range exceeds 30 days or invalid symbol
Solution: Narrow the date range. Check symbol uses dash format.

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup.

## Important notes

- **Max date range: 30 days** — requests spanning more than 30 days are rejected
- Trade response `symbol` uses **slash format** (`BTC/USD`); request path uses **dash format** (`BTC-USD`)
- Default range is 7 days if only one of `start_date`/`end_date` is specified
- `maker: true` = your order was resting on the book; `false` = your order was aggressive

## References

- [schemas.md](references/schemas.md) — Full response schemas and raw wire format
- [Revolut X REST API docs](https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api)
- [Get all trades](https://developer.revolut.com/docs/x-api/get-all-trades) · [Get private trades](https://developer.revolut.com/docs/x-api/get-private-trades) · [Get order fills](https://developer.revolut.com/docs/x-api/get-order-fills)

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Order lifecycle — place orders that generate trades |
| `revolut-x-public-market-data` | Public last trades (no auth, not paginated) |
| `revolut-x-balance` | Check portfolio impact of trades |
