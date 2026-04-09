#!/usr/bin/env python3
"""
Revolut X API — Public (Unauthenticated) Request Helper

Usage:
  python scripts/revx_request.py GET /api/1.0/public/last-trades
  python scripts/revx_request.py GET /api/1.0/public/order-book/BTC-USD

No API keys required — these are public endpoints.

Optional:
  REVX_BASE_URL — defaults to https://revx.revolut.com
"""

import argparse
import json
import os
import sys

try:
    import httpx
except ImportError:
    sys.exit("Error: httpx not installed. Run: pip install httpx")


def main():
    parser = argparse.ArgumentParser(description="Revolut X public API request")
    parser.add_argument("method", choices=["GET"], help="HTTP method")
    parser.add_argument("path", help="API path, e.g. /api/1.0/public/last-trades")
    args = parser.parse_args()

    base_url = os.environ.get("REVX_BASE_URL", "https://revx.revolut.com")
    url = f"{base_url}{args.path}"

    resp = httpx.get(url)
    print(json.dumps(resp.json(), indent=2))
    if resp.status_code >= 400:
        sys.exit(1)


if __name__ == "__main__":
    main()
