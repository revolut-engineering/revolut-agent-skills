# Public Market Data — Request & Response Schemas

## Public Tickers

`GET /api/1.0/public/tickers` — tickers for all currency pairs.

Query parameters: `symbols` (optional, comma-separated dash-format pairs, e.g. `BTC-USD,ETH-USD`), `region` (optional, `UK` or `EEA`; both regions returned when omitted).

### Raw Wire Format Fields

| Field | Description |
|---|---|
| `symbol` | Currency pair, slash format (e.g. `BTC/USD`) |
| `bid` | Current highest buy price |
| `ask` | Current lowest sell price |
| `mid` | Midpoint of best bid and ask |
| `index_price` | Volume-weighted index price across external exchanges |
| `last_price` | Price of the most recent trade |
| `low_24h` | Lowest traded price in the last 24 hours |
| `high_24h` | Highest traded price in the last 24 hours |
| `price_change_24h` | Absolute price change over the last 24 hours |
| `volume_24h` | Traded volume in base currency over the last 24 hours |
| `quote_volume_24h` | Traded volume in quote currency over the last 24 hours |
| `region` | Data region: `UK` or `EEA` |

`metadata.timestamp` is Unix epoch milliseconds.

### Example Response

```json
{
  "data": [
    {
      "symbol": "BTC/USD",
      "bid": "59084.64",
      "ask": "59094.36",
      "mid": "59089.50",
      "index_price": "59090.89",
      "last_price": "59102.68",
      "low_24h": "55229.82",
      "high_24h": "60767.84",
      "price_change_24h": "2889.86",
      "volume_24h": "83.68",
      "quote_volume_24h": "4942000.00",
      "region": "EEA"
    }
  ],
  "metadata": {
    "timestamp": 1795324028767
  }
}
```

---

## Public OHLCV Candles

`GET /api/1.0/public/candles/{symbol}` — up to 1000 candles per request.

Path parameter: `symbol` in dash format (e.g. `BTC-USD`). Query parameters: `interval` (minutes, one of 1, 5, 15, 30, 60, 240, 1440, 2880, 5760, 10080, 20160, 40320; default 5), `since` and `until` (Unix epoch milliseconds; `until` defaults to now), `region` (`UK` or `EEA`, default `EEA`).

### Raw Wire Format Fields

| Field | Description |
|---|---|
| `start` | Candle start time (Unix epoch milliseconds) |
| `open` | Opening price |
| `high` | Highest price during the interval |
| `low` | Lowest price during the interval |
| `close` | Closing price |
| `volume` | Total volume in base currency during the interval |

`metadata` carries `timestamp` (Unix epoch milliseconds) and `region`.

### Example Response

```json
{
  "data": [
    {
      "start": 1795024200000,
      "open": "63054.54",
      "high": "63057.14",
      "low": "62992.84",
      "close": "63055.44",
      "volume": "15.1853899"
    }
  ],
  "metadata": {
    "timestamp": 1795324029056,
    "region": "EEA"
  }
}
```

---

## Public Trade History

`GET /api/1.0/public/trades/all` — paginated trade history.

Query parameters: `symbol` (optional, dash format; omit for all pairs), `start_date` and `end_date` (Unix epoch milliseconds; the window between them must not exceed 1 day, an omitted `start_date` defaults to 1 day before `end_date`, an omitted `end_date` defaults to `start_date` + 1 day or now; split longer ranges into per-day windows), `cursor` (from `metadata.next_cursor`), `limit` (1-100, default 100), `region` (optional, `UK` or `EEA`; both regions returned when omitted).

### Raw Wire Format Fields

| Field | Description |
|---|---|
| `id` | Trade ID (UUID) |
| `symbol` | Currency pair, slash format (e.g. `BTC/USD`) |
| `price` | Trade price |
| `quantity` | Trade quantity in base currency |
| `side` | Trade side: `buy` or `sell` |
| `timestamp` | Trade time (Unix epoch milliseconds) |
| `region` | Data region: `UK` or `EEA` |

`metadata.timestamp` is Unix epoch milliseconds. `metadata.next_cursor` is the pagination cursor; pass it back as `?cursor=...` for the next page. An empty cursor means no more pages.

### Example Response

```json
{
  "data": [
    {
      "id": "1579cd6f-8ea1-3bb9-9c29-7e0937df0daf",
      "symbol": "BTC/USD",
      "price": "59102.68",
      "quantity": "0.01000000",
      "side": "buy",
      "timestamp": 1795323991108,
      "region": "EEA"
    }
  ],
  "metadata": {
    "timestamp": 1795324029859,
    "next_cursor": "ZGF0ZT0xNzk1MzI0MDI5Njc4..."
  }
}
```

---

## Public Order Book v2

`GET /api/2.0/public/order-book/{symbol}` — order book with configurable depth.

Path parameter: `symbol` in dash format (e.g. `BTC-USD`). Query parameters: `limit` (number of price levels, min 1, max 192, default 50), `region` (`UK` or `EEA`, default `EEA`).

