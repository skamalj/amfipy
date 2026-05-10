"""
amfipy.risk_parameters — Disclosure of Risk Parameters.

Endpoint (GET, base: https://www.amfiindia.com):
  /api/risk-parameter-data-revised?date=01-Mar-2026&strCatId=17

Param reference:
  date     : "01-Mon-YYYY" (always day=01, e.g. "01-Mar-2026")
  strCatId : numeric category ID (e.g. 17=Mid Cap Fund)

Note: Category IDs are numeric and not documented by AMFI. Known value: 17=Mid Cap Fund.
      Fetch all available categories from the page or enumerate empirically.
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER = "risk-parameters"
_DATA_PATH = "/api/risk-parameter-data-revised"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class RiskParametersClient:
    """Sync client for Risk Parameters data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def fetch(
        self,
        date: str,
        category_id: int | str,
        as_df: bool = False,
    ) -> Any:
        """Fetch risk parameter data.

        Args:
            date:        "01-Mon-YYYY" e.g. "01-Mar-2026". Always use day=01.
            category_id: Numeric category ID (e.g. 17 for Mid Cap Fund).
            as_df:       Return polars DataFrame.

        Returns:
            Risk parameter data (standard deviation, beta, Sharpe ratio, etc.)
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_DATA_PATH, params={"date": date, "strCatId": str(category_id)})
            r.raise_for_status()
            data = r.json()

        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def fetch_range(
        self,
        dates: list[str],
        category_id: int | str,
        as_df: bool = False,
    ) -> dict[str, Any]:
        """Fetch risk parameters for multiple months.

        Returns ``{"01-Mar-2026": <data>, ...}``.
        """
        return {d: self.fetch(date=d, category_id=category_id, as_df=as_df) for d in dates}


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncRiskParametersClient:
    """Async client for Risk Parameters data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def fetch(self, date: str, category_id: int | str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_DATA_PATH, params={"date": date, "strCatId": str(category_id)})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def fetch_range(
        self, dates: list[str], category_id: int | str, as_df: bool = False
    ) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(*[self.fetch(d, category_id, as_df) for d in dates])
        return dict(zip(dates, results))
