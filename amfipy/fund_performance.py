"""
amfipy.fund_performance — Fund Performance data.

Uses a completely separate backend (gateway/pollingsebi), POST-based.

Endpoints (base: https://www.amfiindia.com/gateway/pollingsebi):
  POST /api/amfi/fundperformancefilters   — filter lists (no body needed)
  POST /api/amfi/getsubcategory           — body: {"category": <id>}
  POST /api/amfi/fundperformance          — body: see FundPerformanceRequest

Filter IDs (from /api/amfi/fundperformancefilters):
  maturityType : 1=Open Ended, 2=Close Ended
  category     : 1=Equity, 2=Debt, 3=Hybrid, 4=Solution Oriented, 5=Other
  subCategory  : dynamic — fetch via get_sub_categories(category)
  mfid         : 0=All, or fund ID from mutualFundList

Note:
  reportDate must be a valid business date in "DD-Mon-YYYY" format
  (e.g. "07-May-2026"). Excel export is client-side only; no server endpoint exists.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from ._client import make_polling_client, make_polling_async_client
from ._utils import maybe_polars

_REFERER = "otherdata/fund-performance"
_FILTERS_PATH = "/api/amfi/fundperformancefilters"
_SUBCAT_PATH = "/api/amfi/getsubcategory"
_PERFORMANCE_PATH = "/api/amfi/fundperformance"

MATURITY_OPEN = 1
MATURITY_CLOSE = 2

CATEGORY_EQUITY = 1
CATEGORY_DEBT = 2
CATEGORY_HYBRID = 3
CATEGORY_SOLUTION = 4
CATEGORY_OTHER = 5


def _last_business_date() -> str:
    d = date.today()
    if d.weekday() == 5:  # Saturday
        d -= timedelta(days=1)
    elif d.weekday() == 6:  # Sunday
        d -= timedelta(days=2)
    return d.strftime("%d-%b-%Y")


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class FundPerformanceClient:
    """Sync client for Fund Performance data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def filters(self) -> dict:
        """Fetch all filter options (maturity types, categories, fund list).

        Returns::

            {
              "maturityTypeList": [{"name": "Open Ended", "id": 1}, ...],
              "investmentTypeList": [{"name": "Equity", "id": 1}, ...],
              "mutualFundList": [{"name": "360 ONE Mutual Fund", "id": 1}, ...]
            }
        """
        with make_polling_client(_REFERER, **self._kw) as c:
            r = c.post(_FILTERS_PATH, json={})
            r.raise_for_status()
            resp = r.json()
            return resp.get("data", resp)

    def sub_categories(self, category: int) -> list[dict]:
        """Fetch sub-categories for a given category ID.

        Args:
            category: Category ID (1=Equity, 2=Debt, 3=Hybrid, 4=Solution Oriented, 5=Other)
        """
        with make_polling_client(_REFERER, **self._kw) as c:
            r = c.post(_SUBCAT_PATH, json={"category": category})
            r.raise_for_status()
            resp = r.json()
            return resp.get("data", resp)

    def fetch(
        self,
        maturity_type: int = MATURITY_OPEN,
        category: int = CATEGORY_EQUITY,
        sub_category: int = 1,
        mf_id: int = 0,
        report_date: str | None = None,
        as_df: bool = False,
    ) -> Any:
        """Fetch fund performance data.

        Args:
            maturity_type:  1=Open Ended, 2=Close Ended
            category:       1=Equity, 2=Debt, 3=Hybrid, 4=Solution Oriented, 5=Other
            sub_category:   Sub-category ID (fetch from :meth:`sub_categories`).
            mf_id:          0=All, or numeric mutual fund ID from :meth:`filters`.
            report_date:    "DD-Mon-YYYY" e.g. "07-May-2026". Defaults to last business day.
            as_df:          Return polars DataFrame (requires ``pip install amfipy[polars]``).

        Returns:
            List of scheme performance records (or polars DataFrame with ``as_df=True``).
        """
        if report_date is None:
            report_date = _last_business_date()

        body = {
            "maturityType": maturity_type,
            "category": category,
            "subCategory": sub_category,
            "mfid": mf_id,
            "reportDate": report_date,
        }
        with make_polling_client(_REFERER, **self._kw) as c:
            r = c.post(_PERFORMANCE_PATH, json=body)
            r.raise_for_status()
            resp = r.json()
        records = resp.get("data", resp)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncFundPerformanceClient:
    """Async client for Fund Performance data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def filters(self) -> dict:
        async with make_polling_async_client(_REFERER, **self._kw) as c:
            r = await c.post(_FILTERS_PATH, json={})
            r.raise_for_status()
            resp = r.json()
            return resp.get("data", resp)

    async def sub_categories(self, category: int) -> list[dict]:
        async with make_polling_async_client(_REFERER, **self._kw) as c:
            r = await c.post(_SUBCAT_PATH, json={"category": category})
            r.raise_for_status()
            resp = r.json()
            return resp.get("data", resp)

    async def fetch(
        self,
        maturity_type: int = MATURITY_OPEN,
        category: int = CATEGORY_EQUITY,
        sub_category: int = 1,
        mf_id: int = 0,
        report_date: str | None = None,
        as_df: bool = False,
    ) -> Any:
        if report_date is None:
            report_date = _last_business_date()

        body = {
            "maturityType": maturity_type,
            "category": category,
            "subCategory": sub_category,
            "mfid": mf_id,
            "reportDate": report_date,
        }
        async with make_polling_async_client(_REFERER, **self._kw) as c:
            r = await c.post(_PERFORMANCE_PATH, json=body)
            r.raise_for_status()
            resp = r.json()
        records = resp.get("data", resp)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)
