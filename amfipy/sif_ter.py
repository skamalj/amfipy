"""
amfipy.sif_ter — TER data for SIF (Specialized Investment Fund) Schemes.

Mirrors amfipy.ter but uses sif-prefixed endpoints and SIF_Id parameter.

Endpoints (all GET, base: https://www.amfiindia.com):
  /api/sif-populate-ter-month?year=YYYY-YYYY
  /api/sif-populate-sub-category?type=TYPE&category=CAT
  /api/sif-populate-te-rdata-revised?SIF_Id=&Month=&strCat=&strType=[&excel=true]
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER = "ter-of-mf-schemes"
_MONTH_PATH = "/api/sif-populate-ter-month"
_SUBCAT_PATH = "/api/sif-populate-sub-category"
_DATA_PATH = "/api/sif-populate-te-rdata-revised"

ALL = "All"
ALL_CAT = "-1"
ALL_TYPE = "-1"


class SIFTERClient:
    """Sync client for SIF TER data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def months(self, year: str = "2025-2026") -> list[dict]:
        """Return available months for a financial year."""
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_MONTH_PATH, params={"year": year})
            r.raise_for_status()
            return r.json()

    def sub_categories(self, fund_type: str = ALL_TYPE, category: str = ALL_CAT) -> list[dict]:
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_SUBCAT_PATH, params={"type": fund_type, "category": category})
            r.raise_for_status()
            return r.json()

    def fetch(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        sif_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> Any:
        """Fetch SIF TER data.

        Args:
            month:     MM-YYYY. Defaults to latest available month.
            year:      Financial year for month lookup (when month=None).
            sif_id:    "All" or numeric SIF fund ID.
            category:  "-1"=All | "Equity Scheme" | "Debt Scheme" | etc.
            fund_type: "-1"=All | "Open Ended" | "Close Ended" | "Interval Fund"
            as_df:     Return polars DataFrame (requires ``pip install amfipy[polars]``).
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
                params={"SIF_Id": str(sif_id), "Month": month, "strCat": category, "strType": fund_type},
            )
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        return maybe_polars(records if isinstance(records, list) else [records], as_df)

    def fetch_range(
        self,
        months: list[str],
        sif_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> dict[str, Any]:
        return {
            m: self.fetch(month=m, sif_id=sif_id, category=category, fund_type=fund_type, as_df=as_df)
            for m in months
        }

    def download_excel(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        sif_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
    ) -> bytes:
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
                    "SIF_Id": str(sif_id),
                    "Month": month,
                    "strCat": category,
                    "strType": fund_type,
                    "excel": "true",
                },
            )
            r.raise_for_status()
            return r.content


class AsyncSIFTERClient:
    """Async client for SIF TER data."""

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
        sif_id: str | int = ALL,
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
                params={"SIF_Id": str(sif_id), "Month": month, "strCat": category, "strType": fund_type},
            )
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        return maybe_polars(records if isinstance(records, list) else [records], as_df)

    async def fetch_range(
        self,
        months: list[str],
        sif_id: str | int = ALL,
        category: str = ALL_CAT,
        fund_type: str = ALL_TYPE,
        as_df: bool = False,
    ) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(
            *[self.fetch(month=m, sif_id=sif_id, category=category, fund_type=fund_type, as_df=as_df) for m in months]
        )
        return dict(zip(months, results))

    async def download_excel(
        self,
        month: str | None = None,
        year: str = "2025-2026",
        sif_id: str | int = ALL,
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
                    "SIF_Id": str(sif_id),
                    "Month": month,
                    "strCat": category,
                    "strType": fund_type,
                    "excel": "true",
                },
            )
            r.raise_for_status()
            return r.content
