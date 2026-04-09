---
name: revolut-x-auth
description: >
  Revolut X API authentication setup, Ed25519 keypair generation, and request signing.
  Use when the user asks to set up Revolut X API access, configure API keys, generate an
  Ed25519 keypair, sign requests manually, or debug 401/403/409 authentication errors.
allowed-tools: Bash
compatibility: Requires Python 3 and OpenSSL (bundled scripts/revx_sign.py helper)
metadata:
  version: "0.1.0"
---

# Revolut X Authentication

## Capabilities

- Generate Ed25519 keypairs for API authentication
- Configure API key and private key environment variables
- Sign authenticated requests via `scripts/revx_sign.py`
- Debug 401/403/409 authentication errors

## Authentication & setup

This skill handles authentication setup for all other Revolut X skills.

### Step 1: Generate an Ed25519 keypair

```bash
openssl genpkey -algorithm ed25519 -out private.pem
openssl pkey -in private.pem -pubout -out public.pem
```

Expected output: Two files — `private.pem` (keep secret) and `public.pem`.

### Step 2: Register the public key

1. Go to [exchange.revolut.com](https://exchange.revolut.com/) -> Profile -> API Keys
2. Paste the full content of `public.pem` (including `-----BEGIN/END PUBLIC KEY-----` lines)
3. Copy the 64-character API key Revolut generates

### Step 3: Configure environment variables

```bash
export REVX_API_KEY='your-64-character-api-key'
export REVX_PRIVATE_KEY='/path/to/private.pem'
```

### Step 4: Verify authentication works

```bash
python scripts/revx_sign.py GET /api/1.0/balances
```

Expected output: JSON array of account balances. If you see this, auth is working.

## API versioning

All endpoints use path-based versioning: `/api/1.0/`. The version is included in every request path.

## Common workflows

### How request signing works

Every authenticated request needs three headers:

| Header | Value |
|---|---|
| `X-Revx-API-Key` | Your 64-character API key |
| `X-Revx-Timestamp` | Unix timestamp in **milliseconds** |
| `X-Revx-Signature` | Base64-encoded Ed25519 signature |

Message to sign (concatenate with **no separators**):

```
{timestamp}{HTTP_METHOD}{/api/path}{query_string}{json_body}
```

The `scripts/revx_sign.py` helper handles all of this automatically. For manual implementation details, see `references/signing-examples.md`.

### Example 1: First-time setup
User says: "Help me set up Revolut X API access"

Actions:
1. Run `openssl genpkey -algorithm ed25519 -out private.pem`
2. Run `openssl pkey -in private.pem -pubout -out public.pem`
3. Ask the user to register the public key at exchange.revolut.com
4. Set env vars: `REVX_API_KEY` and `REVX_PRIVATE_KEY`
5. Verify with `python scripts/revx_sign.py GET /api/1.0/balances`

Result: Authenticated API access confirmed.

### Example 2: Debug a 401 error
User says: "I'm getting 401 errors from Revolut X"

Actions:
1. Check `echo $REVX_API_KEY` — should be 64 chars
2. Check `echo $REVX_PRIVATE_KEY` — file should exist
3. Verify key matches: `openssl pkey -in $REVX_PRIVATE_KEY -pubout` should match registered key
4. Test: `python scripts/revx_sign.py GET /api/1.0/balances`

Result: Identify and fix the auth issue.

## Error handling

**Error: 401 Unauthorized**
Cause: Invalid API key or signature
Solution: Verify API key is correct, private key matches the registered public key, and system clock is accurate.

**Error: 403 Forbidden**
Cause: IP not whitelisted or insufficient permissions
Solution: Check API key settings in exchange.revolut.com.

**Error: 409 Conflict**
Cause: Timestamp skew — system clock is too far off
Solution: Sync system clock. Timestamp must be within a few seconds of server time.

## Important notes

- **Private keys are secret** — never share, commit, or include in requests
- Timestamp must be Unix epoch in **milliseconds**, not seconds
- JSON body in signature must use compact format (no spaces)
- For GET/DELETE without body, omit body from signature entirely
- Base URL: `https://revx.revolut.com/api/1.0`

## References

- [signing-examples.md](references/signing-examples.md) — Full Python and Node.js signing code
- [Revolut X REST API docs](https://developer.revolut.com/docs/x-api/revolut-x-crypto-exchange-rest-api)
- [Revolut OpenAPI spec](https://github.com/revolut-engineering/revolut-openapi)

## Related skills

| Skill | Purpose |
|---|---|
| `revolut-x-configuration` | Available currencies and trading pair constraints |
| `revolut-x-balance` | Check account balances |
| `revolut-x-orders` | Place and cancel orders |
| `revolut-x-trades` | View trade history and fills |
| `revolut-x-market-data` | Tickers, candles, order book (authenticated) |
| `revolut-x-public-market-data` | Public trades and order book (no auth required) |
