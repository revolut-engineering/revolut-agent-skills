# Trades — Request & Response Schemas

## PublicTrade Object (normalized)

Returned by `GET /api/1.0/trades/all/{symbol}`.

| Field | Type | Description |
|---|---|---|
| `id` | string (UUID) | Trade ID (converted from hex `tid`) |
| `symbol` | string | Trading pair in `BASE/QUOTE` format (e.g. `BTC/USD`) |
| `price` | decimal string | Execution price |
| `quantity` | decimal string | Execution quantity |
| `timestamp` | int64 | Trade timestamp in Unix epoch milliseconds |

---

## Trade Object (normalized)

Returned by `GET /api/1.0/trades/private/{symbol}` and `GET /api/1.0/orders/fills/{venue_order_id}`.

All `PublicTrade` fields plus:

| Field | Type | Description |
|---|---|---|
| `side` | string | `buy` \| `sell` |
| `orderId` | string (UUID) | Associated order ID (converted from hex `oid`) |
| `maker` | boolean | `true` = maker (resting order), `false` = taker (aggressive order) |

---

## Raw Wire Format (direct API access)

Both public and private trades use abbreviated field names in the raw response:

### Public Trade Fields

| Field | Description |
|---|---|
| `tdt` | Trade timestamp (Unix epoch milliseconds) |
| `aid` | Asset ID (e.g. `BTC`) |
| `anm` | Asset full name |
| `p` | Price |
| `pc` | Price currency |
| `pn` | Price name |
| `q` | Quantity |
| `qc` | Quantity currency |
| `qn` | Quantity name |
| `tid` | Transaction ID (hex) |
| `ve` | Venue — always `REVX` |
| `vp` | Venue of publication — always `REVX` |
| `pdt` | Publication timestamp |

### Additional Private Trade Fields

| Field | Description |
|---|---|
| `oid` | Order ID (hex, maps to UUID `orderId`) |
| `s` | Trade direction: `buy` \| `sell` |
| `im` | `true` = maker, `false` = taker |

### Field Mapping: Raw to Normalized

| Raw | Normalized | Notes |
|---|---|---|
| `tid` | `id` | Hex to UUID conversion |
| `aid`/`pc` | `symbol` | Combined as `aid/pc` (e.g. `BTC/USD`) |
| `p` | `price` | Direct mapping |
| `q` | `quantity` | Direct mapping |
| `tdt` | `timestamp` | Direct mapping |
| `s` | `side` | Private trades only |
| `oid` | `orderId` | Hex to UUID, private trades only |
| `im` | `maker` | Private trades only |

---

## Query Parameters — Date Ranges

Used by `/trades/all/{symbol}` and `/trades/private/{symbol}`:

| Param | Type             | Default                      | Description                                   |
|---|------------------|------------------------------|-----------------------------------------------|
| `start_date` | int64 (ms)       | `end_date - 7 days`          | Start of date range |
| `end_date` | int64 (ms)       | `start_date + 7 days` or now | End of date range |
| `cursor` | string           | —                            | Pagination cursor from `metadata.next_cursor` |
| `limit` | integer (1-1900) | 1900                         | Results per page |

**Max range: 30 days** — difference between `start_date` and `end_date` must not exceed 30 days.

---

## Pagination

All paginated trade endpoints return:

```json
{
  "data": [...],
  "metadata": {
    "next_cursor": "eyJsYXN0X2lkIjogImFiYzEyMyJ9",
    "timestamp": 1712345678000
  }
}
```

- If `metadata.next_cursor` is present, more pages are available
- Pass the cursor value as the `cursor` query parameter in the next request
- When `next_cursor` is absent or null, you've reached the last page

---

## Example Responses

### PublicTrade

```json
{
  "data": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "symbol": "BTC/USD",
      "price": "95000.50",
      "quantity": "0.001",
      "timestamp": 1712345678000
    }
  ],
  "metadata": {
    "next_cursor": "abc123",
    "timestamp": 1712345678000
  }
}
```

### Trade (private)

```json
{
  "data": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "symbol": "BTC/USD",
      "price": "95000.50",
      "quantity": "0.001",
      "timestamp": 1712345678000,
      "side": "buy",
      "orderId": "7a52e92e-8639-4fe1-abaa-68d3a2d5234b",
      "maker": false
    }
  ],
  "metadata": {
    "next_cursor": null,
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
