---
name: revolut-x-configuration
description: >
  Revolut X exchange configuration data. Use when the user asks about "available
  currencies", "trading pairs", "supported assets", "pair constraints", "min order
  size", "max order size", or needs to validate a symbol before placing an order.
---

# Revolut X Configuration

## Instructions

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

**CRITICAL:** Always check pair `status` is `active` before placing orders. Warn the user if a pair is `inactive`.

---

## Examples

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

---

## Important Notes

- Pairs response uses **slash format** (`BTC/USD`) in keys, but order placement uses **dash format** (`BTC-USD`)
- Always validate pair constraints before placing orders (see `revolut-x-orders`)

For full response field definitions, see `references/schemas.md`.

---

## Troubleshooting

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup.

---

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Use pair constraints to validate order parameters |
| `revolut-x-balance` | Check available currencies in your account |
| `revolut-x-market-data` | Get current prices for listed pairs |
