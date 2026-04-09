# Revolut X — Authentication Code Examples

## Request Signing Overview

Every authenticated request requires three headers:

| Header | Value |
|---|---|
| `X-Revx-API-Key` | Your 64-char API key |
| `X-Revx-Timestamp` | Unix timestamp in **milliseconds** |
| `X-Revx-Signature` | Base64-encoded Ed25519 signature |

### Message to Sign (no separators between parts):
```
{timestamp}{HTTP_METHOD}{/api/path}{query_string}{json_body}
```

---

## Python Example

```python
import base64
import time
import json
import httpx
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from nacl.signing import SigningKey

# Load private key
pem_data = Path("private.pem").read_bytes()
private_key_obj = serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())
raw_private = private_key_obj.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)
signing_key = SigningKey(raw_private)

API_KEY = "YOUR_64_CHAR_API_KEY"
BASE_URL = "https://revx.revolut.com"  # signing path starts from /api/1.0

def sign_request(method: str, path: str, query: str = "", body: dict = None) -> dict:
    timestamp = str(int(time.time() * 1000))
    body_str = json.dumps(body, separators=(',', ':')) if body else ""
    # path must start from /api (e.g. /api/1.0/orders) — no separators between fields
    message = f"{timestamp}{method.upper()}{path}{query}{body_str}".encode()
    signed = signing_key.sign(message)
    signature = base64.b64encode(signed.signature).decode()
    return {
        "X-Revx-API-Key": API_KEY,
        "X-Revx-Timestamp": timestamp,
        "X-Revx-Signature": signature,
        "Content-Type": "application/json",
    }

# Example: Get balances
def get_balances():
    path = "/api/1.0/balances"
    headers = sign_request("GET", path)
    resp = httpx.get(BASE_URL + path, headers=headers)
    return resp.json()

# Example: Place a limit order
def place_limit_order(symbol: str, side: str, size: str, price: str):
    path = "/api/1.0/orders"
    body = {
        "client_order_id": "my-order-001",
        "symbol": symbol,
        "side": side.upper(),
        "order_configuration": {
            "limit": {
                "base_size": size,
                "price": price,
            }
        }
    }
    headers = sign_request("POST", path, body=body)
    resp = httpx.post(BASE_URL + path, headers=headers, json=body)
    return resp.json()

# Example: Get active orders
def get_active_orders():
    path = "/api/1.0/orders/active"
    headers = sign_request("GET", path)
    resp = httpx.get(BASE_URL + path, headers=headers)
    return resp.json()
```

---

## Node.js Example

```javascript
const crypto = require('crypto');
const fs = require('fs');

const API_KEY = 'YOUR_64_CHAR_API_KEY';
const PRIVATE_KEY = fs.readFileSync('private.pem', 'utf8');
const BASE_URL = 'https://revx.revolut.com';  // signing path starts from /api/1.0

function signRequest(method, path, query = '', body = null) {
  const timestamp = Date.now().toString();
  const bodyStr = body ? JSON.stringify(body) : '';
  // path must start from /api (e.g. /api/1.0/orders) — no separators between fields
  const message = `${timestamp}${method.toUpperCase()}${path}${query}${bodyStr}`;
  const signature = crypto.sign(null, Buffer.from(message), PRIVATE_KEY).toString('base64');
  return {
    'X-Revx-API-Key': API_KEY,
    'X-Revx-Timestamp': timestamp,
    'X-Revx-Signature': signature,
    'Content-Type': 'application/json',
  };
}

// Example: Place market buy order
async function placeMarketOrder(symbol, side, quoteSize) {
  const path = '/api/1.0/orders';
  const body = {
    client_order_id: `order-${Date.now()}`,
    symbol,
    side: side.toUpperCase(),
    order_configuration: {
      market: { quote_size: quoteSize }
    }
  };
  const headers = signRequest('POST', path, '', body);
  const res = await fetch(BASE_URL + path, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
  return res.json();
}

// Example: Cancel an order
async function cancelOrder(orderId) {
  const path = `/api/1.0/orders/${orderId}`;
  const headers = signRequest('DELETE', path);
  const res = await fetch(BASE_URL + path, { method: 'DELETE', headers });
  return res.json();
}
```

---

## Signing Edge Cases

- **Empty body (GET/DELETE):** omit body from the message entirely — do not include `""` or `null`
- **GET with query params:** include the full query string with leading `?` in the message, e.g. `?symbols=BTC-USD,ETH-USD`
- **POST with body:** use compact JSON — `json.dumps(body, separators=(',', ':'))` in Python, `JSON.stringify(body)` in Node.js
- **Timestamp:** must be Unix epoch in milliseconds, not seconds

---

## Key API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/1.0/balances` | GET | Yes | Account balances |
| `/api/1.0/orders` | POST | Yes | Place an order (limit: 1000/day for limit orders) |
| `/api/1.0/orders` | DELETE | Yes | Cancel **all** active orders |
| `/api/1.0/orders/active` | GET | Yes | List active orders |
| `/api/1.0/orders/historical` | GET | Yes | Historical orders (paginated) |
| `/api/1.0/orders/{venue_order_id}` | GET | Yes | Get order by ID |
| `/api/1.0/orders/{venue_order_id}` | DELETE | Yes | Cancel order by ID |
| `/api/1.0/orders/fills/{venue_order_id}` | GET | Yes | Get fills for an order |
| `/api/1.0/trades/all/{symbol}` | GET | Yes | All public trades for a symbol (paginated) |
| `/api/1.0/trades/private/{symbol}` | GET | Yes | Client trade history (paginated) |
| `/api/1.0/order-book/{symbol}` | GET | Yes | Order book (up to 20 levels) |
| `/api/1.0/candles/{symbol}` | GET | Yes | OHLCV candles |
| `/api/1.0/tickers` | GET | Yes | All tickers (bid/ask/mid/last) |
| `/api/1.0/configuration/currencies` | GET | Yes | Available currencies |
| `/api/1.0/configuration/pairs` | GET | Yes | Tradeable pairs with size constraints |
| `/api/1.0/public/last-trades` | GET | No | Latest 100 trades across all pairs |
| `/api/1.0/public/order-book/{symbol}` | GET | No | Order book snapshot, max 5 levels |

Base URL: `https://revx.revolut.com/api/1.0`
