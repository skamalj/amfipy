"""
amfipy.ter — TER (Total Expense Ratio) data for MF Schemes.

Endpoints (all GET, base: https://www.amfiindia.com):
  /api/populate-ter-month?year=YYYY-YYYY
  /api/populate-sub-category?type=TYPE&category=CAT
  /api/populate-te-rdata-revised?MF_ID=&Month=&strCat=&strType=[&excel=true]

Param reference:
  year    : "2025-2026"  (financial year)
  Month   : "03-2026"    (MM-YYYY — use months() to list available)
  MF_ID   : "All" or numeric e.g. 62
  strCat  : "-1"=All | "Equity Scheme" | "Debt Scheme" | "Hybrid Scheme"
            | "Other Scheme" | "Solution Oriented Scheme"
  strType : "-1"=All | "Open Ended" | "Close Ended" | "Interval Fund"
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER = "ter-of-mf-schemes"
_MONTH_PATH = "/api/populate-ter-month"
_SUBCAT_PATH = "/api/populate-sub-category"
_DATA_PATH = "/api/populate-te-rdata-revised"

ALL = "All"
ALL_CAT = "-1"
ALL_TYPE = "-1"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class TERClient:
    """Sync client for TER data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    # -- lookups ------------------------------------------------------------

    def months(self, year: str = "2025-2026") -> list[dict]:
        """Return available months for a financial year.

        Returns list of ``{"MonthYear": "March-2026", "MonthNumber": "03-2026"}``.
        First item is the most recent month.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_MONTH_PATH, params={"year": year})
            r.raise_for_status()
            return r.json()

    def sub_categories(self, fund_type: str = ALL_TYPE, category: str = ALL_CAT) -> list[dict]:
        """Return sub-categories for a given fund type and category."""
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_SUBCAT_PATH, params={"type": fund_type, "category": category})
            r.raise_for_status()
            return r.json()

    # -- data ---------------------------------------------------------------

    def fetch(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        mf_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> Any:
        """Fetch TER data as JSON (list of dicts) or polars DataFrame.

        Args:
            month:     MM-YYYY string. Defaults to latest available month.
            year:      Financial year for month lookup (only used when month=None).
            mf_id:     "All" or numeric MF ID.
            category:  "-1"=All | "Equity Scheme" | "Debt Scheme" | "Hybrid Scheme"
                       | "Other Scheme" | "Solution Oriented Scheme"
            fund_type: "-1"=All | "Open Ended" | "Close Ended" | "Interval Fund"
            as_df:     Return a polars DataFrame (requires ``pip install amfipy[polars]``).
        """
        with make_client(_REFERER, **self._kw) as c:
            if month is None:
                r = c.get(_MONTH_PATH, params={"year": year})
                r.raise_for_status()
                months = r.json()
                if not months:
                    raise ValueError(f"No months available for year {year}")
                month = months[0]["MonthNumber"]

            r = c.get(
                _DATA_PATH,
                params={"MF_ID": str(mf_id), "Month": month, "strCat": category, "strType": fund_type},
            )
            r.raise_for_status()
            data = r.json()

        # Normalise: API returns either a list or a dict with a data key
        records = data if isinstance(data, list) else data.get("data", data)
        return maybe_polars(records if isinstance(records, list) else [records], as_df)

    def fetch_range(
        self,
        months: list[str],
        mf_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> dict[str, Any]:
        """Fetch TER data for multiple months.

        Returns ``{"03-2026": <data>, "02-2026": <data>, ...}``.
        """
        return {
            m: self.fetch(month=m, mf_id=mf_id, category=category, fund_type=fund_type, as_df=as_df)
            for m in months
        }

    def download_excel(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        mf_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
    ) -> bytes:
        """Download TER data as raw Excel bytes.

        Example::

            data = client.download_excel(month="03-2026")
            Path("ter_march.xlsx").write_bytes(data)
        """
        with make_client(_REFERER, **self._kw) as c:
            if month is None:
                r = c.get(_MONTH_PATH, params={"year": year})
                r.raise_for_status()
                months_list = r.json()
                if not months_list:
                    raise ValueError(f"No months available for year {year}")
                month = months_list[0]["MonthNumber"]

            r = c.get(
                _DATA_PATH,
                params={
                    "MF_ID": str(mf_id),
                    "Month": month,
                    "strCat": category,
                    "strType": fund_type,
                    "excel": "true",
                },
            )
            r.raise_for_status()
            return r.content


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncTERClient:
    """Async client for TER data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def months(self, year: str = "2025-2026") -> list[dict]:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_MONTH_PATH, params={"year": year})
            r.raise_for_status()
            return r.json()

    async def sub_categories(self, fund_type: str = ALL_TYPE, category: str = ALL_CAT) -> list[dict]:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_SUBCAT_PATH, params={"type": fund_type, "category": category})
            r.raise_for_status()
            return r.json()

    async def fetch(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        mf_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            if month is None:
                r = await c.get(_MONTH_PATH, params={"year": year})
                r.raise_for_status()
                months_list = r.json()
                if not months_list:
                    raise ValueError(f"No months available for year {year}")
                month = months_list[0]["MonthNumber"]

            r = await c.get(
                _DATA_PATH,
                params={"MF_ID": str(mf_id), "Month": month, "strCat": category, "strType": fund_type},
            )
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        return maybe_polars(records if isinstance(records, list) else [records], as_df)

    async def fetch_range(
        self,
        months: list[str],
        mf_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(
            *[self.fetch(month=m, mf_id=mf_id, category=category, fund_type=fund_type, as_df=as_df) for m in months]
        )
        return dict(zip(months, results))

    async def download_excel(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        mf_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
    ) -> bytes:
        async with make_async_client(_REFERER, **self._kw) as c:
            if month is None:
                r = await c.get(_MONTH_PATH, params={"year": year})
                r.raise_for_status()
                months_list = r.json()
                if not months_list:
                    raise ValueError(f"No months available for year {year}")
                month = months_list[0]["MonthNumber"]

            r = await c.get(
                _DATA_PATH,
                params={
                    "MF_ID": str(mf_id),
                    "Month": month,
                    "strCat": category,
                    "strType": fund_type,
                    "excel": "true",
                },
            )
            r.raise_for_status()
            return r.content
