# Public Market Data — Request & Response Schemas

## Public Last Trades

`GET /api/1.0/public/last-trades` — returns the latest 100 trades across all pairs.

### Raw Wire Format Fields

| Field | Description |
|---|---|
| `tdt` | Trade timestamp (ISO-8601 string) |
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
| `pdt` | Publication timestamp (ISO-8601 string) |

### Example Response

```json
{
  "data": [
    {
      "tdt": "2026-07-29T07:23:53.816Z",
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
      "pdt": "2026-07-29T07:23:53.817Z"
    }
  ]
}
```

---

## Public Order Book

`GET /api/1.0/public/order-book/{symbol}` — max 5 price levels.

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
| `pdt` | Publication timestamp (ISO-8601 string) |

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
        "pdt": "2026-07-29T07:23:53.816Z"
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
        "pdt": "2026-07-29T07:23:53.816Z"
      }
    ]
  },
  "metadata": {
    "timestamp": "2026-07-29T08:23:53.816Z"
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
