"""
amfipy.tracking — Tracking Error and Tracking Difference.

Endpoints (all GET, base: https://www.amfiindia.com):
  /api/tracking-error-data?MF_ID=all&strdt=31-mar-2026
  /api/tracking-difference?MF_ID=all&date=01-Apr-2026

Date formats:
  tracking_error:      strdt="31-mar-2026"  (DD-mon-YYYY, lowercase month)
  tracking_difference: date="01-Apr-2026"   (DD-Mon-YYYY, title-case month)
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER = "otherdata/tracking-error"
_ERROR_PATH = "/api/tracking-error-data"
_DIFF_PATH = "/api/tracking-difference"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class TrackingClient:
    """Sync client for Tracking Error and Tracking Difference data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def error(
        self,
        date: str,
        mf_id: str | int = "all",
        as_df: bool = False,
    ) -> Any:
        """Fetch tracking error data.

        Args:
            date:   Date in "DD-mon-YYYY" format (lowercase month),
                    e.g. "31-mar-2026".
            mf_id:  "all" or numeric fund ID.
            as_df:  Return polars DataFrame.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_ERROR_PATH, params={"MF_ID": str(mf_id), "strdt": date})
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def difference(
        self,
        month: str,
        mf_id: str | int = "all",
        as_df: bool = False,
    ) -> Any:
        """Fetch tracking difference data.

        Args:
            month:  Month in "01-Apr-2026" format (DD-Mon-YYYY, title-case month).
                    Always use day=01.
            mf_id:  "all" or numeric fund ID.
            as_df:  Return polars DataFrame.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_DIFF_PATH, params={"MF_ID": str(mf_id), "date": month})
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def error_range(
        self,
        dates: list[str],
        mf_id: str | int = "all",
        as_df: bool = False,
    ) -> dict[str, Any]:
        """Fetch tracking error for multiple dates.

        Returns ``{"31-mar-2026": <data>, ...}``.
        """
        return {d: self.error(date=d, mf_id=mf_id, as_df=as_df) for d in dates}

    def difference_range(
        self,
        months: list[str],
        mf_id: str | int = "all",
        as_df: bool = False,
    ) -> dict[str, Any]:
        """Fetch tracking difference for multiple months."""
        return {m: self.difference(month=m, mf_id=mf_id, as_df=as_df) for m in months}


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncTrackingClient:
    """Async client for Tracking Error and Tracking Difference data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def error(self, date: str, mf_id: str | int = "all", as_df: bool = False) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_ERROR_PATH, params={"MF_ID": str(mf_id), "strdt": date})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def difference(self, month: str, mf_id: str | int = "all", as_df: bool = False) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_DIFF_PATH, params={"MF_ID": str(mf_id), "date": month})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def error_range(
        self, dates: list[str], mf_id: str | int = "all", as_df: bool = False
    ) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(*[self.error(d, mf_id, as_df) for d in dates])
        return dict(zip(dates, results))

    async def difference_range(
        self, months: list[str], mf_id: str | int = "all", as_df: bool = False
    ) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(*[self.difference(m, mf_id, as_df) for m in months])
        return dict(zip(months, results))
