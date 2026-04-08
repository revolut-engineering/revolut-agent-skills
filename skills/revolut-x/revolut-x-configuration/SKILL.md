---
name: revolut-x-configuration
version: 0.1.0
description: >
  Revolut X exchange configuration — available currencies, trading pairs,
  pair constraints (min/max order size, step), and asset status.
allowed-tools: [Bash]
sources:
  - https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api
  - https://developer.revolut.com/docs/x-api/get-all-currencies
---

# Revolut X Configuration

## Capabilities

- List all available currencies with type, scale, and status
- List all trading pairs with constraints (min/max order size, step)
- Validate whether a pair is active before placing orders

## Authentication & setup

All endpoints require authentication. See [revolut-x-auth](../revolut-x-auth/SKILL.md) for setup.

## API versioning

All endpoints use path-based versioning: `/api/1.0/`. The version is included in every request path.

## Common workflows

### Get all currencies

```bash
python scripts/revx_sign.py GET /api/1.0/configuration/currencies
```

Expected output: JSON map keyed by symbol (e.g. `BTC`, `USD`) with `name`, `scale`, `asset_type`, `status`.

### Get all trading pairs

```bash
python scripts/revx_sign.py GET /api/1.0/configuration/pairs
```

Expected output: JSON map keyed by pair (e.g. `BTC/USD`) with `base`, `quote`, `min_order_size`, `max_order_size`, `base_step`, `quote_step`, `status`.

**CRITICAL:** Always check pair `status` is `active` before placing orders. Flag inactive pairs before proceeding.

### Example 1: Check if a pair is tradeable
User says: "Can I trade SOL-USD on Revolut X?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/configuration/pairs`
2. Look for `SOL/USD` key (note: response uses slash format)
3. Check `status` field

Result: "SOL/USD is active. Min order: 0.01 SOL, max: 10000 SOL."

### Example 2: Get min order size
User says: "What's the minimum BTC-USD order?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/configuration/pairs`
2. Find `BTC/USD`, read `min_order_size` and `min_order_size_quote`

Result: "Min order for BTC-USD: 0.00001 BTC or $1.00 USD."

### Example 3: List all crypto assets
User says: "What cryptocurrencies does Revolut X support?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/configuration/currencies`
2. Filter where `asset_type` is `crypto` and `status` is `active`
3. Present as a list

Result: Table of supported cryptocurrencies with name, symbol, and precision.

## Error handling

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup.

## Important notes

- Pairs response uses **slash format** (`BTC/USD`) in keys, but order placement uses **dash format** (`BTC-USD`)
- Always validate pair constraints before placing orders (see `revolut-x-orders`)

## References

- [schemas.md](references/schemas.md) — Full response field definitions

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Use pair constraints to validate order parameters |
| `revolut-x-balance` | Check available currencies in your account |
| `revolut-x-market-data` | Get current prices for listed pairs |
