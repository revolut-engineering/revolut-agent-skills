---
name: revolut-x-market-data
description: >
  Revolut X authenticated market data. Use when the user asks for "order book",
  "price of BTC", "candles", "OHLCV", "ticker", "bid ask spread", "candlestick
  chart", or needs detailed market data for analysis or trading decisions.
---

# Revolut X Market Data

## Instructions

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

---

## Examples

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

---

## Important Notes

- Candle `interval` is in **minutes** as an integer (60 = 1 hour, 1440 = 1 day)
- Ticker `symbol` in responses uses slash format (`BTC/USD`), request params use dash (`BTC-USD`)
- For unauthenticated order book (5 levels only), see `revolut-x-public-market-data`

For full response field definitions, see `references/schemas.md`.

---

## Troubleshooting

**Error: 400 Bad Request**
Cause: Invalid symbol or interval value
Solution: Check symbol uses dash format in URL. Use valid interval: 1, 5, 15, 30, 60, 240, 1440, etc.

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup.

---

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Act on market data — place orders based on prices |
| `revolut-x-balance` | Combine with tickers to compute portfolio fiat value |
| `revolut-x-configuration` | Check valid pairs and their constraints |
| `revolut-x-public-market-data` | Unauthenticated order book (5 levels) and last trades |
