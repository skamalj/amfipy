"""
amfipy.nav — NAV data (Latest, History, Download).

Endpoints (base: https://www.amfiindia.com):
  GET /api/latest-nav?type=TYPE&mfid=MFID
  GET /api/latest-nav-category?mfid=MFID&type=TYPE
  GET /api/get-nav-history/navs?mf_id=ID          — scheme list for an AMC
  GET /api/nav-history?query_type=...&...          — historical NAV
  portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt=DD-Mon-YYYY

query_type values (actual API params):
  "all_for_date"       — all scheme NAVs on a date (from_date required)
  "historical_period"  — NAV history for a scheme (sd_id + from/to_date)
  "high_low_nav"       — high/low NAV (sd_id + from/to_date + period_type + nav_type)
  "compare_dates"      — compare NAV on two dates (sd_id + from_date + to_date)

high_low_nav params:
  period_type: "Month" | "Annual"
  nav_type:    "high" | "Low" | "Both"

schemes() response fields: nav_id, nav_name, MF_ID
Use nav_id as sd_id in history calls.

Date formats:
  from_date / to_date : "YYYY-MM-DD"
  frmdt (portal)      : "DD-Mon-YYYY" e.g. "31-Mar-2026"
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client, make_portal_client, make_portal_async_client
from ._utils import maybe_polars

_REFERER = "net-asset-value"
_LATEST_PATH = "/api/latest-nav"
_LATEST_CAT_PATH = "/api/latest-nav-category"
_SCHEME_LIST_PATH = "/api/get-nav-history/navs"
_HISTORY_PATH = "/api/nav-history"
_PORTAL_DOWNLOAD = "/DownloadNAVHistoryReport_Po.aspx"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class NAVClient:
    """Sync client for NAV data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    # -- Latest NAV ---------------------------------------------------------

    def latest(
        self,
        mf_id: str | int = "all",
        fund_type: str = "",
        as_df: bool = False,
    ) -> Any:
        """Fetch latest NAV for all (or one) AMC.

        Args:
            mf_id:     "all" or numeric AMC ID (e.g. 62 for 360 ONE).
            fund_type: ""=All | "Open Ended" | "Close Ended" | "Interval Fund"
            as_df:     Return polars DataFrame (requires ``pip install amfipy[polars]``).

        Returns:
            ``{"data": [{type, categories: [...]}], "count": N}``
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_LATEST_PATH, params={"mfid": str(mf_id), "type": fund_type})
            r.raise_for_status()
            return r.json()

    def latest_by_category(
        self,
        mf_id: str | int = "all",
        fund_type: str = "",
    ) -> dict:
        """Fetch latest NAV grouped by category."""
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_LATEST_CAT_PATH, params={"mfid": str(mf_id), "type": fund_type})
            r.raise_for_status()
            return r.json()

    # -- Scheme lookup ------------------------------------------------------

    def schemes(self, mf_id: int) -> list[dict]:
        """Return all schemes for a given AMC (by numeric ID).

        Returns list of ``{"nav_id": "154043", "nav_name": "Scheme Name", "MF_ID": "85"}``.
        Use ``nav_id`` as ``sd_id`` in history calls.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_SCHEME_LIST_PATH, params={"mf_id": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data.get("data", data) if isinstance(data, dict) else data

    # -- History ------------------------------------------------------------

    def all_navs_for_date(self, date: str, as_df: bool = False) -> Any:
        """All scheme NAVs as of a specific date.

        Args:
            date:  "YYYY-MM-DD" (e.g. "2026-03-31").
            as_df: Return polars DataFrame.

        Returns:
            List of AMC groups, each with ``schemes`` sub-list.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_HISTORY_PATH, params={"query_type": "all_for_date", "from_date": date})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def history(
        self,
        sd_id: int | str,
        from_date: str,
        to_date: str,
        as_df: bool = False,
    ) -> Any:
        """Historical NAV for a scheme over a date range.

        Args:
            sd_id:     Scheme ID (``nav_id`` from :meth:`schemes`).
            from_date: "YYYY-MM-DD"
            to_date:   "YYYY-MM-DD"
            as_df:     Return polars DataFrame.

        Returns:
            Dict with ``mf_name``, ``scheme_name``, ``date_range``, ``nav_groups``.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_HISTORY_PATH, params={
                "query_type": "historical_period",
                "sd_id": str(sd_id),
                "from_date": from_date,
                "to_date": to_date,
            })
            r.raise_for_status()
            data = r.json()
        inner = data.get("data", data) if isinstance(data, dict) else data
        if as_df:
            return _flatten_history_df(inner)
        return inner

    def high_low(
        self,
        sd_id: int | str,
        from_date: str,
        to_date: str,
        period_type: str = "Month",
        nav_type: str = "Both",
        as_df: bool = False,
    ) -> Any:
        """High/Low NAV for a scheme over a period.

        Args:
            sd_id:       Scheme ID.
            from_date:   "YYYY-MM-DD"
            to_date:     "YYYY-MM-DD"
            period_type: "Month" | "Annual"
            nav_type:    "high" | "Low" | "Both"
            as_df:       Return polars DataFrame.

        Returns:
            Dict with ``mf_name``, ``scheme_name``, ``date_range``, ``nav_data``, ``nav_type``.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_HISTORY_PATH, params={
                "query_type": "high_low_nav",
                "sd_id": str(sd_id),
                "from_date": from_date,
                "to_date": to_date,
                "period_type": period_type,
                "nav_type": nav_type,
            })
            r.raise_for_status()
            data = r.json()
        inner = data.get("data", data) if isinstance(data, dict) else data
        if as_df:
            rows = inner.get("nav_data", []) if isinstance(inner, dict) else inner
            if not isinstance(rows, list):
                rows = [rows]
            return maybe_polars(rows, as_df)
        return inner

    def compare(
        self,
        sd_id: int | str,
        date1: str,
        date2: str,
        as_df: bool = False,
    ) -> Any:
        """Compare NAV of a scheme on two dates.

        Args:
            sd_id:  Scheme ID.
            date1:  "YYYY-MM-DD" (from_date)
            date2:  "YYYY-MM-DD" (to_date)
            as_df:  Return polars DataFrame.

        Returns:
            Dict with ``mf_name``, ``scheme_name``, ``dates``, ``nav_comparisons``.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_HISTORY_PATH, params={
                "query_type": "compare_dates",
                "sd_id": str(sd_id),
                "from_date": date1,
                "to_date": date2,
            })
            r.raise_for_status()
            data = r.json()
        inner = data.get("data", data) if isinstance(data, dict) else data
        if as_df:
            rows = inner.get("nav_comparisons", []) if isinstance(inner, dict) else inner
            if not isinstance(rows, list):
                rows = [rows]
            return maybe_polars(rows, as_df)
        return inner

    # -- Bulk download ------------------------------------------------------

    def download_file(self, date: str) -> bytes:
        """Download the full NAV flat file for a date from AMFI portal.

        Returns raw bytes of the plain-text NAV file (same as the classic NAVAll.txt).

        Args:
            date: "DD-Mon-YYYY" e.g. "31-Mar-2026".

        Example::

            data = client.download_file("31-Mar-2026")
            Path("navs.txt").write_bytes(data)
        """
        with make_portal_client(**self._kw) as c:
            r = c.get(_PORTAL_DOWNLOAD, params={"frmdt": date})
            r.raise_for_status()
            return r.content

    def fetch_range(
        self,
        sd_id: int | str,
        months: list[tuple[str, str]],
        as_df: bool = False,
    ) -> list[Any]:
        """Fetch historical NAV for a scheme across multiple date ranges.

        Args:
            sd_id:  Scheme ID.
            months: List of ``(from_date, to_date)`` tuples, each "YYYY-MM-DD".
            as_df:  Return polars DataFrames.

        Returns list in same order as ``months``.
        """
        return [
            self.history(sd_id=sd_id, from_date=f, to_date=t, as_df=as_df)
            for f, t in months
        ]


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncNAVClient:
    """Async client for NAV data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def latest(self, mf_id: str | int = "all", fund_type: str = "") -> dict:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_LATEST_PATH, params={"mfid": str(mf_id), "type": fund_type})
            r.raise_for_status()
            return r.json()

    async def latest_by_category(self, mf_id: str | int = "all", fund_type: str = "") -> dict:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_LATEST_CAT_PATH, params={"mfid": str(mf_id), "type": fund_type})
            r.raise_for_status()
            return r.json()

    async def schemes(self, mf_id: int) -> list[dict]:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_SCHEME_LIST_PATH, params={"mf_id": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data.get("data", data) if isinstance(data, dict) else data

    async def all_navs_for_date(self, date: str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_HISTORY_PATH, params={"query_type": "all_for_date", "from_date": date})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def history(
        self, sd_id: int | str, from_date: str, to_date: str, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_HISTORY_PATH, params={
                "query_type": "historical_period",
                "sd_id": str(sd_id),
                "from_date": from_date,
                "to_date": to_date,
            })
            r.raise_for_status()
            data = r.json()
        inner = data.get("data", data) if isinstance(data, dict) else data
        if as_df:
            return _flatten_history_df(inner)
        return inner

    async def high_low(
        self, sd_id: int | str, from_date: str, to_date: str,
        period_type: str = "Month", nav_type: str = "Both", as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_HISTORY_PATH, params={
                "query_type": "high_low_nav",
                "sd_id": str(sd_id),
                "from_date": from_date,
                "to_date": to_date,
                "period_type": period_type,
                "nav_type": nav_type,
            })
            r.raise_for_status()
            data = r.json()
        inner = data.get("data", data) if isinstance(data, dict) else data
        if as_df:
            rows = inner.get("nav_data", []) if isinstance(inner, dict) else inner
            if not isinstance(rows, list):
                rows = [rows]
            return maybe_polars(rows, as_df)
        return inner

    async def compare(
        self, sd_id: int | str, date1: str, date2: str, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_HISTORY_PATH, params={
                "query_type": "compare_dates",
                "sd_id": str(sd_id),
                "from_date": date1,
                "to_date": date2,
            })
            r.raise_for_status()
            data = r.json()
        inner = data.get("data", data) if isinstance(data, dict) else data
        if as_df:
            rows = inner.get("nav_comparisons", []) if isinstance(inner, dict) else inner
            if not isinstance(rows, list):
                rows = [rows]
            return maybe_polars(rows, as_df)
        return inner

    async def download_file(self, date: str) -> bytes:
        async with make_portal_async_client(**self._kw) as c:
            r = await c.get(_PORTAL_DOWNLOAD, params={"frmdt": date})
            r.raise_for_status()
            return r.content

    async def fetch_range(
        self, sd_id: int | str, months: list[tuple[str, str]], as_df: bool = False
    ) -> list[Any]:
        import asyncio
        return list(await asyncio.gather(
            *[self.history(sd_id=sd_id, from_date=f, to_date=t, as_df=as_df) for f, t in months]
        ))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flatten_history_df(data: Any) -> Any:
    """Flatten historical_period response into a list of date+nav rows for polars."""
    rows = []
    if isinstance(data, dict):
        mf_name = data.get("mf_name", "")
        scheme_name = data.get("scheme_name", "")
        for group in data.get("nav_groups", []):
            nav_name = group.get("nav_name", "")
            for rec in group.get("historical_records", []):
                rows.append({
                    "mf_name": mf_name,
                    "scheme_name": scheme_name,
                    "nav_name": nav_name,
                    **rec,
                })
    return maybe_polars(rows, True)
