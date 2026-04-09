---
name: revolut-x-market-data
description: >
  Revolut X authenticated market data — ticker prices (bid/ask/mid/last), OHLCV candles at
  multiple intervals, and order book depth up to 20 levels. Use when the user asks for the
  price of a crypto asset, candlestick data, order book depth, or bid/ask spread on Revolut X.
allowed-tools: Bash
compatibility: Requires Python 3 and the bundled scripts/revx_sign.py helper
metadata:
  version: "0.1.0"
---

# Revolut X Market Data

## Capabilities

- Fetch ticker prices (bid, ask, mid, last) for all or specific pairs
- Retrieve OHLCV candles at multiple intervals (1m to 4w)
- View order book depth (up to 20 price levels)

## Authentication & setup

All endpoints require authentication. See [revolut-x-auth](../revolut-x-auth/SKILL.md) for setup.

## API versioning

All endpoints use path-based versioning: `/api/1.0/`. The version is included in every request path.

## Common workflows

### Get ticker prices

```bash
python scripts/revx_sign.py GET /api/1.0/tickers
```

For specific pairs:

```bash
python scripts/revx_sign.py GET /api/1.0/tickers --query '?symbols=BTC-USD,ETH-USD'
```

Expected output: JSON with `data[]` array — each with `symbol`, `bid`, `ask`, `mid`, `last_price`.

### Get order book

```bash
python scripts/revx_sign.py GET /api/1.0/order-book/BTC-USD
```

Expected output: `data.asks[]` and `data.bids[]` with up to **20 price levels**. Each level: `{ price, quantity, orderCount }`.

### Get OHLCV candles

```bash
python scripts/revx_sign.py GET /api/1.0/candles/BTC-USD --query '?interval=60'
```

Query parameters:
- `interval` — candle width in minutes: `1`, `5`, `15`, `30`, `60`, `240`, `1440` (1d), `10080` (1w), `40320` (4w)
- `since` — start time in Unix ms (default: last 100 candles)
- `until` — end time in Unix ms (default: now)
- Max 1000 candles per request

Expected output: JSON array of candles — each with `start`, `open`, `high`, `low`, `close`, `volume`.

### Example 1: Check current price
User says: "What's the price of BTC?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/tickers --query '?symbols=BTC-USD'`
2. Extract `bid`, `ask`, `mid`, `last_price` from first entry

Result: "BTC-USD: Bid $95,000 / Ask $95,100 / Last $95,050"

### Example 2: Get 4-hour candles for last 30 days
User says: "Show me BTC-USD 4h candles for the last month"

Actions:
1. Calculate `since` = now - 30 days (in ms): `python -c "import time; print(int((time.time() - 30*86400) * 1000))"`
2. Run `python scripts/revx_sign.py GET /api/1.0/candles/BTC-USD --query '?interval=240&since={since}'`
3. Parse the candle array (~180 candles)

Result: Table or summary of 4h OHLCV data.

### Example 3: View full order book depth
User says: "Show me the ETH-USD order book"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/order-book/ETH-USD`
2. Display asks (sell orders) and bids (buy orders) with price, quantity, order count

Result: 20-level order book with bid/ask spread.

### Example 4: Compare prices across pairs
User says: "What are all the current prices?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/tickers`
2. Present all pairs in a comparison table: symbol, bid, ask, last

Result: Price overview for all trading pairs.

## Error handling

**Error: 400 Bad Request**
Cause: Invalid symbol or interval value
Solution: Check symbol uses dash format in URL. Use valid interval: 1, 5, 15, 30, 60, 240, 1440, etc.

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup.

## Important notes

- Candle `interval` is in **minutes** as an integer (60 = 1 hour, 1440 = 1 day)
- Ticker `symbol` in responses uses slash format (`BTC/USD`), request params use dash (`BTC-USD`)
- For unauthenticated order book (5 levels only), see `revolut-x-public-market-data`

## References

- [schemas.md](references/schemas.md) — Full response field definitions
- [Revolut X REST API docs](https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api)
- [Get ticker](https://developer.revolut.com/docs/x-api/get-ticker) · [Get order book](https://developer.revolut.com/docs/x-api/get-order-book) · [Get candles](https://developer.revolut.com/docs/x-api/get-candles)

## Related skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Act on market data — place orders based on prices |
| `revolut-x-balance` | Combine with tickers to compute portfolio fiat value |
| `revolut-x-configuration` | Check valid pairs and their constraints |
| `revolut-x-public-market-data` | Unauthenticated order book (5 levels) and last trades |
