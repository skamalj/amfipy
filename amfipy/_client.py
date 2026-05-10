"""Shared HTTP client configuration for amfipy."""
from __future__ import annotations

import httpx

BASE_URL = "https://www.amfiindia.com"
PORTAL_URL = "https://portal.amfiindia.com"
POLLING_BASE = "https://www.amfiindia.com/gateway/pollingsebi"

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
}


def _headers(referer: str) -> dict[str, str]:
    return {**_DEFAULT_HEADERS, "Referer": f"{BASE_URL}/{referer.lstrip('/')}"}


def make_client(referer: str = "", **kwargs) -> httpx.Client:
    return httpx.Client(
        base_url=BASE_URL,
        headers=_headers(referer),
        timeout=60,
        follow_redirects=True,
        **kwargs,
    )


def make_async_client(referer: str = "", **kwargs) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=BASE_URL,
        headers=_headers(referer),
        timeout=60,
        follow_redirects=True,
        **kwargs,
    )


def make_polling_client(referer: str = "otherdata/fund-performance", **kwargs) -> httpx.Client:
    return httpx.Client(
        base_url=POLLING_BASE,
        headers=_headers(referer),
        timeout=60,
        follow_redirects=True,
        **kwargs,
    )


def make_polling_async_client(referer: str = "otherdata/fund-performance", **kwargs) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=POLLING_BASE,
        headers=_headers(referer),
        timeout=60,
        follow_redirects=True,
        **kwargs,
    )


def make_portal_client(**kwargs) -> httpx.Client:
    return httpx.Client(
        base_url=PORTAL_URL,
        headers=_DEFAULT_HEADERS,
        timeout=120,
        follow_redirects=True,
        **kwargs,
    )


def make_portal_async_client(**kwargs) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=PORTAL_URL,
        headers=_DEFAULT_HEADERS,
        timeout=120,
        follow_redirects=True,
        **kwargs,
    )
