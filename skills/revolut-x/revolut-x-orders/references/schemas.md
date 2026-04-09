# Orders — Request & Response Schemas

## Order Placement Request

`POST /api/1.0/orders`

```json
{
  "client_order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",  // UUID, required — for idempotency
  "symbol": "BTC-USD",                                          // required
  "side": "buy",                                                // "buy" | "sell", required
  "order_configuration": {                                      // required — exactly one of:
    "limit": {
      "price": "90000.10",        // required for limit
      "base_size": "0.1",         // one of base_size or quote_size
      "quote_size": "500.00",     // one of base_size or quote_size
      "execution_instructions": ["post_only"]  // [] | ["allow_taker"] | ["post_only"]
    },
    "market": {
      "base_size": "0.1",         // one of base_size or quote_size
      "quote_size": "500.00"      // one of base_size or quote_size
    }
  }
}
```

### Execution Instructions

- `allow_taker` — default; order can execute as a taker
- `post_only` — order cancelled if it would execute immediately (maker only)
- Pass `[]` for no instructions

---

## Order Placement Response

```json
{
  "data": {
    "venue_order_id": "7a52e92e-8639-4fe1-abaa-68d3a2d5234b",
    "client_order_id": "984a4d8a-2a9b-4950-822f-2a40037f02bd",
    "state": "new"
  }
}
```

---

## Order Object (full)

Returned by GET `/orders/active`, `/orders/historical`, `/orders/{venue_order_id}`:

| Field | Type | Description |
|---|---|---|
| `id` | uuid | System order ID (`venue_order_id`) |
| `client_order_id` | uuid | Client-assigned ID |
| `previous_order_id` | uuid | Set if this order replaced another |
| `symbol` | string | Trading pair (e.g. `BTC-USD`) |
| `side` | string | `buy` \| `sell` |
| `type` | string | `market` \| `limit` \| `conditional` \| `tpsl` |
| `quantity` | decimal string | Order size in base currency (sell: initial locked amount) |
| `filled_quantity` | decimal string | Amount executed so far |
| `leaves_quantity` | decimal string | Amount remaining to fill |
| `amount` | decimal string | Order size in quote currency (buy: initial locked amount) |
| `price` | decimal string | Worst acceptable price (max for buy, min for sell) |
| `average_fill_price` | decimal string | Quantity-weighted average execution price |
| `status` | string | See order statuses below |
| `reject_reason` | string | Present only when `status=rejected` |
| `time_in_force` | string | `gtc` \| `ioc` \| `fok` |
| `execution_instructions` | array | `allow_taker` and/or `post_only` |
| `conditional` | object | Present only for `type=conditional` — see OrderTrigger |
| `take_profit` | object | Present for `type=tpsl` — see OrderTrigger |
| `stop_loss` | object | Present for `type=tpsl` — see OrderTrigger |
| `created_date` | int64 | Unix epoch milliseconds |
| `updated_date` | int64 | Unix epoch milliseconds |

---

## Order Statuses

- `pending_new` — accepted by matching engine, not yet working
- `new` — working order
- `partially_filled` — partially executed
- `filled` — fully executed
- `cancelled` — cancelled
- `rejected` — rejected (check `reject_reason`)
- `replaced` — replaced by another order

---

## Time in Force

- `gtc` — Good till cancelled: stays active until filled or manually cancelled
- `ioc` — Immediate or cancel: unfilled portion cancelled immediately
- `fok` — Fill or kill: must fill entirely immediately or be cancelled (no partial fills)

---

## OrderTrigger (for conditional / TPSL)

| Field | Type | Description |
|---|---|---|
| `trigger_price` | decimal string | Price level that activates the order |
| `type` | string | `market` \| `limit` |
| `trigger_direction` | string | `ge` (>= trigger) \| `le` (<= trigger) |
| `limit_price` | decimal string | Execution price — required for limit triggers |
| `time_in_force` | string | `gtc` \| `ioc` |
| `execution_instructions` | array | `allow_taker` and/or `post_only` |

---

## Active Orders — Query Filters

`GET /api/1.0/orders/active`:

| Param | Values                                   | Description                                   |
|---|------------------------------------------|-----------------------------------------------|
| `symbols` | comma-separated                          | e.g. `BTC-USD,ETH-USD`                        |
| `order_states` | `pending_new`, `new`, `partially_filled` |                                               |
| `order_types` | `limit`, `conditional`, `tpsl`           |                                               |
| `side` | `buy`, `sell`                            |                                               |
| `cursor` | string                                   | Pagination cursor from `metadata.next_cursor` |
| `limit` | 1-300                                    | Default 300                                   |

---

## Historical Orders — Query Filters

`GET /api/1.0/orders/historical`:

| Param | Values                                        | Description            |
|---|-----------------------------------------------|------------------------|
| `symbols` | comma-separated                               | e.g. `BTC-USD,ETH-USD` |
| `order_states` | `filled`, `cancelled`, `rejected`, `replaced` |                        |
| `order_types` | `market`, `limit`                             |                        |
| `start_date` / `end_date` | int64 ms                                      | Max 30-day range       |
| `cursor` | string                                        | Pagination cursor      |
| `limit` | 1-1900                                        | Default 1900           |

---

## Date Range Parameters

Used by `/orders/historical`:

- `start_date` — Unix epoch ms. Defaults to `end_date - 7 days`
- `end_date` — Unix epoch ms. Defaults to `start_date + 7 days` or current time
- **Max range: 30 days** — difference between `start_date` and `end_date` must not exceed 30 days

---

## Pagination

All paginated order endpoints return:

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

## Error Response

All errors return:

```json
{
  "error_id": "7d85b5e7-d0f0-4696-b7b5-a300d0d03a5e",
  "message": "Human-readable description",
  "timestamp": 3318215482991
}
```

| HTTP Status | Meaning |
|---|---|
| `400` | Bad request (e.g. invalid symbol, insufficient funds, order rejected) |
| `401` | Unauthorized (invalid/missing API key or signature) |
| `403` | Forbidden (e.g. IP not whitelisted) |
| `404` | Order not found |
| `409` | Conflict (e.g. timestamp in the future) |
| `429` | Rate limit exceeded — check `Retry-After` header (milliseconds) |
| `5XX` | Server error |
