"""
amfipy.aum — AUM (Assets Under Management) data.

Five sub-modules, each corresponding to an AMFI AUM page:

1. Average AUM  (/aum-data/average-aum)
   Fund-wise:
     GET /api/average-aum-fundwise                         — list financial years
     GET /api/average-aum-fundwise?fyId=<id>               — list periods
     GET /api/average-aum-fundwise?fyId=<id>&periodId=<id> — fund-wise data
   Scheme-wise (Categorywise | Typewise):
     GET /api/average-aum-schemewise?strType=<type>
     GET /api/average-aum-schemewise?strType=<type>&fyId=<id>
     GET /api/average-aum-schemewise?strType=<type>&fyId=<id>&periodId=<id>&MF_ID=<id>
   Excel append: &excel=true to any data endpoint

2. AUM–AAUM Disclosure  (/aum-data/aum-disclosure)
   GET /api/get-disclosure-category?fyId=<fy>       — quarterly disclosure by category
   GET /api/get-disclosureby-geography?fyId=<fy>    — quarterly disclosure by geography
   fyId uses string format: "2025-26", "2024-25", etc.

3. Age-wise / Folio Data  (/aum-data/age-wise-folio-data)
   GET /api/aum-agewise-folio-report?Month=<month>  — age-wise AUM + folio data
   Month format: "March-2026" (MonthName-YYYY)
   Excel: ?Month=<month>&excel=true

4. Classified Average AUM  (/aum-data/classified-average-aum)
   State-wise:
     GET /api/statewise-data?MF_ID=<id>&date=<date>
   Scheme-category-wise:
     GET /api/scheme-catwise-data?MF_ID=<id>&date=<date>
   Date format: "01-mon-yyyy" (lowercase month, always day=01)
   e.g. "01-apr-2026", "01-mar-2026"
   Excel: append &excel=true

5. Bifurcation of AUM  (/aum-data/bifurcation-of-aum)
   GET /api/bifurcationaumdata?strdt=<date>          — bifurcation data
   Date format: "DD-Mon-YYYY" e.g. "31-Mar-2026"
   Excel: ?strdt=<date>&excel=true
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER_AVG = "aum-data/average-aum"
_REFERER_DISC = "aum-data/aum-disclosure"
_REFERER_AGE = "aum-data/age-wise-folio-data"
_REFERER_CLASS = "aum-data/classified-average-aum"
_REFERER_BIF = "aum-data/bifurcation-of-aum"

_AVG_FUNDWISE = "/api/average-aum-fundwise"
_AVG_SCHEMEWISE = "/api/average-aum-schemewise"
_DISC_CATEGORY = "/api/get-disclosure-category"
_DISC_GEOGRAPHY = "/api/get-disclosureby-geography"
_AGE_FOLIO = "/api/aum-agewise-folio-report"
_STATEWISE = "/api/statewise-data"
_CATWISE = "/api/scheme-catwise-data"
_BIF = "/api/bifurcationaumdata"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class AUMClient:
    """Sync client for AUM data (all five sub-modules)."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    # -- Average AUM: Fund-wise ---------------------------------------------

    def financial_years(self) -> list[dict]:
        """List available financial years for Average AUM.

        Returns:
            ``[{"id": 1, "financial_year": "April 2025 - March 2026"}, ...]``
        """
        with make_client(_REFERER_AVG, **self._kw) as c:
            r = c.get(_AVG_FUNDWISE)
            r.raise_for_status()
            data = r.json()
        return data.get("data", data) if isinstance(data, dict) else data

    def periods(self, fy_id: int) -> dict:
        """List periods within a financial year for Average AUM.

        Args:
            fy_id: Financial year ID from :meth:`financial_years`.

        Returns:
            ``{"financial_year": "...", "periods": [{"id": 1, "period": "January - March 2026"}, ...]}``
        """
        with make_client(_REFERER_AVG, **self._kw) as c:
            r = c.get(_AVG_FUNDWISE, params={"fyId": fy_id})
            r.raise_for_status()
            data = r.json()
        return data.get("data", data) if isinstance(data, dict) else data

    def average_aum_fundwise(
        self,
        fy_id: int,
        period_id: int,
        as_df: bool = False,
    ) -> Any:
        """Fetch fund-wise Average AUM for a given quarter.

        Args:
            fy_id:     Financial year ID (from :meth:`financial_years`).
            period_id: Period ID (from :meth:`periods`).
            as_df:     Return polars DataFrame.

        Returns:
            List of fund records with ``MutualFundName`` and ``averageAUM``.
        """
        with make_client(_REFERER_AVG, **self._kw) as c:
            r = c.get(_AVG_FUNDWISE, params={"fyId": fy_id, "periodId": period_id})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def average_aum_fundwise_excel(self, fy_id: int, period_id: int) -> bytes:
        """Download fund-wise Average AUM as Excel bytes."""
        with make_client(_REFERER_AVG, **self._kw) as c:
            r = c.get(_AVG_FUNDWISE, params={"fyId": fy_id, "periodId": period_id, "excel": "true"})
            r.raise_for_status()
            return r.content

    # -- Average AUM: Scheme-wise -------------------------------------------

    def average_aum_schemewise(
        self,
        fy_id: int,
        period_id: int,
        str_type: str = "Categorywise",
        mf_id: int | str = 0,
        as_df: bool = False,
    ) -> Any:
        """Fetch scheme-wise Average AUM for a given quarter.

        Args:
            fy_id:     Financial year ID (from :meth:`financial_years`).
            period_id: Period ID (from :meth:`periods`).
            str_type:  ``"Categorywise"`` | ``"Typewise"``
            mf_id:     AMC numeric ID; 0 = All.
            as_df:     Return polars DataFrame.

        Returns:
            List of scheme-category records with nested ``schemes`` data.
        """
        with make_client(_REFERER_AVG, **self._kw) as c:
            r = c.get(_AVG_SCHEMEWISE, params={
                "strType": str_type,
                "fyId": fy_id,
                "periodId": period_id,
                "MF_ID": str(mf_id),
            })
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def average_aum_schemewise_excel(
        self,
        fy_id: int,
        period_id: int,
        str_type: str = "Categorywise",
        mf_id: int | str = 0,
    ) -> bytes:
        """Download scheme-wise Average AUM as Excel bytes."""
        with make_client(_REFERER_AVG, **self._kw) as c:
            r = c.get(_AVG_SCHEMEWISE, params={
                "strType": str_type,
                "fyId": fy_id,
                "periodId": period_id,
                "MF_ID": str(mf_id),
                "excel": "true",
            })
            r.raise_for_status()
            return r.content

    # -- AUM–AAUM Disclosure ------------------------------------------------

    def disclosure_years(self) -> list[dict]:
        """List available financial years for AUM–AAUM Disclosure.

        Returns:
            ``[{"id": "2025-26", "title": "April 2025-March 2026"}, ...]``
        """
        with make_client(_REFERER_DISC, **self._kw) as c:
            r = c.get(_DISC_CATEGORY, params={"fyId": "2025-26"})
            r.raise_for_status()

        years = []
        from datetime import date
        current_year = date.today().year
        for y in range(current_year, 2020, -1):
            short = f"{str(y-1)[-2:]}-{str(y)[-2:]}" if y > 2000 else f"{y-1}-{y}"
            years.append({
                "id": f"{y-1}-{str(y)[-2:]}",
                "title": f"April {y-1}-March {y}",
            })
        return years

    def disclosure_by_category(self, fy_id: str, as_df: bool = False) -> Any:
        """Quarterly AUM disclosure by fund category.

        Args:
            fy_id: Financial year string, e.g. ``"2025-26"``.
            as_df: Return polars DataFrame.

        Returns:
            List of quarterly records with ``Period``, ``pdfURL``, ``excelURL``.
        """
        with make_client(_REFERER_DISC, **self._kw) as c:
            r = c.get(_DISC_CATEGORY, params={"fyId": fy_id})
            r.raise_for_status()
            data = r.json()
        groups = data.get("QuarterlyDisclosureAUMbyCategorywise", [])
        records = groups[0].get("data", []) if groups else []
        return maybe_polars(records, as_df)

    def disclosure_by_geography(self, fy_id: str, as_df: bool = False) -> Any:
        """Quarterly AUM disclosure by geography.

        Args:
            fy_id: Financial year string, e.g. ``"2025-26"``.
            as_df: Return polars DataFrame.

        Returns:
            List of quarterly records with ``Period``, ``pdfURL``, ``excelURL``.
        """
        with make_client(_REFERER_DISC, **self._kw) as c:
            r = c.get(_DISC_GEOGRAPHY, params={"fyId": fy_id})
            r.raise_for_status()
            data = r.json()
        groups = data.get("QuarterlyDisclosureAUMbyGeography", [])
        records = groups[0].get("data", []) if groups else []
        return maybe_polars(records, as_df)

    # -- Age-wise / Folio Data ----------------------------------------------

    def agewise_folio(self, month: str, as_df: bool = False) -> Any:
        """Age-wise AUM and folio data for a month.

        Args:
            month: ``"March-2026"`` format (MonthName-YYYY).
            as_df: Return polars DataFrame.

        Returns:
            Dict with ``investorClassification`` and ``ageWiseAUM`` lists.
        """
        with make_client(_REFERER_AGE, **self._kw) as c:
            r = c.get(_AGE_FOLIO, params={"Month": month})
            r.raise_for_status()
            data = r.json()
        if as_df:
            rows = []
            for group in (data.get("data", {}).get("ageWiseAUM", []) if isinstance(data, dict) else []):
                scheme_type = group.get("schemeTypeName", "")
                for cl in group.get("classifications", []):
                    rows.append({"schemeTypeName": scheme_type, **cl})
            return maybe_polars(rows, as_df)
        return data

    def agewise_folio_excel(self, month: str) -> bytes:
        """Download age-wise / folio data as Excel bytes."""
        with make_client(_REFERER_AGE, **self._kw) as c:
            r = c.get(_AGE_FOLIO, params={"Month": month, "excel": "true"})
            r.raise_for_status()
            return r.content

    # -- Classified Average AUM ---------------------------------------------

    def classified_dates(self, mf_id: int | str = 0) -> list[dict]:
        """List available months for Classified Average AUM.

        Makes a probe call and returns the ``monthYear`` list from the response.

        Returns:
            ``[{"date": "April-2026"}, {"date": "March-2026"}, ...]``
        """
        with make_client(_REFERER_CLASS, **self._kw) as c:
            r = c.get(_STATEWISE, params={"MF_ID": str(mf_id), "date": "01-apr-2026"})
            r.raise_for_status()
            data = r.json()
        return data.get("monthYear", []) if isinstance(data, dict) else []

    def statewise(
        self,
        date: str,
        mf_id: int | str = 0,
        as_df: bool = False,
    ) -> Any:
        """State-wise classified Average AUM for a month.

        Args:
            date:  ``"01-mon-yyyy"`` format (lowercase month, always day=01),
                   e.g. ``"01-apr-2026"`` or ``"01-mar-2026"``.
            mf_id: AMC numeric ID; 0 = All.
            as_df: Return polars DataFrame.

        Returns:
            Dict with ``data`` (list of state records) and ``monthYear`` (available dates).
        """
        with make_client(_REFERER_CLASS, **self._kw) as c:
            r = c.get(_STATEWISE, params={"MF_ID": str(mf_id), "date": date})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", []) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def statewise_excel(self, date: str, mf_id: int | str = 0) -> bytes:
        """Download state-wise classified AUM as Excel bytes."""
        with make_client(_REFERER_CLASS, **self._kw) as c:
            r = c.get(_STATEWISE, params={"MF_ID": str(mf_id), "date": date, "excel": "true"})
            r.raise_for_status()
            return r.content

    def scheme_catwise(
        self,
        date: str,
        mf_id: int | str = 0,
        as_df: bool = False,
    ) -> Any:
        """Scheme-category-wise classified Average AUM for a month.

        Args:
            date:  ``"01-mon-yyyy"`` format, e.g. ``"01-apr-2026"``.
            mf_id: AMC numeric ID; 0 = All.
            as_df: Return polars DataFrame.

        Returns:
            List of scheme-category records (includes header and data rows).
        """
        with make_client(_REFERER_CLASS, **self._kw) as c:
            r = c.get(_CATWISE, params={"MF_ID": str(mf_id), "date": date})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def scheme_catwise_excel(self, date: str, mf_id: int | str = 0) -> bytes:
        """Download scheme-category-wise classified AUM as Excel bytes."""
        with make_client(_REFERER_CLASS, **self._kw) as c:
            r = c.get(_CATWISE, params={"MF_ID": str(mf_id), "date": date, "excel": "true"})
            r.raise_for_status()
            return r.content

    # -- Bifurcation of AUM -------------------------------------------------

    def bifurcation(self, date: str, as_df: bool = False) -> Any:
        """Bifurcation of AAUM under Direct Plan for a month.

        Args:
            date:  ``"DD-Mon-YYYY"`` format, e.g. ``"31-Mar-2026"``.
            as_df: Return polars DataFrame.

        Returns:
            List with one record containing ``TotalAAUMunderDirectPlan``,
            ``AAUMunderRegisteredAdvisers``, ``AAUMunderPMS``,
            ``AAUMunderDIYclients``, ``Month_Date``.
        """
        with make_client(_REFERER_BIF, **self._kw) as c:
            r = c.get(_BIF, params={"strdt": date})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else [data]
        return maybe_polars(records, as_df)

    def bifurcation_range(self, dates: list[str], as_df: bool = False) -> dict[str, Any]:
        """Fetch bifurcation data for multiple dates.

        Returns ``{"31-Mar-2026": <data>, "28-Feb-2026": <data>, ...}``.
        """
        return {d: self.bifurcation(date=d, as_df=as_df) for d in dates}

    def bifurcation_excel(self, date: str) -> bytes:
        """Download bifurcation data as Excel bytes."""
        with make_client(_REFERER_BIF, **self._kw) as c:
            r = c.get(_BIF, params={"strdt": date, "excel": "true"})
            r.raise_for_status()
            return r.content


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncAUMClient:
    """Async client for AUM data (all five sub-modules)."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def financial_years(self) -> list[dict]:
        async with make_async_client(_REFERER_AVG, **self._kw) as c:
            r = await c.get(_AVG_FUNDWISE)
            r.raise_for_status()
            data = r.json()
        return data.get("data", data) if isinstance(data, dict) else data

    async def periods(self, fy_id: int) -> dict:
        async with make_async_client(_REFERER_AVG, **self._kw) as c:
            r = await c.get(_AVG_FUNDWISE, params={"fyId": fy_id})
            r.raise_for_status()
            data = r.json()
        return data.get("data", data) if isinstance(data, dict) else data

    async def average_aum_fundwise(
        self, fy_id: int, period_id: int, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER_AVG, **self._kw) as c:
            r = await c.get(_AVG_FUNDWISE, params={"fyId": fy_id, "periodId": period_id})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def average_aum_fundwise_excel(self, fy_id: int, period_id: int) -> bytes:
        async with make_async_client(_REFERER_AVG, **self._kw) as c:
            r = await c.get(_AVG_FUNDWISE, params={"fyId": fy_id, "periodId": period_id, "excel": "true"})
            r.raise_for_status()
            return r.content

    async def average_aum_schemewise(
        self, fy_id: int, period_id: int,
        str_type: str = "Categorywise", mf_id: int | str = 0, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER_AVG, **self._kw) as c:
            r = await c.get(_AVG_SCHEMEWISE, params={
                "strType": str_type, "fyId": fy_id,
                "periodId": period_id, "MF_ID": str(mf_id),
            })
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def average_aum_schemewise_excel(
        self, fy_id: int, period_id: int,
        str_type: str = "Categorywise", mf_id: int | str = 0
    ) -> bytes:
        async with make_async_client(_REFERER_AVG, **self._kw) as c:
            r = await c.get(_AVG_SCHEMEWISE, params={
                "strType": str_type, "fyId": fy_id,
                "periodId": period_id, "MF_ID": str(mf_id), "excel": "true",
            })
            r.raise_for_status()
            return r.content

    async def disclosure_by_category(self, fy_id: str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER_DISC, **self._kw) as c:
            r = await c.get(_DISC_CATEGORY, params={"fyId": fy_id})
            r.raise_for_status()
            data = r.json()
        groups = data.get("QuarterlyDisclosureAUMbyCategorywise", [])
        records = groups[0].get("data", []) if groups else []
        return maybe_polars(records, as_df)

    async def disclosure_by_geography(self, fy_id: str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER_DISC, **self._kw) as c:
            r = await c.get(_DISC_GEOGRAPHY, params={"fyId": fy_id})
            r.raise_for_status()
            data = r.json()
        groups = data.get("QuarterlyDisclosureAUMbyGeography", [])
        records = groups[0].get("data", []) if groups else []
        return maybe_polars(records, as_df)

    async def agewise_folio(self, month: str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER_AGE, **self._kw) as c:
            r = await c.get(_AGE_FOLIO, params={"Month": month})
            r.raise_for_status()
            data = r.json()
        if as_df:
            rows = []
            for group in (data.get("data", {}).get("ageWiseAUM", []) if isinstance(data, dict) else []):
                scheme_type = group.get("schemeTypeName", "")
                for cl in group.get("classifications", []):
                    rows.append({"schemeTypeName": scheme_type, **cl})
            return maybe_polars(rows, as_df)
        return data

    async def agewise_folio_excel(self, month: str) -> bytes:
        async with make_async_client(_REFERER_AGE, **self._kw) as c:
            r = await c.get(_AGE_FOLIO, params={"Month": month, "excel": "true"})
            r.raise_for_status()
            return r.content

    async def classified_dates(self, mf_id: int | str = 0) -> list[dict]:
        async with make_async_client(_REFERER_CLASS, **self._kw) as c:
            r = await c.get(_STATEWISE, params={"MF_ID": str(mf_id), "date": "01-apr-2026"})
            r.raise_for_status()
            data = r.json()
        return data.get("monthYear", []) if isinstance(data, dict) else []

    async def statewise(
        self, date: str, mf_id: int | str = 0, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER_CLASS, **self._kw) as c:
            r = await c.get(_STATEWISE, params={"MF_ID": str(mf_id), "date": date})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", []) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def statewise_excel(self, date: str, mf_id: int | str = 0) -> bytes:
        async with make_async_client(_REFERER_CLASS, **self._kw) as c:
            r = await c.get(_STATEWISE, params={"MF_ID": str(mf_id), "date": date, "excel": "true"})
            r.raise_for_status()
            return r.content

    async def scheme_catwise(
        self, date: str, mf_id: int | str = 0, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER_CLASS, **self._kw) as c:
            r = await c.get(_CATWISE, params={"MF_ID": str(mf_id), "date": date})
            r.raise_for_status()
            data = r.json()
        records = data.get("data", data) if isinstance(data, dict) else data
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def scheme_catwise_excel(self, date: str, mf_id: int | str = 0) -> bytes:
        async with make_async_client(_REFERER_CLASS, **self._kw) as c:
            r = await c.get(_CATWISE, params={"MF_ID": str(mf_id), "date": date, "excel": "true"})
            r.raise_for_status()
            return r.content

    async def bifurcation(self, date: str, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER_BIF, **self._kw) as c:
            r = await c.get(_BIF, params={"strdt": date})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else [data]
        return maybe_polars(records, as_df)

    async def bifurcation_range(self, dates: list[str], as_df: bool = False) -> dict[str, Any]:
        import asyncio
        results = await asyncio.gather(*[self.bifurcation(d, as_df) for d in dates])
        return dict(zip(dates, results))

    async def bifurcation_excel(self, date: str) -> bytes:
        async with make_async_client(_REFERER_BIF, **self._kw) as c:
            r = await c.get(_BIF, params={"strdt": date, "excel": "true"})
            r.raise_for_status()
            return r.content
