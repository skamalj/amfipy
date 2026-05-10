"""
amfipy.research — AMFI Research & Information data.

Covers pages that serve data via Next.js RSC (React Server Components) payloads
rather than standalone JSON APIs.  Each method fetches the page once with an RSC
header and extracts the embedded JSON from the response stream.

Pages covered:
  /otherdata/categorisation-of-stocks
      Avg. Market Capitalisation of listed companies, grouped by year.
      ``stockData`` key → {year: [{period, pdfUrl, excelUrl}]}

Note on Benchmark Indices:
  The AMFI website has no accessible JSON API or RSC endpoint for benchmark
  index tables.  The ``Benchmark`` column that appears in tracking-error data
  (see ``client.tracking.error()``) is the closest available data.
"""
from __future__ import annotations

import json
from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_RSC_HEADERS = {
    "RSC": "1",
    "Next-Router-State-Tree": "%5B%22%22%2C%7B%7D%5D",
    "Accept": "text/html, */*",
}

_CATEG_PATH = "/otherdata/categorisation-of-stocks"
_REFERER_CATEG = "otherdata/categorisation-of-stocks"


def _extract_rsc_key(content: str, key: str) -> Any:
    """Extract a JSON value following ``"key":`` in an RSC payload."""
    marker = f'"{key}":'
    idx = content.find(marker)
    if idx == -1:
        raise ValueError(f"Key '{key}' not found in RSC payload")
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(content, idx + len(marker))
    return obj


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class ResearchClient:
    """Sync client for AMFI Research & Information pages.

    Data is embedded in the page via Next.js RSC (React Server Components)
    and is extracted from the RSC payload on each request.
    """

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def categorisation_of_stocks(self, as_df: bool = False) -> Any:
        """Fetch Avg. Market Capitalisation data (Categorisation of Stocks).

        Data is published bi-annually (Jan–Jun, Jul–Dec) from 2017 onwards.
        Each entry contains PDF and Excel download links.

        Returns:
            Dict keyed by year string (e.g. ``"2024"``), each value a list of::

                {"period": "Jul - Dec",
                 "pdfUrl": "https://...",
                 "excelUrl": "https://..."}

            With ``as_df=True``, returns a flat polars DataFrame with columns
            ``year``, ``period``, ``pdfUrl``, ``excelUrl``.

        Example::

            data = client.research.categorisation_of_stocks()
            # data["2024"] → [{"period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}]

            # Flat list
            flat = client.research.categorisation_of_stocks_flat()
        """
        headers = {**_RSC_HEADERS, "Referer": f"https://www.amfiindia.com/{_REFERER_CATEG}"}
        with make_client(_REFERER_CATEG, **self._kw) as c:
            r = c.get(_CATEG_PATH, headers=headers)
            r.raise_for_status()
        data = _extract_rsc_key(r.text, "stockData")
        if as_df:
            rows = [
                {"year": yr, "period": item["period"],
                 "pdfUrl": item.get("pdfUrl", ""), "excelUrl": item.get("excelUrl", "")}
                for yr, items in data.items()
                for item in items
            ]
            return maybe_polars(rows, True)
        return data

    def categorisation_of_stocks_flat(self) -> list[dict]:
        """Return categorisation data as a flat list ordered by year/period.

        Each item: ``{"year": "2024", "period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}``.
        """
        data = self.categorisation_of_stocks()
        rows = []
        for yr in sorted(data.keys()):
            for item in data[yr]:
                rows.append({"year": yr, **item})
        return rows

    def download_categorisation_file(self, url: str) -> bytes:
        """Download a categorisation PDF or Excel file.

        Args:
            url: Full URL from ``pdfUrl`` or ``excelUrl`` field.

        Returns:
            Raw file bytes.

        Example::

            flat = client.research.categorisation_of_stocks_flat()
            pdf = client.research.download_categorisation_file(flat[-1]["pdfUrl"])
            open("categ_latest.pdf", "wb").write(pdf)
        """
        import httpx as _httpx
        r = _httpx.get(url, headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }, follow_redirects=True, timeout=120)
        r.raise_for_status()
        return r.content


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncResearchClient:
    """Async client for AMFI Research & Information pages."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def categorisation_of_stocks(self, as_df: bool = False) -> Any:
        headers = {**_RSC_HEADERS, "Referer": f"https://www.amfiindia.com/{_REFERER_CATEG}"}
        async with make_async_client(_REFERER_CATEG, **self._kw) as c:
            r = await c.get(_CATEG_PATH, headers=headers)
            r.raise_for_status()
        data = _extract_rsc_key(r.text, "stockData")
        if as_df:
            rows = [
                {"year": yr, "period": item["period"],
                 "pdfUrl": item.get("pdfUrl", ""), "excelUrl": item.get("excelUrl", "")}
                for yr, items in data.items()
                for item in items
            ]
            return maybe_polars(rows, True)
        return data

    async def categorisation_of_stocks_flat(self) -> list[dict]:
        data = await self.categorisation_of_stocks()
        rows = []
        for yr in sorted(data.keys()):
            for item in data[yr]:
                rows.append({"year": yr, **item})
        return rows

    async def download_categorisation_file(self, url: str) -> bytes:
        import httpx as _httpx
        async with _httpx.AsyncClient(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            },
            follow_redirects=True,
            timeout=120,
        ) as client:
            r = await client.get(url)
            r.raise_for_status()
            return r.content
