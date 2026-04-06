---
name: revolut-x-trades
description: >
  Revolut X trade data. Use when the user asks to "view trade history", "get fills",
  "see recent trades", "check my trades", "execution details", "order fills", or
  needs fill information for completed orders on Revolut X.
---

# Revolut X Trades

## Instructions

### Get all public trades for a symbol

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

---

## Examples

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

---

## Important Notes

- **Max date range: 30 days** — requests spanning more than 30 days are rejected
- Trade response `symbol` uses **slash format** (`BTC/USD`); request path uses **dash format** (`BTC-USD`)
- Default range is 7 days if only one of `start_date`/`end_date` is specified
- `maker: true` = your order was resting on the book; `false` = your order was aggressive

For full response schemas and raw wire format, see `references/schemas.md`.

---

## Troubleshooting

**Error: 400 Bad Request**
Cause: Date range exceeds 30 days or invalid symbol
Solution: Narrow the date range. Check symbol uses dash format.

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup.

---

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Order lifecycle — place orders that generate trades |
| `revolut-x-public-market-data` | Public last trades (no auth, not paginated) |
| `revolut-x-balance` | Check portfolio impact of trades |
