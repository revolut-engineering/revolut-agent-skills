# Balance — Request & Response Schemas

## Balance Object

`GET /api/1.0/balances` — returns an array of balance objects.

| Field | Type | Description |
|---|---|---|
| `currency` | string | Currency symbol (e.g. `BTC`, `USD`) |
| `available` | decimal string | Free funds — can be used for new orders |
| `reserved` | decimal string | Locked funds — held by open orders |
| `staked` | decimal string | Funds earning staking rewards (if applicable) |
| `total` | decimal string | Sum of `available` + `reserved` + `staked` |

### Field Semantics

- **available** — funds you can use right now for placing new orders or withdrawing
- **reserved** — funds locked by your currently active orders; freed when orders are cancelled or filled
- **staked** — funds participating in staking programs; not available for trading
- **total** — the complete balance across all states

### Example Response

```json
[
  {
    "currency": "BTC",
    "available": "0.50000000",
    "reserved": "0.10000000",
    "staked": "0.00000000",
    "total": "0.60000000"
  },
  {
    "currency": "USD",
    "available": "10000.00",
    "reserved": "5000.00",
    "staked": "0.00",
    "total": "15000.00"
  }
]
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