Response structure: `data.asks[]`, `data.bids[]`, and `metadata`. Field names differ from the deprecated v1 order book.

### Raw Wire Format Fields (per level)

| Field | Description |
|---|---|
| `price` | Price at this level |
| `quantity` | Aggregated quantity at this level |
| `count` | Number of orders at this level (integer) |

`metadata` carries `region` and `timestamp` (Unix epoch milliseconds).

### Example Response

```json
{
  "data": {
    "asks": [
      {
        "price": "59094.58",
        "quantity": "0.06495626",
        "count": 1
      }
    ],
    "bids": [
      {
        "price": "59084.64",
        "quantity": "0.19486877",
        "count": 1
      }
    ]
  },
  "metadata": {
    "region": "EEA",
    "timestamp": 1795324030097
  }
}
```

---

## Public Configuration

`GET /api/1.0/public/configuration/currencies` and `GET /api/1.0/public/configuration/pairs`.

Optional `region` query parameter (`UK` or `EEA`; both regions returned when omitted). Both endpoints return a top-level object keyed by currency or pair code, with no `data`/`metadata` wrapper.

### Currency Fields

| Field | Description |
|---|---|
| `name` | Currency full name (e.g. `Bitcoin`) |
| `symbol` | Currency display symbol (e.g. `BTC`, `$`) |
| `scale` | Decimal scale of the currency (integer) |
| `asset_type` | `crypto` or `fiat` |
| `status` | e.g. `active` |

### Currency Pair Fields

| Field | Description |
|---|---|
| `base` | Base currency code |
| `quote` | Quote currency code |
| `base_step` | Minimum base increment |
| `quote_step` | Minimum quote increment |
| `min_order_size` / `max_order_size` | Order size bounds in base currency |
| `min_order_size_quote` | Minimum order size in quote currency |
| `status` | e.g. `active` |

### Example Responses

```json
{
  "BTC": {
    "name": "Bitcoin",
    "symbol": "BTC",
    "scale": 8,
    "asset_type": "crypto",
    "status": "active"
  }
}
```

```json
{
  "BTC/USD": {
    "base": "BTC",
    "quote": "USD",
    "base_step": "0.000001",
    "quote_step": "0.001",
    "min_order_size": "0.000001",
    "max_order_size": "100000",
    "min_order_size_quote": "0.1",
    "status": "active"
  }
}
```

---

## Public Last Trades (deprecated)

`GET /api/1.0/public/last-trades` — returns the latest 100 trades across all pairs. Deprecated in the official spec; use `/api/1.0/public/trades/all` for new work.

### Raw Wire Format Fields

| Field | Description |
|---|---|
| `tdt` | Trade timestamp (Unix epoch milliseconds) |
| `aid` | Asset ID (e.g. `BTC`) |
| `anm` | Asset full name (e.g. `Bitcoin`) |
| `p` | Price |
| `pc` | Price currency (e.g. `USD`) |
| `pn` | Price currency name |
| `q` | Quantity |
| `qc` | Quantity currency |
| `qn` | Quantity currency name |
| `tid` | Transaction ID (hex) |
| `ve` | Venue — always `REVX` |
| `vp` | Venue of publication — always `REVX` |
| `pdt` | Publication timestamp |

### Example Response

```json
{
  "data": [
    {
      "tdt": 1712345678000,
      "aid": "BTC",
      "anm": "Bitcoin",
      "p": "95000.50",
      "pc": "USD",
      "pn": "US Dollar",
      "q": "0.001",
      "qc": "BTC",
      "qn": "Bitcoin",
      "tid": "a1b2c3d4",
      "ve": "REVX",
      "vp": "REVX",
      "pdt": 1712345678001
    }
  ]
}
```

---

## Public Order Book (deprecated)

`GET /api/1.0/public/order-book/{symbol}` — max 5 price levels. Deprecated in the official spec; use `/api/2.0/public/order-book/{symbol}` for new work.

Response structure: `data.asks[]`, `data.bids[]`, and `metadata.timestamp`.

### Raw Wire Format Fields (per level)

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

### Side Values

- `SELL` — ask side (sell orders)
- `BUYI` — bid side (buy orders)

### Example Response

```json
{
  "data": {
    "asks": [
      {
        "aid": "BTC",
        "anm": "Bitcoin",
        "p": "95100.00",
        "pc": "USD",
        "pn": "US Dollar",
        "q": "0.5",
        "qc": "BTC",
        "qn": "Bitcoin",
        "no": 3,
        "s": "SELL",
        "ve": "REVX",
        "ts": "CLOB",
        "pdt": 1712345678000
      }
    ],
    "bids": [
      {
        "aid": "BTC",
        "anm": "Bitcoin",
        "p": "95000.00",
        "pc": "USD",
        "pn": "US Dollar",
        "q": "1.2",
        "qc": "BTC",
        "qn": "Bitcoin",
        "no": 5,
        "s": "BUYI",
        "ve": "REVX",
        "ts": "CLOB",
        "pdt": 1712345678000
      }
    ]
  },
  "metadata": {
    "timestamp": 1712345678000
  }
}
```

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
