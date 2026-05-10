"""
amfipy.cdmdf — CDMDF (Corporate Debt Market Development Fund) NAV.

Endpoints (base: https://www.amfiindia.com):
  GET /api/cdmdf-nav-history?date=31-mar-2026   — historical CDMDF NAV

Note:
  Latest CDMDF NAV is server-rendered (embedded in the Next.js page HTML).
  Only the history endpoint has a clean JSON API.
  Date format: "DD-mon-YYYY" with lowercase month (e.g. "31-mar-2026").
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER = "net-asset-value/cdmdf-nav"
_HISTORY_PATH = "/api/cdmdf-nav-history"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class CDMDFClient:
    """Sync client for CDMDF NAV data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def history(self, date: str, as_df: bool = False) -> Any:
        """Fetch historical CDMDF NAV for a specific date.

        Args:
            date:   Date in "DD-mon-YYYY" format (lowercase month),
                    e.g. "31-mar-2026".
            as_df:  Return polars DataFrame.

        Returns:
            CDMDF NAV data for the given date.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_HISTORY_PATH, params={"date": date})
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def history_range(self, dates: list[str], as_df: bool = False) -> dict[str, Any]:
        """Fetch CDMDF NAV history for multiple dates.

        Returns ``{"31-mar-2026": <data>, "28-feb-2026": <data>, ...}``.
        """
        return {d: self.history(date=d, as_df=as_df) for d in dates}


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncCDMDFClient:
    """Async client for CDMDF NAV data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def history(self, date: str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_HISTORY_PATH, params={"date": date})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def history_range(self, dates: list[str], as_df: bool = False) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(*[self.history(d, as_df) for d in dates])
        return dict(zip(dates, results))
