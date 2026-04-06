# Market Data — Request & Response Schemas

## Ticker Object

`GET /api/1.0/tickers` — returns `data` array + `metadata.timestamp`.

| Field | Type | Description |
|---|---|---|
| `symbol` | string | Trading pair, e.g. `BTC/USD` (slash format) |
| `bid` | decimal string | Best buy price (top of buy book) |
| `ask` | decimal string | Best sell price (top of sell book) |
| `mid` | decimal string | `(bid + ask) / 2` |
| `last_price` | decimal string | Price of the most recent trade |

### Example Response

```json
{
  "data": [
    {
      "symbol": "BTC/USD",
      "bid": "95000.00",
      "ask": "95100.50",
      "mid": "95050.25",
      "last_price": "95075.00"
    }
  ],
  "metadata": {
    "timestamp": 1712345678000
  }
}
```

---

## Candle Object (OHLCV)

`GET /api/1.0/candles/{symbol}` — returns array of candle objects.

| Field | Type | Description |
|---|---|---|
| `start` | int64 | Candle start time, Unix epoch milliseconds |
| `open` | decimal string | Opening price |
| `high` | decimal string | Highest price in interval |
| `low` | decimal string | Lowest price in interval |
| `close` | decimal string | Closing price |
| `volume` | decimal string | Total trading volume in base currency |

### Query Parameters

| Param | Type | Default | Description |
|---|---|---|---|
| `interval` | integer (minutes) | `5` | Candle width: `1`, `5`, `15`, `30`, `60`, `240`, `1440`, `2880`, `5760`, `10080`, `20160`, `40320` |
| `since` | int64 (ms) | `until - (interval * 100)` | Start of range |
| `until` | int64 (ms) | current time | End of range |

**Constraint:** Max 1000 candles per request: `(until - since) / (interval * 60000) <= 1000`

If no trades occurred in a period, candle is based on mid price (bid/ask average).

### Example Response

```json
[
  {
    "start": 1712345400000,
    "open": "95000.00",
    "high": "95200.00",
    "low": "94900.00",
    "close": "95100.00",
    "volume": "12.5"
  }
]
```

---

## Order Book

`GET /api/1.0/order-book/{symbol}` — up to 20 levels.

Response structure: `data.asks[]`, `data.bids[]` (sorted by price descending), and `metadata.timestamp`.

### Normalized Level Format (authenticated endpoint)

| Field | Type | Description |
|---|---|---|
| `price` | decimal string | Price at this level |
| `quantity` | decimal string | Aggregated quantity at this level |
| `orderCount` | number | Number of orders at this level |

### Raw Wire Format (direct API access)

| Field | Description |
|---|---|
| `aid` | Asset ID (e.g. `ETH`) |
| `anm` | Asset full name |
| `p` | Price |
| `pc` | Price currency |
| `pn` | Price name |
| `q` | Aggregated quantity at this level |
| `qc` | Quantity currency |
| `qn` | Quantity name |
| `no` | Number of orders at this level |
| `s` | Side: `SELL` \| `BUYI` |
| `ve` | Venue — always `REVX` |
| `ts` | Trading system — always `CLOB` |
| `pdt` | Publication timestamp |

### Example Response (normalized)

```json
{
  "data": {
    "asks": [
      { "price": "95100.00", "quantity": "0.5", "orderCount": 3 },
      { "price": "95150.00", "quantity": "1.2", "orderCount": 7 }
    ],
    "bids": [
      { "price": "95000.00", "quantity": "0.8", "orderCount": 4 },
      { "price": "94950.00", "quantity": "2.1", "orderCount": 9 }
    ]
  },
  "metadata": {
    "timestamp": 1712345678000
  }
}
```

---

## Interval Reference

| Minutes | Shorthand | Description |
|---|---|---|
| `1` | 1m | 1 minute |
| `5` | 5m | 5 minutes |
| `15` | 15m | 15 minutes |
| `30` | 30m | 30 minutes |
| `60` | 1h | 1 hour |
| `240` | 4h | 4 hours |
| `1440` | 1d | 1 day |
| `2880` | 2d | 2 days |
| `5760` | 4d | 4 days |
| `10080` | 1w | 1 week |
| `20160` | 2w | 2 weeks |
| `40320` | 4w | 4 weeks |

---

## Error Response

All errors return:

```json
{
  "error_id": "UUID",
  "message": "Human-readable description",
  "timestamp": 1234567890123
}
```
