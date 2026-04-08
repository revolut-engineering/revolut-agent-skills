---
name: revolut-x-balance
version: 0.1.0
description: >
  Revolut X account balance queries — available, reserved, staked, and total
  funds per currency. Verify funds before placing orders.
allowed-tools: [Bash]
sources:
  - https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api
  - https://developer.revolut.com/docs/x-api/get-all-balances
---

# Revolut X Balance

## Capabilities

- Fetch all account balances (available, reserved, staked, total)
- Verify sufficient funds before placing orders
- Compute portfolio value in fiat using ticker data

## Authentication & setup

All endpoints require authentication. See [revolut-x-auth](../revolut-x-auth/SKILL.md) for setup.

## API versioning

All endpoints use path-based versioning: `/api/1.0/`. The version is included in every request path.

## Common workflows

### Fetch balances

```bash
python scripts/revx_sign.py GET /api/1.0/balances
```

Expected output: JSON array of balance objects with `currency`, `available`, `reserved`, `staked`, `total` fields.

Display balances in a readable table. Key fields:
- **available** — funds ready for new orders
- **reserved** — locked by open orders
- **staked** — earning staking rewards
- **total** — available + reserved + staked

### Example 1: Check portfolio balances
User says: "What's my balance on Revolut X?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/balances`
2. Parse the JSON array
3. Present as a formatted table: currency, available, reserved, total

Result: Table showing all currency balances.

### Example 2: Verify funds before ordering
User says: "Do I have enough USD to buy $500 of BTC?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/balances`
2. Find USD entry, check `available` >= 500
3. Report yes/no with exact available amount

Result: "You have $10,000.00 USD available — sufficient for a $500 order."

### Example 3: Portfolio value in fiat
User says: "What's my total portfolio worth in USD?"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/balances`
2. Run `python scripts/revx_sign.py GET /api/1.0/tickers` (see `revolut-x-market-data`)
3. Multiply each crypto balance's `total` by its USD `last_price`
4. Sum all values

Result: Total portfolio value in USD.

## Error handling

**Error: 401 Unauthorized**
Cause: API key or signature invalid
Solution: Run `revolut-x-auth` setup. Verify `REVX_API_KEY` and `REVX_PRIVATE_KEY` env vars.

**Error: 429 Rate limit exceeded**
Cause: Too many requests
Solution: Wait for duration in `Retry-After` header (milliseconds), then retry.

## Important notes

- Balance `available` reflects funds not locked by open orders — use this for pre-order validation
- Zero-balance currencies may still appear in the response
- To compute fiat portfolio value, combine with ticker data from `revolut-x-market-data`

## References

- [schemas.md](references/schemas.md) — Full response field definitions

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-orders` | Place orders after verifying sufficient balance |
| `revolut-x-configuration` | Check available currencies and pair constraints |
| `revolut-x-market-data` | Get ticker prices to compute fiat value of holdings |
