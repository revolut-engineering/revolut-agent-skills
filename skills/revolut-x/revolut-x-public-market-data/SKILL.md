---
name: revolut-x-public-market-data
description: >
  Revolut X public market data — tickers, OHLCV candles, paginated trade history, public order
  book, and currency/pair configuration. No authentication required. Use when the user wants a
  quick price check, recent trade data, or pair details and has not configured API keys, or asks
  about public market data.
allowed-tools: Bash
compatibility: Requires Python 3 and the bundled scripts/revx_request.py helper
metadata:
  version: "0.2.0"
---

# Revolut X Public Market Data

## Capabilities

- Fetch tickers for all pairs (bid/ask/mid, 24h stats, no auth required)
- Fetch OHLCV candles for a pair (no auth required)
- Fetch paginated trade history across all pairs or one pair (no auth required)
- Fetch public order book with configurable depth (no auth required)
- Fetch supported currencies and currency pairs configuration (no auth required)
- Quick price checks without API key configuration

## Authentication & setup

No authentication required. These endpoints are publicly accessible.

## API versioning

Endpoints use path-based versioning: `/api/1.0/` or `/api/2.0/`. The version is included in every request path.

**Deprecated endpoints:** the official spec deprecates `GET /api/1.0/public/last-trades` and `GET /api/1.0/public/order-book/{symbol}`. Prefer the replacements below (`/api/1.0/public/trades/all` and `/api/2.0/public/order-book/{symbol}`); the deprecated endpoints still respond today but may be removed.

## Common workflows

### Get tickers

```bash
python scripts/revx_request.py GET /api/1.0/public/tickers
```

Expected output: JSON with `data[]` of tickers for all pairs. Optional `?symbols=BTC-USD,ETH-USD` filters pairs; `?region=UK|EEA` filters region (both returned when omitted). Fields: `symbol` (note slash format, `BTC/USD`), `bid`, `ask`, `mid`, `index_price`, `last_price`, `low_24h`, `high_24h`, `price_change_24h`, `volume_24h`, `quote_volume_24h`, `region`. `metadata.timestamp` is Unix epoch milliseconds.

### Get OHLCV candles

```bash
python scripts/revx_request.py GET "/api/1.0/public/candles/BTC-USD?interval=60"
```

Expected output: JSON with `data[]` of candles, each `start` (Unix epoch milliseconds), `open`, `high`, `low`, `close`, `volume`. `interval` is in minutes (1, 5, 15, 30, 60, 240, 1440, 2880, 5760, 10080, 20160, 40320; default 5). Optional `since`/`until` bound the range in epoch milliseconds; returns up to 1000 candles. `metadata` carries `timestamp` (epoch ms) and `region` (defaults to EEA, pass `?region=UK` for UK).

### Get trade history (paginated)

```bash
python scripts/revx_request.py GET "/api/1.0/public/trades/all?symbol=BTC-USD&limit=100"
```

Expected output: JSON with `data[]` of trades: `id` (UUID), `symbol` (slash format), `price`, `quantity`, `side` (`buy`/`sell`), `timestamp` (Unix epoch milliseconds), `region`. Paginate with `metadata.next_cursor`: pass it back as `?cursor=...` until it comes back empty. Optional `start_date`/`end_date` bound the range in epoch milliseconds; `limit` defaults to 100; `region` omitted returns both regions.

### Get public order book (v2, configurable depth)

```bash
python scripts/revx_request.py GET "/api/2.0/public/order-book/BTC-USD?limit=20"
```

Expected output: JSON with `data.asks[]` and `data.bids[]`. Each level: `price`, `quantity`, `count` (order count). `limit` sets depth (default 50). `metadata` carries `region` (defaults to EEA, pass `?region=UK` for UK) and `timestamp` (epoch ms). Field names differ from the deprecated v1 order book (`p`/`q`/`no`/`s`), so do not reuse v1 parsing.

### Get currencies and currency pairs configuration

