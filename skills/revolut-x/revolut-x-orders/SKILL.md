---
name: revolut-x-orders
description: >
  Revolut X order management. Use when the user asks to "place an order", "buy BTC",
  "sell ETH", "market order", "limit order", "cancel order", "cancel all orders",
  "view open orders", "order history", or anything related to trading on Revolut X.
---

# Revolut X Orders

## Behavioral Instructions for Claude

### CRITICAL: Human Confirmation Required

**NEVER place or cancel orders without explicit user confirmation.** These operations move real money.

Before executing, present a confirmation summary:

> **Order to place:**
> - Pair: BTC-USD
> - Side: buy
> - Type: limit @ $95,000
> - Size: 0.001 BTC
>
> Shall I proceed?

Only execute after the user explicitly approves.

For cancel-all (`DELETE /api/1.0/orders`), warn that this cancels **every** open order.

### Missing Parameters — Always Ask, Never Guess

Required for every order:
1. **Symbol** — which pair? (e.g. `BTC-USD`)
2. **Side** — buy or sell?
3. **Size** — how much? (base_size or quote_size)
4. **Order type** — market or limit? (if limit, at what price?)

If the user says "buy some BTC", ask: How much? Market or limit?

---

## Instructions

### Place a market order

```bash
python scripts/revx_sign.py POST /api/1.0/orders --body '{"client_order_id":"UUID","symbol":"BTC-USD","side":"buy","order_configuration":{"market":{"quote_size":"500"}}}'
```

### Place a limit order

```bash
python scripts/revx_sign.py POST /api/1.0/orders --body '{"client_order_id":"UUID","symbol":"BTC-USD","side":"buy","order_configuration":{"limit":{"price":"95000","base_size":"0.001","execution_instructions":["allow_taker"]}}}'
```

Execution instructions: `allow_taker` (default) or `post_only` (maker only — cancelled if would execute immediately).

### Get active orders

```bash
python scripts/revx_sign.py GET /api/1.0/orders/active
```

With filters:

```bash
python scripts/revx_sign.py GET /api/1.0/orders/active --query '?symbols=BTC-USD&side=buy'
```

### Get historical orders

```bash
python scripts/revx_sign.py GET /api/1.0/orders/historical --query '?start_date=START_MS&end_date=END_MS'
```

Max date range: 30 days.

### Get order by ID

```bash
python scripts/revx_sign.py GET /api/1.0/orders/ORDER_UUID
```

### Cancel an order

```bash
python scripts/revx_sign.py DELETE /api/1.0/orders/ORDER_UUID
```

### Cancel ALL orders

```bash
python scripts/revx_sign.py DELETE /api/1.0/orders
```

**Warning:** Cancels every open limit, conditional, and TPSL order.

---

## Pre-flight Validation

Before placing any order:
1. Check pair is active and get constraints: `python scripts/revx_sign.py GET /api/1.0/configuration/pairs` (see `revolut-x-configuration`)
2. Check sufficient balance: `python scripts/revx_sign.py GET /api/1.0/balances` (see `revolut-x-balance`)
3. Verify order size meets min/max constraints

---

## Examples

### Example 1: Place a market buy
User says: "Buy $500 worth of BTC at market price"

Actions:
1. Check pair constraints: `python scripts/revx_sign.py GET /api/1.0/configuration/pairs`
2. Check USD balance: `python scripts/revx_sign.py GET /api/1.0/balances`
3. Present confirmation summary and wait for approval
4. Generate UUID for `client_order_id`
5. Run `python scripts/revx_sign.py POST /api/1.0/orders --body '{"client_order_id":"GENERATED_UUID","symbol":"BTC-USD","side":"buy","order_configuration":{"market":{"quote_size":"500"}}}'`

Result: Order placed, `venue_order_id` returned.

### Example 2: Place a post-only limit sell
User says: "Sell 0.1 ETH at $3,500, maker only"

Actions:
1. Validate pair and balance
2. Present confirmation summary
3. Run `python scripts/revx_sign.py POST /api/1.0/orders --body '{"client_order_id":"UUID","symbol":"ETH-USD","side":"sell","order_configuration":{"limit":{"price":"3500","base_size":"0.1","execution_instructions":["post_only"]}}}'`

Result: Post-only limit order placed.

### Example 3: Cancel a specific order
User says: "Cancel order abc-123"

Actions:
1. Present cancellation confirmation
2. Run `python scripts/revx_sign.py DELETE /api/1.0/orders/abc-123`

Result: Order cancelled.

### Example 4: Review and cancel all open orders
User says: "Cancel all my orders"

Actions:
1. Run `python scripts/revx_sign.py GET /api/1.0/orders/active` to show current orders
2. Present the list and warn: "This will cancel ALL open orders"
3. After confirmation: `python scripts/revx_sign.py DELETE /api/1.0/orders`

Result: All open orders cancelled.

---

## Important Notes

- **Limit order rate limit:** 1000 placements per day
- `client_order_id` is for idempotency — use a unique UUID for each order
- Market orders: specify `base_size` OR `quote_size`, not both
- Symbols use **dash format** (`BTC-USD`) in requests

For full request/response schemas, order statuses, time-in-force values, and query filters, see `references/schemas.md`.

---

## Troubleshooting

**Error: 400 Bad Request**
Cause: Invalid params, insufficient funds, or order rejected
Solution: Check pair constraints, verify balance, review order parameters.

**Error: 404 Not Found**
Cause: Invalid `venue_order_id`
Solution: Verify the order ID from active orders or placement response.

**Error: 429 Rate Limit**
Cause: Too many requests (or 1000 limit orders/day exceeded)
Solution: Wait for `Retry-After` header duration, then retry.

---

## Related Skills

| Skill | Purpose |
|---|---|
| `revolut-x-auth` | API key setup and request signing |
| `revolut-x-balance` | Check available funds before placing orders |
| `revolut-x-configuration` | Validate pair constraints (min/max size, step) |
| `revolut-x-trades` | View fills and execution details after orders execute |
| `revolut-x-market-data` | Check current prices before placing orders |
