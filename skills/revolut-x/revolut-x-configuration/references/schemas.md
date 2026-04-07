# Configuration — Request & Response Schemas

## Currency Object

`GET /api/1.0/configuration/currencies` — returns a map keyed by symbol.

| Field | Type | Description |
|---|---|---|
| `symbol` | string | Currency symbol, e.g. `BTC` |
| `name` | string | Full name, e.g. `Bitcoin` |
| `scale` | integer | Decimal places (e.g. `8` means precision to 0.00000001) |
| `asset_type` | string | `fiat` \| `crypto` |
| `status` | string | `active` \| `inactive` |

### Example Response

```json
{
  "BTC": {
    "symbol": "BTC",
    "name": "Bitcoin",
    "scale": 8,
    "asset_type": "crypto",
    "status": "active"
  },
  "USD": {
    "symbol": "USD",
    "name": "US Dollar",
    "scale": 2,
    "asset_type": "fiat",
    "status": "active"
  }
}
```

---

## Currency Pair Object

`GET /api/1.0/configuration/pairs` — returns a map keyed by pair (e.g. `BTC/USD`).

| Field | Type          | Description                              |
|---|---------------|------------------------------------------|
| `base` | string        | Base currency (e.g. `BTC`)               |
| `quote` | string        | Quote currency (e.g. `USD`)              |
| `base_step` | decimal string | Min increment for base currency quantity |
| `quote_step` | decimal string | Min increment for quote currency amount  |
| `min_order_size` | decimal string | Min order quantity in base currency      |
| `max_order_size` | decimal string | Max order quantity in base currency      |
| `min_order_size_quote` | decimal string | Min order quantity in quote currency     |
| `status` | string        | `active` \| `inactive`                   |
| `slippage` | integer        | Max price deviation in basis points (1 bp = 0.01%)      |

### Example Response

```json
{
  "BTC/USD": {
    "base": "BTC",
    "quote": "USD",
    "base_step": "0.00001",
    "quote_step": "0.01",
    "min_order_size": "0.00001",
    "max_order_size": "10",
    "min_order_size_quote": "1",
    "status": "active",
    "slippage": 5
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