```bash
python scripts/revx_request.py GET /api/1.0/public/configuration/currencies
python scripts/revx_request.py GET /api/1.0/public/configuration/pairs
```

Expected output: top-level objects keyed by currency code or pair code (no `data`/`metadata` wrapper). Currency fields: `name`, `symbol`, `scale`, `asset_type`, `status`. Pair fields: `base`, `quote`, `base_step`, `quote_step`, `min_order_size`, `max_order_size`, `min_order_size_quote`, `max_order_size_quote`, `status`, `slippage`. Optional `?region=UK|EEA`; omitted returns both regions.

### Get latest public trades (deprecated)

```bash
python scripts/revx_request.py GET /api/1.0/public/last-trades
```

Expected output: JSON with `data[]` array of the latest 100 trades across all pairs. Fields use abbreviated names (raw wire format) — see `references/schemas.md`.

Key fields: `tdt` (timestamp), `aid` (asset), `p` (price), `q` (quantity), `tid` (trade ID).

### Get public order book (deprecated)

```bash
python scripts/revx_request.py GET /api/1.0/public/order-book/BTC-USD
```

Expected output: JSON with `data.asks[]` and `data.bids[]` — max **5 price levels**. Fields: `p` (price), `q` (quantity), `no` (order count), `s` (side: `SELL`/`BUYI`). Note: `BUYI` is the actual API wire format abbreviation for buy-side, not a typo. This endpoint is deprecated in the official spec; use `/api/2.0/public/order-book/{symbol}` for new work.

### Example 1: Quick price check without API key
User says: "What's the current BTC price?"

Actions:
1. Run `python scripts/revx_request.py GET "/api/1.0/public/tickers?symbols=BTC-USD"`
2. Read `data[0].bid` and `data[0].ask`
3. Present: "BTC-USD: Bid $95,000 / Ask $95,100"

Result: Current bid/ask spread for BTC-USD.

### Example 2: Recent market activity
User says: "Show me recent trades on Revolut X"

Actions:
1. Run `python scripts/revx_request.py GET "/api/1.0/public/trades/all?limit=20"`
2. Parse the `data[]` array
3. Present recent trades with asset, price, quantity, timestamp

Result: Table of last 100 trades across all pairs.

## Error handling

**Error: 400 Bad Request**
Cause: Invalid symbol format
Solution: Use `BASE-QUOTE` dash format in the URL path, e.g. `BTC-USD`.

## Important notes

- Symbol formats differ: URL path and query parameters use dash format (`BTC-USD`), while `symbol` fields inside responses use slash format (`BTC/USD`)
- The deprecated v1 endpoints (`last-trades`, v1 `order-book`) use abbreviated field names and return ISO-8601 timestamp strings; the current endpoints (tickers, candles, trades/all, v2 order book) use full field names and Unix epoch millisecond timestamps. Check which endpoint a response came from before parsing timestamps
- `/api/1.0/public/last-trades` returns only the latest 100 trades and is not paginated; use `/api/1.0/public/trades/all` for history
- Configuration endpoints return top-level objects without a `data`/`metadata` wrapper

## References

- [schemas.md](references/schemas.md) — Full wire format field mappings
- [Revolut X REST API docs](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange)
- [Get tickers](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-tickers-public) · [Get candles](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-candles-public) · [Get trade history](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-trade-history-public) · [Get order book](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-order-book-public) · [Get currencies](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-currencies-public) · [Get currency pairs](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-currency-pairs-public)
- Deprecated: [Get last trades](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-last-trades-deprecated) · [Get public order book](https://developer.revolut.com/docs/api/revolut-x-crypto-exchange#get-public-order-book-deprecated)

## Related skills

| Skill | Purpose |
|---|---|
| `revolut-x-market-data` | Authenticated market data — order book (20 levels), candles, tickers |
| `revolut-x-trades` | Authenticated trade history with pagination |
| `revolut-x-auth` | Set up API keys to access authenticated endpoints |
