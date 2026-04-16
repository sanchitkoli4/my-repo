#!/usr/bin/env python3
"""Simple health check utility.

Usage:
  python health_check.py              # checks http://localhost:8000/index.html
  python health_check.py --url http://example.com
"""
import argparse
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

DEFAULT_URL = "http://localhost:8000/index.html"


def check(url: str, timeout: float = 5.0) -> int:
    req = Request(url, headers={"User-Agent": "health-check/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", None) or resp.getcode()
            content = resp.read(1024)
            # print a short preview (safe bytes -> str)
            try:
                preview = content.decode("utf-8", errors="replace")
            except Exception:
                preview = str(content)
            print(f"URL: {url}")
            print(f"Status: {status}")
            print("--- Response preview ---")
            print(preview[:1000])
            print("--- end preview ---")
            return int(status)
    except HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        return e.code or 0
    except URLError as e:
        print(f"URL error: {e.reason}")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Health check for a URL (no external deps)")
    p.add_argument("--url", "-u", default=DEFAULT_URL, help="URL to check")
    p.add_argument("--timeout", "-t", type=float, default=5.0, help="Request timeout seconds")
    args = p.parse_args(argv)

    code = check(args.url, timeout=args.timeout)
    # exit code 0 for success (200-399), non-zero otherwise
    if 200 <= code < 400:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
