#!/usr/bin/env python3
"""
Revolut X API — Signed Request Helper

Usage:
  python scripts/revx_sign.py GET /api/1.0/balances
  python scripts/revx_sign.py GET /api/1.0/orders/active --query '?symbols=BTC-USD'
  python scripts/revx_sign.py POST /api/1.0/orders --body '{"client_order_id":"...","symbol":"BTC-USD","side":"buy","order_configuration":{"market":{"quote_size":"100"}}}'
  python scripts/revx_sign.py DELETE /api/1.0/orders/ORDER_ID

Environment variables (required):
  REVX_API_KEY       — 64-character API key from exchange.revolut.com
  REVX_PRIVATE_KEY   — path to Ed25519 private key PEM file

Optional:
  REVX_BASE_URL      — defaults to https://revx.revolut.com
"""

import argparse
import base64
import json
import os
import sys
import time

try:
    import httpx
except ImportError:
    sys.exit("Error: httpx not installed. Run: pip install httpx")

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
except ImportError:
    sys.exit("Error: cryptography not installed. Run: pip install cryptography")

try:
    from nacl.signing import SigningKey
except ImportError:
    sys.exit("Error: PyNaCl not installed. Run: pip install pynacl")


def load_signing_key(private_key_path: str) -> SigningKey:
    pem_data = open(private_key_path, "rb").read()
    private_key_obj = serialization.load_pem_private_key(
        pem_data, password=None, backend=default_backend()
    )
    raw_private = private_key_obj.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return SigningKey(raw_private)


def sign_request(
    signing_key: SigningKey,
    api_key: str,
    method: str,
    path: str,
    query: str = "",
    body: dict | None = None,
) -> dict:
    timestamp = str(int(time.time() * 1000))
    body_str = json.dumps(body, separators=(",", ":")) if body else ""
    message = f"{timestamp}{method.upper()}{path}{query}{body_str}".encode()
    signed = signing_key.sign(message)
    signature = base64.b64encode(signed.signature).decode()
    return {
        "X-Revx-API-Key": api_key,
        "X-Revx-Timestamp": timestamp,
        "X-Revx-Signature": signature,
        "Content-Type": "application/json",
    }


def main():
    parser = argparse.ArgumentParser(description="Revolut X signed API request")
    parser.add_argument("method", choices=["GET", "POST", "DELETE"], help="HTTP method")
    parser.add_argument("path", help="API path, e.g. /api/1.0/balances")
    parser.add_argument("--query", default="", help="Query string with leading ?, e.g. '?symbols=BTC-USD'")
    parser.add_argument("--body", default=None, help="JSON request body (for POST)")
    args = parser.parse_args()

    api_key = os.environ.get("REVX_API_KEY")
    private_key_path = os.environ.get("REVX_PRIVATE_KEY")
    base_url = os.environ.get("REVX_BASE_URL", "https://revx.revolut.com")

    if not api_key:
        sys.exit("Error: REVX_API_KEY environment variable not set.\n"
                 "Set it: export REVX_API_KEY='your-64-char-key'")
    if not private_key_path:
        sys.exit("Error: REVX_PRIVATE_KEY environment variable not set.\n"
                 "Set it: export REVX_PRIVATE_KEY='/path/to/private.pem'")
    if not os.path.exists(private_key_path):
        sys.exit(f"Error: Private key file not found: {private_key_path}")

    signing_key = load_signing_key(private_key_path)
    body = json.loads(args.body) if args.body else None
    headers = sign_request(signing_key, api_key, args.method, args.path, args.query, body)

    url = f"{base_url}{args.path}{args.query}"

    if args.method == "GET":
        resp = httpx.get(url, headers=headers)
    elif args.method == "POST":
        resp = httpx.post(url, headers=headers, json=body)
    elif args.method == "DELETE":
        resp = httpx.delete(url, headers=headers)

    print(json.dumps(resp.json(), indent=2))
    if resp.status_code >= 400:
        sys.exit(1)


if __name__ == "__main__":
    main()
